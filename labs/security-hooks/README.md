# Guardrail Hook Kit — Lab Guide (Section 6)

```bash
echo '{"tool_name":"Bash","tool_input":{"command":"rm -rf /tmp/x"}}' | python guardrail_hook.py; echo exit=$?   # 2 = blocked
echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | python guardrail_hook.py; echo exit=$?              # 0 = allowed
python test_guardrail.py
```

Wire it into Claude Code via the `PreToolUse` hook in `../claude-code-config/.claude/settings.json`, or as an Agent SDK hook callback returning a block decision.

**The 24-item checklist:** input delimiting • sanitisation • injection tests in CI • least-privilege tools • write-approval gates • destructive-command hook • output schema validation • no blind execution of model output • PII minimisation • no secrets in prompts • keys in env/secret manager • per-env keys & limits • rotation runbook • log redaction • sandboxed code execution • egress allowlist • rate limits/timeouts • plugin pinning • MCP credential scoping • tool-call audit log • leaked-key incident plan • app authN/authZ • content-policy tests • per-tenant session isolation.

**Exercises:** add a rule for `git push --force` to protected branches; write an indirect-injection test page; audit one of your own projects against the 24 items.
