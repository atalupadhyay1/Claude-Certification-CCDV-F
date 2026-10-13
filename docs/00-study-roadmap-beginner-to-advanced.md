# 00 — Study Roadmap: Beginner → Advanced (Step by Step)

> **Direct answer:** If you study in the order of the course (API first, agents later), do one lab per concept, and only sit mocks *after* finishing all 7 sections, a beginner needs roughly **35–50 focused hours** to reach the readiness bar (>800 equivalent, no domain <60%). Experienced Claude builders need **15–25 hours**, mostly on Domains 2, 5 and 7.

---

## 1. Who This Is For — Be Honest About Your Level

| Level | You are here if… | Your risk on exam day |
|---|---|---|
| **Beginner** | You code in Python/TS but have never called an LLM API | You treat Claude like a chatbot, not an API — you’ll miss mechanics questions |
| **Intermediate** | You’ve called the Messages API, written prompts, maybe used tools | You know the *happy path* but not errors, caching breakpoints, batch trade-offs |
| **Advanced** | You’ve shipped a Claude feature/agent to production | You over-trust intuition; exam wants the *guaranteed* mechanism, not the clever one |

**Human truth:** The exam does not reward “I’ve used ChatGPT a lot.” It rewards *“I know exactly which knob guarantees this outcome, and why the other three knobs don’t.”*

## 2. The Two Golden Rules of Every CCDV-F Question

Learn these now; they will eliminate 1–2 wrong options on almost every item.

### Rule 1 — The Constraint Rule
> Find the **binding constraint** in the stem (deadline, budget, latency, “within 2 days”, “must never”), pick the mechanism **built for that constraint**, strike every option that just “turns a generic knob” (e.g. *increase max_tokens*, *use a bigger model*) without addressing it.

*Example pattern:* “20,000 emails/day, results within 48 hours, lowest cost” → constraint = volume + loose deadline → **Message Batches API + small model**, not realtime streaming with the largest model.

### Rule 2 — The Guarantee Rule
> When the stem says **must / never / guarantee / block**, advice-level options (“tell the model not to…”, “add a warning to the prompt”) are **distractors**. Only an **enforcing mechanism** can be correct: a hook, schema validation, permission gate, allowlist, sandbox.

*Example pattern:* “The agent must **never** run `rm -rf`” → correct = **PreToolUse hook that exits non-zero**, not “add ‘never delete files’ to the system prompt.” Prompts *influence*; hooks *enforce*.

## 3. Step-by-Step Path (Preserves Course Order)

### Phase 0 — Setup (Day 1, ~1 hour)
- [ ] Install Python 3.11+ and/or Node 20+; create a project folder and a virtual env / `npm init`.
- [ ] (Optional) Get an Anthropic API key from the Console → store it as an **environment variable**, never in code:
  ```bash
  export ANTHROPIC_API_KEY="sk-ant-..."   # macOS/Linux
  $env:ANTHROPIC_API_KEY="sk-ant-..."    # Windows PowerShell
  ```
- [ ] Run every lab once with `--mock` — feel the request/response shape before spending a cent.
- [ ] Attempt the 10 diagnostic questions in `practice/exam-trainers-84.md` (Trainer 0) and note weak domains.

### Phase 1 — The Big Third: API & Applications (Days 2–6)
Study `docs/01…`, labs `01_*`. You must be able to, from memory: draw a Messages request, name every `stop_reason`, pick retry vs. fail-fast per error type, and explain CLAUDE.md scopes.

### Phase 2 — Engine & Money: Model Selection (Days 7–9)
Study `docs/02…`, run the cost calculator on 5 scenarios until pricing a request feels like estimating a taxi fare — automatic.

### Phase 3 — Talking Well: Prompts, Context, Output (Days 10–13)
Study `docs/03…`; practise defensive parsing until “the model returned prose around JSON” stops scaring you.

### Phase 4 — Hands: Tools & MCP (Days 14–18)
Study `docs/04…`; run FlagDesk MCP server, inspect it, break it, fix it.

### Phase 5 — Autopilot: Agents & Claude Code (Days 19–24)
Study `docs/05…`; decide workflow-vs-agent on 10 scenarios out loud, in one sentence each.

### Phase 6 — Locks: Security (Days 25–27)
Study `docs/06…`; install the guardrail hook and *try* to make it run a destructive command. It should refuse.

### Phase 7 — Exam Mode (Days 28–30+)
Study `docs/07…`; sit the 53-Q mock under a real 120-minute timer, score by domain in `assets/readiness-scorecard.csv`, restudy only the gaps, repeat with trainer questions.

## 4. Three Ready-Made Timetables

| Track | Who | Daily load | Structure |
|---|---|---|---|
| **6-week gentle** | Beginner, working full-time | 1 h/day weekdays | 1 section/week, mock in week 6 |
| **4-week standard** | Intermediate | 1.5–2 h/day | 2 sections/week in weeks 1–2, labs week 3, mocks week 4 |
| **2-week sprint** | Advanced / retake | 3 h/day | Docs skimmed, labs + trainers daily, mocks on days 10, 12, 14 |

**Study-hours-by-gap formula (from the course scorecard):** after a mock, give each domain below 80% a share of your next 10 hours proportional to `(weight × (100 − your %))`. Big *and* weak beats small *and* weak.

## 5. How to Use Each Chapter (The Learning Loop)

For every section, repeat this loop — it is how adults actually retain technical material:

1. **Preview (5 min):** Read the “Direct answer” box and the exam-weight table.
2. **Concept (25 min):** Read with a pen; say each idea back in your own words (Feynman technique).
3. **Lab (25 min):** Type the code — don’t copy-paste the important lines. Break one thing on purpose; read the error.
4. **Trainer (15 min):** 12 questions, timed. For every wrong answer, write *why the correct one wins* in one line.
5. **Teach (5 min):** Explain the section to an imaginary junior. If you stumble, that’s your revision list.

## 6. Exam Logistics Checklist

- [ ] Register via **Anthropic Partner Academy**; exam delivered by **Pearson VUE**.
- [ ] Fee **$125** ready; ID matching your registration name exactly.
- [ ] Online proctoring: quiet room, clear desk, working webcam/mic, stable internet; test your system a week before.
- [ ] Know the rules: 53 items, 120 min, scaled 720 to pass, result = pass/fail + scaled score + % by domain.
- [ ] Credential valid **12 months**; failed attempt → **≥14 days** before retake.

## 7. Anti-Patterns That Fail Good Engineers

| Trap | Why it feels right | What the exam wants |
|---|---|---|
| “Use the smartest model” for everything | Safer quality | Tier by task; Haiku-class for classification/routing, Opus-class only where reasoning pays |
| “Add it to the prompt” for safety | Prompts are flexible | Enforcement (hooks/permissions/validation) for *must/never* requirements |
| Streaming for a nightly bulk job | Streaming feels modern | Batch API: 50%-class discount, no realtime need |
| Long system prompt re-sent every call | It works | Prompt caching with breakpoints; cache the stable prefix |
| Trusting model JSON blindly | It usually parses | Schema + defensive parsing + retry-with-error-feedback |

➡️ **Next:** [`01-claude-api-and-applications.md`](01-claude-api-and-applications.md)
