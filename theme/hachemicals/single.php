<?php
/** Dynamic article template. */
get_header();
while ( have_posts() ) :
    the_post();
    $categories = get_the_category();
    $label = 'Article';
    foreach ( $categories as $category ) {
        if ( 'uncategorized' !== $category->slug ) { $label = $category->name; break; }
    }
    $related = get_posts( array( 'post_type' => 'post', 'post_status' => 'publish', 'posts_per_page' => 3, 'post__not_in' => array( get_the_ID() ), 'orderby' => 'date', 'order' => 'DESC' ) );
    ?>
    <div class="breadcrumb"><div class="wrap"><a href="<?php echo esc_url( home_url( '/' ) ); ?>">Home</a> / <a href="<?php echo esc_url( home_url( '/blog/' ) ); ?>">Blog</a> / <?php echo esc_html( wp_trim_words( get_the_title(), 8, '…' ) ); ?></div></div>
    <article><div class="wrap post-wrap">
        <span class="tag" data-reveal><?php echo esc_html( $label ); ?> &middot; <?php echo esc_html( get_the_date( 'j F Y' ) ); ?></span>
        <h1 data-reveal style="--i:1"><?php the_title(); ?></h1>
        <div class="post-hero" data-reveal style="--i:2"><img src="<?php echo esc_url( hachemicals_post_image_url( get_the_ID(), 'full' ) ); ?>" alt="<?php echo esc_attr( get_the_title() ); ?>"></div>
        <div class="pd-body post-body" data-reveal style="--i:3"><?php echo hachemicals_clean_rich_content( get_the_content() ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?></div>
        <div class="pd-actions" data-reveal><a class="btn btn-primary" href="<?php echo esc_url( hachemicals_quote_url() ); ?>" data-ripple>Request a Quote <span class="arw" aria-hidden="true">→</span></a><a class="btn btn-outline" href="<?php echo esc_url( hachemicals_shop_url() ); ?>" data-ripple>Browse Products</a></div>
    </div></article>
    <?php if ( $related ) : ?><section class="bg-surface"><div class="wrap"><div class="section-head"><div><div class="eyebrow" data-reveal>Keep reading</div><h2 data-reveal="wipe" style="font-size:26px">More guides</h2></div></div><div class="grid grid-3"><?php foreach ( $related as $index => $post ) { hachemicals_render_post_card( $post, $index ); } ?></div></div></section><?php endif; ?>
<?php endwhile; ?>
<?php get_footer(); ?>

