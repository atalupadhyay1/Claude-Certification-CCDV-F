"""Lab 03 — Structured output: parse -> validate -> retry with error feedback (Section 3).
Run: python 03_structured_output.py --mock [--break-it]"""
import argparse, json

CATEGORIES = {"billing", "login", "bug", "shipping", "other"}
SCHEMA_HINT = 'Return ONLY JSON: {"category": <enum>, "priority": "low|normal|high", "summary": str}'

def validate(obj):
    if not isinstance(obj, dict): return "top level must be an object"
    if obj.get("category") not in CATEGORIES: return f"category must be one of {sorted(CATEGORIES)}"
    if obj.get("priority") not in {"low", "normal", "high"}: return "priority must be low|normal|high"
    if not isinstance(obj.get("summary"), str) or not obj["summary"]: return "summary must be non-empty string"
    return None

def extract_json(text):
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1: raise ValueError("no JSON object found")
    return json.loads(text[start:end+1])

def fake_model(attempt, break_it):
    if break_it and attempt == 1:
        return 'Sure! The category is billingg {"category": "billingg", "priority": "urgent", "summary": "x"'
    if break_it and attempt == 2:
        return '{"category": "billing", "priority": "normal", "summary": "Charged twice for order 4411"}'
    return '{"category": "billing", "priority": "normal", "summary": "Charged twice for order 4411"}'

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--mock", action="store_true")
    ap.add_argument("--break-it", action="store_true"); args = ap.parse_args()
    prompt = SCHEMA_HINT
    for attempt in (1, 2, 3):
        raw = fake_model(attempt, args.break_it)
        print(f"--- attempt {attempt} raw: {raw}")
        try:
            obj = extract_json(raw); err = validate(obj)
        except Exception as e:
            err = f"parse error: {e}"
        if err is None:
            print("✅ VALID:", obj); return
        print(f"❌ {err} -> retry, feeding the error back into the prompt")
        prompt += f"\nYour previous reply failed validation: {err}. Fix it and return ONLY valid JSON."
    print("⚠️ Retries exhausted -> fallback: route to human queue (never crash, never guess).")

if __name__ == "__main__":
    main()
