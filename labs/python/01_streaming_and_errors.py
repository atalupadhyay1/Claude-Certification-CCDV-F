"""Lab 01b — Streaming (SSE) shape + retry-by-error-type. Run: python 01_streaming_and_errors.py --mock"""
import argparse, random, time

EVENTS = [
    ("message_start", {}), ("content_block_start", {"index": 0}),
    ("content_block_delta", {"text": "Billing"}), ("content_block_delta", {"text": " issue"}),
    ("content_block_delta", {"text": " confirmed."}), ("content_block_stop", {"index": 0}),
    ("message_delta", {"stop_reason": "end_turn", "output_tokens": 6}), ("message_stop", {}),
]
RETRYABLE = {429, 500, 502, 503, 529}

def should_retry(status: int) -> bool:
    return status in RETRYABLE

def call_with_backoff(fn, max_retries=3):
    for attempt in range(max_retries + 1):
        try:
            return fn()
        except RuntimeError as e:
            status = int(str(e).split()[0])
            if not should_retry(status) or attempt == max_retries:
                raise
            delay = (2 ** attempt) + random.uniform(0, 0.5)
            print(f"  status {status} retryable -> backoff {delay:.1f}s (attempt {attempt+1})")
            time.sleep(min(delay, 0.2))  # shortened for the lab

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--mock", action="store_true"); ap.parse_args()
    print("=== STREAM ===")
    text = ""
    for name, data in EVENTS:
        print(f"event: {name} {data}")
        text += data.get("text", "")
    print("assembled:", text)
    print("\n=== RETRY POLICY ===")
    for s in (400, 401, 403, 404, 413, 429, 500, 529):
        print(f"  {s}: {'RETRY (backoff)' if should_retry(s) else 'FAIL FAST (fix the cause)'}")
    calls = {"n": 0}
    def flaky():
        calls["n"] += 1
        if calls["n"] < 3: raise RuntimeError("529 overloaded")
        return "ok"
    print("flaky call ->", call_with_backoff(flaky))

if __name__ == "__main__":
    main()
