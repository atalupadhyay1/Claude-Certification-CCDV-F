"""PreToolUse guardrail hook (Section 6 lab). Reads a tool-call JSON event on stdin.
Exit 0 = allow. Exit 2 = BLOCK (stderr message is shown to the model/user)."""
import json, re, sys

DANGEROUS = [
    r"\brm\s+-rf\b", r"\brm\s+.*--no-preserve-root", r"\bDROP\s+(TABLE|DATABASE)\b",
    r"\bmkfs\b", r"\bdd\s+.*of=/dev/", r"curl[^|]*\|\s*(sh|bash)", r"wget[^|]*\|\s*(sh|bash)",
    r":\(\)\s*\{", r">\s*/dev/sd[a-z]",
]

def main() -> None:
    try:
        event = json.load(sys.stdin)
    except Exception:
        sys.exit(0)  # nothing parseable -> nothing to block here; other layers still apply
    if event.get("tool_name") != "Bash":
        sys.exit(0)
    cmd = str(event.get("tool_input", {}).get("command", ""))
    for pattern in DANGEROUS:
        if re.search(pattern, cmd, re.IGNORECASE):
            print(f"🛑 Guardrail blocked destructive command: {cmd!r} (matched /{pattern}/)", file=sys.stderr)
            sys.exit(2)
    sys.exit(0)

if __name__ == "__main__":
    main()
