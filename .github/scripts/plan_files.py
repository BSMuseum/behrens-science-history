"""Report changes to the research plan in a pull request.

Usage: python3 -I .github/scripts/plan_files.py <base-sha> <head-sha>
Run from a checkout of main. It reads both versions with `git show` and never runs
code from the pull request. Exit status 1 if the plan changes.

The plan is:
  whole files   CONTRIBUTING.md, LICENSE, CITATION.cff, tools/check_claims.py,
                tools/fold_proposals.py, everything under .github/
  sections      docs/charter.md: "Scope decisions", "Method that works"
                claims/README.md: "Questions", "Claims", "Dependencies between claims",
                "Rule R1 for choosing texts", "Decisions"
  registries    data/questions.json: the conventions; any existing question removed, or
                its wording, theme, parent or an existing answer code's label changed
                (new questions, new answer codes, new names and drawn_from are routine;
                so is a status change from "anticipated")
                data/snapshots.json: grid, regions, mvp_regions; a snapshot removed, or
                its window or chosen texts changed
Status lines, findings, entries, claims files, the site and the other tools are not
the plan and change freely.
"""
import json, re, subprocess, sys

WHOLE = ["CONTRIBUTING.md", "LICENSE", "CITATION.cff", "tools/check_claims.py", "tools/fold_proposals.py"]
WHOLE_DIRS = [".github/"]
SECTIONS = {
    "docs/charter.md": ["Scope decisions", "Method that works"],
    "claims/README.md": ["Questions", "Claims", "Dependencies between claims", "Rule R1 for choosing texts", "Decisions"],
}

def show(rev, path):
    r = subprocess.run(["git", "show", f"{rev}:{path}"], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None

def sections(md):
    out, cur = {}, None
    for line in (md or "").splitlines(keepends=True):
        m = re.match(r"## (.+?)\s*$", line)
        if m: cur = m.group(1); out[cur] = ""
        elif cur: out[cur] += line
    return out

def main(base, head):
    changed = subprocess.run(["git", "diff", "--name-only", f"{base}...{head}"],
                             capture_output=True, text=True, check=True).stdout.split()
    found = []
    for p in changed:
        if p in WHOLE or any(p.startswith(d) for d in WHOLE_DIRS):
            found.append(f"{p}: changed")
    for p, names in SECTIONS.items():
        if p not in changed: continue
        a, b = sections(show(base, p)), sections(show(head, p))
        for n in names:
            if a.get(n) != b.get(n):
                found.append(f'{p}, section "{n}": ' + ("removed or renamed" if n not in b else "changed"))
    if "data/questions.json" in changed:
        A, B = json.loads(show(base, "data/questions.json")), json.loads(show(head, "data/questions.json") or "{}")
        if A.get("conventions") != B.get("conventions"): found.append("data/questions.json: conventions changed")
        bq = {q["id"]: q for q in B.get("questions", [])}
        for q in A["questions"]:
            n = bq.get(q["id"])
            if n is None: found.append(f"data/questions.json: question {q['id']} removed"); continue
            for k in ("wording", "theme", "parent"):
                if q.get(k) != n.get(k): found.append(f"data/questions.json: {q['id']} {k} changed")
            if q.get("status") != n.get("status") and q.get("status") != "anticipated":
                found.append(f"data/questions.json: {q['id']} status changed from {q.get('status')}")
            nl = {x["code"]: x.get("label") for x in n.get("answers", [])}
            for x in q.get("answers", []):
                if x["code"] not in nl: found.append(f"data/questions.json: {q['id']} answer {x['code']} removed")
                elif nl[x["code"]] != x.get("label"): found.append(f"data/questions.json: {q['id']} answer {x['code']} label changed")
    if "data/snapshots.json" in changed:
        A, B = json.loads(show(base, "data/snapshots.json")), json.loads(show(head, "data/snapshots.json") or "{}")
        for k in ("grid", "regions", "mvp_regions"):
            if A.get(k) != B.get(k): found.append(f"data/snapshots.json: {k} changed")
        bs = {s["id"]: s for s in B.get("snapshots", [])}
        for s in A["snapshots"]:
            n = bs.get(s["id"])
            if n is None: found.append(f"data/snapshots.json: snapshot {s['id']} removed"); continue
            for k in ("window", "texts"):
                if s.get(k) != n.get(k): found.append(f"data/snapshots.json: snapshot {s['id']} {k} changed")
    if found:
        print("This pull request changes the research plan:")
        for f in found: print("  -", f)
        return 1
    print(f"No change to the research plan ({len(changed)} files changed).")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1], sys.argv[2]))
    except Exception as e:  # a broken check must not look like a plan change (exit 1)
        print(f"plan_files.py could not run: {e!r}")
        sys.exit(2)
