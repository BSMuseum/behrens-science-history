"""Citation helpers shared by the claims builders. Offsets as used by the published site."""
MDZ = "https://www.digitale-sammlungen.de/en/view/"
IA = "https://archive.org/details/"

def _first(page):
    return int(str(page).replace("–", "-").split("-")[0].split(",")[0])

def B(page, rf="unknown", section=None):  # Biwald, Physica generalis 1769
    c = {"page": str(page), "url": f"{MDZ}bsb10130800?page={_first(page) + 22}", "read_from": rf}
    if section: c["section"] = section
    return c

def BP(page, rf="unknown", section=None):  # Biwald, Physica particularis 1768
    c = {"page": str(page), "url": f"{MDZ}bsb10130796?page={_first(page) + 10}", "read_from": rf}
    if section: c["section"] = section
    return c

def E(page, leaf, rf="unknown", section=None):  # Erxleben 1772; leaf given explicitly (offsets drift)
    c = {"page": str(page), "url": f"{IA}anfangsgrndeder00lautgoog/page/n{leaf}/mode/1up", "read_from": rf}
    if section: c["section"] = section
    return c

def EN(page, rf="unknown", section=None, canvas=None):  # Erxleben, Anfangsgruende der Naturgeschichte, 2nd ed. 1773 (MDZ bsb10075646); canvas = page + 44
    c = {"page": str(page), "url": f"{MDZ}bsb10075646?page={canvas if canvas else _first(page) + 44}", "read_from": rf,
         "work": "Anfangsgründe der Naturgeschichte (1773)"}
    if section: c["section"] = section
    return c

def PA(vol, page, rf="unknown", section=None):  # Para du Phanjas, Theorie des etres sensibles, Paris 1772; IA /page/n = page + 85 (t. 1), page + 9 (t. 2)
    off = {1: 85, 2: 9}[vol]
    c = {"vol": str(vol), "page": str(page), "url": f"{IA}b30539584_000{vol}/page/n{_first(page) + off}/mode/1up", "read_from": rf}
    if section: c["section"] = section
    return c

def N(vol, page, leaf, rf="unknown"):  # Nollet, Lecons; leaf given explicitly
    c = {"page": str(page), "url": f"{IA}CHEPFL_LIPR_AXA5_0{vol}/page/n{leaf}/mode/1up", "read_from": rf}
    if vol != 1: c["vol"] = str(vol)
    return c

def S(page, leaf, rf="unknown"):  # Sigaud de la Fond, Traite de l'electricite 1776; leaf = page + 35, preliminaries roman + 5
    return {"page": str(page), "url": f"{IA}b33001674/page/n{leaf}/mode/1up", "read_from": rf}

EBFILES = {"i": "Volume 1, A-B", "ii": "Volume 2, C-L", "iii": "Volume 3, M-Z"}
def EB(vol, page, leaf=None, rf="unknown", entry=None):
    c = {"vol": vol, "page": str(page), "url": f"{IA}1771EncyclopediaBritannicaNLS", "read_from": rf}
    if leaf: c["scan"] = {"file": EBFILES[vol], "leaf": leaf}
    if entry: c["entry"] = entry
    return c

def P(name, dates, role, note=None):
    p = {"name": name, "dates": dates, "role": role}
    if note: p["note"] = note
    return p

def R(kind, detail=None):
    r = {"kind": kind}
    if detail: r["detail"] = detail
    return r

def conf(level, printed=None, translation=None, note=None):
    c = {"level": level}
    if printed is not None: c["printed"] = printed
    if translation: c["translation"] = translation
    if note: c["note"] = note
    return c

def quote(lang, orig, tr=None, note=None):
    q = {"lang": lang, "orig": orig, "from_image": True}
    if tr: q["tr"] = tr
    if note: q["note"] = note
    return q

class Claims:
    def __init__(self, entry):
        self.entry, self.items, self.n = entry, [], 0
    def add(self, question, text, stance, part, statement, answer=None, between=None, confidence=None,
            reasons=None, persons=None, cites=None, quote=None):
        self.n += 1
        c = {"id": f"{self.entry}-{self.n:03d}", "question": question, "text": text}
        if answer: c["answer"] = answer
        c["stance"] = stance
        if between: c["between"] = between
        c["part"] = part
        c["statement"] = statement
        if confidence: c["confidence"] = confidence
        elif stance not in ("not_found", "not_taken_up", "declines"): c["confidence"] = {"level": "asserted"}
        if reasons: c["reasons"] = reasons
        if persons: c["persons"] = persons
        if cites: c["cites"] = cites
        if quote: c["quote"] = quote
        self.items.append(c)

def M(page, leaf, rf="unknown", section=None):  # Martin, The Philosophical Grammar, London 1778 (IA bim_..._martin-benjamin_1778); /page/n = leaf; leaf = page + 11 at pp. 35-58, + 25 at pp. 103-116, + 47 at pp. 197-202, + 57 at pp. 238-257, + 65 at p. 291
    c = {"page": str(page), "url": f"{IA}bim_eighteenth-century_the-philosophical-gramma_martin-benjamin_1778/page/n{leaf}/mode/1up", "read_from": rf}
    if section: c["section"] = section
    return c

# c. 1675 texts (offsets read from the page images, 2026-11-22)
def RO(page, rf="unknown", section=None):  # Rohault, Traite de physique, Paris 1675, vol. 1 (MDZ bsb10131888); canvas = page + 40 (pp. 291-342)
    c = {"page": str(page), "url": f"{MDZ}bsb10131888?page={_first(page) + 40}", "read_from": rf}
    if section: c["section"] = section
    return c

def SP(page, rf="unknown", section=None):  # Sperling, Institutiones physicae, Wittenberg 1664 (MDZ bsb11273836); canvas = page + 18 (pp. 495-526; p. 518 is misprinted 418; pp. 568-598 checked for the water entry)
    c = {"page": str(page), "url": f"{MDZ}bsb11273836?page={_first(page) + 18}", "read_from": rf}
    if section: c["section"] = section
    return c

def GO(page, rf="unknown", section=None):  # Goudin, Philosophia, Cologne 1681, t. 3 (MDZ bsb11110404); canvas = page + 20 (pp. 91-104), + 24 after the plates (pp. 105-110)
    p = _first(page)
    c = {"page": str(page), "url": f"{MDZ}bsb11110404?page={p + (20 if p <= 104 else 24)}", "read_from": rf}
    if section: c["section"] = section
    return c

def LG(page, rf="unknown", section=None):  # Le Grand, Institutio philosophiae, London 1675 (IA bub_gb_hXF3IYaUJc4C); /page/n = page + 55 (Part II, pp. 90-92), + 59 (pp. 165-285), + 60 (pp. 510-512)
    p = _first(page)
    off = 55 if 90 <= p <= 92 else 59 if p < 500 else 60
    c = {"page": str(page), "url": f"{IA}bub_gb_hXF3IYaUJc4C/page/n{p + off}/mode/1up", "read_from": rf}
    if section: c["section"] = section
    return c

# Added with the 1675 water entry (2026-11-22; offsets read from the page images: strips of pp. 140-282, 568-598, 122-132, 273-285, 340-365)
def RO2(page, rf="unknown", section=None):  # Rohault, Traite de physique, Paris 1675, vol. 2 (MDZ bsb10131889); canvas = page + 4 (pp. 140-282)
    c = {"vol": "2", "page": str(page), "url": f"{MDZ}bsb10131889?page={_first(page) + 4}", "read_from": rf}
    if section: c["section"] = section
    return c

def GO2(page, rf="unknown", section=None):  # Goudin t. 3, later pages: canvas = page + 24 (pp. 105-134), + 26 (pp. 270-290)
    p = _first(page)
    off = 20 if p <= 104 else 24 if p <= 134 else 26
    c = {"page": str(page), "url": f"{MDZ}bsb11110404?page={p + off}", "read_from": rf}
    if section: c["section"] = section
    return c

def LG2(page, rf="unknown", section=None):  # Le Grand, Part VI: /page/n = page + 60 (pp. 340-365, read from the images)
    p = _first(page)
    c = {"page": str(page), "url": f"{IA}bub_gb_hXF3IYaUJc4C/page/n{p + 60}/mode/1up", "read_from": rf}
    if section: c["section"] = section
    return c

# Goudin t. 2 (physics part 1), Bologna 1686 (Longi), IA bub_gb_D2e2JGtx1rwC, read under R1 clause 6 in place of
# the Cologne 1681 t. 2 (not found). Added with the 1675 matter-form, causes, place-void-time and motion entries
# (2026-11-27; merged 2026-11-28). The /page/n index drifts and some leaves repeat (n29-n38 repeat pp. 20-29;
# others between pp. 275 and 282), so pages outside the checked ranges raise rather than guess.
# Checked on the images: n = page - 1 (pp. 21-29), + 9 (pp. 30-63), + 13 (pp. 85-103), + 17 (pp. 133-277),
# + 26 (pp. 282-290), + 25 (pp. 311-378).
GOUDIN2_LEAF = {9: 8, 21: 20, 22: 21, 23: 22, 24: 23, 25: 24, 26: 25, 27: 26, 28: 27, 29: 28, 78: 89}
GOUDIN2_RANGES = [(30, 63, 9), (85, 103, 13), (133, 277, 17), (282, 290, 26), (311, 378, 25)]

def GT(page, rf="unknown", section=None):  # Goudin t. 2, Bologna 1686
    p = _first(page)
    n = GOUDIN2_LEAF.get(p)
    if n is None:
        n = next((p + off for lo, hi, off in GOUDIN2_RANGES if lo <= p <= hi), None)
    if n is None:
        raise ValueError(f"Goudin t. 2: no leaf recorded for p. {p}")
    c = {"vol": "2", "page": str(page), "url": f"{IA}bub_gb_D2e2JGtx1rwC/page/n{n}/mode/1up", "read_from": rf}
    if section: c["section"] = section
    return c
