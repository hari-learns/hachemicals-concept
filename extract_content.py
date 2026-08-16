#!/usr/bin/env python3
"""Pull the real page copy out of the scraped WordPress content and write it
to src_data/content.json.

The first build invented six services that don't exist on their site. Their
site has exactly five, each with substantial copy that must survive verbatim.
"""
import json
import os
import re
from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.abspath(__file__))
PAGES = json.load(open(os.path.join(ROOT, "src_data/pages.json")))

SERVICE_TITLES = [
    "Electrical installation",
    "Earthing systems",
    "Cathodic protection",
    "ELV installation",
    "Telecommunication installation",
]


def text_blocks(html):
    """Flatten to (heading_or_none, [paragraphs]) in document order."""
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style"]):
        tag.decompose()
    return soup


def extract_services():
    """Each service title is followed by its paragraphs until the next title."""
    soup = text_blocks(PAGES["services"])
    # collect every text-bearing node in order
    nodes = []
    for el in soup.find_all(["h1", "h2", "h3", "h4", "h5", "p", "span", "div"]):
        if el.find(["p", "h1", "h2", "h3", "h4", "h5"]):
            continue  # container, not a leaf
        txt = el.get_text(" ", strip=True)
        if txt:
            nodes.append(txt)

    # dedupe consecutive repeats (Elementor duplicates nodes for responsive variants)
    clean = []
    for t in nodes:
        if not clean or clean[-1] != t:
            clean.append(t)

    services = []
    idx = {}
    for i, t in enumerate(clean):
        for title in SERVICE_TITLES:
            if t == title and title not in idx:
                idx[title] = i

    ordered = sorted(idx.items(), key=lambda kv: kv[1])
    for n, (title, start) in enumerate(ordered):
        end = ordered[n + 1][1] if n + 1 < len(ordered) else len(clean)
        paras = []
        for t in clean[start + 1:end]:
            # real copy is long-form; skip nav crumbs and stray labels
            if len(t) < 60:
                continue
            if t not in paras:
                paras.append(t)
        services.append({"title": title, "paragraphs": paras})
    return services


def main():
    services = extract_services()
    data = {
        "services": services,
        "services_intro": {
            "eyebrow": "Explore Our Solutions",
            "heading": "Innovative Solutions to Meet Every Need",
            "lede": (
                "At HA International Chemicals Trading LLC, we offer a wide selection "
                "of high-quality chemicals suitable for many industries. From industrial "
                "solutions to specialty products, our range is crafted to enhance your "
                "operations and fuel your success."
            ),
        },
        # real values from their Elementor markup — the live site renders these as 0
        # because the scroll-triggered counter never fires
        "counters": [
            {"label": "Chain of Factories", "value": 176},
            {"label": "Projects Completed", "value": 800},
            {"label": "Expert Engineers", "value": 230},
        ],
        "progress": [
            {"label": "Construction", "value": 78},
            {"label": "Building", "value": 36},
        ],
        "years_experience": 18,
    }
    out = os.path.join(ROOT, "src_data/content.json")
    json.dump(data, open(out, "w"), indent=2)

    for s in services:
        words = sum(len(p.split()) for p in s["paragraphs"])
        print(f"  {s['title']:<32} {len(s['paragraphs'])} para, {words} words")
    print(f"\n-> {out}")


if __name__ == "__main__":
    main()
