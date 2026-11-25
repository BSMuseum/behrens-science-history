# Contributing

Entries are written one per branch, so several sessions (Claude tabs now, volunteers later) can work at once without editing the same files. A separate merge pass folds their changes to the shared registries into `data/`, and a separate verification pass checks each entry against the page images.

## Before writing anything

Read [`docs/charter.md`](docs/charter.md) (scope, method, entry sections and entry conventions) and [`claims/README.md`](claims/README.md) (the claims format, the persistent questions and rule R1 for choosing texts). The worked examples are `claims/1775-body.json` and `claims/1775-gravity.json` with their entries in `entries/1775/`. `tools/cites.py` builds citations with each text's page-to-scan offsets.

Start every session from a fresh clone of `main`. Nothing from an earlier session's workspace is needed.

## An entry branch

Name it `entry/<snapshot>-<topic>`, for example `entry/1675-air`. It writes only these files:

| File | What |
|---|---|
| `claims/<snapshot>-<topic>.json` | the claims file |
| `entries/<snapshot>/<topic>.html` | the entry, one `<article class="view" id="v-<topic>">` block, in the year page's markup |
| `proposals/<snapshot>-<topic>.json` | every change the entry needs in the shared files (below) |
| `tools/cites-<name>.py` | only if the entry needs citation helpers for a text `cites.py` lacks |

It does **not** edit `data/`, `site/pages.json`, `entries/<snapshot>/home.html`, `tools/cites.py`, the README or the charter. Those are shared, and every parallel branch would conflict on them.

Before opening the pull request:

```
python3 -I tools/check_claims.py --urls   # 0 errors; reads proposals/ as if folded in
python3 -I tools/build_site.py            # 0 problems; open _site/c-<snapshot>/#<topic> and look at it
```

The builder shows an entry not yet listed in `site/pages.json` after the listed ones, titled from its `<h1>`, so the entry can be seen in the built page before it is merged. GitHub runs both checks on the pull request and will not show it green with errors.

The pull request description says what was read, which judgment calls a reviewer should look at, and anything the merge pass must do by hand.

## The proposals file

```json
{
  "questions":   [ { "id": "...", "theme": "...", "status": "...", "wording": "...", "answers": [ ... ], "drawn_from": [ ... ] } ],
  "answers":     { "<existing question id>": [ { "code": "...", "label": "..." } ] },
  "drawn_from":  { "<existing question id>": [ "<snapshot>-<topic>:<part>" ] },
  "texts":       [ { "id": "...", ... } ],
  "texts_notes": "page-to-scan offsets and other notes for existing texts in texts.json",
  "snapshot":    "the status line and topic_texts / boundary_notes changes for snapshots.json",
  "home":        "the change to the snapshot's home view: the topic row and the status line",
  "page_title":  "the entry's browser-tab title, e.g. 'Air and Its Spring c. 1675'",
  "cites":       "helpers to move into tools/cites.py, if any",
  "notes":       "anything else"
}
```

Only `questions`, `answers`, `drawn_from` and `texts` are folded by script; the rest is applied by hand in the merge pass. New question ids and answer codes follow the rules in `claims/README.md`: worded to be askable of any period, never renamed or reused.

## The merge pass

About once a week, or after a batch of entries:

1. Merge the entry pull requests into a branch `merge/<date>`, resolving any clash of new question ids or answer codes between them (two branches may propose the same question under different ids; keep one and recode the other entry's claims).
2. `python3 -I tools/fold_proposals.py` folds the registry changes into `data/` and deletes the proposals files; it prints the parts to apply by hand.
3. Apply those: `data/snapshots.json`, the topic's row and the status line in `entries/<snapshot>/home.html`, the entry's place and title in `site/pages.json`, new helpers into `tools/cites.py`, and the status lines in `claims/README.md` and `docs/charter.md`.
4. Run the checker and the builder, open a pull request, and merge it. The site updates on its own.

## The verification pass

Done by a different session from the one that wrote the entry. It checks every quotation and a stated sample of other claims against the page images, corrects the claims file and the entry, and fills the claims file's `verification` block (status, by, date) by its own pull request.

## Rules that hold everywhere

- Anything in quotation marks has been read from the page image, never from OCR.
- Every claim cites edition, section and printed page, with a scan link.
- The period's ideas in the period's terms. Modern concepts only as brief glosses in the entry's "terms for modern readers".
- A change to rule R1 or to the claims format is a numbered decision recorded in `claims/README.md`, made by Bruce, not by an entry branch.
