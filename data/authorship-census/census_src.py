"""The authorship census of the leesharks.com apparatus wing, first batch (2026-11-01). Writes census.json.

Operator, 2026-11-01: "and now leesharks.com... i think in the apparatus wing, a meta-aggregator: avant-garde/experimental, data poetics, ai and
authorship... what else? whats out there?"; then, on the split from training-layer literature, "tll is a separate question... it probably needs a
meta-aggregator too, and that is a useful way to distinguish and individuate the purposes"; "yes, lets build both". The apparatus wing is the
site's defensive layer (provenance, rights, captures, disambiguation). Organizing question: whose authorship does the resource keep, under what
name, and how does it hold a name the author chose? Anchors: EA-HETERONYMY-01, Heteronymy as Ethical Operation Against Civil-Name Reduction (#940,
AXN:03B8), and AI Calls You Fake: The Existence Tax on Real People and Real Work (#1722, AXN:0B2A).

Each row is written in rows/<slug>.py from the saved sources only (sources/, dated and hashed in sources/manifest.json). Every quoted value is
checked verbatim (whitespace-normalised) against the saved text of its source. A resource's own terms are kept as its own; where it meets the
census's question is stated separately, in ls_reading, as the archive's reading.
"""
import json, pathlib, re
HERE = pathlib.Path(__file__).parent
MAN = json.load(open(HERE / "sources/manifest.json"))

AREAS = {'avant-garde-archives': 'Avant-garde and experimental archives: the record of experimental writing, sound, visual and procedural work, and of its small presses', 'heteronymy': 'Heteronymy and pseudonymous authorship: works held under names their authors made', 'collective-authorship': 'Collective and distributed authorship: works and practices whose authorship is shared, transformative or unnamed', 'ai-authorship': 'AI and authorship: law, policy, certification and litigation on who or what can be an author', 'meta-aggregation': 'Meta-aggregation: a resource that itself gathers and reads other resources'}
EVIDENCE_KINDS = ['primary text', 'audio recording', 'facsimile', 'scholarly edition', 'critical commentary', 'catalogue', 'wiki', 'registration guidance', 'legal decision', 'litigation record', 'policy statement', 'certification', 'consultation record', 'census of resources']


def Q(src, quote, basis="operator"):
    return {"src": src, "basis": basis, "quote": quote}


ROWS = []
def row(**r): ROWS.append(r)


ORDER = ['ubuweb', 'pennsound', 'epc', 'jacket2', 'eclipse', 'dada-iowa', 'oulipo', 'arquivo-pessoa', 'pessoa-digital', 'fanlore', 'otw-ao3', 'copyright-office-ai', 'gwu-dail', 'chatgpt-eating-the-world', 'authors-guild-human-authored', 'wipo-frontier', 'cope-ai']
for slug in ORDER:
    p = HERE / "rows" / f"{slug}.py"
    if p.exists():
        exec(compile(p.read_text(encoding="utf-8"), str(p), "exec"), {"row": row, "Q": Q})

def norm(s): return re.sub(r"\s+", " ", s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')).strip()
problems = []
REQ = ["slug", "name", "url", "operator", "areas", "evidence_kind", "kind", "unit", "record_object", "record", "method",
       "holdings", "stated_limits", "answers", "does_not_answer", "ls_reading", "lifecycle", "version_and_time", "negative_tags", "evidence"]
for r in ROWS:
    miss = [k for k in REQ if k not in r]
    if miss: problems.append((r.get("slug"), "missing fields", miss))
    for i in r.get("areas") or []:
        if i not in AREAS: problems.append((r["slug"], "unknown area", i))
    for k in r.get("evidence_kind") or []:
        if k not in EVIDENCE_KINDS: problems.append((r["slug"], "unknown evidence kind", k))
    rec = r.get("record") or {}
    for k in ('keeps', 'name', 'holder'):
        if k not in rec: problems.append((r.get("slug"), "record missing", k))
    srcs = {}
    for f, ev in (r.get("evidence") or {}).items():
        sid = ev["src"]
        if sid not in MAN:
            problems.append((r["slug"], f, "source not saved", sid)); continue
        srcs[sid] = {"url": MAN[sid]["url"], "read": MAN[sid]["fetched"][:10], "sha256": MAN[sid]["sha256"], "http": MAN[sid]["http"]}
        if ev.get("quote"):
            txt = norm((HERE / "sources" / f"{sid}.txt").read_text(encoding="utf-8"))
            if norm(ev["quote"]) not in txt:
                problems.append((r["slug"], f, sid, ev["quote"][:80]))
    r["sources"] = srcs
    r.setdefault("observed", {"on": "2026-11-01", "fetch": "read"})
unread = {k: {"url": v["url"], "http": v["http"], "fetched": v["fetched"]} for k, v in MAN.items() if v["http"] != "200" or v["text_chars"] < 100}
out = {"name": 'Lee Sharks apparatus meta-aggregator census: authorship', "compiled": "2026-11-01", "schema_version": "1.0", "editor": "Lee Sharks",
       "family": "Meta-Aggregators of the Crimson Hexagon",
       "schema_note": "The MMRS, provenance, Labor Vector and left-census core (slug, name, aka, url, operator, kind, unit, count, lifecycle, version_and_time, negative_tags, evidence, relations, unchecked, sources) extended for authorship: areas (one or more of five), evidence_kind, record_object (what it records), record (keeps: whose authorship it keeps; name: under what name it holds a work, and whether it keeps a pseudonym, heteronym, collective or absent name as the author gave it, as the resource itself shows, or 'not recorded'; holder: who holds it and on what terms), method, coverage, holdings, stated_limits, answers and does_not_answer, and ls_reading (where it meets the question of #940 and #1722: the archive's reading, kept apart from the resource's own terms). Every quote is verbatim from a saved source.",
       "organizing_question": 'Whose authorship does it keep, under what name, and how does it hold a name the author chose?',
       "anchor": {'deposits': [{'deposit': 940, 'axn': 'AXN:03B8', 'title': 'EA-HETERONYMY-01 v0.2: Heteronymy as Ethical Operation Against Civil-Name Reduction', 'url': 'https://www.alexanarch.org/s/records/940/'}, {'deposit': 1722, 'axn': 'AXN:0B2A', 'title': 'AI Calls You Fake: The Existence Tax on Real People and Real Work', 'url': 'https://www.alexanarch.org/s/records/1722/'}]},
       "areas": AREAS, "evidence_kinds": EVIDENCE_KINDS, "unread_sources": unread, "pending": [], "rows": ROWS}
json.dump(out, open(HERE / "census.json", "w"), ensure_ascii=False, indent=1)
print(len(ROWS), "rows;", sum(len(r.get("evidence") or {}) for r in ROWS), "evidence items;", len(problems), "problems")
for p in problems: print("  ", p)
