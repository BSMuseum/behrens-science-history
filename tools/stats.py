#!/usr/bin/env python3
"""Counts across the claims files, by snapshot: agreement between regions,
the kinds of reason the texts give, how confidently they speak, whom they
name, and how answers to the same question change between snapshots.

    python3 -I tools/stats.py                  # every entry
    python3 -I tools/stats.py --topics light water
    python3 -I tools/stats.py --json > stats.json

Descriptive only: it reads claims/*.json and data/texts.json and writes
nothing. Supplementary texts (role "supplementary" in a claims file, or
status "supplementary" in texts.json) are left out. Texts are grouped by
region (texts.json), so a region's texts for different topics count as one
voice; where an entry has two texts from one region, both count for it.

Agreement: for each pair of regions, over the (entry, question) pairs where
both hold a coded answer, the share where they hold at least one answer in
common. Hedged = confidence probable, possible or doubtful. Open = stance
reports, undecided or declines.

The counts inherit every coding choice in the claims files (reason kinds,
confidence levels, which positions get a claim). They are unverified until
the verification pass has run.
"""

import argparse
import collections
import glob
import itertools
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEDGED = {"probable", "possible", "doubtful"}
OPEN = {"reports", "undecided", "declines"}
POSITION = {"holds", "rejects", "leans", "reports", "undecided"}


def load(topics):
    texts = json.load(open(os.path.join(ROOT, "data", "texts.json")))["texts"]
    info = {t["id"]: t for t in texts}
    entries = []
    for path in sorted(glob.glob(os.path.join(ROOT, "claims", "*.json"))):
        d = json.load(open(path))
        e = d["entry"]
        if topics and e["topic"] not in topics:
            continue
        regions = {}
        for sig, t in d["texts"].items():
            tid = t["text"]
            if t.get("role") == "supplementary" or info.get(tid, {}).get("status") == "supplementary":
                continue
            regions[sig] = info.get(tid, {}).get("region", tid)
        entries.append((e["snapshot"], e["topic"], d["claims"], regions))
    return entries, info


def stats(entries, info):
    out = {}
    by_snap = collections.defaultdict(list)
    for s, topic, claims, regions in entries:
        by_snap[s].append((topic, claims, regions))
    answers = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    for s in sorted(by_snap):
        n = 0
        stance, conf, reason, person = (collections.Counter() for _ in range(4))
        held = collections.defaultdict(lambda: collections.defaultdict(set))
        topics = []
        for topic, claims, regions in by_snap[s]:
            topics.append(topic)
            for c in claims:
                reg = regions.get(c["text"])
                if reg is None:
                    continue
                n += 1
                stance[c["stance"]] += 1
                conf[(c.get("confidence") or {}).get("level") or "unmarked"] += 1
                for r in c.get("reasons", []):
                    reason[r["kind"]] += 1
                for p in c.get("persons", []):
                    person[f'{p.get("name")} ({p.get("role")})'] += 1
                if c["stance"] == "holds" and c.get("answer"):
                    held[(topic, c["question"])][reg].add(c["answer"])
                if c["stance"] in POSITION:
                    key = c.get("answer") or "(no code)"
                    if c["stance"] == "rejects":
                        key = "not " + key
                    answers[c["question"]][s][key] += 1
        agree = {}
        for m in held.values():
            for a, b in itertools.combinations(sorted(m), 2):
                k = f"{a} / {b}"
                tot, same = agree.get(k, (0, 0))
                agree[k] = (tot + 1, same + bool(m[a] & m[b]))
        out[s] = {
            "topics": sorted(topics),
            "claims": n,
            "stances": dict(stance.most_common()),
            "confidence": dict(conf.most_common()),
            "hedged": sum(conf[k] for k in HEDGED),
            "open": sum(stance[k] for k in OPEN),
            "reasons": dict(reason.most_common()),
            "persons": dict(person.most_common(20)),
            "agreement": {k: {"shared": t, "agree": a} for k, (t, a) in sorted(agree.items())},
        }
    snaps = sorted(by_snap)
    out["across"] = {
        q: {s: dict(v[s].most_common()) for s in snaps}
        for q, v in sorted(answers.items())
        if sum(1 for s in snaps if v[s]) > 1
    }
    return out


def pct(a, b):
    return f"{100 * a / b:.0f}%" if b else "-"


def report(out):
    for s, d in out.items():
        if s == "across":
            continue
        n = d["claims"]
        print(f"== c. {s}: {n} claims, topics: {', '.join(d['topics'])}")
        print(f"   hedged {d['hedged']} ({pct(d['hedged'], n)}); open {d['open']} ({pct(d['open'], n)}); "
              f"asserted {d['confidence'].get('asserted', 0)} ({pct(d['confidence'].get('asserted', 0), n)})")
        print("   stances: " + ", ".join(f"{k} {v}" for k, v in d["stances"].items()))
        r = sum(d["reasons"].values())
        print(f"   reasons ({r}): " + ", ".join(f"{k} {pct(v, r)}" for k, v in d["reasons"].items()))
        print("   agreement between regions (questions both hold an answer on):")
        for k, v in d["agreement"].items():
            print(f"     {k}: {v['agree']}/{v['shared']} = {pct(v['agree'], v['shared'])}")
        print("   most-named persons: " + "; ".join(f"{k} {v}" for k, v in list(d["persons"].items())[:12]))
        print()
    print("== Questions answered in more than one snapshot (claims per answer; 'not x' = rejects x)")
    for q, v in out["across"].items():
        print(f"   {q}")
        for s, a in v.items():
            if a:
                print(f"     {s}: " + ", ".join(f"{k} {n}" for k, n in a.items()))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--topics", nargs="+", help="only these topic ids (e.g. light water)")
    ap.add_argument("--json", action="store_true", help="print the counts as JSON")
    args = ap.parse_args()
    entries, info = load(set(args.topics or []))
    if not entries:
        sys.exit("no claims files match")
    out = stats(entries, info)
    if args.json:
        json.dump(out, sys.stdout, ensure_ascii=False, indent=1)
        print()
    else:
        report(out)


if __name__ == "__main__":
    main()
