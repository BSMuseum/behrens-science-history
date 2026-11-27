# Contributing

## Ways to help

- **Report an error.** Open an issue, or write through the museum's [contact page](https://bsmuseum.org/contact/). Give the entry, the claim and what is wrong with it. No GitHub skills needed.
- **Check an entry.** Take a published entry that has not been verified and check it against the page images. This is the verification pass below.
- **Write an entry.** Take a topic not yet written, in a snapshot already started, and write it on its own branch. The rest of this file explains how.
- **Fund compute time.** See [Supporting the project](https://history.bsmuseum.org/#support) on the site.

Volunteers work to the research plan as it stands. Proposals to change the plan are welcome as issues, but Bruce decides them (see "Who merges" below).

## How entries are written

Entries are written one per branch, so several sessions (Claude tabs now, volunteers later) can work at once without editing the same files. A separate merge pass folds their changes to the shared registries into `data/`, and a separate verification pass checks each entry against the page images.

## Before writing anything

Read [`docs/charter.md`](docs/charter.md) (scope, method, entry sections and entry conventions) and [`claims/README.md`](claims/README.md) (the claims format, the persistent questions and rule R1 for choosing texts). The worked examples are `claims/1775-body.json` and `claims/1775-gravity.json` with their entries in `entries/1775/`. `tools/cites.py` builds citations with each text's page-to-scan offsets.

Start every session from a fresh clone of `main`. Nothing from an earlier session's workspace is needed.

## Claiming a topic

A session told to work on the project takes the next topic as follows, so that two sessions, Bruce's tabs or volunteers', never write the same one. The claim is an open pull request, because a pull request shows on this repository whether its branch is here or in a fork.

1. The snapshot in progress is 1675, then 1575. Within it, go down the `topics` list in `data/snapshots.json` in order.
2. Take the first topic whose status is "planned", which has no file `entries/<snapshot>/<topic>.html` on `main`, and which has no open pull request from a branch named `entry/<snapshot>-<topic>` (`gh api 'repos/BSMuseum/behrens-science-history/pulls?state=open&per_page=100' --jq '.[].head.ref'`).
3. Claim it before reading anything: create the branch from `main` (in this repository if you can push to it, otherwise in your fork), commit nothing but an empty commit (`git commit --allow-empty -m "Claim <snapshot>-<topic>"`), push it, and open a **draft** pull request to `main` titled `Claim <snapshot>-<topic>`.
4. Then list the open pull requests again. If another open pull request with a lower number has a branch of the same name, that one holds the topic: close yours, delete its branch, and go back to step 2.
5. The open pull request is the claim. Do the work on the same branch and mark the pull request ready for review when the entry is done. A session that abandons a topic closes its pull request and says so in it.

A session asked for a particular topic still checks step 2 first and stops if the topic is taken.

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

## Dependencies

Every entry codes, for each claim, the positions of the same text that the text itself uses as grounds for it (`rests_on`, defined in `claims/README.md`), in this topic or any topic already written, and sets the entry block's `rests_on` marker. Where the supporting position belongs to a topic not yet written, give its question and answer code; the tab that writes that topic later replaces them with the claim id, in the earlier file as well as its own (the one exception to "writes only these files", and only for `rests_on`).

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
4. Run the checker and the builder and open a pull request. Bruce merges it; the site updates on its own.

## The verification pass

Done by a different session from the one that wrote the entry. It checks every quotation and a stated sample of other claims against the page images, corrects the claims file and the entry, and fills the claims file's `verification` block (status, by, date) by its own pull request.

## Who merges

`main` accepts changes only through pull requests, and only Bruce merges them. Sessions open pull requests; they never merge one, their own or anyone else's, and never add or remove labels.

A pull request that changes the research plan fails the **plan-files** check until Bruce reviews it and adds the label `approved-plan-change`. The plan is the charter's scope and method, the rules and format in `claims/README.md` (questions, claims, dependencies, rule R1, decisions), the existing questions and answer codes in `data/questions.json`, the grid, regions and chosen texts in `data/snapshots.json`, this file, the checker, the fold script and everything under `.github/`. The full list is in `.github/scripts/plan_files.py`. An entry, verification or merge pull request should not touch any of it; if one needs to, it says so in its description and leaves the decision to Bruce.

## Rules that hold everywhere

- Anything in quotation marks has been read from the page image, never from OCR.
- Every claim cites edition, section and printed page, with a scan link.
- The period's ideas in the period's terms. Modern concepts only as brief glosses in the entry's "terms for modern readers".
- A change to rule R1 or to the claims format is a numbered decision recorded in `claims/README.md`, made by Bruce, not by an entry branch.
