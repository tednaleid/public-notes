#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# ///
# ABOUTME: Checks a chunk-written HTML page: no leftover sentinel, no em-dashes, every SVG parses.
# ABOUTME: Usage: scripts/check_page.py path/to/page.html [more.html ...]
import html, re, sys
import xml.etree.ElementTree as ET

EM_DASH = chr(0x2014)
EM_DASH_ENTITY_RE = re.compile(r"&mdash;|&#8212;|&#x2014;", re.IGNORECASE)


def check(path):
    text = open(path, encoding="utf-8").read()
    problems = []
    if "<!--CHUNK-->" in text:
        problems.append("leftover <!--CHUNK--> sentinel")
    if EM_DASH in text:
        problems.append(f"{text.count(EM_DASH)} em-dashes")
    entities = EM_DASH_ENTITY_RE.findall(text)
    if entities:
        problems.append(f"{len(entities)} em-dash entities")
    for i, svg in enumerate(re.findall(r"<svg\b.*?</svg>", text, re.DOTALL), 1):
        try:
            ET.fromstring(html.unescape(svg).replace("&", "&amp;"))
        except ET.ParseError as err:
            problems.append(f"svg #{i} does not parse: {err}")
    return problems


failed = False
for path in sys.argv[1:]:
    problems = check(path)
    failed = failed or bool(problems)
    print(f"{path}: " + ("; ".join(problems) or "clean"))
sys.exit(1 if failed else 0)
