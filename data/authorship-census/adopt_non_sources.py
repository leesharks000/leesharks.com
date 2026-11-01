"""Adopt the /non composers' fetched field sources into the leesharks.com authorship census (2026-11-01): each B<n>.txt of a row's intake
that its field ledger records as fetched with HTTP 200, and whose text the census has not already saved, is copied to
sources/<census slug>--non-<B>.txt and entered in sources/manifest.json, marked adopted, with the /non row, the file's sha256 and the URL the
field ledger gives. Census corrections may then quote them under the census's verbatim check."""
import json, pathlib, re, hashlib, shutil, sys
AX = pathlib.Path("/home/claude/alexanarch"); V = AX / "datasets/negative-of-the-negative/v2"
C = pathlib.Path("/home/claude/fleet/leesharks.com/data/authorship-census")
MAP = {"the-next":"the-next","electronic-literature-lab":"electronic-literature-lab","output-anthology":"output-anthology","wordcraft":"wordcraft",
 "coauthor":"coauthor","in2writing":"in2writing","creative-ai-lab-database":"creative-ai-lab-database","orcid":"orcid-names","isni":"isni",
 "viaf":"viaf","wikidata":"wikidata","arquivo-pessoa":"arquivo-pessoa","pessoa-digital":"pessoa-digital","ubuweb":"ubuweb","pennsound":"pennsound",
 "electronic-poetry-center":"epc","jacket2":"jacket2","eclipse":"eclipse","international-dada-archive":"dada-iowa","copyright-office-ai":"copyright-office-ai",
 "dail":"gwu-dail","chatgpt-eating-the-world":"chatgpt-eating-the-world","authors-guild-human-authored":"authors-guild-human-authored"}
AXN = {k: e.get("axn") for k, e in json.load(open(V / "axn.json"))["entries"].items()}
def norm(x): return re.sub(r"\s+", " ", x).strip()
def code_of(f):
    fe = f.get("fetched")
    if isinstance(fe, dict):
        if fe.get("unreachable"): return "unreachable"
        c = fe.get("http")
        if c is None and fe.get("tries"): c = fe["tries"][-1].get("http")
        return str(c)
    s = str(fe or "")
    if "unreachable" in s: return "unreachable"
    m = re.search(r"HTTP (\d{3})", s)
    return m.group(1) if m else "none"
man = json.load(open(C / "sources/manifest.json"))
census_txt = {}
for k, v in man.items():
    p = C / "sources" / f"{k}.txt"
    if not v.get("adopted") and p.exists(): census_txt.setdefault(v.get("entity"), []).append(norm(p.read_text(encoding="utf-8", errors="replace")))
added = 0; per = {}; skipped = []
for row, cs in MAP.items():
    led = json.load(open(V / "ledgers" / row / "field.json")); intake = next((V / "intake").glob(f"{row}-2026*"))
    for f in led["field"]:
        b = f["id"]; t = intake / f"{b}.txt"
        if not t.exists(): continue
        txt = t.read_text(encoding="utf-8", errors="replace")
        c = code_of(f)
        if c != "200" or len(txt.strip()) < 100 or "no article" in str(f.get("card") or "") + str(f.get("kind") or ""):
            skipped.append((cs, b, c)); continue
        if norm(txt) in census_txt.get(cs, []):
            skipped.append((cs, b, "census copy")); continue
        url = f.get("url") if f.get("url") not in (None, "None") else None
        if not url and isinstance(f.get("fetched"), dict): url = f["fetched"].get("url")
        if not url: url = (re.search(r"https?://[^\s,;)]+", str(f.get("fetched") or "")) or [None])[0]
        sid = f"{cs}--non-{b}"
        shutil.copyfile(t, C / "sources" / f"{sid}.txt")
        man[sid] = {"entity": cs, "id": f"non-{b}", "url": url or f"https://www.alexanarch.org/non/{row}/", "final_url": url or "", "http": "200",
                    "content_type": "text/plain", "fetched": "2026-11-01T00:00:00Z", "sha256": hashlib.sha256(t.read_bytes()).hexdigest(),
                    "bytes": t.stat().st_size, "text_chars": len(txt), "error": "",
                    "adopted": {"from": f"alexanarch.org /non row {row} ({AXN.get(row)}), its field source {b}", "path": str(t.relative_to(AX)),
                                "card": f.get("card") or f.get("kind"), "origin": f.get("origin"), "pool": f.get("pool")}}
        added += 1; per.setdefault(cs, []).append(b)
if "--write" in sys.argv: json.dump(man, open(C / "sources/manifest.json", "w"), ensure_ascii=False, indent=1)
print(added, "adopted;", len(skipped), "skipped")
for k, v in per.items(): print(" ", k, v)
print("skipped:", skipped)
