# Hachemicals — build & go-live notes

Static site generated from HA International Chemicals' own WordPress data.
No framework, no npm — Python 3 and Pillow only.

---

## Build

```bash
python3 build.py                 # concept build  — noindex, GitHub Pages URL
python3 build.py --production    # live build     — indexable, hachemicals.com
```

Output goes to `site/`. **Always use `--production` for anything served from
hachemicals.com**, and never for the shareable concept — the concept is
deliberately `noindex` so it can't compete with the client's own domain for
their own content.

| | concept (default) | `--production` |
|---|---|---|
| `<meta name="robots">` | `noindex,nofollow` | `index,follow` |
| canonical / OG / schema URLs | github.io | hachemicals.com |
| `robots.txt` | `Disallow: /` | allow all + AI crawlers |

### Regenerating from scratch

```bash
python3 scrape_bg_images.py   # CSS background images the src= scrape missed
python3 assets.py             # build_src/img/* -> assets/img/*.webp (67MB -> 2MB)
python3 extract_content.py    # verbatim services copy + real counter values
python3 build.py --production
```

`build_src/` is git-ignored (68 MB of originals). It is fully reproducible from
the two scrape scripts, so it does not belong in the repo.

---

## Going live on WordPress

The plan is to replace the current theme output with this markup. Options, best
first:

1. **Static export served by the host, WordPress kept for admin only.** Fastest
   and keeps every SEO gain. Needs host-level control of the document root.
2. **Convert to a minimal WordPress theme.** `styles.css` and `script.js` drop in
   as-is; the page templates become PHP. Products map to the existing
   WooCommerce post type, so `build.py:ROOMS`-style data is replaced by
   `WP_Query`.
3. **Paste per-page into Elementor as HTML widgets.** Quickest, but the theme
   keeps injecting its own CSS and you lose much of the performance win. Not
   recommended.

### Must-do at cutover

- [ ] Build with `--production`
- [ ] Copy `sitemap.xml`, `robots.txt`, `llms.txt` to the **domain root**
      (`hachemicals.com/robots.txt` — a subdirectory copy does nothing)
- [ ] Confirm no SEO plugin (Yoast/RankMath) is emitting a second, conflicting
      `robots` meta or canonical — duplicates cancel each other out
- [ ] Redirect old URLs. Current product URLs are
      `/shop/chemicals/<slug>/`; this build uses `/product/<slug>.html`.
      **Either match their existing structure or 301 every old URL** — getting
      this wrong drops existing rankings
- [ ] Submit sitemap to **Google Search Console** *and* **Bing Webmaster Tools**
      (ChatGPT search runs on Bing — this is the commonly missed one)
- [ ] Validate schema at <https://search.google.com/test/rich-results>

---

## Post-launch SEO — the part that actually drives AI visibility

Structured data makes the site *understandable*. Being found is a separate job:

1. **Google Business Profile** for the Abu Dhabi address — biggest single lever
   for a local B2B supplier.
2. **Consistent NAP** (name, address, phone) everywhere it appears online.
   Inconsistency splits the entity and weakens all of it.
3. **UAE / industry directory listings.** Models weight a claim far higher when
   it's corroborated off the company's own domain.
4. **Query-shaped content.** Long-tail wins here: "cenosphere supplier Abu
   Dhabi" is winnable; "chemical supplier UAE" is not. The 26 product pages are
   26 separate entry points — that's the strategy.
5. Expect **months, not days**. Indexing takes days-to-weeks, ranking longer.

---

## Known issues on the client's live site

Verified against hachemicals.com — worth fixing regardless of this rebuild.

| Issue | Detail |
|---|---|
| Statistics render as `0` | Chain of Factories (176), Projects Completed (800), Expert Engineers (230), Construction (78%), Building (36%) all set correctly but display as zero — the scroll animation never fires |
| Template demo text | About page reads "Get to Know **Austry**" and "**Austry** Feedbacks". Austry is the theme's demo company |
| Contradictory experience claim | Homepage says 38 years / "four decades"; About counter says 18 |
| Nothing is purchasable | All 26 products are `price: 0`, `is_purchasable: false` |
| Two products uncategorised | Ferric Chloride and Calcium Chloride 94–97 % sit outside the Chemicals category and are missing from category browsing |
| Product copy carries pasted styling | 122 instances of authoring-tool CSS classes in descriptions, rendering tables unstyled |
| Empty sections | "What they're saying?" testimonials and "Our Experts Contractors" are headings with no content |
| Likely product-name typo | "Drilling **Strach**" — searches for "drilling starch" won't match |

---

## Open decisions

- **Public pricing vs quote-only.** Quote-only is normal for B2B chemicals and
  is materially less work than full checkout. Decide before building payments.
- **Payment gateway.** Telr / PayTabs / Network International (N-Genius) /
  Stripe / Amazon Payment Services are the realistic UAE options. Requires trade
  licence, corporate bank account, VAT registration (UAE VAT is 5 %).
  ⚠️ **Register the domain in the gateway dashboard at setup** — an unregistered
  domain is exactly what silently broke payments on the Lakefront project.
- **Chemical services missing.** The services page lists five *electrical*
  services and no chemical services, despite this being a chemicals trading
  company with 21 chemicals in the catalogue.

---

## File map

| File | Purpose |
|---|---|
| `build.py` | Page generator. `PRODUCTION` flag, schema, sitemap/robots/llms |
| `styles.css` | Brand palette, layout, motion, ripple |
| `script.js` | Ripple, scroll reveals, counters, hero slider, nav |
| `assets.py` | WebP pipeline |
| `scrape_bg_images.py` | Fetches CSS background images |
| `extract_content.py` | Pulls verbatim services copy + real counter values |
| `clean_html.py` | Strips pasted styling from product descriptions |
| `src_data/*.json` | Scraped source of truth |
