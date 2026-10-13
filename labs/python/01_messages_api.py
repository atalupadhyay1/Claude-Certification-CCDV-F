"""Lab 01 — Messages API anatomy (Section 1). Run: python 01_messages_api.py --mock"""
import argparse, json, os, sys

MOCK_RESPONSE = {
    "id": "msg_mock_001", "type": "message", "role": "assistant", "model": "mock-claude",
    "content": [{"type": "text", "text": '{"category": "billing", "priority": "normal"}'}],
    "stop_reason": "end_turn",
    "usage": {"input_tokens": 412, "output_tokens": 14, "cache_read_input_tokens": 0},
}

def build_request() -> dict:
    return {
        "model": os.environ.get("CLAUDE_MODEL", "claude-sonnet-5"),
        "max_tokens": 256,
        "system": "You are a support triage assistant. Reply ONLY with JSON: {category, priority}.",
        "messages": [
            {"role": "user", "content": "<ticket>Order #4411 was charged twice</ticket>\nClassify this ticket."}
        ],
    }

def main() -> None:
    ap = argparse.ArgumentParser(); ap.add_argument("--mock", action="store_true"); args = ap.parse_args()
    req = build_request()
    print("=== REQUEST ==="); print(json.dumps(req, indent=2))
    if args.mock:
        resp = MOCK_RESPONSE
    else:
        if not os.environ.get("ANTHROPIC_API_KEY"):
            sys.exit("Set ANTHROPIC_API_KEY or run with --mock")
        import anthropic
        resp = anthropic.Anthropic().messages.create(**req).model_dump()
    print("\n=== RESPONSE ==="); print(json.dumps(resp, indent=2))
    print(f"\nstop_reason={resp['stop_reason']}  usage={resp['usage']}")
    assert resp["stop_reason"] == "end_turn"
    parsed = json.loads(resp["content"][0]["text"])
    assert parsed["category"] == "billing"
    print("✅ Parsed & validated:", parsed)
    print("TRY: set max_tokens=5 in build_request() and observe stop_reason='max_tokens'.")

if __name__ == "__main__":
    main()
