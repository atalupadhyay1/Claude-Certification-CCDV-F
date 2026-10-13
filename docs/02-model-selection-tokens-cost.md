# Section 2 — Claude Model Selection: Opus, Sonnet, Haiku, Tokens, Prompt Caching
### Course lecture: Model Selection, Tokens, and Cost: Pick the Claude Model, Cut the Bill (44:22)
### Exam weight: Domain 5 “Model Selection and Optimization” = **16.8%** (9 questions)

> **Direct answer:** Pick the **smallest, fastest model that passes your eval**, price every request with `cost = input_tokens × input_price + output_tokens × output_price (+ cache terms)`, then cut the bill with **prompt caching** (stable prefix, 5-minute or 1-hour TTL) or the **Batch API (~50% off)** — in that order. Most production systems should default to the mid tier (Sonnet-class) and route only hard cases upward.

---

## 2.1 LLM Fundamentals — What’s Actually Happening (5.2%)

Human version: Claude reads your text chopped into **tokens** (roughly ¾ of an English word each; code and non-English text tokenise less efficiently) and predicts **one token at a time**, each step sampling from a probability distribution over what could come next.

| Concept | One-line human explanation | Exam consequence |
|---|---|---|
| **Token** | A chunk of text (~4 characters in English) | You pay & are limited **per token**, not per word/request |
| **Context window** | The model’s “desk size” — max tokens it can see at once (input + output) | Long history + big tools + thinking must all fit; overflow = truncation/failure |
| **Next-token sampling** | Each token is drawn from probabilities | Same prompt can give different answers → **non-determinism** |
| **Temperature / sampling controls** | How “adventurous” the draw is | Low ≈ factual/stable for extraction; support & defaults vary by model — verify in docs |
| **Zero / one / few-shot** | 0, 1, or several examples in the prompt | Few-shot is the cheapest reliability upgrade for format tasks |
| **Extended / adaptive thinking** | Model reasons in thinking blocks before answering | Better hard reasoning; costs output tokens + latency |
| **Effort levels** | How hard the model should think/work on a task | Raise for hard tasks; lowering saves tokens on easy ones |
| **Fast mode** | Speed-optimised serving where offered | Latency ↓; check price/availability trade-offs |

**Why non-determinism matters in production:** never assert exact-string equality in tests against a live model; assert *schema, categories, properties* instead. And pin model IDs — a new model release can change behaviour (“breaking behaviour changes across model releases” is blueprint text).

## 2.2 Meet the Family — Model Tiers and Trade-offs (2.7%)

Anthropic ships tiered families (the course covers Fable, Opus, Sonnet, Haiku classes). **Always verify the current model IDs and prices in the official docs/pricing page before an exam answer or a purchase** — tiers are stable concepts; IDs and numbers move.

| Tier | Personality | Reach for it when… | Avoid when… |
|---|---|---|---|
| **Opus-class** (frontier) | Deepest reasoning, best hard-code/agent performance | Complex multi-step reasoning, hard code generation, high-stakes analysis | High-volume simple tasks — you’re burning money |
| **Sonnet-class** (balanced) | The production default: strong + fast + economical | Most apps: chat, RAG, agents, coding assistants | Trivial classification at huge scale (go smaller) |
| **Haiku-class** (fast/cheap) | Quick, light, inexpensive | Classification, routing, tagging, summarisation at volume, first-pass triage | The hardest reasoning — escalate failures upward |
| **Fable-class** | Newest specialised tier covered in the course | Follow current docs for its positioned strengths | Assuming — read the model card |

### The routing pattern (tested constantly)
```
Haiku-class classifier/router ──easy (90%)──▶ answer directly
                              └─hard/unsure──▶ Sonnet/Opus-class
```
You get near-frontier quality at near-small-model average cost. The reverse (frontier model for everything) is the classic wrong answer.

### Decision table

| Requirement in the stem | Binding constraint | Model answer |
|---|---|---|
| 12-way ticket classification, 20k/day, ≥95% on eval | Cost at volume | Smallest tier passing eval + Batch |
| Multi-file refactor with tests | Quality | Opus/Sonnet-class + thinking |
| Chat, first token < 1 s perceived | Latency | Sonnet/Haiku + streaming; consider fast mode |
| “Best possible, cost no object, offline” | Quality | Frontier tier + higher effort + Batch if deadline allows |

## 2.3 Technical Fundamentals (6.1%) — SDKs Wrap REST

- Client SDKs (Python/TypeScript/etc.) wrap the REST API: they add typed objects, automatic retries (429/5xx), streaming helpers and error classes. Anything the SDK does, the REST API can do — the SDK just does it safely by default.
- **WebSockets vs SSE:** Claude’s streaming is **server-sent events over HTTP**, not a WebSocket you manage. Exam options offering “open a WebSocket to Claude for streaming” are smells.
- Know sync vs async clients, and that `usage` in every response is your source of truth for tokens.

## 2.4 The Cost Formula — Price One Request (2.8%)

```
cost = (input_tokens        / 1e6 × input_price_per_MTok)
     + (output_tokens       / 1e6 × output_price_per_MTok)
     + (cache_write_tokens  / 1e6 × cache_write_price)     // premium on write
     + (cache_read_tokens   / 1e6 × cache_read_price)      // steep discount on read
Batch API: roughly × 0.5 on input + output.
```

**Worked example (illustrative prices — replace with current pricing):** A support call with 4,000 input tokens (3,800 cached-read) + 300 output on a mid-tier model at $3/$15 per MTok:
- No cache: `4000×3/1e6 + 300×15/1e6 = $0.0120 + $0.0045 = $0.0165`
- Cached: `200×3/1e6 + 3800×0.30/1e6 + 300×15/1e6 ≈ $0.0006 + $0.0011 + $0.0045 = $0.0062` → **~62% cheaper**, and faster (cached prefix isn’t reprocessed).

Habits of engineers who pass this domain: log `usage` per request, alert on cost per *successful outcome* (not per call), and re-price after every prompt change.

## 2.5 Prompt Caching — Mechanics That Get Tested

Caching stores a processed **prefix** of your prompt so repeated calls reuse it.

1. Mark breakpoints with `cache_control: {"type": "ephemeral"}` on content blocks (system prompt, big document, tool list).
2. **TTL:** default **5 minutes**, extended **1 hour** option (higher write premium). Cache refreshes on use within TTL.
3. **Minimum cacheable length** applies (order of ~1k tokens, tier-dependent — check docs): tiny prompts won’t cache.
4. **Prefix must match exactly** up to the breakpoint — one changed token early invalidates everything after it. → Put **stable content first, variable content last** (user question at the end).
5. **Up to 4 breakpoints**; caching is per-model/per-workspace scope — never assume data leaks across customers; the cache stores prompt *processing*, and you must still follow privacy rules for what you send.
6. Verify with `usage.cache_read_input_tokens > 0`. Zero reads when you expected hits = prefix changed or TTL expired.

**Exam traps:** caching does **not** help one-off unique prompts; moving the user’s question *before* the big manual kills the cache; cache reads are cheap but writes cost extra — caching pays when a prefix is reused **several times within its TTL**.

## 2.6 Thinking, Effort and Fast Mode — Spending Deliberately

- Hard multi-step problem → thinking/effort **up**. Classification/extraction → **off/low** (thinking tokens would dwarf the answer).
- Latency-sensitive UX → streaming first, smaller tier, lower effort; fast mode where available.
- Always budget: `input + thinking + output ≤ context window`, and `thinking + output ≤ max_tokens`.

## 2.7 Hands-On Lab

```bash
python labs/python/02_cost_calculator.py            # interactive pricing + caching/batch scenarios
python labs/python/02_cost_calculator.py --scenario support-bot
```
**Exercises:** (1) Price your own app’s typical call. (2) Find the reuse count where caching a 10k-token manual breaks even. (3) Re-price a 50k/night job realtime vs Batch and present the saving in one sentence a manager would understand.

## 2.8 Self-Check
1. Your cache reads are 0 but you set `cache_control`. Name two causes.
2. Why is “use Opus for classification to be safe” usually the wrong exam answer?
3. A stem demands lowest cost, 48-h deadline. Which two levers combine best?
4. What does `usage` tell you that your own tokeniser estimate can’t?

➡️ **Next:** [`03-prompt-context-engineering.md`](03-prompt-context-engineering.md) • Trainer 3 in the practice file.
