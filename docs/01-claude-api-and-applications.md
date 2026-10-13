# Section 1 — Claude API and Applications: Messages API, SDKs, Design, Config
### Course lectures: 1) Claude API Mechanics and Engineering Foundations (44:19) • 2) Application Design and Configuration: Claude Code Config Files (45:14)
### Exam weight: Domain 2 “Applications and Integration” = **33.1%** (17–18 questions) — the biggest domain on the exam

> **Direct answer:** One in three exam questions lives here. Master (a) the anatomy of a Messages API request/response, (b) streaming, errors & retries, (c) batch vs realtime, (d) how Claude reads instructions on each surface, and (e) configuration files and their scopes — and you have banked the largest, most predictable chunk of marks on the paper.

---

## 1.1 First Principles: What *Is* the Claude API? (Beginner)

Think of Claude not as a website, but as a **very smart colleague you can only talk to by sending written notes through a slot in a wall**:

- You write a note (the **request**: JSON over HTTPS).
- The colleague reads the *entire conversation so far* every time (Claude is **stateless** — the API remembers nothing between calls; *you* resend history).
- They write back a note (the **response**: JSON with content blocks + a reason they stopped).
- You pay per word-ish unit read and written (**tokens**).

Every concept in this section is just a refinement of that picture.

### The five surfaces — same model, different “office rules”

| Surface | Who drives | How instructions arrive | Exam keyword |
|---|---|---|---|
| **Messages API / client SDKs** | Your code | `system` param + `messages[]` you control fully | “programmatic”, “integrate” |
| **Claude Agent SDK** | Your code + SDK loop | System prompt, tools, hooks, subagents configured in code | “agent”, “hosted/self-hosted” |
| **Claude Code** | Developer in terminal/IDE | `CLAUDE.md` files, `settings.json`, slash commands, skills | “repository”, “headless” |
| **claude.ai / Desktop apps** | Human user | Project instructions, user’s messages, attached files | “end user”, “no code” |
| **Third-party platforms** | Your code via cloud | Same Messages shape via **Amazon Bedrock, Google Cloud (Vertex AI), Microsoft Foundry** | “Bedrock”, “Vertex”, “Foundry” |

**Exam trap:** A behaviour that works in claude.ai (e.g. the app keeping context) does **not** automatically exist via the API. If the stem says “via the API”, *your code* must supply history, memory and retries.

## 1.2 The Messages API — Request Anatomy (Core, heavily tested)

```jsonc
POST /v1/messages
{
  "model": "claude-sonnet-5",          // pin a specific model ID in production
  "max_tokens": 1024,                  // REQUIRED ceiling on OUTPUT tokens (not a target)
  "system": "You are a support triage assistant. Reply only with JSON.",
  "messages": [
    {"role": "user",      "content": "My invoice is wrong"},
    {"role": "assistant", "content": "{\"category\":\"billing\"}"},
    {"role": "user",      "content": "Order #4411 charged twice"}
  ],
  "temperature": 0.0,                  // sampling randomness (support varies by model — check docs)
  "tools": [ /* tool definitions, see Section 4 */ ],
  "stream": false
}
```

**Rules that appear in questions again and again:**

1. **`max_tokens` is mandatory** and caps *output*. Hitting it → `stop_reason: "max_tokens"` and a truncated answer. Raising it does **not** improve quality — it only removes the ceiling (Constraint Rule!).
2. **Roles must alternate** user/assistant (consecutive same-role messages are merged by the API in current versions, but exam logic still assumes clean alternation). The conversation conventionally **starts with `user`**.
3. **`system` is separate from `messages`** — it is not “the first user message”. Put durable role/rules/format in `system`; put the task data in `user` turns.
4. **Assistant prefill:** ending with a partial `assistant` turn historically steered format; on newer models behaviour differs — the exam-safe steer is explicit instruction + structured outputs (Section 3). Don’t rely on tricks the docs don’t guarantee for your model.
5. **Content is blocks, not just strings.** A message’s `content` can be an array: `text`, `image`, `document`, `tool_use`, `tool_result`, `thinking`. Questions love asking *which block type carries what*.

### Response anatomy

```jsonc
{
  "id": "msg_...", "type": "message", "role": "assistant",
  "model": "claude-sonnet-5",
  "content": [ {"type": "text", "text": "{\"category\":\"billing\"}"} ],
  "stop_reason": "end_turn",           // ← memorise the table below
  "usage": {"input_tokens": 412, "output_tokens": 9,
            "cache_creation_input_tokens": 0, "cache_read_input_tokens": 380}
}
```

| `stop_reason` | Meaning in plain English | Correct developer action |
|---|---|---|
| `end_turn` | Finished naturally | Parse & proceed ✅ |
| `max_tokens` | Cut off by your ceiling | Raise `max_tokens` / shorten prompt; treat output as incomplete |
| `stop_sequence` | Hit a stop string you set | Proceed; expected in some parsers |
| `tool_use` | Wants you to run a tool | Execute tool, append `tool_result`, call again (Section 4) |
| `pause_turn` | Long turn paused (server tools) | Resend conversation to continue |
| `refusal` | Declined for safety | Handle gracefully; don’t loop-retry the same prompt |

## 1.3 Images, Files and Thinking Blocks

- **Vision:** send an `image` block (base64 or URL source, with media type) inside a `user` message alongside text: “Describe the error in this screenshot.” Same Messages call — no separate “vision API”.
- **Documents/files:** PDF/document blocks let Claude read long files natively; the **Files API** lets you upload once and reference by file ID across calls (useful when the same file feeds many requests).
- **Thinking:** current Claude models support extended/adaptive **thinking** — the model reasons in `thinking` blocks before answering. You control it with the `thinking` parameter and, on newer models, an **effort** level. Thinking tokens are billed as output tokens and *improve hard reasoning at the cost of latency and money* — enable deliberately, not by default (see Section 2).

## 1.4 Streaming with Server-Sent Events (SSE)

> Streaming = the colleague writes the note **word by word while you watch**, instead of handing you the finished page.

- Set `"stream": true` (SDK: `messages.stream(...)`). Events arrive as SSE: `message_start → content_block_start → content_block_delta (×N) → content_block_stop → message_delta → message_stop`.
- **Why:** perceived latency for humans (chat UIs). **Why not:** bulk jobs, back-office pipelines — nobody is watching; use a normal or batch call.
- In code, accumulate deltas; the final `message_delta` carries `stop_reason` and cumulative `usage`.
- **Exam smell:** “users complain the spinner takes 20 s before any text appears” → streaming. “Nightly job, 50k documents” → **not** streaming (that’s Batch, §1.6).

## 1.5 Errors, Retries and Timeouts (Exam favourite)

| HTTP / type | Plain meaning | Retry? | Correct strategy |
|---|---|---|---|
| `400 invalid_request_error` | Your JSON/params are wrong | ❌ No | Fix the request; retrying repeats the same failure |
| `401 authentication_error` | Bad/missing API key | ❌ No | Fix credentials |
| `403 permission_error` | Key lacks access to that model/resource | ❌ No | Change key/model/permissions |
| `404 not_found_error` | Wrong model ID / endpoint | ❌ No | Correct the identifier |
| `413 request_too_large` | Payload over limits | ❌ No | Split / prune / use Files API |
| `429 rate_limit_error` | Too many requests/tokens per minute | ✅ Backoff | Exponential backoff + jitter; honour `retry-after`; reduce concurrency |
| `500 api_error` / `529 overloaded_error` | Anthropic-side problem | ✅ Backoff | Exponential backoff; SDKs retry these by default (default max retries = 2) |
| Timeout (client-side) | No response in your window | ⚠️ Careful | Raise timeout for long generations/streaming; make calls idempotent-safe before retrying |

**Three laws:** (1) Retry only *transient* errors (429/5xx/timeouts). (2) Backoff must be **exponential with jitter**, not a fixed 0 ms loop. (3) The official SDKs already retry 429/5xx — questions testing “the SDK retries twice by default, then raises” are common.

**Async with a limit:** for many concurrent calls use async SDK clients + a **semaphore** (e.g. 5–10 in flight), so *you* stay under rate limits instead of bouncing off 429s.

## 1.6 Realtime vs Message Batches API — The Classic Decision

| Dimension | Realtime Messages API | Message Batches API |
|---|---|---|
| Latency | Seconds | Up to 24 h (usually much faster) |
| Price | Standard | **~50% discount** on input+output |
| Interaction | Interactive, streaming possible | Fire-and-forget: submit → poll/retrieve results |
| Best for | Chat, user-facing features | Nightly classification, bulk summarisation, evals, backfills |

**Decision sentence to memorise:** *“If a human is waiting, go realtime; if a cron job is waiting, go Batch.”*
Limits to know: batch size caps (100k requests / 256 MB class), results retrieved per-request with per-request success/error — one bad request does **not** fail the batch.

## 1.7 Claude on Bedrock, Google Cloud and Microsoft Foundry

Same Claude models, billed/governed through the cloud you already use: **Amazon Bedrock**, **Google Cloud Vertex AI**, **Microsoft Foundry**. Choose them for existing cloud commitments, data-residency, IAM/VPC controls. Exam point: model access must be **enabled per cloud/region**, IDs differ (Bedrock inference-profile IDs etc.), and some newest features land on the first-party API first. “Invoke Claude through third-party vendors” is listed verbatim in API Mechanics — expect one question.

## 1.8 Software Engineering Foundations (7.4% — “the quarter that isn’t about Claude”)

- **REST + JSON fluency:** resources, verbs, status codes, idempotency, headers (`x-api-key`, `anthropic-version`).
- **Async programming:** non-blocking calls, `Promise.all`/gather, concurrency caps, timeouts.
- **Version control discipline:** prompts, `CLAUDE.md`, `settings.json` and tool schemas are **code** — commit them, review them in PRs, tag releases.
- **CI code review & safe refactoring with Claude:** run Claude Code in CI for review suggestions; refactor safely = small diffs, tests green before/after, human approves merges. Claude proposes; **tests dispose**.

## 1.9 Lecture 2 — Application Design and Configuration

### From business requirement → design (Requirements 3.4% + Life Cycle 2.8%)

1. **Functional requirements:** what the system must *do* (“classify tickets into 12 categories, ≥95% agreement with human labels”).
2. **Infrastructure / non-functional:** latency, volume, budget, privacy, regions, uptime.
3. **Success criteria written before building:** metric + threshold + eval set. “Feels good” is not a criterion.
4. **Life cycle:** plan → develop → implement → operate → maintain. Model IDs get **pinned**, prompts get **versioned**, usage gets **monitored** ( operate/maintain is where caching & cost work lives).

### Content boundaries, schemas, session hygiene

- **Content boundaries:** clearly delimit *instructions* vs *data* (XML tags like `<ticket>…</ticket>`, separate params). This is both a quality and a security control (Section 6).
- **Output schemas first:** decide the JSON shape your code consumes *before* prompting; validate every response against it.
- **Session hygiene:** new task → new session/conversation. Dragging an old, irrelevant history into a new task causes drift, cost and confused answers. Summarise-or-restart deliberately.

### Configuration files and their scopes (Config Mgmt 4.1%)

| Scope (Claude Code) | Location | Shared? | Use for |
|---|---|---|---|
| Managed/policy | OS-level managed settings | IT-enforced | Org-wide non-overridable rules |
| User | `~/.claude/settings.json`, `~/.claude/CLAUDE.md` | Just you | Personal defaults across projects |
| Project | `.claude/settings.json`, `CLAUDE.md` / `.claude/CLAUDE.md` | Team (committed) | Repo rules, permissions, model pin |
| Local | `.claude/settings.local.json`, `CLAUDE.local.md` | No (gitignored) | Your machine-only overrides |

- **Precedence:** more specific beats broader (local > project > user), managed policy beats all.
- **`CLAUDE.md` hierarchy:** files are discovered from the working directory upward (and into subdirectories on demand) and *concatenated* — closer-to-cwd instructions effectively win attention; keep them short and factual.
- **Model pinning:** pin exact model IDs in config/code; “latest” aliases can shift behaviour under you. Upgrades = deliberate PR + eval run (breaking-behaviour changes across releases are explicitly in the blueprint).
- **Prompt versioning:** prompts live in version control or a prompt store with versions, not in a PM’s spreadsheet.
- **Plugin dependencies:** declare Claude Code plugins/skills in project config so a new teammate gets the same setup; unpinned plugins are a supply-chain and reproducibility risk.

## 1.10 Worked Scenario (AI-Mode style)

**Q: A helpdesk wants 20,000 tickets/day classified, results by next morning, cheapest reliable setup.**
**A:** Batch API (deadline is loose, volume high) + smallest model that passes a labelled eval (start Haiku-class), structured output with the 12-category enum, retries only on transient errors, results joined back by custom ID. *Why not the distractors?* Realtime streaming (pays for interactivity nobody uses), biggest model (pays for reasoning classification doesn’t need), “increase max_tokens” (output is a tiny label — not the binding constraint).

## 1.11 Hands-On Labs

```bash
python labs/python/01_messages_api.py --mock        # request/response anatomy, stop_reasons
python labs/python/01_messages_api.py               # real call (needs ANTHROPIC_API_KEY)
python labs/python/01_streaming_and_errors.py --mock
# TypeScript:
cd labs/typescript && npm install && npx tsx 01_messages_api.ts
```
**Lab exercises:** (1) Force a `max_tokens` stop and handle it. (2) Make a 400 error; confirm your code does *not* retry it. (3) Convert the classifier to a Batch job and compute the saving with Section 2’s calculator.

## 1.12 Common Exam Traps

- ❌ “Retry every error 3 times” → ✅ only 429/5xx/timeout, with backoff.
- ❌ “The API remembers our last conversation” → ✅ stateless; resend history.
- ❌ “Put the system prompt as the first user message” → ✅ separate `system` param.
- ❌ Streaming/batch swapped → ✅ human waiting = stream; deadline loose = batch.

## 1.13 Self-Check (answers in Trainer 1)
1. Which `stop_reason` means “run the requested function and call me back”?
2. A call returns 400. Your retry loop fires 5 times. What’s wrong?
3. Where does a repo-shared Claude Code rule belong — user, project or local settings?
4. Nightly 80k-document job, 24 h deadline: realtime or Batch, and why?

➡️ **Next:** [`02-model-selection-tokens-cost.md`](02-model-selection-tokens-cost.md) • Practice: Trainer 1–2 in [`../practice/exam-trainers-84.md`](../practice/exam-trainers-84.md)
