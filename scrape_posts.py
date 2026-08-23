#!/usr/bin/env python3
"""Fetch the blog posts published on hachemicals.com.

The first scrape only looked at `pages`. The Blog page itself returns empty
content because it is a dynamic listing, so it read as "no posts" — but seven
articles are live, each on its own URL. This pulls them properly.
"""
import html as htmllib
import json
import os
import re
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
API = "https://hachemicals.com/wp-json/wp/v2/posts?per_page=100&_embed=1"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return json.loads(urllib.request.urlopen(req, timeout=30).read())


def plain(markup):
    return re.sub(r"\s+", " ", re.sub("<[^>]+>", " ", markup)).strip()


def main():
    posts = []
    for p in fetch(API):
        embedded = p.get("_embedded", {})
        media = embedded.get("wp:featuredmedia") or []
        image = media[0].get("source_url") if media and "source_url" in media[0] else None
        terms = embedded.get("wp:term") or []
        cats = [t["name"] for group in terms for t in group
                if t.get("taxonomy") == "category"]

        posts.append({
            "id": p["id"],
            "slug": p["slug"],
            "title": htmllib.unescape(plain(p["title"]["rendered"])),
            "date": p["date"][:10],
            "link": p["link"],
            "categories": cats,
            "image": image,
            "excerpt": htmllib.unescape(plain(p["excerpt"]["rendered"]))[:300],
            "content": p["content"]["rendered"],
        })

    posts.sort(key=lambda x: x["date"], reverse=True)
    out = os.path.join(ROOT, "src_data/posts.json")
    json.dump(posts, open(out, "w"), indent=2)

    for p in posts:
        words = len(plain(p["content"]).split())
        img = "img" if p["image"] else "no img"
        print(f"  {p['date']}  {words:>4}w  {img:>6}  {p['title'][:52]}")
    print(f"\n{len(posts)} posts -> {out}")


if __name__ == "__main__":
    main()
