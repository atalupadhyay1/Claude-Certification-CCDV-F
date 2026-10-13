# Section 4 — Claude Tool Use and MCP Servers: Function Calling, Skills, stdio
### Course lecture: Tools and MCP Servers: Tool Schemas and a Working MCP Server (44:27)
### Exam weight: Domain 8 “Tools and MCPs” = **10.6%** (≈ 5–6 questions)

> **Direct answer:** A tool is a **function Claude can ask your systems to run**. Define it with a strict JSON Schema and a description written like a manual for a smart new hire, run the loop (`tool_use` → execute → `tool_result` → repeat until `end_turn`), gate writes behind approval, and return errors as tool results the model can recover from. When many apps need the same capability, package it once as an **MCP server** (tools/resources/prompts over stdio or HTTP) instead of re-implementing it per app.

---

## 4.1 Three Places a Tool Runs — Know Who Executes What

| Kind | Runs where | Examples | You write |
|---|---|---|---|
| **Custom (client-side) tools** | **Your code** | `get_order_status`, `create_ticket` | Definition + executor |
| **Anthropic server tools** | **Anthropic’s servers** | Web search, web fetch, code execution | Just declare them; results return inline |
| **MCP tools** | An **MCP server** process | Database, GitHub, internal APIs via MCP | The MCP server (once) |

Claude never “runs” your custom tool itself — it **requests** it. Your harness executes and reports back. Half of all tool questions are secretly testing whether you know this.

## 4.2 Tool Definition — The Strict Schema

```jsonc
{
  "name": "create_ticket",
  "description": "Create a support ticket. Use only after classifying the issue. Returns the new ticket ID.",
  "input_schema": {
    "type": "object",
    "properties": {
      "title":    {"type": "string", "description": "One-line summary, max 80 chars"},
      "category": {"type": "string", "enum": ["billing","login","bug","other"]},
      "priority": {"type": "string", "enum": ["low","normal","high"], "default": "normal"}
    },
    "required": ["title", "category"],
    "additionalProperties": false
  }
}
```

**Description-writing rules (the #1 quality lever):**
1. Say **what it does, when to use it, when NOT to**, and what it returns — like onboarding a careful colleague.
2. Describe every parameter, its format and examples (`order_id` looks like `ORD-12345`).
3. Prefer **enums** over free text wherever the real world is enumerable; set `additionalProperties: false`.
4. Granularity: one clear job per tool. `manage_database` is a smell; `get_order`, `list_orders` are tools.
5. `tool_choice` control: `auto` (model decides), `any` (must call some tool), a forced specific tool, or disable parallel tool use when order matters. Multiple independent calls *can* arrive in one turn — handle them all.

## 4.3 The Tool-Use Loop — The Five Steps

```
1. Send messages + tool definitions
2. Claude replies stop_reason="tool_use" with tool_use block(s): {id, name, input}
3. YOUR code validates input → (approval gate if write/destructive) → executes
4. Append assistant turn (the tool_use) + user turn with tool_result block(s) {tool_use_id, content}
5. Call again → repeat until stop_reason="end_turn"
```

**Non-negotiables:**
- Echo history faithfully — dropping the `tool_use`/`tool_result` pair corrupts the conversation.
- **Errors are tool results too:** return `{"error": "order not found"}` with `is_error: true` so Claude can apologise/retry/choose another tool, instead of crashing your loop.
- **Approval gate for writes:** reads flow freely; writes/deletes/payments pause for human approval (or policy check) *in your code* — not by asking the model to be careful.
- Bound the loop: max iterations, timeout per tool, validate inputs against the schema before executing.

## 4.4 MCP — Model Context Protocol (2.1% server dev + big concept weight)

> Human analogy: MCP is **USB-C for AI apps**. Before USB, every gadget had its own plug. Before MCP, every AI app hand-wired every data source. MCP defines one plug: a server exposes capabilities; any MCP client (Claude Code, Desktop, your Agent SDK app) can use them.

### The three primitives

| Primitive | Controlled by | Human analogy | Example |
|---|---|---|---|
| **Tools** | Model (with host approval) | Functions the model can call | `query_tickets(status="open")` |
| **Resources** | Application/user | Readable data/context | `ticket://4411`, a file, a DB row as URI |
| **Prompts** | User | Slash-command-like templates | “Summarise this ticket” template |

### Transports
- **stdio:** client launches the server as a subprocess; messages over stdin/stdout. Perfect for local dev tools. *Logs go to stderr — printing to stdout corrupts the protocol stream.*
- **Streamable HTTP:** remote/hosted servers, auth headers, multi-user.

### Building a server (official MCP SDK — Python or TypeScript)
```python
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("flagdesk")

@mcp.tool()
def get_ticket(ticket_id: str) -> dict:
    """Return one support ticket by ID, e.g. 'T-4411'."""
    return DB.get(ticket_id) or {"error": f"ticket {ticket_id} not found"}

if __name__ == "__main__":
    mcp.run(transport="stdio")
```
Register it with your client (e.g. Claude Code: `claude mcp add flagdesk -- python server.py`, or `.mcp.json` in the repo) and the tools appear alongside built-ins.

**Exam angles:** MCP server = the *reusable, governed* way to expose a capability to many clients; tool descriptions/schemas matter exactly as in §4.2; scope servers by least privilege (a read-only DB server should hold read-only credentials); test with the MCP Inspector.

## 4.5 Four Ways to Extend Claude — The Comparison the Exam Loves (4.1%)

| Mechanism | What it is | Choose when… | Not when… |
|---|---|---|---|
| **Built-in / server tools** | Anthropic-provided (web search, code execution…) | The generic capability already exists | You need your private data/actions |
| **Custom tools** | Functions in *your* app’s tool loop | One app needs your API/DB actions | Five apps need the same thing (→ MCP) |
| **Skills** | Packaged instructions + resources/scripts Claude loads on demand (`SKILL.md`) | Repeatable *know-how/workflows* (brand review checklist, deploy runbook) | You need live external actions (→ tool/MCP) |
| **MCP servers** | Standalone capability servers, reusable across clients | Shared, governed access to systems for many clients/agents | A single script in one app would do (overkill) |

**Memory hook:** *Tools = hands, Skills = training manuals, MCP = the standardised toolbox anyone can pick up.*

## 4.6 Hands-On Labs — FlagDesk MCP Server

```bash
cd labs/mcp-server-python
pip install -r requirements.txt
python server.py            # runs over stdio (Ctrl+C to stop) — inspect via MCP Inspector:
npx @modelcontextprotocol/inspector python server.py
python labs/python/04_tool_loop.py --mock   # the manual tool loop, no MCP
```
**Exercises:** (1) Add a `list_open_tickets` tool with an enum filter. (2) Make `create_ticket` require approval in the client loop. (3) Return a deliberate error and watch Claude recover. (4) Connect FlagDesk to Claude Code via `.mcp.json` (see `labs/claude-code-config/`).

## 4.7 Exam Traps
- ❌ “Claude executes the function” → ✅ Claude *requests*; your code/MCP server executes.
- ❌ Swallowing tool errors as exceptions that kill the agent → ✅ return `tool_result` with `is_error`.
- ❌ Building an MCP server for a one-app, one-function need → ✅ custom tool; MCP pays off when shared.
- ❌ A Skill that “calls the payments API” → ✅ Skills carry know-how; tools/MCP carry actions.

➡️ **Next:** [`05-agent-sdk-and-claude-code.md`](05-agent-sdk-and-claude-code.md) • Trainer 6.
