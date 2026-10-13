# 08 — Cheat Sheets, Flashcards & Memory Aids (Last-Day Revision)

> **How to use:** Read the tables actively — cover the right column, recall, check. Then run the flashcard list as “know it / still learning” piles, exactly like the course’s study games.

## A. Numbers That Must Be Reflexes
| Fact | Value |
|---|---|
| Questions / minutes / per-question | 53 / 120 / ≈2.26 min |
| Pass | Scaled **720** of 100–1,000 |
| Fee / retake wait / validity | $125 / ≥14 days / 12 months |
| Domain weights | Apps&Integration 33.1 • ModelSel 16.8 • Agents 14.7 • Prompt&Context 11.0 • Tools&MCP 10.6 • Security 8.1 • ClaudeCode 3.1 • Eval&Debug 2.6 |
| Batch discount / latency | ~50% / up to 24 h |
| Prompt-cache TTLs | 5 min (default), 1 h (extended) |
| SDK default retries | 2 (on 429/5xx) |

## B. Decision Tables (the exam in miniature)
| Stem says… | Answer shape |
|---|---|
| Human waiting, spinner complaints | Streaming (SSE) |
| Bulk + loose deadline + cheapest | Batch API + smallest passing model |
| Stable big prompt reused | Prompt caching, stable prefix first |
| Must *never* happen | Hook / permission / validation — never prompt-only |
| Steps drawable in advance | Workflow (chain/route/parallel/orchestrate/evaluate) |
| Steps depend on findings | Agent (SDK loop) |
| Same capability, many apps | MCP server |
| Repeatable know-how, no live action | Skill |
| One app, my API action | Custom tool |
| Broken JSON mid-string | `max_tokens` truncation (integration layer) |
| 400 after deploy | Integration bug — don’t retry, fix payload |
| Hidden instructions in a webpage | Indirect injection → delimit, least privilege, approval |

## C. Flashcards (Q → A)
1. Stateless? → API remembers nothing; resend history.
2. `stop_reason: tool_use`? → Run tool, append `tool_result`, call again.
3. Retry which errors? → 429, 5xx, timeouts — exponential backoff + jitter.
4. Cache breakpoint rule? → Stable prefix first, variable last; verify `cache_read_input_tokens`.
5. Smallest model rule? → Smallest tier that *passes your eval*; route hard cases up.
6. Workflow vs agent decider? → Can you draw the steps in advance?
7. Tool error handling? → Return `tool_result` with `is_error: true`; don’t crash the loop.
8. MCP primitives? → Tools (model), Resources (app/user), Prompts (user).
9. stdio gotcha? → Logs to stderr; stdout is protocol.
10. PreToolUse block? → Exit 2 (Claude Code) / decision:block (Agent SDK).
11. Key storage? → Env/secret manager; never code, prompt, log or client-side.
12. Config precedence? → Local > project > user; managed policy beats all.
13. “Choose two” check? → Exactly two; judge each independently.
14. Context rot cure? → Prune tool output, compact history, subagent isolation.
15. Guarantee rule? → *Must/never* ⇒ enforcing mechanism, not advice.

## D. One-Sentence Domain Summaries
- **Apps & Integration:** Stateless Messages API, errors/retries, batch-vs-realtime, config scopes. *(33% — live here.)*
- **Model Selection:** Tokens, tiers, cost formula, caching breakpoints.
- **Agents:** Workflow if drawable, agent if discovered; subagents isolate context.
- **Prompt & Context:** System=user rules vs task; schema + validate + retry-with-feedback.
- **Tools & MCP:** Claude requests, you execute; MCP is the reusable USB-C.
- **Security:** Data ≠ instructions; layers; hooks enforce.
- **Claude Code:** `CLAUDE.md`, `settings.json`, commands/skills/agents, headless `-p`.
- **Eval & Debugging:** Which layer failed? Prove fixes on a golden set.

## E. Exam-Morning Checklist
ID ✓ quiet room ✓ system test done ✓ water/break rules known ✓ clock checkpoints (18/35/53) ✓ flag-don’t-freeze ✓ no blanks ✓.

*You’ve done the work. Trust the system: constraint → mechanism → eliminate smells → answer.* 🍀
