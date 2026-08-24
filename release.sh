#!/usr/bin/env bash
# Produce the deployable production build.
#
# Run this only on client greenlight. It writes to release/ — never to site/ or
# docs/, because docs/ is served publicly by GitHub Pages and must stay noindex.
set -euo pipefail

cd "$(dirname "$0")"
OUT="release"

echo "==> refreshing source assets"
python3 scrape_bg_images.py
python3 assets.py
python3 extract_content.py

echo
echo "==> building for hachemicals.com (indexable)"
python3 build.py --production

rm -rf "$OUT"
cp -r site "$OUT"

# put the concept build back so the repo is never left holding an indexable
# copy that could be committed into docs/ by accident
python3 build.py >/dev/null
rm -rf docs && cp -r site docs

echo
echo "==> verifying $OUT"
fail=0
grep -q 'content="index,follow' "$OUT/index.html" \
  || { echo "  FAIL: pages are not indexable"; fail=1; }
grep -q 'https://hachemicals.com' "$OUT/sitemap.xml" \
  || { echo "  FAIL: sitemap not pointing at the live domain"; fail=1; }
grep -q '^Sitemap: https://hachemicals.com/sitemap.xml' "$OUT/robots.txt" \
  || { echo "  FAIL: robots.txt missing sitemap line"; fail=1; }
grep -q 'Disallow: /' "$OUT/robots.txt" \
  && { echo "  FAIL: robots.txt still blocking crawlers"; fail=1; }
[ "$(grep -c '<loc>' "$OUT/sitemap.xml")" -eq 40 ] \
  || { echo "  FAIL: expected 40 sitemap URLs"; fail=1; }
grep -q 'noindex' "docs/index.html" \
  || { echo "  FAIL: docs/ is not noindex — do not push"; fail=1; }

[ "$fail" -eq 0 ] && echo "  all checks passed" || { echo; echo "BUILD NOT SAFE TO SHIP"; exit 1; }

cat <<'NEXT'

==> ready: ./release

Deploy that folder, then:
  1. sitemap.xml / robots.txt / llms.txt must sit at the DOMAIN ROOT
  2. disable any SEO plugin emitting a second robots meta or canonical
  3. check existing product permalinks still resolve
  4. set real prices, or switch the catalogue to quote-only
  5. submit the sitemap to Google Search Console AND Bing Webmaster Tools
  6. validate schema: https://search.google.com/test/rich-results

Full detail in HANDOVER.md
NEXT
