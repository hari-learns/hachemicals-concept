#!/usr/bin/env python3
"""Fetch the CSS background-image assets the first scrape missed.

The original pass only matched src="..." attributes, so every Elementor
background image — including both hero photographs — was skipped.
"""
import os
import urllib.request

DEST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build_src/img")
BASE = "https://hachemicals.com/wp-content/uploads/"

URLS = [
    # hero slides
    BASE + "2024/03/environmental-pollution-factory-exterior-night.jpg",
    BASE + "2024/03/distant-shot-port-with-boats-loaded-with-cargo-shipment-during-nighttime.jpg",
    # section backgrounds / decor
    BASE + "2024/02/bg-3.jpg",
    BASE + "2024/02/bg-6.png",
    BASE + "2024/02/image-61.jpg",
    BASE + "2024/02/image-66.jpg",
    BASE + "2024/03/image-6.jpg",
    BASE + "2024/03/image2-6.jpg",
    BASE + "2024/02/img_bg_business_Home01-STE4HQX-e1686194116880.jpg",
    BASE + "2024/03/img_person_About-NB84JQ3.png",
    BASE + "2024/03/line-1.jpg",
    BASE + "2024/02/Icon-4.png",
    BASE + "2026/07/safety-training-chemical-handling-procedures.jpg",
]


def main():
    os.makedirs(DEST, exist_ok=True)
    ok = failed = skipped = 0
    for url in URLS:
        name = url.split("/")[-1]
        path = os.path.join(DEST, name)
        if os.path.exists(path):
            skipped += 1
            continue
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            data = urllib.request.urlopen(req, timeout=20).read()
            with open(path, "wb") as fh:
                fh.write(data)
            print(f"  got  {name}  ({len(data)//1024} KB)")
            ok += 1
        except Exception as exc:
            print(f"  FAIL {name}: {exc}")
            failed += 1
    print(f"\ndownloaded {ok}, skipped {skipped}, failed {failed}")


if __name__ == "__main__":
    main()
