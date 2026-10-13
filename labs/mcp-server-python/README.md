# FlagDesk MCP Server — Lab Guide (Section 4)

**Goal:** run a real MCP server, inspect its tools/resources/prompts, then connect it to a client.

```bash
pip install -r requirements.txt
npx @modelcontextprotocol/inspector python server.py   # visual inspector
python server.py                                       # raw stdio (Ctrl+C to stop)
```

**Exercises**
1. Call `get_ticket("T-4411")` and `get_ticket("T-9999")` in the Inspector — note the error-as-result pattern.
2. Add a `create_ticket` tool; give it an enum `category`. In the *client*, gate it behind approval.
3. Break it: add a `print("hello")` (stdout) and watch the client fail. Move the log to `sys.stderr`. Remember forever.
4. Connect to Claude Code: copy `../claude-code-config/.mcp.json` next to your project and restart Claude Code.

**Exam links:** tools vs resources vs prompts • stdio vs HTTP transport • least-privilege credentials • description quality.
