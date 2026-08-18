#!/usr/bin/env python3
"""apply_shell.py — stamps the shared shell (plaque, nav, foot) onto pages.

The shell is declared ONCE in scripts/shell-manifest.json and propagated by
this script between markers. Idempotent: re-running replaces marker blocks.
No page hand-edits its shell. This is leesharks gate zero.
"""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
M = json.load(open(ROOT/'scripts/shell-manifest.json'))

def nav_html(current_path):
    parts = []
    for href, label in M['nav']:
        cur = ' aria-current="page"' if ('/'+current_path.split('/')[0]+'/' == href) else ''
        parts.append(f'<a href="{href}"{cur}>{label}</a>')
    return '<nav class="shell-nav">' + ' '.join(parts) + '</nav>'

def head_block(page_path):
    return ('<!-- SHELL:HEAD -->'
            f'<div class="shell-plaque">{M["plaque"]}</div>'
            f'{nav_html(page_path)}'
            '<!-- /SHELL:HEAD -->')

FOOT = ('<!-- SHELL:FOOT -->'
        '<div class="shell-foot">'
        f'<div class="colophon-mini">{M["colophon_mini"]}</div>'
        '<div class="ember"></div>'
        '</div>'
        '<!-- /SHELL:FOOT -->')

def stamp(rel, depth):
    p = ROOT/rel
    s = p.read_text()
    orig = s
    # ensure the shared css is linked
    if 'gallery-type.css' not in s:
        s = s.replace('</title>', '</title>\n<link rel="stylesheet" href="/assets/gallery-type.css">', 1)
    # body carries its depth
    s = re.sub(r'<body(?![^>]*data-depth)([^>]*)>', f'<body data-depth="{depth}"\\1>', s, count=1)
    s = re.sub(r'(<body[^>]*data-depth=")\d+(")', f'\\g<1>{depth}\\g<2>', s, count=1)
    # retire page-local flat grounds so the depth theme governs
    s = re.sub(r'background:#efe6d0;?', '', s)
    # head block: replace existing or insert after <body...>
    hb = head_block(rel)
    if '<!-- SHELL:HEAD -->' in s:
        s = re.sub(r'<!-- SHELL:HEAD -->.*?<!-- /SHELL:HEAD -->', hb, s, flags=re.S)
    else:
        s = re.sub(r'(<body[^>]*>)', '\\1\n'+hb, s, count=1)
    # foot block: depth 0 keeps its grand footer; interiors get the shell foot
    if depth == 0:
        s = re.sub(r'<!-- SHELL:FOOT -->.*?<!-- /SHELL:FOOT -->\n?', '', s, flags=re.S)
    elif '<!-- SHELL:FOOT -->' in s:
        s = re.sub(r'<!-- SHELL:FOOT -->.*?<!-- /SHELL:FOOT -->', FOOT, s, flags=re.S)
    else:
        s = s.replace('</body>', FOOT+'\n</body>')
    if s != orig:
        p.write_text(s)
        return True
    return False

if __name__ == '__main__':
    changed = []
    for pg in M['pages']:
        if stamp(pg['path'], pg['depth']):
            changed.append(pg['path'])
    print('stamped:', changed or 'nothing (all current)')
