"""Lab 04 — The manual tool-use loop with approval gate + error-as-tool-result (Section 4).
Run: python 04_tool_loop.py --mock"""
import argparse, json

TOOLS = [{
    "name": "create_ticket",
    "description": "Create a support ticket after classifying. Returns the new ticket ID. Write action.",
    "input_schema": {"type": "object",
        "properties": {"title": {"type": "string"},
                       "category": {"type": "string", "enum": ["billing", "login", "bug", "other"]}},
        "required": ["title", "category"], "additionalProperties": False},
}]
WRITE_TOOLS = {"create_ticket"}

def execute(name, args, approve):
    if name in WRITE_TOOLS and not approve:
        return {"error": "approval_required: a human must approve this write"}, True
    if args.get("category") not in {"billing", "login", "bug", "other"}:
        return {"error": f"unknown category {args.get('category')}"}, True
    return {"ticket_id": "T-9001", "title": args["title"]}, False

def fake_claude(turn):
    if turn == 1:
        return {"stop_reason": "tool_use", "content": [{"type": "tool_use", "id": "toolu_1",
                "name": "create_ticket", "input": {"title": "Charged twice", "category": "billing"}}]}
    return {"stop_reason": "end_turn", "content": [{"type": "text", "text": "Done — ticket T-9001 created."}]}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--mock", action="store_true"); args = ap.parse_args()
    APPROVED = True  # simulate human approval in the harness (NOT by asking the model)
    history = [{"role": "user", "content": "Customer charged twice on order 4411 — log it."}]
    for turn in (1, 2, 3):
        resp = fake_claude(turn if turn == 1 or history[-1].get("content") else 2)
        print(f"turn {turn}: stop_reason={resp['stop_reason']}")
        if resp["stop_reason"] != "tool_use":
            print("final:", resp["content"][0]["text"]); break
        call = resp["content"][0]
        result, is_error = execute(call["name"], call["input"], APPROVED)
        print(f"  executed {call['name']}({call['input']}) -> {result} is_error={is_error}")
        history += [{"role": "assistant", "content": [call]},
                    {"role": "user", "content": [{"type": "tool_result", "tool_use_id": call["id"],
                     "content": json.dumps(result), "is_error": is_error}]}]
    print("LESSON: Claude requests; YOUR code validates, gates writes, executes, reports errors back.")

if __name__ == "__main__":
    main()
