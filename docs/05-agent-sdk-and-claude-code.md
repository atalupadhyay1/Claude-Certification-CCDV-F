# Section 5 — Claude Agent SDK and Claude Code: Subagents, Hooks, Headless Mode
### Course lecture: Agents, Agent SDK, and Claude Code: Agent Loops and Repository Setup (42:40)
### Exam weight: Domain 1 “Agents and Workflows” **14.7%** + Domain 3 “Claude Code” **3.1%** (≈ 9–10 questions)

> **Direct answer:** Use a **workflow** when you can draw the steps in advance (predictable, auditable, cheaper) and an **agent** when the task itself decides the steps (open-ended, exploratory). Build agents with the **Claude Agent SDK** unless you need a hand-rolled loop, isolate noisy work in **subagents**, enforce non-negotiables with **hooks**, and set up **Claude Code** per-repo with `CLAUDE.md` + `settings.json` so a whole team gets identical behaviour.

---

## 5.1 Workflow or Agent? — The Foundational Decision (4.5%)

| | Workflow | Agent |
|---|---|---|
| Who decides the steps? | **You**, in code, in advance | **The model**, at runtime, in a loop |
| Shape | Chains, routers, parallel fans, pipelines | Observe → think → tool → observe … until done |
| Predictability / cost | High / lower | Lower / higher (more turns) |
| Best for | Classification pipelines, doc processing, report generation | Debugging, research, multi-file changes, ambiguous tasks |
| Exam wording | “steps are known”, “same every time”, “audit each step” | “depends what it finds”, “open-ended”, “explore” |

**Anthropic’s workflow patterns (know all five):**
1. **Prompt chaining** — step A’s output feeds B (draft → review → polish), with programmatic gates between.
2. **Routing** — classifier sends input to specialised handlers (Haiku router, §2.2).
3. **Parallelization** — sectioning (independent chunks at once) or voting (same task N times, majority/aggregate).
4. **Orchestrator–workers** — a lead model breaks a task down, delegates to worker models, synthesises results.
5. **Evaluator–optimizer** — generator + critic loop until quality bar met.

If a stem’s steps can be drawn as one of these five, the credited answer is almost never “free-running agent”.

## 5.2 The Agent Loop and Your Three Build Options (5.3% + 4.9%)

```
        ┌──────────────────────────────────────────────┐
        ▼                                              │
  send messages+tools → Claude → tool_use? → execute → append result
                                   │no
                                   ▼
                                end_turn → final answer
  Guardrails around the loop: max turns • timeouts • approval gates • hooks
```

| Build option | You get | You own | Choose when |
|---|---|---|---|
| **Claude Agent SDK** (Python/TS) | Loop, built-in tools (file/bash/search), permissions, hooks, subagents, session handling | Your tools, prompts, policy | Default for real agents |
| **Hand-rolled harness** | Full control via Messages API tool loop (§4.3) | Everything incl. loop bugs | Special constraints, learning, tiny agents |
| **Framework** (LangGraph, Strands, PydanticAI…) | Graph/state abstractions, ecosystem integrations | Orchestration semantics | Team already standardised on one |

**Hosted vs self-hosted:** Anthropic-hosted/managed agent runtimes reduce ops (sandboxing, scaling) vs self-hosted gives network/data control (VPC, private tools). Choose by compliance + ops appetite, state the trade-off explicitly in design answers.

## 5.3 Subagents — Context Isolation (and Claude Code agents)

A **subagent** is a fresh Claude instance with its own context window, system prompt, tool subset and (optionally) model — spawned for a bounded job, returning **only its conclusion**.

- **Why:** the main thread stays clean (context isolation), noisy exploration is quarantined, subagents can run in **parallel**, and each gets **least-privilege tools** (researcher = read-only).
- **Manager/supervisor hierarchies:** an orchestrator decomposes, delegates, checks, synthesises. Keep the hierarchy shallow; every layer costs tokens and latency.
- In **Claude Code**, subagents are defined as Markdown files with frontmatter in `.claude/agents/` (project) or `~/.claude/agents/` (user): `name`, `description` (when to delegate — write it for the *router*), `tools`, `model`.

## 5.4 Hooks — Deterministic Enforcement Inside Agents (bridges to Security)

Hooks are **your code** that runs at fixed lifecycle points — they don’t ask the model’s permission.

| Hook | Fires | Classic uses |
|---|---|---|
| `PreToolUse` | Before a tool executes | **Block destructive commands**, require approval, validate args |
| `PostToolUse` | After a tool returns | Log, format/check output, redact |
| `UserPromptSubmit` | User prompt enters | Inject context, screen input |
| `Stop` / `SubagentStop` | Agent (subagent) finishes | Verify deliverable exists, run tests |
| `SessionStart` / `PreCompact` | Session lifecycle | Load context, save state before compaction |

Exit-code contract (Claude Code): exit 0 = allow; **exit 2 = block with message** (stderr is fed back); other non-zero = error. In the Agent SDK, hooks are callbacks in code with the same spirit: return a decision (`allow`/`deny`/`ask` + optional modified input).

## 5.5 Memory for Agents

Short-term = the conversation/tool history (manage it like Section 3 teaches). Long-term = **external**: files, a memory tool/store, vector DB — the model only “remembers” across sessions what your system persists and re-injects. Agent memory in Claude Code (per-agent persistent notes where supported) follows the same rule: it’s stored state, not magic.

## 5.6 Claude Code — Repository Setup (Domain 3, 3.1%)

Claude Code is Anthropic’s agentic coding tool (terminal/IDE/desktop). Exam surface is small but very “listable”:

| Feature | What it is |
|---|---|
| **`CLAUDE.md`** | Project memory/instructions auto-loaded per hierarchy (§1.9). Keep short, factual, committed |
| **`settings.json`** | Permissions allow/deny lists, model pin, env, hooks — scopes: managed > user > project > local precedence as in §1.9 |
| **Slash commands** | Reusable prompts in `.claude/commands/` (project) / `~/.claude/commands/` (personal), invoked `/name` |
| **Skills** | `.claude/skills/<name>/SKILL.md` — know-how loaded on demand (§4.5) |
| **Subagents** | `.claude/agents/*.md` with own tools/model (§5.3) |
| **MCP in Claude Code** | `claude mcp add …` or `.mcp.json` — scopes: local/project/user |
| **Plan mode** | Claude researches & proposes a plan without editing until approved |
| **Headless mode** | `claude -p "…"` non-interactive, structured output options — for CI/scripts |
| **Auto / permission modes** | How much executes without asking; least privilege by default |
| **Session management** | Resume/continue sessions; fresh session per task (hygiene, §3.2) |

**Team setup recipe (the lab):** commit `CLAUDE.md` + `.claude/settings.json` (permissions + model pin) + `.claude/agents/` + `.mcp.json`; gitignore `settings.local.json`; document it in the repo README. A new hire clones → identical Claude behaviour.

## 5.7 Hands-On Labs

```bash
cat labs/claude-code-config/CLAUDE.md
cat labs/claude-code-config/.claude/settings.json
claude -p "Explain this repo's structure" --output-format json   # headless, if Claude Code installed
python labs/python/05_agent_loop.py --mock                        # minimal hand-rolled agent
```
**Exercises:** (1) Classify 6 scenarios as workflow/agent in one sentence each. (2) Write a read-only `reviewer` subagent definition. (3) Add a `Stop` hook that runs the test suite. (4) Run the same task in a fresh vs polluted session; compare.

## 5.8 Exam Traps
- ❌ Agent for a fixed 3-step pipeline → ✅ workflow (chaining).
- ❌ “Ask the agent not to delete files” → ✅ PreToolUse hook blocks it.
- ❌ One mega-agent with all tools for everything → ✅ subagents, least-privilege tool subsets.
- ❌ Personal API-taming rules in project `CLAUDE.md` → ✅ personal → user/local scope; shared → project.

➡️ **Next:** [`06-security-guardrails-hooks.md`](06-security-guardrails-hooks.md) • Trainer 7 in practice file (Domains 1+3).
