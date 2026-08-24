<?php
/** Reusable quote call-to-action. */
$heading = $args['heading'] ?? 'Need a chemical or spec sheet fast?';
$text    = $args['text'] ?? 'Send us your requirement and we will respond with pricing and availability.';
$label   = $args['label'] ?? 'Get a Free Quote';
$href    = $args['href'] ?? hachemicals_quote_url();
?>
<section class="cta-band">
    <div class="wrap">
        <h2 data-reveal><?php echo esc_html( $heading ); ?></h2>
        <p data-reveal style="--i:1"><?php echo esc_html( $text ); ?></p>
        <div data-reveal style="--i:2"><a class="btn btn-secondary" href="<?php echo esc_url( $href ); ?>" data-ripple><?php echo esc_html( $label ); ?> <span class="arw" aria-hidden="true">→</span></a></div>
    </div>
</section>

