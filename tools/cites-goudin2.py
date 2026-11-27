"""Citation helper for Goudin's t. 2 (physics part 1), added with the 1675 matter-and-form entry.

Goudin, Philosophia juxta inconcussa tutissimaque Divi Thomae dogmata, t. 2, Bologna 1686 (Longi),
IA bub_gb_D2e2JGtx1rwC, read under R1 clause 6 in place of the Cologne 1681 t. 2 (not found).
The /page/n index drifts, and leaves n29-n38 repeat pp. 20-29, so every page used is given explicitly,
read from the page images on 2026-11-27. For the merge pass to move into tools/cites.py.
"""
IA = "https://archive.org/details/"

# printed page -> /page/n, read from the images (n = page - 1 for pp. 21-29; n = page + 9 for pp. 30-63;
# n = page + 11 at p. 78; n = page + 13 for pp. 85-103)
GOUDIN2_LEAF = {9: 8, 21: 20, 22: 21, 23: 22, 24: 23, 25: 24, 26: 25, 27: 26, 28: 27, 29: 28,
                78: 89, 85: 98, 89: 102, 97: 110, 99: 112, 100: 113, 103: 116}

def _first(page):
    return int(str(page).replace("–", "-").split("-")[0].split(",")[0])

def GT(page, rf="unknown", section=None):  # Goudin t. 2, Bologna 1686
    p = _first(page)
    n = GOUDIN2_LEAF.get(p, p + 9 if 30 <= p <= 63 else None)
    if n is None:
        raise ValueError(f"Goudin t. 2: no leaf recorded for p. {p}")
    c = {"vol": "2", "page": str(page), "url": f"{IA}bub_gb_D2e2JGtx1rwC/page/n{n}/mode/1up", "read_from": rf}
    if section: c["section"] = section
    return c
