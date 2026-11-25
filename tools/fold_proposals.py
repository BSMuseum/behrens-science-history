"""Fold proposals/*.json into the registries in data/ (the merge tab's job; see CONTRIBUTING.md).

Usage: python3 -I tools/fold_proposals.py [--dry-run]

Adds each proposal's new questions, new answer codes, new texts and drawn_from additions to
data/questions.json and data/texts.json, then deletes the proposal file. Refuses to fold if any
id clashes (rename in the branch first). Everything else in a proposal (offset notes,
snapshots.json status lines, notes) is printed for the merge tab to apply by hand.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QF, TF = os.path.join(ROOT, "data", "questions.json"), os.path.join(ROOT, "data", "texts.json")
PD = os.path.join(ROOT, "proposals")

def main(dry):
    Qd, Td = json.load(open(QF)), json.load(open(TF))
    qs = {q["id"]: q for q in Qd["questions"]}
    ts = {t["id"] for t in Td["texts"]}
    files = sorted(f for f in os.listdir(PD) if f.endswith(".json")) if os.path.isdir(PD) else []
    errs, done = [], []
    for fn in files:
        P = json.load(open(os.path.join(PD, fn)))
        for q in P.get("questions", []):
            if q["id"] in qs: errs.append(f"{fn}: question {q['id']} already exists")
            else: qs[q["id"]] = q; Qd["questions"].append(q)
        for qid, ans in P.get("answers", {}).items():
            if qid not in qs: errs.append(f"{fn}: answers for unknown question {qid}"); continue
            have = {a["code"] for a in qs[qid].setdefault("answers", [])}
            for a in ans:
                if a["code"] in have: errs.append(f"{fn}: answer {qid}/{a['code']} already exists")
                else: qs[qid]["answers"].append(a)
        for qid, refs in P.get("drawn_from", {}).items():
            if qid not in qs: errs.append(f"{fn}: drawn_from for unknown question {qid}"); continue
            df = qs[qid].setdefault("drawn_from", [])
            df.extend(r for r in refs if r not in df)
        for t in P.get("texts", []):
            if t["id"] in ts: errs.append(f"{fn}: text {t['id']} already exists")
            else: ts.add(t["id"]); Td["texts"].append(t)
        rest = {k: v for k, v in P.items() if k not in ("questions", "answers", "drawn_from", "texts")}
        if rest:
            print(f"== {fn}: apply by hand\n" + json.dumps(rest, indent=2, ensure_ascii=False))
        done.append(fn)
    for e in errs: print("ERROR", e)
    if errs or dry:
        print(f"{len(errs)} errors; nothing written"); return 1 if errs else 0
    for path, data in ((QF, Qd), (TF, Td)):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=1, ensure_ascii=False)  # the registries have no final newline
    for fn in done: os.remove(os.path.join(PD, fn))
    print(f"folded {len(done)} proposal files; {len(Qd['questions'])} questions, {len(Td['texts'])} texts")
    return 0

if __name__ == "__main__":
    sys.exit(main("--dry-run" in sys.argv))
