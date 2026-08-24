# WordPress staging acceptance matrix

## Scope

The HA International Chemicals child theme, 41-route inventory, WooCommerce
catalogue, WordPress articles, MetForm contact form, WPForms quote form,
responsive navigation, metadata, structured data, deployment, and rollback.

## Assumptions

Staging is an isolated copy of production. Tests do not alter production. Form
delivery tests require explicit approval immediately before submission.

## Core Checklist

- **ID:** VIS-01 · **Priority:** P0 · **Scenario:** Concept parity · **Setup:** Concept and staging at the same viewport · **Action:** Compare all 41 manifest entries · **Expected:** Copy, hierarchy, palette, imagery, spacing, and controls match with no missing route.
- **ID:** RWD-01 · **Priority:** P0 · **Scenario:** Responsive layout · **Setup:** 320, 375, 768, 1280, and 1440 px viewports · **Action:** Load every template family and open mobile navigation · **Expected:** No horizontal overflow, clipping, unreadable text, or inaccessible control.
- **ID:** CAT-01 · **Priority:** P0 · **Scenario:** Dynamic catalogue · **Setup:** 26 published products · **Action:** Open shop, category, chemical, and VFD pages · **Expected:** All products appear once, the two previously uncategorized chemicals remain discoverable, and no price/cart UI appears.
- **ID:** POST-01 · **Priority:** P0 · **Scenario:** Native publishing · **Setup:** Staging-only draft article · **Action:** Publish, open Blog, then open article · **Expected:** Article appears automatically with correct design, metadata, image, and one H1.
- **ID:** FORM-01 · **Priority:** P0 · **Scenario:** MetForm contact · **Setup:** Approved staging submission · **Action:** Exercise required, invalid, then valid values · **Expected:** Validation is accessible, success is visible, and configured email arrives once.
- **ID:** FORM-02 · **Priority:** P0 · **Scenario:** WPForms quote · **Setup:** Open a product quote deep-link · **Action:** Verify prefill, then submit approved staging data · **Expected:** Product is prefilled, success is visible, and configured email arrives once.
- **ID:** SEO-01 · **Priority:** P0 · **Scenario:** Metadata and schema · **Setup:** Representative page, product, article, and homepage · **Action:** Inspect canonical, description, OG tags, JSON-LD, robots, and sitemap · **Expected:** One canonical, one H1, valid Organization/Product/BlogPosting/Breadcrumb/FAQ schema, and staging remains noindex.
- **ID:** ROL-01 · **Priority:** P0 · **Scenario:** Theme rollback · **Setup:** Tested staging theme · **Action:** Switch to Hello Elementor and back · **Expected:** Both activations succeed without database loss; cache purge exposes the selected theme.

## Variable Matrix

| Priority | Variable | Values | Expected |
|---|---|---|---|
| P0 | Viewport | 320 / 375 / 768 / 1280 / 1440 | Stable layout and navigation |
| P0 | Content | Page / Product / Article / Archive / 404 | Correct template and one H1 |
| P0 | Product family | Chemical / VFD / uncategorized source | Correct visible grouping |
| P1 | Motion | Normal / reduced motion | Content always visible; motion disabled when requested |
| P1 | Session | Logged out / WordPress admin bar | Header and navigation remain usable |
| P1 | Cache | Warm / purged / stale browser cache | Versioned assets and correct active theme |

## Agent Variety Set

- **ID:** AV-01 · **Priority:** P1 · **Scenario:** JavaScript unavailable · **Setup:** Disable scripts · **Action:** Load representative pages · **Expected:** Content and links remain readable; only enhancements stop.
- **ID:** AV-02 · **Priority:** P1 · **Scenario:** Missing form plugin · **Setup:** Staging-only plugin failure simulation · **Action:** Load both form pages · **Expected:** Contact fallback appears without fatal errors.
- **ID:** AV-03 · **Priority:** P1 · **Scenario:** Missing featured image · **Setup:** Product/post without thumbnail · **Action:** Load card and detail page · **Expected:** Local placeholder renders without layout shift.
- **ID:** AV-04 · **Priority:** P1 · **Scenario:** Cache rollback · **Setup:** Warm edge and plugin caches · **Action:** Switch theme, purge, reload from clean session · **Expected:** No mixed-theme assets remain.
- **ID:** AV-05 · **Priority:** P2 · **Scenario:** Long translated-like content · **Setup:** Very long title in staging draft · **Action:** View archive and detail at 320 px · **Expected:** Text wraps without clipping or overflow.

## Coverage Gaps

Email delivery, WordPress.com edge-cache purge, staging sync behavior, and actual
theme rollback can only be proven in WordPress.com staging. Production Search
Console and Bing submission occur after cutover.

## Recommended Run Order

Theme audit → PHP syntax checks → local concept responsive checks → staging
deployment → route/visual matrix → forms → schema/accessibility → rollback drill
→ production backup and cutover.

