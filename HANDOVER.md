# Hachemicals — build & go-live notes

Static site generated from HA International Chemicals' own WordPress data.
No framework, no npm — Python 3 and Pillow only.

---

## Status: built, verified, awaiting client greenlight

Nothing on the client's live site has been touched. The work sits in this repo
and on GitHub Pages as a private-by-obscurity preview that is deliberately
`noindex`, so it cannot compete with hachemicals.com for their own content.

**Preview:** <https://hari-learns.github.io/hachemicals-concept/>

Verified on the current production build:

| Check | Result |
|---|---|
| Pages generated | 34 (8 top-level + 26 products) |
| JSON-LD blocks | 87 valid, 0 invalid — Organization ×34, Product ×26, BreadcrumbList ×26, FAQPage ×1 |
| Titles / descriptions | unique on every page, no duplicates |
| Headings | exactly one `<h1>` per page |
| Images | `alt` on every image; 67 MB → 2 MB as WebP |
| Internal links & assets | all resolve, no 404s |
| Responsive | no horizontal overflow at 320 / 375 / 768 / 1280 / 1440 |
| Source junk | pasted styling, leaked forms and the broken payment link all stripped |
| `robots.txt` | allows Googlebot, Bingbot, GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot, Google-Extended, CCBot |
| `sitemap.xml` / `llms.txt` | generated, 33 URLs |

**On greenlight:** run `python3 build.py --production`, then work the go-live
checklist below.

⚠️ The repo is kept in **concept (noindex)** state on purpose. Never commit a
`--production` build into `docs/` — GitHub Pages serves that folder publicly and
an indexable copy would duplicate the client's own content.

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

**Recommended: convert this build into a WordPress theme.** `styles.css` and
`script.js` drop in unchanged; the page templates become PHP. Products map onto
the existing WooCommerce post type, so the `PROD` list in `build.py` is replaced
by `WP_Query` / WooCommerce template tags.

This was originally scoped as a static export with WordPress kept for admin
only. **That is no longer the right call.** The client wants to write and publish
articles herself, and a static site cannot have someone press Publish and see it
live. Everything below assumes the theme route.

Two consequences worth knowing:

- **The URL-migration risk disappears.** WordPress keeps its own permalinks, so
  `/shop/chemicals/<slug>/` and `/about-us/` survive untouched. No 301 map, no
  lost rankings. (Under a static export those paths would have had to be
  reproduced by hand — the single largest risk in the original plan.)
- **The blog works natively.** Each article gets its own URL, joins the listing
  page, and renders in this design automatically.

Rejected alternative: pasting pages into Elementor as HTML widgets. Quick, but
the theme keeps injecting its own CSS and most of the performance win is lost.

### Blog / self-publishing setup

The client publishes her own articles. Do these before she writes anything:

- [ ] **Set the permalink structure first** — `/blog/%postname%/` or similar.
      Changing this after articles exist breaks every article URL and its
      rankings. Five-minute setting, painful to undo.
- [ ] Invite her as **Editor** (publish freely, cannot touch settings, plugins
      or the theme). Use **Contributor** instead if the work should be reviewed
      before going public.
- [ ] Create categories up front — Drilling, Water Treatment, Electrical.
- [ ] Add `Article` / `BlogPosting` schema to the single-post template.
- [ ] Include new posts in `sitemap.xml`.
- [ ] Give her the one-page cheat sheet and the short screen recordings.

Her own login also removes the shared-password problem noted below.

### Go-live checklist

- [ ] Build with `python3 build.py --production` (never the default — that one
      is deliberately `noindex`)
- [ ] Confirm `<meta name="robots">` reads `index,follow` on the live pages
- [ ] Place `sitemap.xml`, `robots.txt`, `llms.txt` at the **domain root**
      (`hachemicals.com/robots.txt` — a subdirectory copy does nothing)
- [ ] Confirm no SEO plugin (Yoast/RankMath) is emitting a second, conflicting
      `robots` meta or canonical — duplicates cancel each other out
- [ ] Spot-check that existing product permalinks still resolve after the theme
      switch
- [ ] Set real prices, or switch the catalogue to quote-only — every product is
      currently `price: 0` and unpurchasable
- [ ] Submit sitemap to **Google Search Console** *and* **Bing Webmaster Tools**
      (ChatGPT search runs on Bing — this is the commonly missed one)
- [ ] Validate schema at <https://search.google.com/test/rich-results>
- [ ] Create and verify the **Google Business Profile** (postcard to the Abu
      Dhabi address — only the client can complete this)

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
