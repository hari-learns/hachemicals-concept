<?php
/** Dynamic, quote-only product detail. */
defined( 'ABSPATH' ) || exit;
get_header();
while ( have_posts() ) :
    the_post();
    $product = wc_get_product( get_the_ID() );
    if ( ! $product ) {
        continue;
    }
    $name = hachemicals_display_title( $product->get_name() );
    $copy = hachemicals_product_copy( $product );
    $related = hachemicals_get_products( hachemicals_product_is_vfd( $product ) ? 'vfd' : 'chemical', 4, array( $product->get_id() ) );
    ?>
    <div class="breadcrumb"><div class="wrap"><a href="<?php echo esc_url( home_url( '/' ) ); ?>">Home</a> / <a href="<?php echo esc_url( hachemicals_shop_url() ); ?>">Products</a> / <?php echo esc_html( $name ); ?></div></div>
    <section class="pd-grid wrap">
        <div class="pd-media">
            <div class="frame" data-reveal="left"><img src="<?php echo esc_url( hachemicals_product_image_url( $product->get_id(), 'full' ) ); ?>" alt="<?php echo esc_attr( $name ); ?>"></div>
            <div class="quote-box" data-reveal style="--i:1">
                <h4>Request pricing</h4>
                <p>Get a quote with current pricing, MOQ, and lead time for <?php echo esc_html( $name ); ?>.</p>
                <a class="btn btn-primary" href="<?php echo esc_url( hachemicals_quote_url( $product->get_slug() ) ); ?>" data-ripple style="width:100%">Request a Quote <span class="arw" aria-hidden="true">→</span></a>
            </div>
        </div>
        <div class="pd-info">
            <span class="tag" data-reveal><?php echo esc_html( hachemicals_product_label( $product ) ); ?></span>
            <h1 data-reveal style="--i:1"><?php echo esc_html( $name ); ?></h1>
            <div class="pd-body" data-reveal style="--i:2"><?php echo $copy; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- sanitized by helper. ?></div>
            <div class="pd-actions" data-reveal style="--i:3">
                <a class="btn btn-secondary" href="tel:<?php echo esc_attr( HACHEMICALS_PHONE_LINK ); ?>" data-ripple>Call <?php echo esc_html( HACHEMICALS_PHONE ); ?></a>
                <a class="btn btn-outline" href="https://wa.me/971502287866" target="_blank" rel="noopener" data-ripple>WhatsApp</a>
            </div>
        </div>
    </section>
    <?php if ( $related ) : ?>
        <section class="bg-surface"><div class="wrap">
            <div class="section-head"><div><div class="eyebrow" data-reveal>Related</div><h2 data-reveal="wipe" style="font-size:26px">More <?php echo esc_html( hachemicals_product_label( $product ) ); ?>s</h2></div></div>
            <div class="grid grid-4"><?php foreach ( $related as $index => $item ) { hachemicals_render_product_card( $item, $index ); } ?></div>
        </div></section>
    <?php endif; ?>
<?php endwhile; ?>
<?php get_footer(); ?>
