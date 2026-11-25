# Test report: c. 1675 "Water, the sea and springs", arm B (Claude with free OpenRouter models)

Run 2026-11-22, 21:16-23:15 (New York), Claude Opus 5.5 in one tab, with free (`:free`) OpenRouter models. Arm B of the test described in `claude/claims/1675-plan.md`; arm A is `claude/tests/1675-light-claude.md`. The unquoted claims were checked in a second session on 2026-11-23 (section "Check of the unquoted claims" below), and the judgment was revised after it.

## Outputs

- Entry published on the year page "Natural Philosophy c. 1675" (artifact c85e9cc6-ead9-45b3-9246-11977d12dc3b), version 1795407042-e6e8, view `#water`. The home page now says two of 25 topics are written, and the water row links to the entry. Corrected 2026-11-23 to version 1795488936-02cc (below).
- `claude/claims/1675-water.json`: 92 claims (R 25, S 21, G 21, L 25; common 16, dispute 47, open 11, why 18), 34 quotations; `check_claims.py` reports 0 errors (197 questions, 19 texts).
- `claude/claims/questions.json`: 191 to 197 questions. New: tides-follow-moon (under tides-cause), springs-rise and springs-fresh (under springs-origin), sea-higher, tides-in-springs (under tides-cause), sea-current. New codes: sea-salt earth-salt-carried, burnt-exhalation and sun-heat; tides-cause sea-spirits; sea-light salt-sparks. water-purity changed from local to persistent. drawn_from extended on 17 questions.
- `claude/claims/cites.py`: helpers RO2 (Rohault vol. 2, canvas = page + 4), GO2 (Goudin t. 3 with the + 26 offset for pp. 270-290) and LG2 (Le Grand Part VI, /page/n = page + 60). The earlier RO, GO and LG are unchanged, so the light entry's links are not affected.
- Not done: `README.md`, `snapshots.json` and `texts.json` were not updated with the entry or the corrected pages (below); the front-page doc was not touched.

## Pipeline as run

1. **Pages located by Claude** from the MDZ page OCR and word search and the IA hOCR search text, then confirmed with two stacked strips of page tops (20 pages). 101 pages: Rohault vol. 2 pp. 140-152, 169-176, 181-182, 189-191, 275-282 (34); Sperling pp. 568-598 (31); Goudin t. 3 pp. 122-132, 273-285 (24); Le Grand pp. 340-344, 359-365 (12).
2. **Transcription and translation** by particle-ai/particle-1:free, one request per page, page image sent as base64 (see the trial below), output page-tagged JSON (printed page, running head, text, margin notes, translation, unreadable places).
3. **Claim drafts** by nvidia/nemotron-3-ultra-550b-a55b:free and baidu/ernie-5.5-flash-preview:free, one request per text per model (8 drafts), each given the four sections' transcriptions and translations and 25 questions from `questions.json`, and allowed to propose new questions.
4. **Comparison** by a script (`compare.py`): claims matched by text and question, stances and codes compared, every draft quotation searched for in the transcription of its cited page.
5. **Resolution and writing** by Claude: the claims file built in a Python builder from the drafts, the transcriptions and, for disagreements, the free model's translations; then the quotation check against the page images; then the entry.

Corrections to the plan found in step 1: Sperling's chapter on water is IV.3 at pp. 568-598 (canvases 586-616); the plan's pp. 646-681 are his chapter on heat and cold. Rohault's tides run to p. 152, not p. 150. Goudin's III q. 3 a. 3 § 4 begins on p. 273, not 274. Le Grand's Part VI pages are /page/n = page + 60 (pp. 340-365), not + 59. Rohault on the sea's saltness is III.4 arts. XXXIII-XXXVI, pp. 189-191, and on the sparks of the sea arts. XIV-XVII, pp. 181-182.

## Model choice

- **Vision trial (two pages, Rohault p. 141 and Sperling p. 572).** google/gemma-4-31b-it:free and google/gemma-4-26b-a4b-it:free returned HTTP 429 on every request (Google's shared free pool rate-limited upstream; 15 requests, none answered). nvidia/nemotron-3.5-super-vl:free refused image URLs (HTTP 404, "No endpoints found that support image URLs") and worked with base64; inclusionai/ling-3.2-flash:free gave 429s and one truncated answer. particle-ai/particle-1:free answered both pages. Compared word by word, nemotron-vl modernised the spelling against the brief ("même", "notre", "après" for "mesme", "nostre", "aprés") and misread several words ("fera" for "sera", "eft", "colle&tum", "suit" for "fuit", "amplitate" for "amœnitate"); particle-1 kept the period spelling and abbreviations ("appareatq;", "Vocavitq;", "verò") and its only systematic fault was leaving line-end hyphens unjoined. Particle-1 was chosen. Neither of the two vision models the brief suggested could be used: one was unavailable, the other could not take the MDZ or IA URLs.
- **Text models.** nemotron-3-ultra as asked; Ernie 5.5 Flash as the second (1M context, a different maker). Ernie ran out of its 32,000 output tokens on 9 of 14 requests, all spent before any answer appeared; asking for low reasoning effort or capping reasoning tokens did not help, and splitting Sperling in two did not either. It worked at temperature 0.6 instead of 0.1 (the Goudin and Sperling drafts). After the Le Grand drafts the prompt was also shortened (omit questions not raised, statements under 45 words, at most four new questions); nemotron's Le Grand draft was made with the first prompt, the other seven with the second.

## OpenRouter requests

243 requests in all, from 21:20 to 22:56, a maximum of 18 a minute by the client's own spacing; far under the 1,000 a day.

| Model | Requests | Answered | 429 | Out of tokens | Other failures |
|---|---|---|---|---|---|
| particle-ai/particle-1:free (vision) | 195 | 108 | 64 | 22 | 1 connection reset |
| google/gemma-4-31b-it:free (trial) | 12 | 0 | 12 | 0 | 0 |
| google/gemma-4-26b-a4b-it:free (trial) | 3 | 0 | 3 | 0 | 0 |
| nvidia/nemotron-3.5-super-vl:free (trial) | 4 | 2 | 0 | 0 | 2 (image URLs refused) |
| inclusionai/ling-3.2-flash:free (trial) | 10 | 0 | 8 | 2 | 0 |
| nvidia/nemotron-3-ultra-550b-a55b:free (drafts) | 5 | 5 | 0 | 0 | 0 |
| baidu/ernie-5.5-flash-preview:free (drafts) | 14 | 5 | 0 | 9 | 0 |

The two nemotron-ultra and Ernie counts include one test request each. Particle-1 needed more than one request for 49 of the 101 pages; 7 pages failed five attempts in the first run and were sent again, and 3 answers that were cut off mid-JSON were sent again with a larger token limit. A successful page took about 50 seconds. Six parallel workers transcribed the 101 pages in about 45 minutes. Token use reported by OpenRouter: particle-1 169,000 in and 1,242,000 out (most of it reasoning); Ernie 296,000 in and 406,000 out; nemotron-ultra 93,000 in and 48,000 out. All cost 0.

## Claude's own work

- **Tool calls:** about 140. Bash about 75, Read 16 (15 image reads and one file), Projects 15 (10 reads, 3 writes, 1 info, plus this report), Write 7, artifact tools 6, task list 10, ToolSearch 1. No subagents.
- **Page images viewed:** 15 image reads, none of them a whole page. Two were stacked strips of page tops (20 pages) for the offsets; twelve were sheets of crops for the quotation check (34 quotations on 31 pages, then 9 crops again where the first crop missed the line or the reading was in doubt); one was a screenshot of the rendered table. Claude read no page in full from an image. Arm A made 27 image reads, 47 full-page views.
- **Text read instead of images:** the MDZ and IA OCR for locating the sections; the free model's translations of about 30 pages, where the drafts disagreed or a statement needed checking; and the two drafts in full (side by side, about 60 KB).
- **Unexpected costs:** reconstructing `questions.json`, `cites.py` and `check_claims.py` in the workspace, since the project docs are not mounted (about 110 KB written out once); and the running of the pipeline itself (rate limits, retries, the Ernie failures), about 25 tool calls.

## Disagreements between the two drafts and how they were resolved

The comparison script matched 93 text-and-question pairs: 28 agreed, 18 differed in stance or code, 35 were raised only by Ernie and 12 only by nemotron. Ernie proposed 20 new questions and nemotron 8. Main resolutions:

- **Springs from the sea (all four).** Nemotron coded Rohault's springs as condensed-vapour and Le Grand's as several; Ernie coded Rohault sea-underground. Resolved: all four hold that the sea feeds the springs (common ground); how the water climbs became a new question, springs-rise (vapour raised by underground heat for Rohault and Le Grand, the earth's veins for Sperling, several causes for Goudin).
- **Rain.** Only Ernie had Sperling's rejection of rain (ten feet) and of condensed vapours; kept after reading the translation of pp. 573-575. Le Grand coded several (springs that fail in summer come from rain and snow), from p. 343.
- **Why springs are fresh.** Nemotron proposed spring-desalination, Ernie salt-in-wells and salt-springs; merged into springs-fresh with two codes. Both drafts missed that Le Grand also has the springs filtered through sand (p. 343), found in the quotation check and added.
- **Sea's saltness.** The drafts agreed on Sperling (created) and Le Grand (made in the sea by heat), split Goudin between created-salt and made-in-sea, and coded Rohault salt-beds. Resolved with new codes: Rohault earth-salt-carried (salt formed in the earth carried in by underground waters); Goudin created-salt (remote) and burnt-exhalation (nearer); Rohault and Sperling both reject sun-heat, Aristotle's view (Ernie's proposed sun-and-sea-salt questions became this code).
- **Tides.** Ernie had Sperling rejecting moon-attraction, from Scaliger's argument that only the motion of gravity has an internal mover: a misreading of the passage, dropped. Sperling's internal cause (spirits in the sea, after Basso) became the code sea-spirits in place of Ernie's proposed tides-internal-cause. Goudin's rejections of rarefaction and of Plato's whirlpool kept (both drafts). Nemotron coded the tidal timing under earth-motion; the timing became the common-ground question tides-follow-moon.
- **Elements and qualities.** Ernie coded Sperling holding element-change and water-into-earth from petrifying springs and hardened moisture (pp. 576-582): an over-reading, dropped. Nemotron coded the four elements "rejects" for Rohault and Le Grand, though neither names them in the pages read: changed to not_taken_up, with matter-principles cartesian-elements. Water's coldness, fluidity and vapour-is-not-air: the drafts agreed in substance; Goudin's cold-and-moist was not found.
- **Earth's height above the sea, tidal springs, currents.** Both drafts proposed "is the sea higher than the land" for Goudin (sea-higher). Ernie's tidal-springs and tides-in-wells were merged into tides-in-springs; its sea-current kept; its tides-timing, tides-variation, water-transparency, cold-nature, salt-water-weight and the rest were not adopted (single-text details).
- **Scripture and purposes.** Nemotron coded Le Grand and Goudin scripture-nature authority on the strength of one citation each; recoded as leans.

## Quotation check

All 34 quotations in the claims file, on 31 pages (32 with the run-over to Le Grand p. 342), were compared with the page images before publication. The quotations were taken from particle-1's transcriptions, so the check measures that model's accuracy on the passages that mattered most.

| Error type | Count | Cases |
|---|---|---|
| Misreading | 5 quotations (6 words or marks) | Sperling p. 577 "cōmixta" for the printed "cōmista"; p. 568 "Quæ" for "Qua" after the drop capital, and "terra" for "terrà"; p. 587 "ferrum" for "ferrùm"; Goudin p. 122 a printed full stop after "constat" left out; Le Grand p. 359 "Adeò" for "Adeo" |
| Mistranslation | 0 found | in the 34 passages checked (the quotations' translations are Claude's own, from the originals) |
| Wrong page | 1 in the transcriptions, 1 in the drafts | particle-1 put the end of a p. 342 sentence on p. 341 (below); Ernie cited Le Grand's "Quod enim occultum est..." to p. 361, where the transcription and the image have it on p. 362 |
| Invented quotation | 1 in the transcriptions; 8 in the nemotron drafts | particle-1's p. 341 joined "in Vapores vi" to "caloris ascendere", dropping "subterranei resolvi, & per meatus, quos ubique reperit," from the next page. In the drafts, 8 of nemotron's 61 quotations could not be found on any transcribed page (strings joined with ellipses, or rephrased) and 15 more matched only in part; Ernie's 94 had 1 not found and 2 partial |

28 of the 34 quotations matched the transcription exactly (82%). One transcription misreading outside a quoted span was also seen ("Et d'autant" for "Et dautant", Rohault p. 278). The check was made by the same session that resolved the drafts and chose the quotations, so it is independent of the transcriptions but not of the resolution; the claims file's `verification` stays "unverified".

Arm A, for comparison: 27 quotations, all transcribed by Claude from the images; 3 corrected at the check, all of the same small kind (an abbreviation, an accent, a capital).

## Check of the unquoted claims

Run 2026-11-23, 21:48-22:30 (New York), Claude Opus 5.5, a new session with no access to the first session's workspace (the raw model outputs, the builder, the comparison). 22 claims that had no quotation and whose cited pages had been read only through particle-1's transcription and translation were read again from the cited pages. The free model's text was not used. Only the passage each claim rests on was read, from the library OCR: the MDZ page OCR (hOCR from api.digitale-sammlungen.de, turned into lines) for Rohault, Sperling and Goudin, and for Le Grand the IA hOCR search text cut by the page index. A page image was read only where the OCR could not settle the point, or where wording was to be quoted.

**Result: 12 confirmed, 8 corrected, 2 set to not_taken_up. Nothing set to not_found. No code had to change, so `questions.json` is unchanged.**

| # | Claim | Text, pages | Outcome | Error type | What the page says |
|---|---|---|---|---|---|
| 1 | 005 tides-follow-moon | R 141-142 | corrected | unsupported | Claim right. The reason "tide tables and sailors" is not on pp. 140-142: Rohault reckons the delay "sur l'experience de plusieurs jours". Section was arts. III-VI; the claim is arts. IV-VI. |
| 2 | 006 tides-follow-moon | S 585, 587 | corrected | mistranslation | "cum Lunæ cursum sequi, observatum esset" (image): the *sea* was seen to follow the *moon's* course, so the moon was judged its author. The claim had it the other way round. The library OCR also reads "Luna" without the æ, which would give the reversed sense. |
| 3 | 007 tides-follow-moon | G 274 | confirmed | | |
| 4 | 008 tides-follow-moon | L 361, 364 | confirmed | | |
| 5 | 009 water-purity | R 278-280 | set to not_taken_up | unsupported | Coded "no" (natural water hardly ever pure). Rohault says spring and well water must be fresh (art. VIII). Salt springs and medicinal springs are particular cases (arts. IX-X). He does not say whether natural water is pure. p. 278 added to the cites. |
| 6 | 012 water-purity | L 360, 343 | set to not_taken_up | unsupported | Coded "no". p. 360 says the opposite if anything: distilled sea water gives "aqua pura, fontanæ, aut fluviali omnino similis" (image), pure water wholly like spring or river water. Salt in inland wells is unfiltered sea water (p. 343). |
| 7 | 016 water-into-air | L 342, 365 | corrected | unsupported | "holds" changed to "leans". Le Grand never says that vapour is not air. He makes air from the subtler parts of exhalations, which are particles of earthy bodies and differ from the vapours torn from water (pp. 365-366). p. 366 added. |
| 8 | 019 matter-principles | R 169, 175 | corrected | unsupported | Code right. But the account of water is hedged: "il y a lieu de croire qu'un tel amas pourroit bien ressembler à ce qu'on appelle de l'Eau" (image). Confidence changed from asserted to probable. |
| 9 | 020 matter-principles | L 359 | corrected | unsupported | Code right. Descartes is not named on p. 359, so he was removed from the persons. "Long" particles of water are not on the page; p. 360 calls the salt particles long. The two kinds of particle on p. 359 were added. |
| 10 | 025 water-qualities | R 173 | confirmed | | |
| 11 | 038 tides-cause | G 275 | confirmed | | Note: the code lunar-effluvia ("effluvia from the moon fermenting...") is the nearest code. Goudin rejects a lunar fermentation and rarefaction and says nothing of effluvia. |
| 12 | 039 tides-cause | G 273-274 | confirmed | | |
| 13 | 041 springs-rise | R 276 | confirmed | | |
| 14 | 043 springs-rise | L 341 | confirmed | | |
| 15 | 044 springs-rise | S 575 | corrected | mistranslation | "quia validis velut brachiis hinc & hinc terræ se insinuat, diversa accepit nomina": the sea's "strong arms" are its gulfs, which is why it has different names. They are not a way the water works into the earth. The veins and the blood hold. |
| 16 | 045 springs-rise | G 280-281 | corrected | mistranslation | "voraginibus ... absorpta": rivers swallowed by chasms in one place and given back after up to thirty leagues underground, not by whirlpools. Basil (Homily 4 on the Hexaemeron), cited for the spirits shut in the earth, was missing from the persons. |
| 17 | 047 springs-origin | S 573 | confirmed | | |
| 18 | 048 springs-origin | G 278 | confirmed | | |
| 19 | 049 springs-origin | L 343 | corrected | wrong page | The objection, and the answer that such springs come "ut plurimum" from rain and snow, begin on p. 342. p. 342 added. |
| 20 | 054 springs-fresh | G 277 | confirmed | | |
| 21 | 061 sea-salt | G 276-277 | confirmed | | |
| 22 | 063 sea-salt | L 360 | confirmed | | "non videtur probabile" read on the image. |

**Errors by type** (10 claims; one claim, 045, has two errors):

| Type | Count | Claims |
|---|---|---|
| Misreading | 0 | |
| Mistranslation | 3 | 006 (subject and object reversed), 044 (the sea's "arms" applied to the springs), 045 (voragines as whirlpools) |
| Wrong page | 1 | 049 (p. 342 missing) |
| Unsupported | 7 (in 6 claims) | 005 (reason not on the page), 009 and 012 (code not supported), 016 (stance too strong), 019 (confidence too strong), 020 (person and a detail not on the page) |
| Omission | 1 | 045 (Basil not in the persons) |

Where the errors came from cannot be settled now, because particle-1's translations and the drafts stay in the first session's workspace. The three mistranslations are of the kind a translation passes on. The seven unsupported points are coding decisions, made in the drafts or in Claude's resolution. Claims 009 and 012 were common ground that the resolution built across four texts.

**Changes to the entry** (version 1795407042-e6e8, checked live with get_artifact before the edit, to 1795488936-02cc):

- Common ground, "Waters take their tastes and powers from the ground they pass through": Le Grand's sentence now says he does not take the question up, with the p. 360 wording from the image and the inland wells (L 343 added).
- Common ground, "Vapour is not air": Le Grand "implies it without saying so", with the exhalations as particles of earthy bodies (L 366 added).
- The disputes, what water is made of: Rohault's particles are put forward as likely, "il y a lieu de croire".
- The disputes, how the sea water reaches the springs: Sperling's sentence no longer has the sea's "strong arms". Goudin's rivers are swallowed by chasms, not whirlpools. Basil of Caesarea (c. 330-379) is named for the enclosed spirits.
- The disputes, whether rain feeds the springs, and the table row "Does rain feed the springs?": Le Grand's cite is L 342-343.
- Table row "What water is": Rohault's cell begins "Probably".
- Rows "What moves the tides?", "How does sea water reach the springs?", "Why are the springs fresh?", "Why is the sea salt?" and the section "Why they differed": no change needed.

**Claims file.** In the 22 claims, every cite's `read_from` now records this reading: "ocr" means the library OCR, and "image" the page image. A `claim_check` record lists them, and `coverage` says that elsewhere "ocr" still means particle-1. `site.version_encoded` is now 1795488936-02cc. `check_claims.py` reported 0 errors on the first run. It was run in the workspace against copies of `questions.json` and `texts.json` reduced to the 23 questions (ids, parents, codes) and four texts that the file cites, because the project docs are not mounted. The totals are unchanged (92 claims, 34 quotations, R 25, S 21, G 21, L 25).

**Pages read.** Library OCR, 32 pages:
- Rohault vol. 2: pp. 140, 141, 142, 169, 173, 175, 276, 278, 279, 280.
- Sperling: pp. 573, 575, 585, 587.
- Goudin t. 3: pp. 273-281.
- Le Grand: pp. 341, 342, 343, 359, 360, 361, 364, 365, 366.

Page images, 3 crops, all at 900 px (MDZ) or 1200 px (IA) wide:
- Sperling p. 585, top quarter (Lunæ).
- Rohault p. 169, lower half (il y a lieu de croire).
- Le Grand p. 360, middle third (aqua pura...; non videtur probabile).

The MDZ OCR was good enough for every point on Rohault, Goudin and Sperling except the one ending in æ. The IA OCR of Le Grand is noisy (long s as f, broken ligatures) but was readable for all nine pages.

**Tool calls: 50.**
- Bash 26: fetching and converting the OCR (7), reading it (13), image crops (3), the reduced registries, the checker and the counts (3).
- Read 3: the three crops.
- Projects 8: six reads (the report, the claims file, cites.py, questions.json, check_claims.py, texts.json) and two writes.
- Artifact tools 10: get_artifact 2, list_files 1, read_artifact 5 (the water view in parts), edit_version 1, and this count's last check.
- Write 3: the checker, the claims file, this report.

No subagents and no task list. The largest cost was writing the 92-claim file out in full once, since a project doc can only be replaced whole.

**Left open by the check:**
- Claim 033 (Le Grand, tides) also names Descartes as followed. p. 362-363 was not read for it, so whether he is named there is unchecked.
- The common-ground item on waters is now carried by Rohault, Sperling and Goudin under a heading ("tastes and powers from the ground") that is broader than its question, water-purity ("Is natural water pure?"). Only Sperling and Goudin hold "no". Bruce may want the item reworded or moved to the disputes.
- Code lunar-effluvia for Goudin (038) is approximate, as above.
- The other 36 claims whose cites include an "ocr" page from particle-1 were not checked. Their other pages were read on the image in the quotation check, but these were not.

## Judgment

*Revised 2026-11-23 after the check of the unquoted claims.*

**Cost.** The free models did take the first reading off Claude. Claude viewed no page in full (arm A: 47 full-page views), and the image reads fell from 27 to 15, almost all of them crops for the quotation check. They did not cut the number of tool calls (about 140 against 133), because running the pipeline cost what the reading saved:
- Two of the four suggested or tried vision models could not be used at all.
- A third of particle-1's requests and nearly two thirds of Ernie's failed.
- Keeping the six workers and the eight drafts going took about 25 calls.

The check of the unquoted claims added 50 calls and 3 more image reads, for about 190 calls in all against arm A's 133. Bruce's usage bar is the better measure of the cost to Claude; a large part of both sessions' cost was output (the registries, the builder, the entry, the claims file written out whole).

**Quotations.** On accuracy, the free models alone would not have been good enough. Of the 34 quotations, 6 came from the transcription wrong. One of them was a sentence silently stitched across a page break. Nothing in the transcription marked any of them as doubtful: the "unreadable" lists were empty.

**Paraphrases.** The paraphrases were worse than the quotations. Of 22 unquoted claims that rested on particle-1's translation, 10 needed a change and 2 of the 10 had to be withdrawn. In 3, the sense of the Latin was wrong: one reversed subject and object, one put a sentence about the sea's names into an account of springs, and one turned chasms into whirlpools. In 6, the claim said more than the page: a reason the page does not give, a person it does not name, "holds" or "asserted" where the text hedges or only implies, and twice a code that made common ground out of texts that do not take the question up. So the drafts and the resolution together erred on about one claim in two, against one quotation in six for the transcription. The errors were not in reading the letters, which the transcription did fairly well, but in what the Latin says and what the claim may say about it.

The first version of this judgment said the entry was "less certain than arm A on the paraphrases". That was an understatement. Before the check, the entry's common-ground list had one item misrepresenting Le Grand. Its disputes had three statements the texts do not make. The drafts needed a good deal of judgment before this check too:
- Three codes rested on misreadings or over-readings (Sperling on attraction, on water into earth and on the change of elements).
- Several claims were coded under the wrong question.
- Both drafts missed a claim the page states (Le Grand's filtering).
- Nemotron's quotations were often not quotations.

Ernie's drafts were the more complete and the more exact, nemotron's the more conservative. Arm A's unquoted claims have not been checked the same way, so the comparison is not yet fair to arm B. But arm A's claims were read by Claude from the images, not through a second model's translation.

**Verdict.** With these texts the free models saved some of Claude's page reading and no tool calls. The entry they produced was not publishable without a check of every claim, not only of every quotation. The check also showed that the library OCR is good enough for Claude to read paraphrased claims directly. The MDZ OCR is clean for these French and Latin pages; the IA OCR of Le Grand is noisy but readable. A free vision model adds little where library OCR exists, and its translations are where the errors came in.

If the method is kept:
- Use the free vision model only for pages without usable library OCR.
- Have Claude read the library OCR for every claim, and the image for quotations and for points that turn on one letter (like "Luna" for "Lunæ").
- Ask one text model only, if any, for a first list of claims to check, not for paraphrases to publish. Ernie's draft alone would have carried most of what the comparison added.
- If a vision model is used, the two earlier suggestions still hold: send it half-page crops, and have it mark each page's first and last words so a script catches page-break joins.

## Left for later

- Fold this entry into `README.md` (the 1675 entries section and the plan corrections above), `snapshots.json` (water: status and sections, Sperling IV.3 pp. 568-598) and `texts.json` (Rohault vol. 2 offset confirmed on the images; Sperling's chapter on water; Le Grand + 60 in Part VI).
- Front-page doc: the 1675 block still says one topic is written.
- Life dates used and not re-checked online: Seneca (c. 4 BC-AD 65), Plato (c. 428-348 BC), Thomas Aquinas (c. 1225-1274), Basil of Caesarea (c. 330-379), Pliny the Elder (23/24-79), Aristotle, Scaliger, Descartes; Sebastian Basso's dates not found.
- Not read: Rohault pp. 176-189; Sperling pp. 578-582 and 588-590 beyond what is cited; Goudin pp. 128-132 and 281-285 beyond what is cited; Le Grand's other Part VI articles.
- The workspace copies of the raw model outputs (`raw/vision`, `raw/draft_*`), the request log, the comparison and the quotation-check log stay in the session's workspace and are not in the project.
- From the check of the unquoted claims: claim 033's Descartes; the wording or place of the common-ground item on waters; the 36 claims with unchecked particle-1 pages.
