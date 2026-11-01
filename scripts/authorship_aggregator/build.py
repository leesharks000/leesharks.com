"""Render the apparatus meta-aggregator of leesharks.com (authorship census schema 1.0): an index at /apparatus/aggregators/ and one page per resource, from
data/authorship-census/census.json. Every quoted field shows its source, the date read and the hash of the saved copy. Each record page carries two
JSON-LD nodes: the record (the archive's) and the entity it describes (the resource's). The census itself is published at /apparatus/aggregators/census.json.
The apparatus page's styles are taken from apparatus/index.html at build time; the shell (plaque, nav, foot) is copied
verbatim from the stamped apparatus page, so these pages carry the shell the wing carries (scripts/apply_shell.py is not run: its manifest is behind
the live pages' asset version and nav, and a run would rewrite nine pages). Run from the repository root: python3 scripts/authorship_aggregator/build.py"""
import html, json, pathlib, re, shutil
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = json.load(open(ROOT / "data/authorship-census/census.json", encoding="utf-8")); ROWS = D["rows"]; BY = {r["slug"]: r for r in ROWS}
SITE = "https://www.leesharks.com"; PATH = "/apparatus/aggregators/"; BASE = SITE + PATH
OUT = ROOT / "apparatus/aggregators"
e = lambda s: html.escape(str(s if s is not None else ""), quote=True)
AREAS = D["areas"]; SHORT = {k: v.split(":")[0] for k, v in AREAS.items()}
BASIS = {"operator": "the resource's own statement", "third_party": "a third-party account", "reading": "the archive's reading"}
REC = [("keeps", "Whose authorship it keeps"), ("name", "Under what name"), ("holder", "Who holds it"), ("function", "Authorial function and responsibility")]
CARD = ("function", "Authorial function and responsibility")
READING = "ls_reading"
TITLE = "How authorship is made and named: a meta-aggregator"
SIB = ('<p>Its sibling census, on how literature reaches a receiving apparatus and what that apparatus makes from it, is the '
       '<a href="https://www.traininglayerliterature.org/aggregators/">Training-Layer Literature meta-aggregator</a>; the family\'s other censuses are '
       '<a href="https://www.laborvector.org/aggregators/">Labor Vector</a> (labor and AI) and <a href="https://www.maryleelabor.org/aggregators/">Mary Lee Labor</a> (left politics and labor). '
       'The rest of the apparatus wing holds the archive\'s own <a href="/provenance">provenance</a>, <a href="/rights">rights</a> and <a href="/captures">captures</a>.</p>')
LEDE = ("A census of how authorship is made, named, distributed, attributed and sustained: works and practices made with generative models, records of the "
        "writing process, attribution and identity infrastructure, reception research on how readers judge a stated or supposed author, theories of authorship "
        "under AI, heteronymous and experimental archives, and the law and policy that draw authorship's boundary. Each resource is read from its own pages, and "
        "each states what it is to this census: a direct case, a theoretical interlocutor, an empirical comparator, a historical lineage, infrastructure, a "
        "counterposition or a peripheral comparator.")
ANCHOR = ("The question comes from {a0}, which separates a distinct authorial function from the civil bearer who keeps custody and legal responsibility, and "
          "from {a1}, on the existence tax laid on real people and real work. A census that kept only names would miss most of that: how a function is "
          "constituted, how contributions are assigned, and how a work goes on through other composing agents. Revised 2026-11-01 on the operator's ruling, "
          "adopting an outside selection review. The full entity pages wait for each resource's /non article.")

src = (ROOT / "apparatus/index.html").read_text(encoding="utf-8")
SKIN = re.search(r"<style>.*?</style>", src, re.S).group(0)
GCSS = re.search(r'<link rel="stylesheet" href="/assets/gallery-type\.css[^"]*">', src).group(0)
SHEAD = re.search(r"<!-- SHELL:HEAD -->.*?<!-- /SHELL:HEAD -->", src, re.S).group(0)
SFOOT = re.search(r"<!-- SHELL:FOOT -->.*?<!-- /SHELL:FOOT -->", src, re.S).group(0)
CSS = """<style>
.agg{margin:0 auto;padding:.5em 0 2em}
.agg h1{font-variant:small-caps;font-weight:normal;letter-spacing:.14em;text-align:center;line-height:1.2;margin:.6em 0 .4em}
.agg h2{font-variant:small-caps;letter-spacing:.1em;font-weight:normal;font-size:1.15em;color:#5a3f0e;border-bottom:1px solid rgba(90,63,14,.25);margin:1.8em 0 .5em;padding-bottom:.2em}
.agg p{line-height:1.6}
.agg .fam{font-family:'PlexMono',Consolas,monospace;font-size:.66rem;letter-spacing:.13em;text-transform:uppercase;color:#5a3f0e;text-align:center}
.agg p.fam{text-align:left}
.agg .q{font-size:1.08em;border-left:2px solid #7d5e1a;padding:.3em .9em;margin:1.2em 0;background:rgba(125,94,26,.07)}
.agg .card{border-top:1px solid rgba(90,63,14,.2);padding:.7em 0 .8em}
.agg .card h3{margin:0;font-size:1.05em;font-weight:normal}
.agg .card .k{font-family:'PlexMono',Consolas,monospace;font-size:.64rem;letter-spacing:.05em;color:#5a3f0e;margin:.15em 0 .3em}
.agg .card .ls{font-size:.94em;margin-top:.35em}
.agg .chip{display:inline-block;font-family:'PlexMono',Consolas,monospace;font-size:.6rem;letter-spacing:.05em;border:1px solid rgba(90,63,14,.35);border-radius:9px;padding:0 .6em;margin:0 .3em .2em 0;color:#5a3f0e}
.agg .chip.live{border-color:#2f5d3a;color:#2f5d3a}.agg .chip.dead{color:#8a7448}
.agg table{border-collapse:collapse;width:100%;font-size:.92em;margin:1em 0}.agg td,.agg th{border-top:1px solid rgba(90,63,14,.18);padding:.42em .5em;vertical-align:top;text-align:left}
.agg th{width:30%;font-weight:normal;font-variant:small-caps;letter-spacing:.05em;color:#5a3f0e}
.agg ul{line-height:1.6;margin-top:.4em;padding-left:1.2em}.agg li{margin:.25em 0}
.agg .ev{font-size:.88em}.agg .ev li{margin:.55em 0}.agg .ev q{font-style:italic}
.agg .src{font-family:'PlexMono',Consolas,monospace;font-size:.62rem;color:#5a3f0e;word-break:break-all}
.agg .neg li{color:#7a2a17}
.agg input[type=search]{width:100%;padding:.45em .6em;border:1px solid rgba(90,63,14,.35);background:rgba(255,250,235,.7);font:inherit;margin:.6em 0 1em}
.agg a{overflow-wrap:anywhere}
.agg h2+.card{border-top:0}
</style>"""
def lst(v):
    return "; ".join(str(x) for x in v) if isinstance(v, list) else (v or "")


HR_HEAD = [("direct case", "Direct cases"), ("theoretical interlocutor", "Theoretical interlocutors"), ("empirical comparator", "Empirical comparators"),
           ("infrastructure", "Infrastructure"), ("historical lineage", "Historical lineage"), ("meta-aggregation", "Meta-aggregation"),
           ("counterposition", "Counterpositions"), ("peripheral comparator", "Peripheral comparators")]


def chips(r):
    st = (r.get("lifecycle") or {}).get("state", ""); c = {"active": "live", "ended": "dead"}.get(st, "")
    return (f'<span class="chip">{e(r["host_relation"])}</span>' if r.get("host_relation") else "") + "".join(f'<span class="chip">{e(SHORT.get(a, a))}</span>' for a in r["areas"]) + (f'<span class="chip {c}">{e(st)}</span>' if st else "")


def card(r):
    v = (r.get("record") or {}).get(CARD[0], "")
    return (f'<div class="card" data-s="{e((r["name"] + " " + " ".join(r.get("aka") or []) + " " + r["kind"] + " " + r["operator"]).lower())}">'
            f'<h3><a href="{PATH}{e(r["slug"])}">{e(r["name"])}</a></h3><div class="k">{e(r["kind"])} · {e(r["operator"])}</div>'
            f'<div>{chips(r)}</div><div class="ls"><strong>{e(CARD[1])}:</strong> {e(v)}</div></div>')


def page(path, title, desc, body, ld):
    return ('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>{e(title)} — Lee Sharks</title>\n<meta name="description" content="{e(desc)}">\n<link rel="canonical" href="{SITE}{path}">\n'
            '<link rel="icon" href="/favicon.ico">\n' + GCSS + '\n'
            f'<script type="application/ld+json">{ld}</script>\n{SKIN}\n{CSS}\n</head><body data-depth="1">\n'
            f'{SHEAD}<main class="agg">{body}</main>\n'
            f'<p class="cap">LEE SHARKS · APPARATUS · META-AGGREGATOR · {e(D["family"]).upper()} · COMPILED {e(D["compiled"])} · CC BY 4.0</p>\n'
            '<a class="back" href="/apparatus">← APPARATUS</a>' + SFOOT + '\n</body></html>\n')


def anchors():
    a = D["anchor"]["deposits"]
    return [f'<a href="{e(x["url"])}"><em>{e(x["title"])}</em></a> ({e(x["axn"])}, #{x["deposit"]})' for x in a]


def field_html():
    F = D.get("field") or []
    if not F:
        return ""
    names = {}
    for x in F:
        f = ROOT / ("data/authorship-census" if (ROOT / "data/authorship-census").exists() else "data/layer-census") / "rows" / (x["slug"] + ".py")
        got = []
        if f.exists():
            exec(compile(f.read_text(encoding="utf-8"), str(f), "exec"), {"row": lambda **r: got.append(r), "Q": lambda *a, **k: None})
        names[x["slug"]] = (got[0]["name"], got[0].get("url")) if got else (x["slug"], None)
    def li(x):
        n, u = names[x["slug"]]
        return f'<li><a href="{e(u)}">{e(n)}</a>: {e(x["why"])}</li>' if u else f'<li>{e(n)}: {e(x["why"])}</li>'
    li = "".join(li(x) for x in F)
    return ('<section class="area"><h2>The field it maps</h2><p>Works, papers, practices, tools and standards read for this census and held outside it, '
            'because none of them gathers and holds the works or records of others. They are what the aggregators above hold or miss, and the readings cite them. '
            f'{e(D.get("admission_rule") or "")}</p><ul>{li}</ul></section>')


def index():
    groups = []
    quoted = lambda r: any((v.get("quote") or "").strip() for v in (r.get("evidence") or {}).values())
    held = [r for r in ROWS if not quoted(r) or not r.get("areas")]
    for hr, head in HR_HEAD:
        rs = [r for r in ROWS if quoted(r) and r.get("areas") and r.get("host_relation") == hr]
        if not rs: continue
        groups.append(f'<section class="area"><h2>{e(head)}</h2>' + "".join(card(r) for r in rs) + "</section>")
    a0, a1 = anchors()
    un = D.get("unread_sources") or {}
    unread = ("<p>Pages that could not be read on fetch, each recorded with its status, and their fields left unquoted: "
              + "; ".join(f'{e(k)} (http {e(v["http"])})' for k, v in sorted(un.items())) + ".</p>") if un else ""
    hl = ("<p>Resources listed and held for the next batch, none of whose pages could be read on fetch, so nothing of theirs is quoted: "
          + "; ".join(f'<a href="{PATH}{e(r["slug"])}">{e(r["name"])}</a>' for r in held) + ".</p>") if held else ""
    pend = D.get("pending") or []
    if pend:
        hl += "<p>Selected and not yet listed, their pages refused on fetch: " + "; ".join(f'{e(x["name"])} ({e(x["why"])})' for x in pend) + ".</p>"
    body = (f'<div class="fam">{e(D["family"])}</div><h1>{e(TITLE)}</h1>'
            f'<p>{LEDE} Every field is quoted from a saved copy of the resource\'s own pages, with the date read and a hash of the copy. Compiled {e(D["compiled"])}; editor Lee Sharks.</p>'
            f'<div class="q"><strong>The census asks of each resource:</strong> {e(D["organizing_question"])}</div>'
            f'<p>{ANCHOR.format(a0=a0, a1=a1)}</p>{SIB}'
            f'<input type="search" id="q" placeholder="Search {len(ROWS)} resources" aria-label="Search the resources">'
            + "".join(groups)
            + field_html() + f'<section class="area"><h2>The census as data</h2>{hl}{unread}<p><a href="{PATH}census.json">census.json</a> (schema {e(D["schema_version"])}). {e(D["schema_note"])}</p></section>'
            "<script>(function(){var q=document.getElementById('q'),C=[].slice.call(document.querySelectorAll('.card'));q.addEventListener('input',function(){var t=q.value.toLowerCase();C.forEach(function(c){c.style.display=(!t||c.getAttribute('data-s').indexOf(t)>-1)?'':'none'})})})();</script>")
    ld = {"@context": "https://schema.org", "@type": "Dataset", "@id": BASE + "#census", "name": D["name"], "description": D["organizing_question"],
          "url": BASE, "dateModified": D["compiled"], "license": "https://creativecommons.org/licenses/by/4.0/",
          "creator": {"@type": "Person", "name": "Lee Sharks", "identifier": "https://orcid.org/0009-0000-1599-0703"},
          "isBasedOn": [{"@type": "CreativeWork", "name": x["title"], "url": x["url"], "identifier": x["axn"]} for x in D["anchor"]["deposits"]],
          "distribution": {"@type": "DataDownload", "encodingFormat": "application/json", "contentUrl": BASE + "census.json"},
          "hasPart": [{"@type": "WebPage", "@id": BASE + r["slug"], "name": r["name"], "url": BASE + r["slug"]} for r in ROWS]}
    return page(PATH.rstrip("/"), TITLE, D["organizing_question"], body, json.dumps(ld, ensure_ascii=False).replace("</", "<\\/"))


def kv(d):
    return "; ".join(f"{k}: {v}" for k, v in d.items()) if isinstance(d, dict) else lst(d)


def rel_li(x):
    t = x.get("target")
    if t in BY: tgt = f'<a href="{PATH}{e(t)}">{e(BY[t]["name"])}</a>'
    elif x.get("url"): tgt = f'<a href="{e(x["url"])}">{e(x.get("label") or t or x["url"])}</a>'
    else: tgt = e(x.get("label") or t or "")
    return f'<li>{e(x["rel"])}: {tgt}' + (f' ({e(x["note"])})' if x.get("note") else "") + "</li>"


def rec_page(r):
    rec = r.get("record") or {}
    rows = [("Relation to this census", r.get("host_relation")), ("Record type", r.get("record_type")), ("The question it answers", r.get("question")), ("Kind", r["kind"]), ("Operator", r["operator"]), ("Evidence", lst(r.get("evidence_kind"))), ("Unit of record", r["unit"]), ("What it records", r["record_object"])]
    rows += [(lab, rec.get(k)) for k, lab in REC]
    rows += [("Method", r.get("method")), ("Coverage", kv(r.get("coverage") or {})), ("Count", kv(r.get("count") or {})), ("Holdings", lst(r.get("holdings"))),
             ("Stated limits", lst(r.get("stated_limits"))), ("Data access", r.get("data_access")), ("Licence", r.get("license")),
             ("Lifecycle", kv(r.get("lifecycle") or {})), ("Version and time", kv(r.get("version_and_time") or {})), ("Founded", r.get("founded"))]
    tbl = "<table>" + "".join(f"<tr><th>{e(k)}</th><td>{e(v)}</td></tr>" for k, v in rows if v) + "</table>"
    ans = (f'<h2>What its record can settle</h2><ul>' + "".join(f"<li>{e(x)}</li>" for x in r.get("answers") or []) + "</ul>"
           f'<h2>What it cannot settle</h2><ul>' + "".join(f"<li>{e(x)}</li>" for x in r.get("does_not_answer") or []) + "</ul>")
    neg = ('<h2>Kept apart</h2><ul class="neg">' + "".join(f"<li>{e(x)}</li>" for x in r["negative_tags"]) + "</ul>") if r.get("negative_tags") else ""
    ev = '<h2 id="evidence">Evidence</h2><ul class="ev">'
    for f, v in (r.get("evidence") or {}).items():
        s = r["sources"].get(v["src"], {})
        if not (v.get("quote") or "").strip():
            ev += f'<li><strong>{e(f)}</strong>: unread. <div class="src"><a href="{e(s.get("url"))}">{e(s.get("url"))}</a> · fetched {e(s.get("read"))} · http {e(s.get("http"))}</div></li>'; continue
        ev += (f'<li><strong>{e(f)}</strong> ({e(BASIS.get(v.get("basis"), v.get("basis")))}): <q>{e(v.get("quote"))}</q>'
               f'<div class="src"><a href="{e(s.get("url"))}">{e(s.get("url"))}</a> · read {e(s.get("read"))} · http {e(s.get("http"))} · sha256 {e((s.get("sha256") or "")[:16])}…</div></li>')
    ev += "</ul>"
    rel = ("<h2>Relations</h2><ul>" + "".join(rel_li(x) for x in r["relations"]) + "</ul>") if r.get("relations") else ""
    unc = ("<h2>Unchecked</h2><p>" + e(lst(r.get("unchecked"))) + "</p>") if r.get("unchecked") else ""
    body = (f'<p class="fam"><a href="{PATH}">{e(TITLE)}</a> / {e(r["name"])}</p><h1>{e(r["name"])}</h1>'
            f'<p><a href="{e(r["url"])}">{e(r["url"])}</a></p><div>{chips(r)}</div>'
            f'<div class="q"><strong>The archive\'s reading.</strong> {e(r[READING])}</div>' + tbl + ans + neg + rel + ev + unc
            + f'<p class="src">Cite: Lee Sharks, ed. "{e(r["name"])}." {e(TITLE)}, leesharks.com, compiled {e(D["compiled"])}. {BASE}{e(r["slug"])}</p>')
    ent = {"@id": BASE + r["slug"] + "#entity", "@type": "CreativeWork", "name": r["name"], "alternateName": r.get("aka", []), "url": r["url"],
           "creator": {"@type": "Organization", "name": r["operator"]}}
    recd = {"@id": BASE + r["slug"], "@type": "WebPage", "name": f'{r["name"]}: Lee Sharks apparatus meta-aggregator record', "about": {"@id": ent["@id"]},
            "mainEntity": {"@id": ent["@id"]}, "dateModified": D["compiled"], "isPartOf": {"@id": BASE + "#census"},
            "editor": {"@type": "Person", "name": "Lee Sharks", "identifier": "https://orcid.org/0009-0000-1599-0703"},
            "citation": [s["url"] for s in r["sources"].values()], "license": "https://creativecommons.org/licenses/by/4.0/"}
    ld = json.dumps({"@context": "https://schema.org", "@graph": [recd, ent]}, ensure_ascii=False).replace("</", "<\\/")
    return page(f"{PATH}{r['slug']}", r["name"], r[READING][:200], body, ld)


OUT.mkdir(exist_ok=True)
(OUT / "index.html").write_text(index(), encoding="utf-8")
for r in ROWS:
    d = OUT / r["slug"]; d.mkdir(exist_ok=True)
    (d / "index.html").write_text(rec_page(r), encoding="utf-8")
shutil.copy(ROOT / "data/authorship-census/census.json", OUT / "census.json")
print(f"aggregators: index + {len(ROWS)} record pages + census.json")
