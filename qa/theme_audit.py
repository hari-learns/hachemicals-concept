#!/usr/bin/env python3
"""Build the authoritative route manifest and audit the WordPress theme."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
THEME = ROOT / "theme" / "hachemicals"
OUT = ROOT / "qa" / "page-manifest.json"

REQUIRED_THEME_FILES = {
    "style.css", "functions.php", "header.php", "footer.php", "front-page.php",
    "archive-product.php", "single-product.php", "page-services.php",
    "page-electrical-technical-services.php", "page-about-us.php",
    "page-contact-us.php", "page-elementor-1264.php", "home.php", "single.php",
    "page.php", "index.php", "404.php", "inc/schema.php", "assets/js/site.js",
}


def load(name: str):
    return json.loads((ROOT / "src_data" / name).read_text(encoding="utf-8"))


def route(url: str) -> str:
    value = urlparse(url).path or "/"
    return value if value.endswith("/") else value + "/"


def build_manifest() -> list[dict[str, str]]:
    products = load("products.json")
    posts = load("posts.json")
    entries = [
        {"type": "page", "title": "Home", "wordpress_path": "/", "concept_path": "/index.html"},
        {"type": "page", "title": "Products", "wordpress_path": "/products/", "concept_path": "/products.html"},
        {"type": "page", "title": "VFD & Electrical Products", "wordpress_path": "/electrical-technical-services/", "concept_path": "/electrical-technical-services.html"},
        {"type": "page", "title": "Services", "wordpress_path": "/services/", "concept_path": "/services.html"},
        {"type": "page", "title": "About Us", "wordpress_path": "/about-us/", "concept_path": "/about-us.html"},
        {"type": "page", "title": "Blog", "wordpress_path": "/blog/", "concept_path": "/blog.html"},
        {"type": "page", "title": "Contact Us", "wordpress_path": "/contact-us/", "concept_path": "/contact-us.html"},
        {"type": "page", "title": "Free quote", "wordpress_path": "/contact-us/elementor-1264/", "concept_path": "/contact-us.html#quote"},
    ]
    entries.extend(
        {"type": "product", "title": p["name"], "wordpress_path": route(p["permalink"]), "concept_path": f"/product/{p['slug']}.html"}
        for p in products
    )
    entries.extend(
        {"type": "article", "title": p["title"], "wordpress_path": route(p["link"]), "concept_path": f"/blog/{p['slug']}.html"}
        for p in posts
    )
    return entries


def audit() -> list[str]:
    failures: list[str] = []
    products = load("products.json")
    posts = load("posts.json")
    manifest = build_manifest()

    if len(products) != 26:
        failures.append(f"expected 26 products, found {len(products)}")
    if len(posts) != 7:
        failures.append(f"expected 7 articles, found {len(posts)}")
    if len(manifest) != 41:
        failures.append(f"expected 41 manifest entries, found {len(manifest)}")

    paths = [item["wordpress_path"] for item in manifest]
    if len(paths) != len(set(paths)):
        failures.append("duplicate WordPress paths in manifest")

    missing = sorted(path for path in REQUIRED_THEME_FILES if not (THEME / path).is_file())
    if missing:
        failures.append("missing theme files: " + ", ".join(missing))

    php = "\n".join(path.read_text(encoding="utf-8") for path in THEME.rglob("*.php"))
    css = (THEME / "style.css").read_text(encoding="utf-8")
    js = (THEME / "assets/js/site.js").read_text(encoding="utf-8")
    combined = php + css + js

    required = {
        "Template: hello-elementor": css,
        "M02, United Arab Bank Building, Al Danah": php,
        "[metform form_id=\"272\"]": php,
        "[wpforms id=\"1265\"": php,
        "add_theme_support( 'woocommerce'": php,
        "aria-expanded": php + js,
        "prefers-reduced-motion": css,
    }
    for needle, haystack in required.items():
        if needle not in haystack:
            failures.append(f"required integration marker missing: {needle}")

    forbidden = [r"\bM01\b", r"Austry", r"18\s+Years"]
    for pattern in forbidden:
        if re.search(pattern, combined, flags=re.IGNORECASE):
            failures.append(f"forbidden stale content found: {pattern}")

    for match in re.finditer(r"hachemicals_asset\(\s*'img/([^']+)'", php):
        if not (THEME / "assets" / "img" / match.group(1)).is_file():
            failures.append(f"missing referenced image: {match.group(1)}")

    return failures


def main() -> int:
    manifest = build_manifest()
    OUT.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    failures = audit()
    print(f"manifest: {len(manifest)} entries -> {OUT.relative_to(ROOT)}")
    print("inventory: 8 top-level, 26 products, 7 articles")
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1
    print("theme audit: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
