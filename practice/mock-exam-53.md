# CCDV-F Mock Exam — 53 Questions, 120 Minutes (Original)
> **Instructions (read like the real thing):** 53 items, blueprint-weighted (D2≈18, D5≈9, D1≈8, D6≈6, D8≈6, D7≈4, D3≈1, D4≈1). Some items say **(Choose two)** — select exactly that many. Set a 120-minute timer. No notes. Flag hard items and return. **Answer key + scoring are at the very end — do not scroll until the timer ends.**

---

**1. [D2]** Your app must resend conversation history each call because the Messages API is…
A. Cached B. Stateless C. Streaming-only D. Stateful per model

**2. [D2]** A response shows `stop_reason:"tool_use"`. Next step?
A. Show raw JSON to the user B. Execute the tool, append a matching `tool_result`, call again C. Retry the same request D. End the session

**3. [D2]** Which failure must NOT be auto-retried?
A. 429 B. 529 C. 400 invalid request D. Gateway timeout

**4. [D2]** Nightly job: 80,000 documents, results by morning, lowest cost.
A. Realtime + streaming B. Message Batches API C. Frontier model realtime D. WebSockets

**5. [D2]** Chat users complain nothing appears for 15 seconds.
A. Batch B. Raise max_tokens C. Streaming (SSE) D. Prompt caching alone

**6. [D2] (Choose two)** Valid ways Claude receives an image for analysis?
A. `image` content block in a user message B. Files/document reference in a message C. In the `model` string D. Via `stop_sequences`

**7. [D2]** On Google Cloud, Claude is invoked through…
A. Bedrock B. Vertex AI C. Foundry only D. Direct GPU rental

**8. [D2]** A 404 from the Messages endpoint most likely means…
A. Rate limit B. Wrong model ID/endpoint C. Bad API key format D. Prompt too long

**9. [D2]** Team-shared Claude Code instructions live in…
A. Committed project `CLAUDE.md` B. One dev's local settings C. Chat history D. The API key name

**10. [D2]** “p95 < 2s, EU residency, 99.9% uptime” are…
A. Functional requirements B. Infrastructure/non-functional requirements C. Few-shot examples D. Tool schemas

**11. [D2]** Success criteria for an extraction feature should be defined…
A. After launch, from vibes B. Before building: metric + threshold + eval set C. By the model D. Never

**12. [D2] (Choose two)** Safe Claude-assisted refactoring in CI requires…
A. Tests green before/after B. Human-approved merges C. Auto-merge of model diffs D. Disabling review

**13. [D2]** Pinning exact model IDs prevents…
A. All errors B. Silent behaviour drift from alias/release changes C. Rate limits D. Token costs

**14. [D2]** A developer stores team prompts in a shared spreadsheet, edited freely. Exam-grade fix?
A. Longer spreadsheet B. Version-controlled prompts reviewed in PRs C. Put prompts in images D. Email them weekly

**15. [D2]** Session hygiene: a new task should usually…
A. Reuse the longest history B. Start fresh (or from a summary) C. Include all past users' chats D. Disable the system prompt

**16. [D2]** SDK default behaviour includes…
A. Retrying 429/5xx a limited number of times B. Remembering conversations C. Paying your bill D. Choosing your model

**17. [D2]** Payload returns 413 repeatedly. Action?
A. Backoff-retry forever B. Split/prune payload or use Files API C. New API key D. Enable thinking

**18. [D2]** Async fan-out of 500 calls should use…
A. Unlimited concurrency B. Async client + semaphore + backoff/jitter C. Synchronous loop only D. Batch regardless of deadline (user is waiting)

**19. [D5]** Rough token truth: English text tokenises at about…
A. 1 token per word always B. ~¾ word per token (≈4 chars/token) C. 10 words per token D. Tokens = bytes exactly

**20. [D5]** Cheapest model strategy that keeps quality: …
A. Frontier everywhere B. Smallest tier passing eval + route hard cases up C. Cheapest everywhere, no eval D. Random tier per call

**21. [D5]** A stable 8k-token manual precedes every question. Use…
A. Batch B. Prompt caching breakpoint on the manual, question last C. Thinking D. Stop sequences

**22. [D5] (Choose two)** Cache misses happen when…
A. The prefix before the breakpoint changed B. TTL expired C. The model is pinned D. Usage logging is on

**23. [D5]** Extended thinking is best spent on…
A. Sentiment tags B. Hard multi-step reasoning C. Greetings D. Enum routing

**24. [D5]** Cost per call = …
A. Flat fee B. (in×price_in + out×price_out + cache terms)/1M tokens C. Per second D. Per user

**25. [D5]** Non-determinism comes from…
A. Sampling the next token from a distribution B. Caching C. Statelessness D. JSON

**26. [D5]** Latency-critical chat, adequate quality on mid tier. Best set?
A. Frontier + thinking max, no streaming B. Mid/small tier + streaming (+fast mode where offered) C. Batch D. Huge history

**27. [D5]** After upgrading model versions you must…
A. Nothing B. Re-run evals; behaviour can change across releases C. Delete prompts D. Raise prices

**28. [D1]** A task whose steps “depend on what you find” calls for…
A. Fixed workflow B. An agent loop C. A single prompt D. Batch only

**29. [D1]** Draft → critique → revise until quality bar: which pattern?
A. Routing B. Evaluator–optimizer C. Sectioning D. Voting

**30. [D1]** Classify-then-specialist handling is…
A. Chaining B. Routing C. Orchestrator–workers D. Parallel voting

**31. [D1] (Choose two)** Agent SDK provides…
A. Agent loop & permissions/hooks B. Subagent support C. Guaranteed-correct answers D. Infinite context

**32. [D1]** Noisy research flooding the main thread → …
A. Subagent returning only conclusions B. Longer system prompt C. More tools for main agent D. Batch

**33. [D1]** Max turns + timeouts + approval gates around an agent loop are…
A. Optional decoration B. Production guardrails bounding cost/risk C. Prompt tricks D. Caching

**34. [D1]** Lead model decomposes, delegates, synthesises:
A. Orchestrator–workers B. Chaining C. Routing D. Prefilling

**35. [D1]** Hand-rolled harness vs Agent SDK: hand-rolled means you own…
A. Nothing B. The loop, retries, state — everything C. Only the logo D. Anthropic's servers

**36. [D6]** Durable output-format rules belong in…
A. `system` B. A random middle user turn C. Tool results D. The model name

**37. [D6]** Few-shot examples are strongest for…
A. Teaching exact output format/labelling B. Security guarantees C. Lowering token counts D. Replacing validation

**38. [D6]** Context rot is cured by… (Choose two)
A. Pruning tool output B. Compacting old history C. Always adding more history D. Raising temperature

**39. [D6]** `<policy>…</policy><ticket>…</ticket>` gives…
A. Content boundaries B. Free tokens C. Streaming D. Model upgrade

**40. [D6]** Just-in-time context = …
A. Preload everything B. Retrieve when the step needs it C. Never retrieve D. Duplicate history

**41. [D6]** JSON parses but a field has the wrong type. Defence that catches it?
A. Hope B. Schema validation in code C. Streaming D. Caching

**42. [D8]** Custom tool execution happens…
A. Inside the model B. In your code (or MCP server) C. In the browser automatically D. On paper

**43. [D8]** Best tool schema practice?
A. Free-text everything B. Enums + required fields + `additionalProperties:false` C. No descriptions D. One mega-tool

**44. [D8] (Choose two)** MCP exposes…
A. Tools B. Resources C. Operating systems D. API keys by default

**45. [D8]** Many clients, one governed capability → …
A. Copy-paste tools per app B. MCP server C. A Skill with credentials inside D. Longer prompts

**46. [D8]** A runbook/checklist Claude should *know* (no live action) = …
A. Custom tool B. Skill C. Batch job D. Hook

**47. [D8]** Tool errors should return as…
A. Process crash B. `tool_result` with `is_error:true` and a useful message C. Empty history D. A new API key

**48. [D7]** Instructions hidden in a fetched web page hijack an agent. Name + first defences?
A. Direct injection; bigger model B. Indirect injection; delimit data, least-privilege tools, approval for actions C. Context rot; compact D. Rate limiting; backoff

**49. [D7]** “Never exfiltrate customer data” must be enforced by… (Choose two)
A. Prompt text alone B. Tool permissions/egress controls C. Approval gates & validation D. Hope

**50. [D7]** API keys in production: …
A. In the repo README B. Secret manager/env, scoped per service, rotated C. In the system prompt D. In client-side JS

**51. [D7]** A PreToolUse hook blocking `rm -rf` returns/does…
A. Exit 0 B. Blocks the call (exit 2 in Claude Code) with feedback C. Retries the API D. Clears cache

**52. [D3]** Claude Code in CI, non-interactive:
A. `claude -p "…"` headless mode B. Desktop app clicking C. Batch API D. MCP stdio logging to stdout

**53. [D4]** Outputs got worse after a prompt edit. Disciplined response?
A. Revert blindly B. Run the golden-set eval, triage layer (integration vs model), bisect the change C. Change models randomly D. Add retries

---
---

# 🔒 ANSWER KEY & SCORING (open only after the timer)

| # | Ans | Why (one line) | # | Ans | Why |
|---|---|---|---|---|---|
|1|B|Stateless API|28|B|Discovered steps = agent|
|2|B|Tool loop step|29|B|Generator+critic loop|
|3|C|400 is deterministic|30|B|Classifier routes|
|4|B|Loose deadline+volume=Batch|31|A,B|SDK: loop/hooks/subagents|
|5|C|Time-to-first-token|32|A|Context isolation|
|6|A,B|Blocks/files carry media|33|B|Bound the loop|
|7|B|Vertex AI on GCP|34|A|Decompose/delegate|
|8|B|404 = identifier|35|B|You own the loop|
|9|A|Project scope, committed|36|A|Durable rules in system|
|10|B|Non-functional|37|A|Examples teach format|
|11|B|Criteria before building|38|A,B|Prune + compact|
|12|A,B|Tests + human merge|39|A|Boundaries|
|13|B|Anti-drift pinning|40|B|Retrieve on demand|
|14|B|Prompts are code|41|B|Validate in code|
|15|B|Fresh/summary per task|42|B|You execute|
|16|A|Limited default retries|43|B|Strict schema|
|17|B|Shrink the payload|44|A,B|Tools+Resources (+Prompts)|
|18|B|Semaphore+backoff|45|B|Reusable MCP|
|19|B|~4 chars/token EN|46|B|Know-how = Skill|
|20|B|Eval-gated routing|47|B|Error as result|
|21|B|Stable prefix cached|48|B|Data≠instructions|
|22|A,B|Prefix/TTL govern hits|49|B,C|Enforcement layers|
|23|B|Reasoning spend|50|B|Secret manager|
|24|B|Token×price formula|51|B|Block with feedback|
|25|A|Sampling|52|A|Headless `-p`|
|26|B|Tier+streaming|53|B|Eval + triage|
|27|B|Re-eval on upgrade||||

**Wrong-option pattern to notice:** every distractor fails for one of four reasons — generic knob (ignores the constraint), prompt-only guarantee, wrong layer, or absolutist/off-blueprint claim (§7.4).

## Scoring
1. % per domain: D2 = Q1–18, D5 = Q19–27, D1 = Q28–35, D6 = Q36–41, D8 = Q42–47, D7 = Q48–51, D3 = Q52, D4 = Q53.
2. Enter them in `../assets/readiness-scorecard.csv`.
3. **Book the real exam only if:** weighted performance is at the >800-equivalent level **and** no domain < 60%. Otherwise: restudy the weak domain's doc, do its trainer (12 Qs), re-mock in 3–4 days.
