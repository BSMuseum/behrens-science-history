# MVP plan and project direction (2026-11-16)

Written by the tab that did the water and motion entries, from a scoping conversation with Bruce on 2026-11-15/16. Where this conflicts with the charter's "Scope decisions" (Intervals, Order), this document is newer. The next tab should fold these decisions into the charter and then keep this file as background.

## Decisions

Bruce's own decisions:
- Minimum viable product, meant to attract support: natural philosophy at three snapshots, c. 1575, c. 1675 and c. 1775, plus a machine-readable claims file for every entry. Finish 1775 first (earth and the bodies drawn from it, meteors, and the terraqueous globe remain).
- The long-term aim stays comprehensive (medicine, chemistry and alchemy, natural history and so on), because fields move between disciplines over time. The MVP is limited to natural philosophy.
- He may later put the project on a public website where volunteers contribute their own Claude time, possibly as a new site. "Don't do that yet."
- The site artifact stays private. He does not want it shared; he wants it where his agents can update it, which is already the case (see Housekeeping).

Claude's proposals, accepted with "Ok" in the same exchange:
1. Each snapshot keeps its own topic list from the period's own classification. In 1575 natural philosophy still includes the soul (De anima), animals, plants, meteorology and the heavens as the fifth element; do not squeeze 1575 into the 1775 list. Showing subjects leave natural philosophy is the point of the comprehensive scope.
2. A persistent question layer. Each snapshot has its own topics, but every claim is also tagged with a stable question ID that runs across snapshots ("what is light?", "why do heavy bodies fall?", "does the earth move?", "what is fire?", "can water become earth?", "is inertia a force?"). Design it before any 1575 reading; it is the hardest part to retrofit.
3. A fixed, stated rule for choosing texts, applied the same way in every snapshot (for example, the most-reprinted course in each region's main teaching tradition), so that later counts mean something.
4. The MVP includes one or two cross-snapshot visuals: lifelines of answers to three or four persistent questions across 1575-1675-1775, and a diagram of disciplinary boundaries shifting.
5. Grid: shift the early 50-year steps to anchor on 1575 (… 1525, 1575, 1625, then 25-year steps from 1675). This moves the first snapshot from c. 1250 to c. 1275.

## Next step

Design the question list and the claims format against the ten published 1775 entries, before any 1575 reading. Then backfill claims files for the ten entries (a few hours), and record the decisions above in the charter.

Draft claims format (a starting point, not settled):
- texts registry: siglum, author, title, edition, year, place, region, tradition or confession, why chosen (reprint evidence), scan id.
- questions registry: question_id, neutral wording, the period's own names for it, snapshots where it appears.
- claims: id, snapshot, period topic, question_id, text siglum, region, position in a sentence, stance (affirms / denies / undecided / not taken up / not found in the parts read), reasons each tagged by kind (experiment, observation, authority, Scripture, sufficient reason, analogy, design, mathematics, other), confidence language as printed ("demonstrated", "probable", "can never be shaken"), citations (page and scan URL), quotation (original, translation, read from image yes or no).
Keep "not taken up" and "rejected" distinct; the charter's table convention already does.

Candidate texts, to verify against the selection rule (not yet checked):
- c. 1575: Rome, the Jesuit Collegio Romano (Francisco de Toledo's Physics commentary, early 1570s; Benito Pereira, De communibus, 1576); Wittenberg, Melanchthon's Initia doctrinae physicae (1549, many reprints) or its successors; Padua; Paris.
- c. 1675: Paris, Jacques Rohault, Traité de physique (1671), Cartesian; a Jesuit Aristotelian course; England, Antoine Le Grand, Institutio philosophiae (used at Cambridge); a German Protestant course.

## What the corpus would be for (from the discussion)

- Textbook lag: the gap between an idea's appearance in journals and its arrival in teaching texts, by region and confession; whether it shrinks; whether the supposed Catholic lag is real (Biwald, a Jesuit, is more Newtonian than Nollet in Paris).
- How questions die: settled, abandoned unanswered, or redefined away (e.g. whether water into earth left the textbooks before Lavoisier).
- Whether textbook confidence predicted survival: score each taught claim by the confidence with which it was stated, then check how it fared.
- What counted as evidence, by period: the mix of argument types (experiment, authority, Scripture, sufficient reason, analogy, design).
- Who copied whom: the Britannica from Ferguson and Macquer, Biwald from Musschenbroek; a borrowing network among textbooks.
- Maps: a topic-by-snapshot grid shaded by how contested each question was; a map of Europe per snapshot with each region's positions; a flow diagram of fields moving between disciplines; lifelines of ideas (vortices, phlogiston, emission of light).
- Caution: quantitative claims need a designed sample (decision 3).

## Volunteers and a public site (not yet; notes only)

- More writers do not remove the bottleneck, which is verification. The water entry drifted even between two tabs of the same model working from the same charter.
- Turn the charter into a contributor's guide with testable rules; add mechanical checks (every quotation has a scan link, links resolve to the cited page, every table cell cites or says "Not taken up", life dates on first mention); require an independent verifying agent that re-reads quotations from images before anything goes live.
- Good volunteer work: widening each entry from one text per region to 3-5.
- Artifacts belong to one account, so a shared project would need a public repository with entries as pull requests and pages generated from the claims data.

## Cost and effort (measured 2026-11-16)

- This tab's session: 222 requests; 72.3M tokens re-read from cache, 2.0M newly cached, 147k output. Shares: files and commands 53% (page images are the expensive part), instructions re-read every step 31%, artifact and project tools 11%, conversation under 3%.
- At API rates (third-party summaries; the official pricing page was unreachable): about $27 on Opus 5.5 for two entries plus discussion, so $10-13 per entry in long sessions; Fable 5.2 about twice that; Sonnet 5.5 about half. Cache writes were assumed at 1.25 times the input rate.
- The main cost driver is long sessions: the average step re-read about 325k tokens of context. Start a fresh tab every entry or two, search OCR with grep instead of printing it, and show the model only the pages actually quoted. With fresh context per entry, expect about $3-5 per entry on Opus 5.5, plus about half again for an independent verification pass.
- Pro plan: Anthropic does not publish limits as tokens. To measure, note the weekly usage bar in Settings, run one entry, and look again. On Pro, Fable models run on paid usage credits, not plan limits (Anthropic support article "Claude Fable models on your plan"); a third-party site says the Fable 5.2 launch inclusion ran Nov 9-16.
- Recommendation: Opus 5.5 at High for drafting, plus a separate verification pass, rather than Max effort or Fable. The water entry's faults were an unsupported generalization and consistency lapses, which a checking pass catches better than more effort on the draft.

## Housekeeping

- The project is called Behrens Science History (renamed from "History of Science" on 2026-11-17). Doc paths such as claude/history-of-science-charter.md keep their old names so that links from other tabs still work.
- The site artifact is private (read: owner). It belongs to Bruce's account, not the project; project documents hold only text. Every tab runs as Bruce, so every tab can edit it. On 2026-11-15 it was filed in a new Artifacts folder "History of Science" and pinned to the sidebar; on 2026-11-17 it was moved to a new folder "Behrens Science History" (Claude cannot rename or delete folders, so the old, now empty, folder is Bruce's to remove).

## Scoping notes on the period's own map of knowledge (c. 1775)

- Natural philosophy c. 1775 is the physics of inanimate nature; Biwald, Erxleben and Nollet treat no plants, animals or diseases.
- Outside it: medicine (its own faculty: anatomy, physiology or "institutes of medicine", pathology, materia medica, therapeutics, surgery, midwifery); chemistry (often taught in medical faculties); natural history (three kingdoms; Erxleben wrote a separate Anfangsgründe der Naturgeschichte, 1768); mixed mathematics; pneumatology and empirical psychology under metaphysics; sacred history and chronology (the Creation and Flood, Newton's and Whiston's prophecy work; the nearest home for the biblical-prophecy topic in the project description).
- 1771 Britannica, vol. 1 (read from the OCR only, not yet checked against the images): "Alchemy" is the branch of chemistry that pursued transmutation, the panacea, the universal solvent, "and many other things equally ridiculous"; "Astrology" (p. 433) "has long ago become a just subject of contempt and ridicule". The preface says pathology, physiology, materia medica and therapeutics are "not sciences, but parts or accessories of sciences" (of anatomy, botany, chemistry and medicine).
- In 1250-1300 natural philosophy is Aristotle's libri naturales; the 1255 Paris arts statutes include De anima, De animalibus and De plantis. So the boundary moves, and each snapshot's scope differs under the period-classification rule.
- Rough size: natural philosophy only, about 13 topics × 19 snapshots ≈ 250 entries; adding medicine, chemistry or alchemy, and natural history, 40-60 topics per snapshot ≈ 750-1,100 entries; widening to 3-5 texts per region multiplies the reading two to three times.
