<?php
/** Existing public Free Quote page, backed by WPForms form 1265. */
get_header();
?>
<section class="page-hero"><div class="wrap"><div class="eyebrow on-dark">Request Pricing &amp; Availability</div><h1>Free quote</h1><p>Tell us what you need and our team will respond with pricing and availability.</p></div></section>
<section><div class="wrap contact-grid">
    <div>
        <div class="eyebrow" data-reveal>Why us?</div>
        <h2 data-reveal="wipe">Reliable chemical and electrical supply</h2>
        <p data-reveal style="--i:1">Feel free to write our team anytime — we usually respond within one business day.</p>
        <p class="lede" data-reveal style="--i:2">At HA International Chemicals Trading LLC, we prioritize quality and reliability in chemical and electrical supply. Our team coordinates responsive sourcing and timely delivery around your technical and quantity requirements.</p>
        <div class="contact-card" data-reveal style="--i:3"><h4>Direct support</h4><a href="tel:<?php echo esc_attr( HACHEMICALS_PHONE_LINK ); ?>"><?php echo esc_html( HACHEMICALS_PHONE ); ?></a></div>
        <div class="contact-card" data-reveal style="--i:4"><h4>Email</h4><a href="mailto:<?php echo esc_attr( HACHEMICALS_EMAIL ); ?>"><?php echo esc_html( HACHEMICALS_EMAIL ); ?></a></div>
        <div class="contact-card" data-reveal style="--i:5"><h4>Address</h4><p><?php echo esc_html( HACHEMICALS_ADDRESS ); ?></p></div>
    </div>
    <div class="hachemicals-form-shell" data-reveal="right">
        <h2>Quote request details</h2>
        <?php if ( shortcode_exists( 'wpforms' ) ) : ?>
            <?php
            $form_html         = do_shortcode( '[wpforms id="1265" title="false"]' );
            $requested_product = hachemicals_requested_product_name();
            if ( $requested_product ) {
                $prefill   = esc_attr( 'Product: ' . $requested_product );
                $form_html = preg_replace_callback(
                    '/<input\b[^>]*\bid=(["\'])wpforms-1265-field_8\1[^>]*>/i',
                    static function ( $match ) use ( $prefill ) {
                        $input = preg_replace( '/\svalue=(["\']).*?\1/i', '', $match[0] );
                        return substr( $input, 0, -1 ) . ' value="' . $prefill . '">';
                    },
                    $form_html,
                    1
                );
            }
            echo $form_html; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
            ?>
        <?php else : ?>
            <p class="form-unavailable">The quote form is temporarily unavailable. Email <a href="mailto:<?php echo esc_attr( HACHEMICALS_EMAIL ); ?>"><?php echo esc_html( HACHEMICALS_EMAIL ); ?></a> or call <?php echo esc_html( HACHEMICALS_PHONE ); ?>.</p>
        <?php endif; ?>
    </div>
</div></section>
<?php get_footer(); ?>
