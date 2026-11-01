"""Entity articles for the apparatus authorship meta-aggregator, derived from the /non articles (EA-NEGONT-02 v0.10, #1726) on the operator's
ruling of 2026-11-01 ("then come back and flesh out the single pages"). Written in six parts, data/authorship-census/articles-a.py to -f.py,
each checked by /home/claude/fleet/tools/check_articles.py (every figure in a paragraph occurs in the KO sentences it cites). This module merges them."""
import pathlib, runpy
_D = pathlib.Path(__file__).resolve().parents[2] / "data/authorship-census"
ARTICLES = {}
for _p in sorted(_D.glob("articles-*.py")):
    ARTICLES.update(runpy.run_path(str(_p))["ARTICLES"])
