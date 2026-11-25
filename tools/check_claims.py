"""Mechanical checks for the Behrens Science History claims files.

Usage: python3 -I tools/check_claims.py [<dir>] [--urls]
<dir> is the repository root (default: the parent of tools/), with the registries
(questions.json, texts.json) in data/ and the <snapshot>-<topic>.json files in claims/.
A flat folder holding all of them together also works, as in the old project layout.
Exit status 1 if any error is found.

A siglum whose entry in a claims file's "texts" has "role": "supplementary" (a text read
alongside the regional texts but filling no slot, R1 clause 2) may have claims, but is not
required to cover the common-ground questions.
"""
import json, os, re, sys, subprocess

STANCES = {"holds", "rejects", "leans", "undecided", "reports", "declines", "not_taken_up", "not_found"}
NEEDS_ANSWER = {"holds", "rejects", "leans"}
NO_CITE = {"not_taken_up", "not_found"}
REASONS = {"experiment", "observation", "mathematics", "authority", "consensus", "scripture", "design",
           "analogy", "metaphysics", "sufficient-reason", "simplicity", "explanatory-scope", "refutation", "other"}
LEVELS = {"certain", "probable", "possible", "doubtful", "asserted", "none"}
READ_FROM = {"image", "ocr", "unknown"}
PARTS = {"common", "dispute", "open", "why", "place"}
ROLES = {None, "supplementary"}

def main(d, check_urls):
    errs = []
    E = lambda m: errs.append(m)
    dd = os.path.join(d, "data") if os.path.isdir(os.path.join(d, "data")) else d
    cd = os.path.join(d, "claims") if os.path.isdir(os.path.join(d, "claims")) else d
    Q = json.load(open(os.path.join(dd, "questions.json")))["questions"]
    T = json.load(open(os.path.join(dd, "texts.json")))["texts"]
    qs = {}
    for q in Q:
        if q["id"] in qs: E(f"question id repeated: {q['id']}")
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", q["id"]): E(f"bad question id: {q['id']}")
        codes = [a["code"] for a in q.get("answers", [])]
        if len(codes) != len(set(codes)): E(f"{q['id']}: answer code repeated")
        qs[q["id"]] = set(codes)
    for q in Q:
        if q.get("parent") and q["parent"] not in qs: E(f"{q['id']}: parent {q['parent']} missing")
    ts = {t["id"]: t for t in T}
    if len(ts) != len(T): E("text id repeated")
    urls = set()
    for fn in sorted(os.listdir(cd)):
        if not re.fullmatch(r"\d{4}-[a-z0-9-]+\.json", fn): continue
        C = json.load(open(os.path.join(cd, fn)))
        ent = C["entry"]
        if fn != ent["id"] + ".json": E(f"{fn}: entry id {ent['id']} does not match file name")
        sig = C["texts"]
        for s, v in sig.items():
            if v["text"] not in ts: E(f"{fn}: siglum {s} -> unknown text {v['text']}")
            if v.get("role") not in ROLES: E(f"{fn}: siglum {s} has unknown role {v.get('role')}")
        required = {s for s, v in sig.items() if v.get("role") != "supplementary"}
        seen, cover = set(), {}
        for c in C["claims"]:
            cid = c.get("id", "?")
            where = f"{fn} {cid}"
            if cid in seen: E(f"{where}: id repeated")
            seen.add(cid)
            if not cid.startswith(ent["id"] + "-"): E(f"{where}: id should start with {ent['id']}-")
            if c["question"] not in qs: E(f"{where}: unknown question {c['question']}"); continue
            if c["text"] not in sig: E(f"{where}: unknown siglum {c['text']}")
            st = c.get("stance")
            if st not in STANCES: E(f"{where}: bad stance {st}")
            if c.get("part") not in PARTS: E(f"{where}: bad part {c.get('part')}")
            if st in NEEDS_ANSWER and c.get("answer") not in qs[c["question"]]:
                E(f"{where}: answer {c.get('answer')} not among {c['question']}'s answers")
            for b in c.get("between", []):
                if b not in qs[c["question"]]: E(f"{where}: between-code {b} unknown")
            if st not in NO_CITE and not c.get("cites"): E(f"{where}: no citation")
            for ci in c.get("cites", []):
                if not ci.get("url"): E(f"{where}: citation without url")
                else: urls.add(ci["url"])
                if ci.get("read_from", "unknown") not in READ_FROM: E(f"{where}: bad read_from")
            for r in c.get("reasons", []):
                if r.get("kind") not in REASONS: E(f"{where}: bad reason kind {r.get('kind')}")
            lv = c.get("confidence", {}).get("level")
            if st not in NO_CITE and st != "declines" and lv not in LEVELS: E(f"{where}: bad or missing confidence level")
            qu = c.get("quote")
            if qu:
                if qu.get("from_image") is not True: E(f"{where}: quotation not marked as read from the image")
                if not any(ci.get("read_from") == "image" for ci in c.get("cites", [])): E(f"{where}: quotation but no citation read from the image")
                if qu.get("orig") is None and qu.get("lang") != "en" and not qu.get("note"): E(f"{where}: original missing without a note")
            if not c.get("statement"): E(f"{where}: no statement")
            cover.setdefault((c["question"], c.get("part")), set()).add(c["text"])
        # every common-ground question must say something for every regional (non-supplementary) text
        for (q, part), have in cover.items():
            if part in ("common",) and not required <= have:
                E(f"{fn}: common-ground question {q} lacks a claim (or not_found) for {sorted(required - have)}")
    if check_urls:
        for u in sorted(urls):
            code = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-L", "-m", "40", u],
                                  capture_output=True, text=True).stdout
            if code != "200": E(f"url {code}: {u}")
    for e in errs: print("ERROR", e)
    print(f"{len(errs)} errors; {len(qs)} questions, {len(ts)} texts, {len(urls)} distinct citation urls")
    return 1 if errs else 0

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    root = args[0] if args else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.exit(main(root, "--urls" in sys.argv))
