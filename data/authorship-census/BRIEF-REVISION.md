# Brief: the revised census (schema 1.1, 2026-11-01)

Read BRIEF.md in this directory first: everything in it still holds (read-first list, row fields, prose rules, verbatim evidence, the check), except where this brief changes it. Do not run git. Do not fetch anything. Write or edit only the row files you are given.

## What changed and why
The operator found the first selection unrepresentative and ruled the census revised, adopting an outside selection review (selection-review-2026-11-01.md in this directory: read its sections on this census, including its disposition table and its "limit to retain" notes, which state what each candidate's evidence does not establish). The driver census_src.py now carries the revised organizing question, new AREAS, added EVIDENCE_KINDS, HOST_RELATIONS and RECORD_TYPES. Read it again.

## New required fields on every row
- host_relation: one of HOST_RELATIONS, what the resource is to this census (direct case, theoretical interlocutor, empirical comparator, historical lineage, infrastructure, counterposition, peripheral comparator, meta-aggregation). An editorial reading: state it from what the sources show the resource to be, and follow the review's disposition where it gives one unless the saved sources contradict it (then say so in your final message).
- record_type: one of RECORD_TYPES, the exact object recorded (a project, a work, a persona, a paper, a tool...). Where a name covers several objects (a persona, its models and a book of the same name), record the one the row is about and link the others in relations or negative_tags; do not treat them as aliases.
- question: one line, the specific question this resource answers (name preservation, authorial function, contribution, training membership, generative transformation, audience evaluation, legal ownership...), as its record can actually answer it.
- record gains one key. Authorship census: record.function, how the authorial function, contribution and responsibility are constituted and attributed, as the resource shows (or "not recorded"). Layer census: record.makes, what a receiving apparatus makes from the work there, as the resource shows (or "not recorded").
- The reading field (ls_reading / tll_reading) answers the revised organizing question. A resource's own claims stay its own; publisher, artist and author descriptions are quoted as such (basis "operator" for the resource's own pages), and never restated as independently established.

## Not now
No kernel and no article. The full entity pages wait for each entity's /non article.

## Amending an existing row (the amend readers)
Add the new fields, move areas to the new keys (authorship: 'ai-authorship' is now 'governance'; check every area against the new definitions and add or drop where the sources support it), and revise the reading field to the revised question. Keep every existing evidence item and quote unless it is wrong; add evidence for anything new. Set version_and_time.read to the manifest's fetch date.

## Check
`python3.12 census_src.py` from this directory, until your rows show no problems. Final message: your rows with host_relation, record_type, areas and lifecycle; what the sources could not establish; any disagreement with the review's disposition and its ground in the saved sources.
