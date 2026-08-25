<?php
/** VFD and electrical catalogue page. */
get_header();
$vfds   = hachemicals_get_products( 'vfd' );
$extras = hachemicals_get_products( 'chemical', 4 );
?>
<section class="page-hero"><div class="wrap"><div class="eyebrow on-dark">Electrical &amp; Technical</div><h1>VFD &amp; Electrical Products</h1><p>Variable frequency drives and electrical equipment, supplied and supported by our technical team.</p></div></section>
<section><div class="wrap">
    <div class="section-head"><div><div class="eyebrow" data-reveal>In Stock</div><h2 data-reveal="wipe">Variable frequency drives</h2></div></div>
    <div class="grid grid-4"><?php foreach ( $vfds as $index => $product ) { hachemicals_render_product_card( $product, $index ); } ?></div>
</div></section>
<section class="bg-surface"><div class="wrap">
    <div class="section-head section-head--wide"><div><div class="eyebrow" data-reveal>Also Available</div><h2 data-reveal="wipe">Chemicals from our catalogue</h2></div><a class="btn btn-outline" href="<?php echo esc_url( hachemicals_shop_url() ); ?>" data-reveal data-ripple>All Products <span class="arw" aria-hidden="true">→</span></a></div>
    <div class="grid grid-4"><?php foreach ( $extras as $index => $product ) { hachemicals_render_product_card( $product, $index ); } ?></div>
</div></section>
<?php
get_template_part( 'template-parts/cta', null, array( 'heading' => 'Need a drive sized for your motor?', 'text' => "Send us the motor rating and duty cycle — we'll specify the right VFD and quote it.", 'label' => 'Talk to an Engineer' ) );
get_footer();
