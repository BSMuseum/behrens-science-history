# Behrens Science History

What European students were taught about nature, snapshot by snapshot from 1275 to 1900, in the period's own terms, from the most-printed teaching texts of each region, with every claim cited to a page scan.

**Site:** https://history.bsmuseum.org/

A project of the [Behrens Science Museum](https://bsmuseum.org/), compiled by Bruce Behrens with Anthropic's Claude. Corrections are welcome through the museum's [contact page](https://bsmuseum.org/contact/) or as an issue here.

## Scope and plan

Eighteen snapshot dates from 1275 to 1900 (every fifty years to 1625, then every twenty-five), four regions (France, the Protestant and Catholic German lands, the British Isles), in three phases:

1. **Natural philosophy and natural history.** Under way. The first series, and the first milestone, is natural philosophy at c. 1575, c. 1675 and c. 1775.
2. **Scientific method and its assumptions.** Planned, to run alongside Phase 1.
3. **Medicine.** Planned.

Under consideration for later: chemistry and alchemy, sacred chronology, mixed mathematics.

## What a snapshot is

Each snapshot takes the courses most often printed in each region in the decades around its date, chosen by a written rule (rule R1, in [`claims/README.md`](claims/README.md)) applied the same way every time. It takes its topics from those courses' own tables of contents, not from a modern list, and reports what the texts taught, where they disagreed, and the reasons they gave. The product is taught consensus, not discovery: journals are used only to date when an idea entered or left the textbooks.

Every entry has two forms: a page on the site, and a claims file that records each text's position on each question in a machine-readable form. The questions are worded so they can be put in the same words to a text of any period ("What is light?", "Why do heavy bodies fall?", "Does the earth move?"), which is what lets the snapshots be compared.

## Status

- **c. 1775**, natural philosophy: all 13 topics published, one text per region (Biwald, Graz; Erxleben, Göttingen; Nollet, Paris; Ferguson or Martin, London). Claims not yet independently verified.
- **c. 1675**, natural philosophy: 2 of 25 topics published (light and colours; water, the sea and springs).
- **c. 1575**: texts proposed under rule R1; reading not begun.

The plan and its decisions are in [`docs/charter.md`](docs/charter.md); the minimum viable product (three snapshots of natural philosophy) in [`docs/mvp-plan.md`](docs/mvp-plan.md).

## The repository

```
data/          registries: questions.json (the persistent questions and their answer codes),
               texts.json (every text chosen or read, with edition counts and scans),
               snapshots.json (the grid, the regions, each snapshot's texts and topics)
claims/        one claims file per entry, <snapshot>-<topic>.json; README.md gives the format
               and rule R1; british-texts.md and 1675-plan.md are working records
entries/       the prose of each entry as an HTML fragment, entries/<snapshot>/<topic>.html,
               and each snapshot's home view, entries/<snapshot>/home.html
site/          front page, title-page images, the year-page template, style and router, and
               pages.json (each year page's entry order and tab titles)
proposals/     changes to the registries proposed by entry branches, waiting to be folded in
tools/         check_claims.py, build_site.py, fold_proposals.py, cites.py (citation helpers)
docs/          charter, plans, method tests
```

## Checking and building

Python 3, no packages needed.

```
python3 -I tools/check_claims.py          # claims files against the registries; must report 0 errors
python3 -I tools/check_claims.py --urls   # also fetches every cited scan URL (slow)
python3 -I tools/build_site.py            # builds the site into _site/
```

GitHub runs the first and third on every pull request, checks the scan URLs weekly, and rebuilds the site on every push to `main`.

To contribute an entry, see [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Licence and citation

Text and data: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Use them for anything, including commercially, as long as you credit the project: *Behrens Science History, Behrens Science Museum, https://history.bsmuseum.org/*. GitHub's "Cite this repository" button gives the same in standard formats (from [`CITATION.cff`](CITATION.cff)). The code in `tools/` is MIT-licensed. Details in [`LICENSE`](LICENSE).

## Scans

Title pages, frontispieces and every cited page come from public scans at the Internet Archive and the Bayerische Staatsbibliothek, Munich (digitale-sammlungen.de). Each image and citation links to its scan.
