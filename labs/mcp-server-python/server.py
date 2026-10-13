"""FlagDesk — a working MCP server over stdio (Section 4 lab).
Install: pip install -r requirements.txt
Run (stdio): python server.py        Inspect: npx @modelcontextprotocol/inspector python server.py
Claude Code: claude mcp add flagdesk -- python server.py   (or commit .mcp.json, see labs/claude-code-config)
IMPORTANT: never print() to stdout in a stdio server — stdout is the protocol. Log to stderr."""
import sys
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("flagdesk")

_TICKETS = {
    "T-4411": {"id": "T-4411", "title": "Charged twice", "category": "billing", "status": "open"},
    "T-4412": {"id": "T-4412", "title": "Cannot log in", "category": "login", "status": "open"},
}

@mcp.tool()
def get_ticket(ticket_id: str) -> dict:
    """Return one FlagDesk support ticket by ID (format 'T-1234'). Read-only."""
    return _TICKETS.get(ticket_id, {"error": f"ticket {ticket_id} not found"})

@mcp.tool()
def list_open_tickets(category: str = "all") -> list:
    """List open tickets, optionally filtered by category: billing|login|bug|other|all."""
    return [t for t in _TICKETS.values() if t["status"] == "open" and (category == "all" or t["category"] == category)]

@mcp.resource("ticket://{ticket_id}")
def ticket_resource(ticket_id: str) -> str:
    """A ticket exposed as a readable resource (application/user-controlled context)."""
    t = _TICKETS.get(ticket_id)
    return str(t) if t else f"ticket {ticket_id} not found"

@mcp.prompt()
def summarise_ticket(ticket_id: str) -> str:
    """User-invoked template: summarise a ticket for a handover note."""
    return f"Summarise ticket {ticket_id} in two lines: problem, and next action."

if __name__ == "__main__":
    print("flagdesk MCP server starting on stdio", file=sys.stderr)
    mcp.run(transport="stdio")
