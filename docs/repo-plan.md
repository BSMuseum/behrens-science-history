# Plan: move the project to a GitHub repository and serve the site with GitHub Pages (2026-11-23)

**Done 2026-11-24.** Steps 1-8 are built: repository public, site live on GitHub Pages, cut-over made the same day (licence CC BY 4.0 for text and data, MIT for tools). Custom domain history.bsmuseum.org live the same evening (CNAME at WordPress.com to bsmuseum.github.io).

Written at the end of a cost-and-usage discussion with Bruce on 2026-11-23. Nothing here has been built yet. The next tab implements it.

## Why

- **One account no longer fits.** Bruce may crowdfund the project (Experiment.com) and run it on a separate, dedicated Claude Max account. Project docs, artifacts and project memory all belong to one claude.ai account and cannot be shared between personal accounts. A repository can be used from any account, and later by volunteers.
- **Parallel tabs.** Every entry tab now rewrites the shared files (`questions.json`, `snapshots.json`, `texts.json`, `cites.py`, the README, the year-page artifact), so tabs must run one at a time. One branch per entry, merged by pull request, removes that limit. Throughput, not usage, is the bottleneck. The 1675 light entry used 32% of a Pro session and 5% of a Pro week. Pro allows about 14 checked entries a week and Max about 70; one snapshot a week (about 25 entries plus checks) needs parallel tabs.
- **A public site.** GitHub Pages serves the finished pages free from a public repository, at a custom domain. WordPress.com strips page styles on most plans, so bsmuseum.org should link to the Pages site rather than host the pages.

## Bruce's decisions (2026-11-23)

- Build the repository and use GitHub Pages for the site.
- **The repository is public.** Unchecked entries being visible in it "doesn't bother me a bit."
- A next tab should implement this.
- Not yet decided: whether he creates a separate GitHub account for the project or uses an existing one; the repository name; whether the public site shows every entry or only checked ones. Proposal: show every entry, each with its verification status in plain view (the claims files already carry `verification`).

## Steps only Bruce can do

1. Create the GitHub account if a separate one is wanted. Claude cannot do sign-ups: password, email verification, possible CAPTCHA.
2. Create one empty **public** repository, suggested name `behrens-science-history`. Alternatively Claude creates it in his signed-in browser, with his OK before clicking Create.
3. In claude.ai Settings → Connectors, connect GitHub and give the Claude GitHub App access to that repository (with write access). As of 2026-11-23 no GitHub account is linked: `list_repos` reports none.
4. Later, for the custom domain: add a CNAME record for the subdomain (suggested `history.bsmuseum.org`) pointing to `<github-user>.github.io`, wherever bsmuseum.org's DNS is managed. Then the bsmuseum.org top-menu tab links there.
5. If the GitHub App's permissions don't allow it, turn on Pages in the repository: Settings → Pages → Source: GitHub Actions.

## Steps for the implementing tab

Check in with Bruce at each decision point; keep steps short.

1. **Attach the repository** with `add_repo` (access `push`), clone it, and call `register_repo_root`.
2. **Copy the project docs into the repository.** Read each with `project_read` (the docs are not always mounted at `/mnt/project`). Proposed layout:
   ```
   README.md                  project overview for the public, links to the site
   CONTRIBUTING.md            the branch-per-entry workflow (below), the entry conventions
   docs/charter.md            from claude/history-of-science-charter.md
   docs/mvp-plan.md           from claude/mvp-plan.md
   docs/repo-plan.md          this file
   docs/tests/                claude/tests/*.md
   data/questions.json        registries, from claude/claims/
   data/texts.json
   data/snapshots.json
   claims/1775-*.json         claims files, from claude/claims/
   claims/1675-*.json
   claims/README.md           from claude/claims/README.md (the conventions and rule R1)
   claims/british-texts.md
   claims/1675-plan.md
   tools/check_claims.py      adjust paths for the new layout
   tools/cites.py
   tools/build_site.py        new (step 4)
   entries/1775/<topic>.html  entry prose, cut out of the artifacts (step 3)
   entries/1675/<topic>.html
   site/templates/            page shell, styles, scripts from the artifacts
   site/front.html            from claude/site/front-page.html
   site/img/                  title pages and frontispieces (step 3)
   ```
3. **Cut the entries out of the artifacts.** The prose is not in the claims files; it lives only in the year-page artifacts:
   - c. 1775: artifact `14c627fb-e753-4737-ab22-723793622c82`, 13 entries.
   - c. 1675: artifact `c85e9cc6-ead9-45b3-9246-11977d12dc3b`, 2 entries (light, water).
   Read each with `mcp__claude-artifacts__read_file` (`paths: ["index.html"]`). Each entry is an `<article class="view" id="v-<topic>">` block. Save each block as `entries/<snapshot>/<topic>.html`, and the shell (styles, routing script, home view) as templates. The front page's images were sent to Bruce as a zip in an earlier chat and are not in the project; fetch them again from the scan URLs the front-page HTML cites.
4. **Write `tools/build_site.py`.** It builds `_site/` from the templates, the entry fragments and `data/snapshots.json`: the front page, one page per year with its home view and topic list, and each claims file published as a downloadable JSON next to its entry. Check the output against the live artifacts by rendering both in headless Chrome and comparing screenshots; the generated pages should look the same.
5. **GitHub Actions.**
   - `checks.yml`, on every pull request: run `python3 -I tools/check_claims.py` on the data, plus `build_site.py`. No merge with errors.
   - Link check (`--urls`): run it on a schedule or by hand, not on every pull request. The MDZ viewer pages time out from automated environments (see `claude/tests/1675-light-claude.md`).
   - `pages.yml`, on push to `main`: build and deploy to Pages.
6. **The branch-per-entry workflow** goes in `CONTRIBUTING.md`:
   - An entry tab works on a branch `entry/<snapshot>-<topic>` and writes only its own files: `claims/<snapshot>-<topic>.json`, `entries/<snapshot>/<topic>.html`, and proposals in `proposals/<snapshot>-<topic>.json`. A proposals file holds new questions, new codes, `drawn_from` additions, `texts.json` offset notes and `snapshots.json` status lines. Need for a new `cites.py` helper goes in the proposals file too, unless the helper is in a file of its own.
   - The entry tab opens a pull request. It does not touch the shared registries.
   - A merge tab (about once a week, or after a batch) folds the proposals into `data/`, updates `snapshots.json`, the README and the site, resolves question-ID clashes between parallel entries, and merges.
   - Verification is a separate pass, ideally by a different tab, and updates the claims file's `verification` block by its own pull request.
   - Each tab starts from a fresh clone of `main`, so it needs no earlier session's workspace.
7. **Cut-over** (Bruce decides when): the repository becomes the source of truth. The project keeps a short pointer doc and the charter for context; the other `claude/claims/*` docs are frozen. The artifacts stay as private drafts or are retired. Update the charter and README to say so, and update project memory.
8. Push, confirm the Pages site builds, and send Bruce the URL.

## Context for the campaign (from the same discussion)

- Usage so far, at API rates: about $400 of Opus 5.5 (about 1 billion tokens, mostly cache reads) in the ten days from 13 November. A clean entry costs about $12–15 at API rates; the 1775 entries cost about $23 each all-in, because each was redone two or three times.
- Estimates at API rates, Opus 5.5 High with every claim checked, 1275–1900: Phase 1 (natural philosophy and natural history) about $10k, Phase 2 (method) about $4k, Phase 3 (medicine) about $15k; chemistry and alchemy about $5.1k, sacred chronology about $2.9k, mixed mathematics about $4.6k. With Sonnet drafting, a 10% checking sample and a 1475 start, about a third of that.
- On subscriptions the money is the plan: Max $100/month (5x Pro, per five hours and per week, plus $100 a month of API credits), Ultra $200/month (10x Pro weekly, no five-hour cap for verified accounts, $200 of API credits). Twelve months of Max covers Phases 1 and 2. Bruce's own Pro plan is shared with other work, and he uses the project to use up leftover allowance.
- Pre-1600 alchemy and sacred chronology were not taught as printed courses, so rule R1 needs a clause on what counts as taught consensus before those fields start.
