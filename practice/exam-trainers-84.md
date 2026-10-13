# Exam Trainers — 84 Original Practice Questions (7 Trainers × 12)
> Course pattern preserved: 12 questions per lesson, mixed “one best answer” and “choose two”, **instant explanation of why every wrong option fails**. These are original questions — not real exam items. Attempt before reading the answer line.

**How to use:** Cover answers. Score per trainer: 10–12 = exam-ready on this domain; 7–9 = reread the linked doc section; ≤6 = redo the lab, then retry only the missed questions after 24h.

---

## Trainer 1 — API Mechanics (Section 1 · Domain 2: API Mechanics 6.8%)

**1.** A Messages response ends with `stop_reason: "max_tokens"` and truncated JSON. Best first action?
A. Lower temperature B. Raise `max_tokens` and treat prior output as incomplete C. Retry the identical request D. Switch to streaming
**✅ B.** *A:* sampling doesn't fix a ceiling. *C:* identical retry truncates again. *D:* streaming doesn't raise the cap.

**2.** Which errors should an automatic retry cover? (Choose two)
A. 400 invalid request B. 429 rate limit C. 401 auth D. 529 overloaded
**✅ B, D.** *A/C:* deterministic client faults — fix the cause; retrying repeats failure.

**3.** The Claude API “remembered” yesterday’s chat in your app because…
A. The API is stateful B. Your code resent the history C. The model ID pins memory D. Prompt caching stores chats
**✅ B.** The API is stateless. *A/D:* caching stores prompt-prefix processing, not conversations.

**4.** Where does a durable “reply only with JSON” rule belong?
A. First user message B. `system` parameter C. Assistant prefill only D. Tool description
**✅ B.** *A:* mixes rules with data. *C:* fragile/unsupported steer on newer models. *D:* scopes to one tool.

**5.** Users see a 20s blank spinner before text appears in a chat UI. Fix?
A. Batch API B. Raise max_tokens C. Streaming via SSE D. Bigger model
**✅ C.** Perceived latency = stream tokens. *A:* adds hours of latency. *B/D:* don't change time-to-first-token.

**6.** A request returns 413. You should…
A. Retry with backoff B. Split the payload / use Files API C. Change API key D. Enable thinking
**✅ B.** 413 = payload too large (deterministic). *A/C/D* don't shrink it.

**7.** Which are valid content block types in a message? (Choose two)
A. `image` B. `tool_result` C. `spreadsheet_cell` D. `system_block`
**✅ A, B.** *C/D:* not Messages content blocks; system is a top-level parameter.

**8.** `stop_reason: "tool_use"` means…
A. An error occurred B. Claude finished C. Run the tool, append `tool_result`, call again D. The tool already ran on Anthropic's servers (for your custom tool)
**✅ C.** *D* is the classic trap: custom tools execute in *your* code.

**9.** On Amazon Bedrock, a Claude call fails with model access denied. Likely cause?
A. Prompt too long B. Model not enabled for that account/region C. Streaming off D. No few-shot examples
**✅ B.** Third-party platforms require per-cloud/region model enablement.

**10.** Async bulk calls from your service keep hitting 429s. Best design?
A. Retry instantly in a tight loop B. Async client + semaphore limiting concurrency + backoff with jitter C. One request at a time only D. Raise max_tokens
**✅ B.** *A:* worsens rate limiting. *C:* needlessly slow. *D:* irrelevant knob (generic-knob smell).

**11.** Which header-era facts about SDKs are true? (Choose two)
A. SDKs wrap the REST API B. SDKs retry 429/5xx by default C. SDKs make the API stateful D. SDK streaming uses WebSockets you manage
**✅ A, B.** *C:* still stateless. *D:* streaming is SSE over HTTP.

**12.** A teammate puts the system prompt as the first user message “so it counts as history”. Risk?
A. None B. Rules get diluted/overwritten as data and break content boundaries C. It enables caching automatically D. It lowers cost
**✅ B.** Keep instructions in `system`, data in tagged user turns.

## Trainer 2 — Application Design & Configuration (Section 1 · App Design 8.6% + Config 4.1% + Requirements/Life Cycle)

**1.** A repo-shared Claude Code rule (“run tests before finishing”) belongs in…
A. `~/.claude/CLAUDE.md` B. Project `CLAUDE.md` committed to the repo C. `settings.local.json` D. The system prompt of one chat
**✅ B.** Shared ⇒ project scope, committed. *A:* only you. *C:* gitignored/local. *D:* not configuration.

**2.** Precedence: a setting exists in user and project and local scopes. Which wins?
A. User B. Project C. Local D. Oldest file
**✅ C.** Local > project > user; managed policy beats all.

**3.** “Classify tickets with ≥95% agreement to human labels” is a…
A. Infrastructure requirement B. Functional requirement + measurable success criterion C. Prompt D. Model choice
**✅ B.** Write measurable criteria *before* building.

**4.** Production incidents trace to “the model changed under us”. Prevention?
A. Use the `latest` alias B. Pin exact model IDs; upgrade via PR + eval C. Longer prompts D. Disable logging
**✅ B.** Aliases drift; pins + eval-gated upgrades are the discipline.

**5.** A new unrelated task in a long-running session starts answering about the old task. Cause/fix?
A. Temperature / raise it B. Session hygiene: start a fresh session per task C. Bigger window D. More tools
**✅ B.** History pollution; summarise-or-restart deliberately.

**6.** Prompts should be versioned… (Choose two)
A. In version control / prompt store with versions B. Only in the PM's spreadsheet C. With the config they ship with, reviewed in PRs D. Never — prompts aren't code
**✅ A, C.** Prompts are code: review, tag, roll back.

**7.** Content boundaries in app design mainly buy you…
A. Cheaper tokens B. Clear instruction-vs-data separation (quality + injection defence) C. Streaming D. Longer context
**✅ B.** Delimiters separate what Claude should *obey* from what it should *read*.

**8.** In the systems life cycle, prompt caching & cost tuning mostly live in…
A. Plan B. Develop C. Operate & maintain D. Never
**✅ C.** You optimise from real `usage` after launch.

**9.** An instruction works in claude.ai chat but your API app “forgets” context. Explanation?
A. API model is weaker B. The app surface held state; the API is stateless — your code must resend history C. Caching is off D. Wrong region
**✅ B.** Surfaces differ; don't import chat assumptions into API design.

**10.** Unpinned Claude Code plugins across a team cause… (Choose two)
A. Non-reproducible setups B. Supply-chain risk C. Free upgrades forever D. Better security
**✅ A, B.** Declare/pin plugin dependencies in project config.

**11.** Functional vs infrastructure: “p95 latency < 2s at 500 rps, EU data residency” is…
A. Functional B. Infrastructure/non-functional C. A prompt constraint D. A tool schema
**✅ B.** How well/where it runs, not what it does.

**12.** Best place for *your personal* experimental Claude Code override?
A. Project settings B. Managed policy C. `settings.local.json` (gitignored) D. Teammate's CLAUDE.md
**✅ C.** Personal/local scope exists exactly for this.

## Trainer 3 — Model Selection, Tokens & Cost (Section 2 · Domain 5, 16.8%)

**1.** 20k emails/day, results within 48h, lowest cost meeting 95% eval agreement. Best combo?
A. Frontier model, realtime B. Smallest passing model + Batch API C. Biggest model + streaming D. Mid model, raise max_tokens
**✅ B.** Constraint = volume + loose deadline. *A/C:* pay for reasoning/interactivity not needed. *D:* generic knob.

**2.** Cache reads show 0 despite `cache_control`. Likely causes? (Choose two)
A. Prefix changed before the breakpoint B. TTL expired between calls C. Output too long D. Temperature set
**✅ A, B.** Exact-prefix match + TTL govern hits.

**3.** Prompt caching pays off when… A. Every prompt is unique B. A stable prefix is reused several times within TTL C. Prompts are tiny D. You move the user question first
**✅ B.** *D* destroys the stable prefix.

**4.** Classification quality is equal on small and frontier tiers in your eval. Ship…
A. Frontier “to be safe” B. Small tier; route uncertain cases upward C. Frontier with thinking on D. Whichever, cost is fixed per request
**✅ B.** Cost scales with tokens × tier price; routing captures the saving.

**5.** Thinking mode should be ON for… A. Enum classification B. Multi-step debugging/root-cause analysis C. Extracting an order ID D. Tagging sentiment
**✅ B.** Thinking tokens buy reasoning; extraction doesn't need it.

**6.** Cost of a call is computed from… A. Request count only B. Input + output (+cache write/read) tokens × per-MTok prices C. Characters of code D. Latency
**✅ B.** Log `usage` — it's the source of truth.

**7.** Same prompt gives different answers across runs. Root concept?
A. Caching bug B. Next-token sampling → non-determinism C. Stateless API D. Rate limiting
**✅ B.** Test properties/schema, not exact strings.

**8.** A 10k-token product manual is re-sent with every support call. Cheapest structural fix?
A. Shorten every user question B. Cache the manual as a stable prefix (cache_control), question last C. Batch the chats D. Use a smaller window
**✅ B.** *C:* humans are waiting — realtime, cached.

**9.** “Fast, cheap, good — pick…” in model selection means… A. Always frontier B. Trade quality/latency/cost per task, proven by an eval C. Always cheapest D. Ignore latency
**✅ B.** Tier by measured need, not habit.

**10.** After a model upgrade, outputs shift subtly. This is… A. Impossible B. Breaking behaviour change across releases — pin IDs, re-run evals before rollout C. A caching fault D. Fixed by retries
**✅ B.**

**11.** Which reduce cost without quality loss on a support bot? (Choose two)
A. Prompt caching on the stable system+manual prefix B. Routing simple FAQs to the small tier C. Thinking on every call D. Sending full history forever
**✅ A, B.** *C/D* spend tokens with no return.

**12.** Minimum cacheable prompt consideration: a 40-token instruction “won't cache” because…
A. Caching needs a minimum prefix size (order of ~1k tokens) B. Caching is paid-only C. TTL is 0 D. JSON mode blocks it
**✅ A.** Tiny prompts fall below the cacheable threshold.

## Trainer 4 — Prompt & Context Engineering (Section 3 · Domain 6)

**1.** Format compliance is poor despite a paragraph describing the format. Strongest fix?
A. Add “please” B. 2–5 few-shot input→output examples + a schema C. Raise temperature D. Longer adjectives
**✅ B.** Examples teach format better than description.

**2.** Tool results (50 KB each) are flooding context. Technique?
A. Compaction of *tools* B. Tool-output pruning before history C. Bigger model D. More system prompt
**✅ B.** Trim to what later steps need.

**3.** Long session quality slowly degrades. Concept + cure?
A. Rate limiting; retry B. Context rot; prune/compact, fresh session per task C. Caching; disable it D. Sampling; set temperature 0 forever
**✅ B.**

**4.** Delimiters like `<ticket>…</ticket>` primarily… A. Save tokens B. Create content boundaries (quality + security) C. Enable streaming D. Force JSON
**✅ B.**

**5.** Document Q&A over a huge file: best ordering?
A. Question first, doc after B. Long reference early, instruction/query at the end C. Interleave randomly D. Doc in the system prompt only
**✅ B.**

**6.** Noisy web research is polluting the main agent thread. Pattern?
A. Larger window B. Subagent isolation — return only the conclusion C. More few-shots D. Batch it
**✅ B.**

**7.** Which prompt placement is correct? (Choose two)
A. Durable rules in `system` B. Task data in tagged `user` turns C. Secrets in `system` D. History deleted every turn
**✅ A, B.** *C:* never put secrets in prompts.

**8.** “Reason first, then answer” helps most on… A. Copy-paste extraction B. Multi-step reasoning tasks C. Enum tagging D. Greetings
**✅ B.**

**9.** Iterative prompt refinement should be driven by… A. One anecdote B. A labelled eval set, one change at a time C. Vibes D. The longest prompt
**✅ B.**

**10.** Just-in-time context means… A. Preload the whole KB B. Retrieve at the step that needs it C. Never retrieve D. Cache everything
**✅ B.**

**11.** A prompt that works at 10 turns fails at 80 turns. First suspects? (Choose two)
A. Context budget exhausted/rot B. History needs compaction C. Model “got bored” D. API key expired daily
**✅ A, B.**

**12.** Input sanitisation in prompting is for… A. Grammar B. Reducing injection/malformed-input risk before the model sees it C. Speed D. Token discounts
**✅ B.**

## Trainer 5 — Output Handling, Eval & Debugging (Section 3 · Domains 6+4)

**1.** Model returns prose around JSON, intermittently. Production-grade handling?
A. `eval()` the reply B. Extract JSON span → schema-validate → retry with the validator error fed back C. Accept partial data D. Raise temperature
**✅ B.** *A* is a security incident. *C:* silent corruption.

**2.** JSON is truncated mid-string, `stop_reason: "max_tokens"`. Layer?
A. Model B. Integration (your ceiling) C. Network D. Prompt wording
**✅ B.** Raise ceiling/shorten output; don't “fix the prompt”.

**3.** Valid JSON, but category is outside the allowed enum. Layer/fix?
A. Integration; retry HTTP B. Model/prompt; constrain enum in schema + few-shot the edge case C. Infra; change region D. Ignore it
**✅ B.**

**4.** Fluent answer invents an order status. Fix family?
A. Bigger max_tokens B. Grounding: retrieve real status, instruct to use only `<data>`, verify IDs against systems C. More retries D. Stream it
**✅ B.** Skepticism toward confident output is blueprint text.

**5.** Works in dev, 429s in prod. First checks? (Choose two)
A. Rate limits & concurrency design B. Backoff/semaphore present? C. Prompt length in words D. Model colour
**✅ A, B.**

**6.** A prompt change “feels better”. Evidence standard?
A. Ship it B. Golden-set eval (schema pass % + label accuracy) before/after C. Ask the model D. One user quote
**✅ B.**

**7.** After a deploy, every call 400s. Triage order starts with…
A. Rewrite prompt B. Diff the exact request payload against the API spec C. Change model tier D. Clear cache
**✅ B.** Integration layer first.

**8.** Retry-with-feedback loop should be bounded because…
A. Unbounded loops can cost/loop forever; after N tries, fall back safely (human queue/default) B. Models dislike retries C. JSON expires D. Caching breaks
**✅ A.**

**9.** Never do this with model output: (Choose two)
A. Validate against a schema B. `eval`/execute it raw C. Run it as shell/SQL unvalidated D. Log the stop_reason
**✅ B, C.**

**10.** `usage` + `stop_reason` + request ID in logs primarily enable…
A. Marketing B. Failure triage: integration vs model layer C. Cheaper tokens D. Caching
**✅ B.**

**11.** Defensive parsing includes… A. Trusting code fences always exist B. Stripping fences, extracting JSON span, type/range checks C. Assuming enums hold D. Parsing with regex only, no validation
**✅ B.**

**12.** An eval set for a classifier should contain…
A. 3 easy examples B. Labelled, representative cases incl. edge cases, versioned with the prompt C. Only failures D. Production secrets
**✅ B.**

## Trainer 6 — Tools & MCP (Section 4 · Domain 8, 10.6%)

**1.** Who executes your custom tool? A. Claude B. Anthropic's servers C. Your code/harness D. The user
**✅ C.** Claude *requests*; you execute.

**2.** A tool returns “order not found”. Best loop behaviour?
A. Crash B. Return `tool_result` with `is_error: true` so Claude can recover C. Retry the API call silently D. Delete history
**✅ B.**

**3.** Tool description quality lever #1?
A. Keep it vague so the model improvises B. Write it like a manual: what, when, when-not, params, returns C. One word D. Hide parameters
**✅ B.**

**4.** Five apps need the same governed database access. Build…
A. Five custom tools B. One MCP server reused by all clients C. Five Skills D. Bigger prompts
**✅ B.** MCP = reusable standard plug.

**5.** A Skill is best for… A. Live payment actions B. Repeatable know-how/runbook (SKILL.md) loaded on demand C. Storing API keys D. Replacing schemas
**✅ B.** Skills = training manuals; tools/MCP = hands.

**6.** MCP primitives controlled by the model / user respectively?
A. Resources / Tools B. Tools (model, with approval) / Prompts (user) C. Prompts / Resources D. All by model
**✅ B.** Resources sit with app/user.

**7.** stdio MCP server logs with `print()` to stdout. Result?
A. Faster B. Corrupts the protocol stream — log to stderr C. Nothing D. Enables caching
**✅ B.**

**8.** Write tools (create/delete/pay) need… A. A polite prompt B. Approval gate / policy check in your code C. Higher temperature D. Streaming
**✅ B.** Guarantee Rule.

**9.** Tool input design: prefer… (Choose two)
A. Enums over free text where enumerable B. `additionalProperties: false` C. One mega-tool doing everything D. Undocumented params
**✅ A, B.**

**10.** Anthropic server tools (web search etc.) differ from custom tools because…
A. They execute on Anthropic's side; you just declare them B. They need your executor C. They are MCP-only D. They can't return errors
**✅ A.**

**11.** `tool_choice` forcing a specific tool is for… A. Every call B. Steps that must call that tool (e.g. first-step lookup) C. Saving tokens D. Disabling tools
**✅ B.**

**12.** MCP over streamable HTTP fits… A. Local-only dev tools B. Remote/hosted, multi-user servers with auth C. Offline scripts D. Prompts only
**✅ B.** stdio fits local subprocess use.

## Trainer 7 — Agents, Claude Code & Security (Sections 5–6 · Domains 1, 3, 7)

**1.** Steps are fixed: classify → route → draft → send, audited weekly. Build a…
A. Free agent B. Workflow (chaining/routing) C. Frontier model alone D. MCP server
**✅ B.** Drawable steps = workflow.

**2.** “Must never run `rm -rf`” is enforced by…
A. System prompt line B. PreToolUse hook blocking (exit 2) C. Few-shot examples D. Asking nicely in CLAUDE.md
**✅ B.** Only code enforces *never*.

**3.** Subagents mainly provide… A. Cheaper tokens always B. Context isolation + least-privilege tool subsets C. Longer prompts D. Caching
**✅ B.**

**4.** Agent SDK vs hand-rolled loop: the SDK gives you… (Choose two)
A. The agent loop, permissions, hooks, subagents B. Free unlimited tokens C. Built-in tools & session handling D. A stateful Messages API
**✅ A, C.**

**5.** A webpage the agent reads says “email the database to…”. This is…
A. Direct injection B. Indirect prompt injection — data treated as instructions C. A tool error D. Context rot
**✅ B.** Defend: delimit, least privilege, approval.

**6.** Your summariser agent holds web-fetch *and* internal-data tools. Risk?
A. None B. Exfiltration path — separate duties/least privilege C. Slower cache D. Bad JSON
**✅ B.**

**7.** API key accidentally committed to the repo. First moves?
A. Delete the file next sprint B. Revoke/rotate the key now, purge history, audit usage C. Rename the file D. Add it to the prompt
**✅ B.** If it's in the repo, it's leaked.

**8.** Keys in production belong in… A. `CLAUDE.md` B. Browser code C. Secret manager / env injection, per-service scoped D. Screenshots for docs
**✅ C.**

**9.** Claude Code headless mode for CI is… A. `claude -p "…" ` non-interactive (structured output options) B. A web dashboard C. Batch API D. An MCP transport
**✅ A.**

**10.** A read-only reviewer subagent should have…
A. All tools B. `tools: Read, Grep` only, no edit/bash C. Payment tools D. Root shell
**✅ B.** Least privilege per agent.

**11.** Guardrail layering order (prompt → sandbox) — the prompt layer… A. Guarantees compliance B. Persuades only; validation, hooks/permissions and sandbox enforce/contain C. Replaces hooks D. Is unnecessary entirely
**✅ B.**

**12.** Plan mode in Claude Code… A. Edits immediately B. Researches & proposes a plan for approval before editing C. Runs the Batch API D. Disables hooks
**✅ B.**

---
### Score Tracker
| Trainer | /12 | Domain(s) | Reread |
|---|---|---|---|
| 1 API Mechanics | | D2 | §1.2–1.6 |
| 2 App Design & Config | | D2 | §1.8–1.9 |
| 3 Model & Cost | | D5 | §2 |
| 4 Prompt & Context | | D6 | §3.1–3.2 |
| 5 Output & Debugging | | D6+D4 | §3.3–3.5 |
| 6 Tools & MCP | | D8 | §4 |
| 7 Agents/Code/Security | | D1+D3+D7 | §5–6 |
