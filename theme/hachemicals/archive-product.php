<?php
/** Quote-only WooCommerce catalogue. */
defined( 'ABSPATH' ) || exit;
get_header();

if ( is_product_taxonomy() ) {
    $products = array();
    while ( have_posts() ) {
        the_post();
        $product = wc_get_product( get_the_ID() );
        if ( $product ) {
            $products[] = $product;
        }
    }
} else {
    $products = hachemicals_get_products();
}
$chemicals = array_values( array_filter( $products, static function ( $product ) { return ! hachemicals_product_is_vfd( $product ); } ) );
$vfds      = array_values( array_filter( $products, 'hachemicals_product_is_vfd' ) );
$title     = is_product_taxonomy() ? single_term_title( '', false ) : 'Products';
?>
<section class="page-hero">
    <div class="wrap">
        <div class="eyebrow on-dark">Catalogue</div>
        <h1><?php echo esc_html( $title ); ?></h1>
        <p><?php echo esc_html( count( $products ) ); ?> chemicals and electrical products, stocked and ready to quote.</p>
    </div>
</section>
<section>
    <div class="wrap">
        <?php if ( $chemicals && $vfds ) : ?>
            <div class="cat-strip">
                <a href="#chemicals" class="cat-pill active" data-ripple>Industrial Chemicals (<?php echo esc_html( count( $chemicals ) ); ?>)</a>
                <a href="#vfd" class="cat-pill" data-ripple>VFDs &amp; Electrical (<?php echo esc_html( count( $vfds ) ); ?>)</a>
            </div>
        <?php endif; ?>

        <?php if ( $chemicals ) : ?>
            <h2 id="chemicals" style="font-size:24px;margin-bottom:22px" data-reveal="wipe">Industrial Chemicals</h2>
            <div class="grid grid-4" style="margin-bottom:68px">
                <?php foreach ( $chemicals as $index => $product ) { hachemicals_render_product_card( $product, $index ); } ?>
            </div>
        <?php endif; ?>

        <?php if ( $vfds ) : ?>
            <h2 id="vfd" style="font-size:24px;margin-bottom:22px" data-reveal="wipe">VFDs &amp; Electrical</h2>
            <div class="grid grid-4">
                <?php foreach ( $vfds as $index => $product ) { hachemicals_render_product_card( $product, $index ); } ?>
            </div>
        <?php endif; ?>

        <?php if ( ! $products ) : ?>
            <div class="empty-state"><h2>No products found</h2><p>Please contact our team and we will help source your requirement.</p></div>
        <?php endif; ?>
    </div>
</section>
<?php
get_template_part( 'template-parts/cta', null, array( 'heading' => "Can't find what you need?", 'text' => "Our catalogue keeps growing — tell us the chemical or spec you're after and we'll source it.", 'label' => 'Ask Our Team' ) );
get_footer();

