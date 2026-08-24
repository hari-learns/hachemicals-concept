<?php
/** Contact page using the existing MetForm configuration. */
get_header();
?>
<section class="page-hero"><div class="wrap"><div class="eyebrow on-dark">Contact</div><h1>Let's talk about your requirement</h1><p>Feel free to write our team anytime — we usually respond within one business day.</p></div></section>
<section><div class="wrap contact-grid">
    <div>
        <div class="contact-card" data-reveal><h4>Phone</h4><a href="tel:<?php echo esc_attr( HACHEMICALS_PHONE_LINK ); ?>"><?php echo esc_html( HACHEMICALS_PHONE ); ?></a></div>
        <div class="contact-card" data-reveal style="--i:1"><h4>Email</h4><a href="mailto:<?php echo esc_attr( HACHEMICALS_EMAIL ); ?>"><?php echo esc_html( HACHEMICALS_EMAIL ); ?></a></div>
        <div class="contact-card" data-reveal style="--i:2"><h4>Address</h4><p><?php echo esc_html( HACHEMICALS_ADDRESS ); ?></p></div>
        <div class="contact-card" data-reveal style="--i:3"><h4>Hours</h4><p><?php echo esc_html( HACHEMICALS_HOURS ); ?></p></div>
        <div class="contact-card" data-reveal style="--i:4"><h4>WhatsApp</h4><a href="https://wa.me/971502287866" target="_blank" rel="noopener">Message us on WhatsApp</a></div>
    </div>
    <div class="hachemicals-form-shell" data-reveal="right">
        <h2>Request a Quote</h2>
        <?php if ( shortcode_exists( 'metform' ) ) : ?>
            <?php echo do_shortcode( '[metform form_id="272"]' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>
        <?php else : ?>
            <p class="form-unavailable">The contact form is temporarily unavailable. Email <a href="mailto:<?php echo esc_attr( HACHEMICALS_EMAIL ); ?>"><?php echo esc_html( HACHEMICALS_EMAIL ); ?></a> or call <?php echo esc_html( HACHEMICALS_PHONE ); ?>.</p>
        <?php endif; ?>
    </div>
</div></section>
<?php get_footer(); ?>

