# Brief: the authorship census single pages, from the /non articles (2026-11-01)

The operator, 2026-11-01: "so lets get the lists, build the /non articles, then revise and finish the individual pages"; then "now we seat the captures, write the /nons ... then come back and flesh out the single pages". The 23 /non articles are built. You do two things for each entity in your task: correct its census row where the /non composer found a field a fetched source contradicts, leaves short or shows out of date; and write its entity article from its /non knowledge object.

Directory: /home/claude/fleet/leesharks.com/data/authorship-census. Do not run git, do not fetch anything, and write only (a) rows/<census slug>.py for your entities and (b) your own articles file, articles-<letter>.py (letter in your task). Do not touch census_src.py, sources/, any other row or any other file.

## 1. Census corrections (rows/<slug>.py)

Read first: census_src.py (whole: the row() fields, Q(src, quote, basis), the verbatim check), the row file, and its entity's section of /home/claude/alexanarch/rebuild/capture-registry/intake-20261101-authorship-aggregators/REPAIRS-PENDING.md (the composer's reported corrections).

The /non composers' fetched pages are now census sources: sources/<slug>--non-B<n>.txt, entered in sources/manifest.json with "adopted" (its url, the /non row and the field source it was). The census's own sources are sources/<slug>--<id>.txt. Every correction you make rests on a verbatim quote from one of these, added to the row's evidence as Q("<source id>", "<verbatim quote>", "<basis>"). Basis: "operator" for the resource's own page, "third_party" for anyone else's (Wikipedia, press, a partner institution).

- Correct each reported item that a saved source bears out: change the field's value, add the evidence quote, and where the census said "not stated in the saved sources" or "not recorded", state what the source states. Keep the census's form: a resource's own terms as its own; the archive's reading only in ls_reading, record.function and the like, as the field already does.
- Where a reported item rests on a source that is not saved (a card snippet only, a refused page), leave the field and add a line to the row's unchecked list saying what the source is reported to say and that it is unsaved.
- Where two saved sources disagree, state both in the field with their sources (e.g. "2008 (the lab's own site) and 2011 (...)").
- Remove from unchecked, does_not_answer and negative_tags any entry the adopted sources now answer, and say in the field what they answer.
- Run `python3 census_src.py` until it prints 0 problems. It writes census.json; other readers run it too, so a clash is harmless; rerun it last.

## 2. The article (articles-<letter>.py)

Read first: /home/claude/fleet/tools/BRIEF-AGGREGATOR-ARTICLES.md (the form, whole) and the exemplar it names, /home/claude/fleet/machinemediation-org/scripts/meta_aggregator/articles.py (read it whole). Then each entity's /non row, /home/claude/alexanarch/datasets/negative-of-the-negative/v2/rows/<non row>.json: read objects.KO.sentences whole. That knowledge object is your only source of fact for the article, as the brief says.

Write `ARTICLES = { "<census slug>": {...}, ... }` in your file, one entry per entity, in the brief's form exactly: non_row, kernel, kernel_ko, sections, ko. The KO is composed under v0.10 with attribution beneath each sentence; keep that: the article prose names no source except where who holds a claim is part of what is said. The census corrections and the article must agree: where the KO states a fact the corrected row now carries, they say the same thing.

Check: `python3 /home/claude/fleet/tools/check_articles.py articles-<letter>.py` until it reports 0 problems.

## Rules (both parts)
- Mechanics, never motive. Quote verbatim; never paraphrase a source into a claim it does not make.
- Prose: plain declarative English; never "not X but Y", "X, not Y", "rather than" or "instead of" outside quotations; no gendered generics; no hard line breaks inside strings.
- Never use pkill or kill any process.

## Final message
For each entity: the census fields changed (old value, new value, source id), the reported items left unchanged and why, the article's section headings and word count, and anything in a KO or a source that looked wrong to you (report it; do not correct it).
