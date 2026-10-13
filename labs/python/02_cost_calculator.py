"""Lab 02 — Price one Claude request; caching & Batch scenarios (Section 2).
Prices below are ILLUSTRATIVE — replace with current official pricing before real decisions.
Run: python 02_cost_calculator.py [--scenario support-bot]"""
import argparse

PRICES = {  # USD per 1M tokens: (input, output, cache_write, cache_read)
    "haiku-class":  (1.00, 5.00, 1.25, 0.10),
    "sonnet-class": (3.00, 15.00, 3.75, 0.30),
    "opus-class":   (15.00, 75.00, 18.75, 1.50),
}

def cost(tier, inp, out, cache_write=0, cache_read=0, batch=False):
    pi, po, pw, pr = PRICES[tier]
    total = (inp*pi + out*po + cache_write*pw + cache_read*pr) / 1e6
    return total * 0.5 if batch else total

def show(label, value): print(f"  {label:<55} ${value:,.4f}")

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--scenario", default="support-bot"); args = ap.parse_args()
    print(f"Scenario: {args.scenario} — 4,000 input (3,800 stable manual) + 300 output, sonnet-class")
    show("Realtime, no cache", cost("sonnet-class", 4000, 300))
    show("Realtime, cached prefix", cost("sonnet-class", 200, 300, cache_read=3800))
    show("Batch, no cache (x0.5)", cost("sonnet-class", 4000, 300, batch=True))
    print("\n50,000 such calls/month:")
    show("Realtime no cache / month", cost("sonnet-class", 4000, 300) * 50000)
    show("Realtime cached / month", cost("sonnet-class", 200, 300, cache_read=3800) * 50000)
    show("Haiku-class, cached / month", cost("haiku-class", 200, 300, cache_read=3800) * 50000)
    print("\nTier comparison for one 4k-in / 300-out call:")
    for tier in PRICES: show(tier, cost(tier, 4000, 300))
    print("\nLESSON: tier choice > caching > batch — combine all three when the stem allows.")

if __name__ == "__main__":
    main()
