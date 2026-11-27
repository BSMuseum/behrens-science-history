#!/usr/bin/env python3
"""Score the predictions made before an entry was read against its claims.

    python3 -I tools/score_predictions.py                 # every entry with a predictions file
    python3 -I tools/score_predictions.py 1675-air        # one entry, with each prediction listed

Reads predictions/<entry>.json and claims/<entry>.json; writes nothing.

A prediction is about one text (entry siglum) on one question. It scores
1 if the claims bear it out, 0 if they show something else, and is left
unscored if the entry has no claim on that question from any text (the
question did not come up), or only not_found claims for that text:

- holds X:  1 if the text holds or leans X.
- rejects X: 1 if the text rejects X.
- reports, undecided, declines: 1 if the text has a claim with that stance.
- not_taken_up: 1 if the text's claims on the question are all not_taken_up,
  or the text has none while another text has one.

Brier score = mean of (p - outcome)^2 over scored predictions: 0 is perfect,
0.25 is what always saying p = 0.5 earns. The "expected" list (free-text
expectations about common ground, disputes and new questions) is not scored
here; the entry's pull request scores it by hand.
"""

import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BINS = [(0.0, 0.6), (0.6, 0.8), (0.8, 0.95), (0.95, 1.01)]


def outcome(pred, claims):
    q, t = pred["question"], pred["text"]
    on_q = [c for c in claims if c["question"] == q]
    if not on_q:
        return None
    mine = [c for c in on_q if c["text"] == t and c["stance"] != "not_found"]
    if not mine:
        if any(c["text"] == t for c in on_q):  # only not_found
            return None
        return int(pred["stance"] == "not_taken_up")
    st = pred["stance"]
    if st == "not_taken_up":
        return int(all(c["stance"] == "not_taken_up" for c in mine))
    if st == "holds":
        return int(any(c["stance"] in ("holds", "leans") and c.get("answer") == pred["answer"] for c in mine))
    if st == "rejects":
        return int(any(c["stance"] == "rejects" and c.get("answer") == pred["answer"] for c in mine))
    return int(any(c["stance"] == st for c in mine))


def score(entry, verbose):
    preds = json.load(open(os.path.join(ROOT, "predictions", entry + ".json")))
    path = os.path.join(ROOT, "claims", entry + ".json")
    if not os.path.exists(path):
        print(f"{entry}: no claims file yet")
        return []
    claims = json.load(open(path))["claims"]
    rows = []
    for p in preds["predictions"]:
        o = outcome(p, claims)
        rows.append((p, o))
        if verbose:
            mark = "unscored" if o is None else ("right" if o else "WRONG")
            ans = f" {p['answer']}" if p.get("answer") else ""
            print(f"  {mark:8} p={p['p']:.2f}  {p['text']} {p['question']}: {p['stance']}{ans}")
    summary(entry, rows)
    return rows


def summary(label, rows):
    s = [(p["p"], o) for p, o in rows if o is not None]
    n = len(s)
    if not n:
        print(f"{label}: {len(rows)} predictions, none scorable")
        return
    brier = sum((p - o) ** 2 for p, o in s) / n
    right = sum(o for _, o in s)
    print(f"{label}: {len(rows)} predictions, {n} scored, {right} right ({100 * right / n:.0f}%), "
          f"mean p {sum(p for p, _ in s) / n:.2f}, Brier {brier:.3f}")
    for lo, hi in BINS:
        b = [o for p, o in s if lo <= p < hi]
        if b:
            print(f"    p {lo:.2f}-{min(hi, 1):.2f}: {sum(b)}/{len(b)} right")


def main():
    args = sys.argv[1:]
    if args:
        for e in args:
            print(e)
            score(e, True)
        return
    files = sorted(glob.glob(os.path.join(ROOT, "predictions", "*.json")))
    if not files:
        sys.exit("no predictions files")
    allrows = []
    for f in files:
        allrows += score(os.path.basename(f)[:-5], False)
    if len(files) > 1:
        summary("all entries", allrows)


if __name__ == "__main__":
    main()
