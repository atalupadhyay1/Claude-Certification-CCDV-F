# Section 3 — Prompt and Context Engineering: Structured Output and Debugging
### Course lecture: Prompts, Context, Output, and Debugging: Prompts That Hold Under Load (44:15)
### Exam weight: Domain 6 “Prompt and Context Engineering” **11.0%** + Domain 4 “Eval, Testing & Debugging” **2.6%** (≈ 7–8 questions combined)

> **Direct answer:** Put **durable rules in `system`, task data in `user`**, delimit data with tags, show 2–5 few-shot examples for format-critical work, demand a **schema**, then **validate every response in code and retry with the validation error fed back**. Manage context like a budget: prune tool output, compact old history, isolate noisy work in subagents. When something breaks, first decide *which layer failed* — your integration or the model’s output — because the fix (and the exam answer) is completely different.

---

## 3.1 Prompt Anatomy — Where Each Part Goes (4.6%)

| Part | Lives in | Contains | Example |
|---|---|---|---|
| Role & durable rules | `system` | Persona, policy, output contract | “You are a triage assistant. Reply only with JSON matching the schema.” |
| Context / documents | `user` (tagged) | Retrieved text, ticket body | `<ticket>Order 4411 charged twice</ticket>` |
| Few-shot examples | `user`/`assistant` pairs or system | Input→ideal output pairs | 3 classified tickets |
| The actual task | Final `user` turn | The question/instruction | “Classify this ticket.” |
| Output constraints | `system` + schema | Format, length, enum values | `category ∈ {billing, login, …}` |

**Craft rules that survive load:**
1. **Be explicit, not vibes-based.** “Summarise well” fails; “Summarise in ≤3 bullets, each ≤20 words, keep order numbers verbatim” holds.
2. **Delimit everything.** XML-style tags (`<policy>`, `<ticket>`) create content boundaries the model respects — and that prompt-injection defences rely on (Section 6).
3. **Few-shot beats adjectives.** Two perfect examples teach format better than a paragraph describing it.
4. **Let Claude think where it helps:** “Reason step by step inside `<thinking>` tags, then give the final JSON” (or native thinking, Section 2) for hard tasks; skip it for extraction.
5. **Iterate with an eval set,** not single anecdotes: change one thing, re-run 30 labelled cases, keep what measurably wins (input sanitisation + refinement loop is blueprint text).

## 3.2 Context Engineering — The Budget Mindset (3.8%)

Your context window is a shared desk: system prompt + history + retrieved docs + tool definitions + tool results + thinking must all fit, and **more clutter = worse attention + higher cost** (“context rot”: quality degrades as irrelevant tokens pile up).

| Technique | What it means | Reach for it when… |
|---|---|---|
| **Tool-output pruning** | Trim/filter tool results before they enter history (drop verbose fields, cap lines) | A search tool returns 50 KB per call |
| **Compaction / summarisation** | Replace old turns with a faithful summary | Long sessions; keep decisions & IDs verbatim, compress chit-chat |
| **Truncation strategy** | Drop oldest *low-value* turns, never the system prompt or the latest task | Hard window limit approaching |
| **Subagent isolation** | A subagent burns its own context on noisy research and returns only the conclusion | Web/file research would flood the main thread |
| **Just-in-time retrieval** | Fetch context at the step that needs it instead of preloading everything | Large knowledge bases; RAG patterns |
| **Long-context ordering** | Put long reference material early, the query/instruction at the end; quote-grounded answers | Document Q&A over huge inputs |

**Session hygiene (from Section 1):** new task → fresh session. A support agent that still “remembers” yesterday’s unrelated refund will eventually answer about it.

## 3.3 Structured Output & Defensive Parsing (2.6%)

The pipeline your code should implement — memorise the order:

```
prompt w/ schema → model reply → extract → JSON-parse → schema-validate
      ▲                                                    │
      └──── retry (≤2–3) with the validator error fed back ┘
                          │ still failing
                          ▼
              fallback: safe default / human queue / smaller re-ask
```

- **Prefer native structured outputs / tool-forced JSON** where your model supports it (constrain to a JSON Schema) over “please output JSON” prompting; prompting persuades, schemas *constrain* (Guarantee Rule again).
- **Defensive parsing:** strip code fences, tolerate leading prose by extracting the JSON span, validate types/enums/ranges, never `eval` model output.
- **Skepticism toward confident output:** Claude can state wrong facts fluently. Ground with retrieval, cite sources, verify IDs/amounts against your systems, and route low-confidence or high-impact outputs to humans.
- **Never execute model output blindly** — no `eval`, no raw SQL, no shell. Validate, allowlist, then act (bridges to Section 6).

## 3.4 Failure Triage — Integration Layer or Model Output? (Domain 4, 2.6%)

Ask in this order — it’s the course’s “failure triage tree”:

1. **Did the request even arrive correctly?** Log the exact payload. (Wrong model ID, missing `max_tokens`, malformed blocks → *integration*.)
2. **What did the API say?** HTTP status + error type (Section 1.5 table) + `stop_reason`. (`max_tokens` truncation looks like “broken JSON” but is *your ceiling*.)
3. **Is the raw text well-formed but wrong-shaped?** JSON parses but fails schema → *model output / prompt problem*: tighten schema, add an example.
4. **Well-shaped but factually wrong?** → grounding problem: better retrieval, citations, smaller task, stronger model — or an eval revealing the task is ambiguous.
5. **Intermittent?** Check rate limits, timeouts, token budget creep (history growth), cache misses.

| Symptom | Likely layer | First fix |
|---|---|---|
| 400s after a deploy | Integration | Diff the payload against docs; you changed a field |
| JSON truncated mid-string | Integration (`max_tokens`) | Raise ceiling / shorten output |
| Valid JSON, wrong enum value | Model/prompt | Constrain enum in schema; few-shot the edge case |
| Fluent but invented order status | Model/grounding | Retrieve real status; instruct “only use `<data>`” |
| Works in testing, 429s in prod | Integration/limits | Backoff, semaphore, request quota review |
| Slowly degrading quality in long chats | Context | Compact/prune; fresh session per task |

**Eval habit (Domain 4 mindset):** keep a small golden set (30–100 labelled cases). Every prompt/model/config change runs it. Score = % passing schema + % correct label. This one habit answers most “how do you know the change helped?” questions.

## 3.5 Debugging Toolkit

- Log (safely, PII-redacted): request ID, model, `usage`, `stop_reason`, latency, validator verdict.
- Reproduce with the *exact* logged payload at temperature-stable settings; bisect the prompt (remove halves until the failure vanishes).
- Trace multi-step agents per step: which tool, what args, what result, what the model saw (Section 5).

## 3.6 Hands-On Labs

```bash
python labs/python/03_structured_output.py --mock   # parse → validate → retry-with-feedback loop
python labs/python/03_structured_output.py --mock --break-it   # watch it recover from bad JSON
```
**Exercises:** (1) Add a new enum category end-to-end (prompt, schema, validator). (2) Feed a 60-turn history and compact it to a summary + last 4 turns; compare token counts. (3) Break the prompt deliberately; classify the failure with the triage tree before fixing.

## 3.7 Exam Traps
- ❌ “The model returned bad JSON, so increase temperature for creativity” → ✅ constrain schema + retry with error feedback.
- ❌ “Keep entire history forever for best quality” → ✅ prune/compact; context rot is real.
- ❌ Prompt-only output guarantees → ✅ validation in code is the guarantee.

➡️ **Next:** [`04-tools-and-mcp-servers.md`](04-tools-and-mcp-servers.md) • Trainers 4–5.
