#!/usr/bin/env python3
"""Image pipeline: build_src/img/*  ->  assets/img/*.webp

Several source photos ship at 5-10 MB straight from the WordPress media
library, which is unusable on a real page. Everything gets capped, converted
to WebP, and product cut-outs keep their transparency.
"""
import os
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "build_src/img")
OUT = os.path.join(ROOT, "assets/img")

# name -> (max_width, quality). Wide photographic backgrounds get more width,
# product cut-outs stay square-ish and small.
WIDE = 2000
HERO_Q = 80
DEFAULT = 1000
DEFAULT_Q = 82

OVERRIDES = {
    "environmental-pollution-factory-exterior-night": (WIDE, HERO_Q),
    "distant-shot-port-with-boats-loaded-with-cargo-shipment-during-nighttime": (WIDE, HERO_Q),
    "safety-training-chemical-handling-procedures": (1600, HERO_Q),
    "img_bg_business_Home01-STE4HQX-e1686194116880": (1400, HERO_Q),
    "img_about_Home01-7DPAR8H": (1200, 82),
}

# the seven large facility photographs
FACILITY_PREFIX = "710_"
FACILITY = (1600, 80)

SKIP = {"woocommerce-placeholder"}


def target_for(stem):
    if stem in OVERRIDES:
        return OVERRIDES[stem]
    if stem.startswith(FACILITY_PREFIX):
        return FACILITY
    return (DEFAULT, DEFAULT_Q)


def main():
    os.makedirs(OUT, exist_ok=True)
    saved = skipped = 0
    before = after = 0

    for fname in sorted(os.listdir(SRC)):
        stem, ext = os.path.splitext(fname)
        if ext.lower() not in {".jpg", ".jpeg", ".png", ".webp", ".avif"}:
            continue
        if stem in SKIP:
            skipped += 1
            continue

        src_path = os.path.join(SRC, fname)
        if os.path.getsize(src_path) == 0:
            print(f"  skip {fname} (empty file)")
            skipped += 1
            continue

        try:
            im = Image.open(src_path)
        except Exception as exc:
            print(f"  FAIL {fname}: {exc}")
            skipped += 1
            continue

        max_w, quality = target_for(stem)

        # keep alpha for product cut-outs / logos, flatten photos to RGB
        has_alpha = im.mode in ("RGBA", "LA") or (
            im.mode == "P" and "transparency" in im.info
        )
        im = im.convert("RGBA" if has_alpha else "RGB")

        if im.width > max_w:
            ratio = max_w / im.width
            im = im.resize((max_w, round(im.height * ratio)), Image.LANCZOS)

        dest = os.path.join(OUT, stem + ".webp")
        im.save(dest, "WEBP", quality=quality, method=6)

        before += os.path.getsize(src_path)
        after += os.path.getsize(dest)
        saved += 1

    mb = lambda n: n / (1024 * 1024)
    print(f"\n{saved} images -> {OUT}  ({skipped} skipped)")
    print(f"{mb(before):.1f} MB  ->  {mb(after):.1f} MB "
          f"({100 - after / before * 100:.0f}% smaller)")


if __name__ == "__main__":
    main()
