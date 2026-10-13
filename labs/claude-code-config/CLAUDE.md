# Project: FlagDesk Support Platform (example CLAUDE.md — commit this file)

## What this repo is
Support-ticket platform. Python API in `labs/`, MCP server in `labs/mcp-server-python/`.

## Rules Claude must follow in this repo
- Run tests with `python -m pytest -q` before declaring any change done.
- Never edit `labs/security-hooks/` without adding a test case for the new rule.
- Model IDs are pinned in settings/config — never switch a model without updating the eval notes.
- Do not commit `.env` files, API keys, or `settings.local.json`.

## Style
- Python: type hints on public functions, no print() in MCP stdio servers (stderr only).
- Keep prompts and tool schemas in version control; change them via PR.
