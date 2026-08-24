# HA International Chemicals WordPress theme

Production child theme for `hello-elementor`. It translates the approved static
concept into native WordPress and WooCommerce templates while keeping products,
posts, media, forms, users, and administration in WordPress.

## Runtime dependencies

- Parent theme: Hello Elementor
- WooCommerce for the 26-product catalogue
- MetForm form `272` on `/contact-us/`
- WPForms form `1265` on `/contact-us/elementor-1264/`

The front end is quote-only. No product price or add-to-cart UI is rendered, but
WooCommerce data and wp-admin behavior are not modified.

## Deployment

Deploy this directory as a theme artifact. Test and activate it on the included
WordPress.com staging environment first. Production activation must use the exact
artifact that passed staging. Keep Hello Elementor installed for rollback.

## Required staging checks

Run `python3 qa/theme_audit.py`, then verify the 41-entry manifest in
`qa/page-manifest.json`. Complete the responsive and integration matrix in
`qa/TEST_MATRIX.md` before production activation.

