# Claude Certification CCDV-F — Complete Study Material
### Exam Trainers + Mock Exam | Beginner to Advanced | Step-by-Step with Hands-On Labs

> **In one line:** This repository is a complete, humanised, lab-first study companion for the **Claude Certified Developer – Foundations (CCDV-F)** exam — it preserves the structure of the Udemy course *“Claude Certification CCDV-F: Exam Trainers + Mock Exam”*, explains every concept like a friendly expert trainer (Google AI-Mode style: direct answer first, then the *why*, tables, examples and traps), and gives you runnable Python + TypeScript labs for every domain.

> ⚠️ **Disclaimer:** This is an **independent, original** study material created for learning. It is **not** affiliated with, sponsored by, or endorsed by Anthropic or Udemy, and it contains **no real exam questions / dumps**. All practice questions are original. Facts such as exam format, fee and domain weights are summarised from the publicly available CCDV-F Exam Guide v1.0 (July 2026) — always re-check the official guide before booking, because programs change.

---

## 📌 Quick Answer — What is CCDV-F?

| Question | Answer |
|---|---|
| Full name | Claude Certified Developer – Foundations |
| Exam code | CCDV-F |
| Validates | You can **build, integrate and ship production-grade applications, agents and workflows** using Claude |
| Questions | **53** items — multiple-choice (1 best answer) + multiple-response (“choose two”, stem states how many) |
| Time | **120 minutes** → **≈ 2.26 minutes per question** |
| Passing score | **720** on a scaled score of 100–1,000 *(720 ≠ 72% correct — scaled scoring weights difficulty)* |
| Fee | **US $125 per attempt** |
| Retake | Failed attempt → wait **at least 14 days**, pay again |
| Validity | **12 months** from award date |
| Delivery | Proctored — online (Pearson VUE / OnVUE) or test centre; register via Anthropic Partner Academy |
| Recommended experience | 1–5 years software engineering, ≥ 6 months with Claude/comparable LLMs, Python **or** TypeScript, REST APIs + CLI fluency |
| Mandatory prerequisites | **None enforced** — recommended ≠ required |

**The one fact most candidates get wrong:** One domain — **Applications and Integration — is 33.1% of the exam** (about 17–18 of 53 questions). Most people over-study agents & prompts and under-study API mechanics, application design and configuration. This material fixes that imbalance.

---

## 🗺️ How This Material Preserves the Course Structure

The Udemy course has **7 sections • 8 lectures • ~5h 49m**. Every section below maps 1-to-1, and expands it with concept deep-dives, labs, trainers and checklists.

| # | Original Course Section (preserved) | Study Doc | Hands-On Lab | Exam Trainer |
|---|---|---|---|---|
| 1 | **Claude API and Applications: Messages API, SDKs, Design, Config** (2 lectures, 1h 30m) | [`docs/01-claude-api-and-applications.md`](docs/01-claude-api-and-applications.md) | `labs/python/01_*`, `labs/typescript/01_*` | 12 Qs — Domain 2 skills |
| 2 | **Claude Model Selection: Opus, Sonnet, Haiku, Tokens, Prompt Caching** (44m) | [`docs/02-model-selection-tokens-cost.md`](docs/02-model-selection-tokens-cost.md) | `labs/python/02_cost_calculator.py` | 12 Qs — Domain 5 |
| 3 | **Prompt and Context Engineering: Structured Output and Debugging** (44m) | [`docs/03-prompt-context-engineering.md`](docs/03-prompt-context-engineering.md) | `labs/python/03_*` | 12 Qs — Domains 6 + 4 |
| 4 | **Claude Tool Use and MCP Servers: Function Calling, Skills, stdio** (44m) | [`docs/04-tools-and-mcp-servers.md`](docs/04-tools-and-mcp-servers.md) | `labs/mcp-server-python/` (FlagDesk) | 12 Qs — Domain 8 |
| 5 | **Claude Agent SDK and Claude Code: Subagents, Hooks, Headless Mode** (43m) | [`docs/05-agent-sdk-and-claude-code.md`](docs/05-agent-sdk-and-claude-code.md) | `labs/claude-code-config/` | 12 Qs — Domains 1 + 3 |
| 6 | **Claude Security: Prompt Injection, Guardrails, Hooks, API Keys** (44m) | [`docs/06-security-guardrails-hooks.md`](docs/06-security-guardrails-hooks.md) | `labs/security-hooks/` | 12 Qs — Domain 7 |
| 7 | **CCDV-F Mock Exam: 53 Questions, Timer and Readiness Score** (40m) | [`docs/07-exam-strategy-and-mock-exam.md`](docs/07-exam-strategy-and-mock-exam.md) | [`practice/mock-exam-53.md`](practice/mock-exam-53.md) | Full 53-Q mock |
| — | Getting started / how to study | [`docs/00-study-roadmap-beginner-to-advanced.md`](docs/00-study-roadmap-beginner-to-advanced.md) | — | Diagnostic |
| — | Last-day revision | [`docs/08-cheat-sheets-and-flashcards.md`](docs/08-cheat-sheets-and-flashcards.md) | `assets/readiness-scorecard.csv` | Flashcards |

**Totals in this repo:** 9 study docs • 84 trainer questions ([`practice/exam-trainers-84.md`](practice/exam-trainers-84.md)) • 53-question timed mock • Python + TypeScript labs • a working MCP server • Claude Code config pack • guardrail hook kit • readiness scorecard.

---

## 🎯 The 8 Exam Domains & 25 Skills (Exam Guide v1.0)

| Domain | Weight | ≈ Qs / 53 | Skills inside (with skill weight) |
|---|---:|---:|---|
| 1. Agents and Workflows | 14.7% | 8 | Agent Construction 5.3% • Agent Patterns & Frameworks 4.9% • Agent Architecture 4.5% |
| 2. Applications and Integration | **33.1%** | 17–18 | App Design 8.6% • SWE Foundations 7.4% • API Mechanics 6.8% • Config Mgmt 4.1% • Requirements 3.4% • Systems Life Cycle 2.8% |
| 3. Claude Code | 3.1% | 1–2 | Claude Code Operation 3.1% |
| 4. Eval, Testing & Debugging | 2.6% | 1–2 | Debugging & Error Handling 2.6% |
| 5. Model Selection & Optimization | 16.8% | 9 | Technical Fundamentals 6.1% • LLM Fundamentals 5.2% • Cost & Token Mgmt 2.8% • Model Selection & Tradeoffs 2.7% |
| 6. Prompt & Context Engineering | 11.0% | 6 | Prompt Engineering 4.6% • Context Engineering 3.8% • Output Handling 2.6% |
| 7. Security & Safety | 8.1% | 4 | AI App Security 3.2% • Guardrails & Safe Deployment 2.3% • Identity/Secrets/Keys 1.6% • Claude Hooks 1.0% |
| 8. Tools & MCPs | 10.6% | 5–6 | Tool Implementation 4.4% • Agentic Customization 4.1% • MCP Server Development 2.1% |
| **Total** | **100%** | **53** | **25 skills** |

> 🧠 **Human way to remember it:** Think of the exam as building a house. **Applications & Integration (33%) is the foundation + wiring.** Model Selection (17%) is choosing the engine. Agents (15%) is the autopilot. Prompts/Context (11%) is how you talk to it. Tools/MCP (11%) are its hands. Security (8%) is the locks. Claude Code (3%) and Eval/Debugging (3%) are small — but easy marks if you prepare them.

---

## 🚀 Start Here (5 minutes)

1. Read [`docs/00-study-roadmap-beginner-to-advanced.md`](docs/00-study-roadmap-beginner-to-advanced.md) and pick your track (2-week / 4-week / 6-week).
2. Run the labs **without an API key first** — every Python lab has a `--mock` mode so you can learn the *shape* for free:
   ```bash
   cd labs/python && pip install -r requirements.txt
   python 01_messages_api.py --mock
   python 02_cost_calculator.py
   python 03_structured_output.py --mock
   ```
3. After each doc, attempt its 12 trainer questions *before* looking at the answers.
4. Finish with the timed mock. **Course readiness bar (stricter than the real pass mark): weighted score > 800 equivalent AND no domain below 60%.** Only then book.

## 📂 Repository Map

```
├── README.md                        ← you are here
├── docs/                            ← step-by-step conceptual study material (00–08)
├── labs/
│   ├── python/                      ← Messages API, streaming, batches, cost, structured output, tool loop
│   ├── typescript/                  ← same core flows in TypeScript
│   ├── mcp-server-python/           ← FlagDesk — a working MCP server over stdio
│   ├── claude-code-config/          ← CLAUDE.md hierarchy, settings.json, subagents, hooks, skills
│   └── security-hooks/              ← PreToolUse guardrail hook that blocks destructive commands
├── practice/
│   ├── exam-trainers-84.md          ← 7 trainers × 12 Qs, every wrong option explained
│   └── mock-exam-53.md              ← full timed mock (questions, then answer key separately)
└── assets/
    └── readiness-scorecard.csv      ← weighted readiness score by domain
```

*Happy building — and good luck. You don't need to be a genius to pass this exam; you need to be systematic. One domain at a time.* 💪
