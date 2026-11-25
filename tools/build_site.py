"""Build the static site into _site/ (or the folder given as the first argument).

Usage: python3 -I tools/build_site.py [<out>]

  _site/index.html                  site/front.html
  _site/img/                        site/img/
  _site/c-<year>/index.html         one page per snapshot: site/templates/year.html filled with
                                    site/templates/style.css, entries/<year>/home.html, then the
                                    entries in the order site/pages.json gives, and the router
  _site/c-<year>/claims/<id>.json   each entry's claims file, for download
  _site/data/*.json                 the registries

site/pages.json lists, per snapshot, the page title, the order of the entries and each entry's
browser-tab title. An entry fragment is an <article class="view" id="v-<topic>"> block.
A fragment not yet listed in pages.json is built after the listed ones, titled from its <h1>.
"""
import json, os, re, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def read(*p):
    with open(os.path.join(ROOT, *p), encoding="utf-8") as f:
        return f.read()

def js_obj(d):
    # single-quoted object literal, as the hand-written pages had it
    return "{ " + ", ".join(f"{k}: '{v}'" for k, v in d.items()) + " }"

def build(out):
    if os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(out)
    open(os.path.join(out, ".nojekyll"), "w").close()
    shutil.copy(os.path.join(ROOT, "site", "front.html"), os.path.join(out, "index.html"))
    shutil.copytree(os.path.join(ROOT, "site", "img"), os.path.join(out, "img"))
    os.makedirs(os.path.join(out, "data"))
    for f in ("questions.json", "texts.json", "snapshots.json"):
        shutil.copy(os.path.join(ROOT, "data", f), os.path.join(out, "data", f))

    pages = json.loads(read("site", "pages.json"))
    shell = read("site", "templates", "year.html")
    style = read("site", "templates", "style.css")
    router = read("site", "templates", "router.js")
    problems = []
    for snap, P in pages.items():
        parts = [read("entries", snap, "home.html")]
        for t in P["order"]:
            frag = read("entries", snap, f"{t}.html")
            if not frag.startswith(f'<article class="view" id="v-{t}">'):
                problems.append(f"entries/{snap}/{t}.html does not open with its article tag")
            parts.append(frag)
            if t not in P["titles"]:
                problems.append(f"site/pages.json: no title for {snap} {t}")
        on_disk = {f[:-5] for f in os.listdir(os.path.join(ROOT, "entries", snap)) if f.endswith(".html")} - {"home"}
        for t in sorted(on_disk - set(P["order"])):
            # a new entry from an entry branch: shown after the listed ones until the merge
            # tab adds it to site/pages.json and to the home view
            frag = read("entries", snap, f"{t}.html")
            if not frag.startswith(f'<article class="view" id="v-{t}">'):
                problems.append(f"entries/{snap}/{t}.html does not open with its article tag")
            h1 = re.search(r"<h1>(.*?)</h1>", frag, re.S)
            P["titles"][t] = (re.sub(r"<[^>]+>", "", h1.group(1)).strip() if h1 else t) + f" c. {snap}"
            parts.append(frag)
            print(f"note: entries/{snap}/{t}.html is not in site/pages.json; built with the tab title '{P['titles'][t]}'")
        views = {"home": "v-home", **{t: f"v-{t}" for t in P["titles"]}}
        titles = {"home": P["page_title"], **P["titles"]}
        script = router.replace("__VIEWS__", js_obj(views)).replace("__TITLES__", js_obj(titles))
        html = (shell.replace("{{title}}", P["page_title"]).replace("{{style}}", style)
                     .replace("{{script}}", script).replace("{{body}}", "\n".join(parts)))
        d = os.path.join(out, f"c-{snap}")
        os.makedirs(os.path.join(d, "claims"))
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)
        for t in P["order"]:
            src = os.path.join(ROOT, "claims", f"{snap}-{t}.json")
            if os.path.exists(src):
                shutil.copy(src, os.path.join(d, "claims", f"{snap}-{t}.json"))
            else:
                problems.append(f"claims/{snap}-{t}.json missing")
    for p in problems:
        print("ERROR", p)
    print(f"built {out}: {len(pages)} snapshot pages; {len(problems)} problems")
    return 1 if problems else 0

if __name__ == "__main__":
    sys.exit(build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "_site")))
