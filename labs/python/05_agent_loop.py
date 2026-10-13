"""Lab 05 — Minimal hand-rolled agent vs workflow thinking (Section 5). Run: python 05_agent_loop.py --mock
Workflow = steps YOU fix in advance. Agent = model picks next step in a bounded loop."""
import argparse

def workflow(ticket):
    steps = ["classify", "route", "draft_reply", "send"]  # fixed, auditable
    return " -> ".join(steps) + f"  [{ticket}]"

MAX_TURNS = 5
def agent(goal):
    findings = []
    for turn in range(1, MAX_TURNS + 1):
        action = ["search_logs", "read_config", "conclude"][min(turn - 1, 2)]  # mocked model choice
        findings.append(action)
        print(f"  turn {turn}: model chose {action}")
        if action == "conclude":
            return f"agent done in {turn} turns: {goal} | path={findings}"
    return "stopped by MAX_TURNS guardrail"

if __name__ == "__main__":
    argparse.ArgumentParser().add_argument("--mock", action="store_true")
    print("WORKFLOW:", workflow("T-4411"))
    print("AGENT:"); print(" ", agent("why did checkout fail?"))
    print("LESSON: drawable steps -> workflow; discovered steps -> agent with max-turns + hooks.")
