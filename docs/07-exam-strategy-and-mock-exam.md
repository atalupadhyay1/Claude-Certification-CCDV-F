# Section 7 — CCDV-F Mock Exam: 53 Practice Questions, Timer and Readiness Score
### Course lecture: Exam Strategy and Mock Exam: Readiness Score and 53-Question Test (40:26)

> **Direct answer:** Book the real exam only when a **blueprint-weighted mock puts you above the 800-equivalent readiness bar with no domain under 60%**. In the hall, budget **2.26 minutes per question**, flag-and-move on anything over budget, and eliminate options with the four “option smells” below before choosing.

---

## 7.1 The Exam on One Page

| Fact | Value |
|---|---|
| Items / time | 53 items / 120 minutes (multiple-choice + multiple-response; stem states how many to pick) |
| Scoring | Scaled 100–1,000; **720 passes**; report shows scaled score + % correct per domain |
| Fee / retake / validity | $125 per attempt; ≥14 days after a fail; credential valid 12 months |
| Blueprint | 8 domains, 25 skills — weights in the README table; Domain 2 alone = 33.1% |
| Delivery | Pearson VUE proctored (online or centre), booked via Anthropic Partner Academy |

## 7.2 The Readiness Score — How to Know You’re Ready

The course’s bar is deliberately stricter than the pass mark (the readiness score is the *course’s* estimate, not Anthropic’s scoring):

```
weighted % = Σ (domain % correct × domain weight) / Σ weights
Ready  ⇔  weighted equivalent > 800-level performance  AND  min domain ≥ 60%
```

| Zone | Signal | Action |
|---|---|---|
| 🔴 Not yet | Weighted < ~720-equivalent or any domain < 50% | Full restudy of weak domains; no booking |
| 🟠 Close | Passing overall but a domain is 50–60% | Targeted trainer drills on that domain only; re-mock in 3–4 days |
| 🟢 Book it | > 800-equivalent **and** every domain ≥ 60% (aim ≥ 70%) | Book within 1–2 weeks while it’s fresh |

Use `assets/readiness-scorecard.csv`: enter % per domain after each mock; it weights them and applies the formula from §00.4 to split your next study hours by gap.

## 7.3 The 120-Minute Time Plan

| Phase | Clock | Do |
|---|---|---|
| Pass 1 | 0–75 min | Answer everything you can in ≤2 min; **flag** the rest, guess tentatively |
| Pass 2 | 75–105 min | Flagged items only; apply Constraint/Guarantee rules slowly |
| Review | 105–120 min | Check flagged + “choose two” items (count your selections!); never leave blanks |

2.26 min/item is an average, not a ration: bank time on recall items, spend it on scenario items.

## 7.4 The Four Option Smells — Cross These Out First

1. **Generic-knob smell:** “increase `max_tokens` / use a bigger model / add more context” when the stem’s constraint is cost, deadline or safety.
2. **Prompt-only guarantee:** “instruct the model never to…” for a *must/never* requirement — enforcement (hook/schema/permission) beats advice.
3. **Wrong-layer smell:** fixing a 400 error by rewriting the prompt; fixing bad JSON shape by adding retries at the HTTP layer.
4. **Absolutist / off-blueprint smell:** “always”, “never needs validation”, brand-new features the guide never mentions, or options that leak keys/PII.

Then the two golden rules (§00.2): find the binding constraint; for *must/never*, pick the enforcing mechanism.

## 7.5 Multiple-Response (“Choose Two”) Discipline
- The stem states the count — select **exactly** that many.
- Evaluate each option true/false independently *before* looking at pairings.
- The common pattern: one option from each of two layers (e.g. delimiting **and** least-privilege tools).

## 7.6 Exam-Day Rules
- Week before: system-test proctoring, ID check, quiet room booked.
- Day before: light revision (cheat sheet, §08), early night; no new topics.
- During: no blanks, watch the clock at items 18 / 35 / 53 checkpoints (≈ 40 / 79 / 120 min).
- After a fail (if it happens): your domain report *is* your study plan; ≥14 days, restudy gaps, re-mock, retake. The credential renews on a 12-month cycle — keep building with Claude and renewal prep is just revision.

## 7.7 Sit the Mock — Now
1. Set a **120-minute timer**. Open [`../practice/mock-exam-53.md`](../practice/mock-exam-53.md) — questions first, answer key is separated at the end (no peeking).
2. Score per domain into `assets/readiness-scorecard.csv`.
3. For every miss, write the one-line reason and the doc section to reread. Restudy, then drill that domain’s trainer (12 Qs) in [`../practice/exam-trainers-84.md`](../practice/exam-trainers-84.md).

➡️ **Final revision:** [`08-cheat-sheets-and-flashcards.md`](08-cheat-sheets-and-flashcards.md)
