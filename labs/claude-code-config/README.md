# Claude Code Config Pack — Lab Guide (Sections 1 + 5)

Copy into a real repo root: `CLAUDE.md`, `.claude/settings.json`, `.claude/agents/`, `.claude/skills/`, `.mcp.json`.
Keep `settings.local.json` personal and gitignored.

**Exercises**
1. Start Claude Code in the repo — confirm `CLAUDE.md` rules are loaded; ask it to run the tests.
2. Try a denied command (`rm -rf …` in a scratch request) — settings deny-list + the guardrail hook should stop it twice.
3. Delegate a review to the `reviewer` subagent; notice it cannot edit (tools: Read, Grep only).
4. Run headless mode: `claude -p "Summarise this repo" --output-format json`.
5. Change the pinned model in `settings.json` via a PR-style commit message explaining the eval you ran.
