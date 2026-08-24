<?php
/** Dynamic WordPress posts index. */
get_header();
?>
<section class="page-hero"><div class="wrap"><div class="eyebrow on-dark">Blog</div><h1>Insights &amp; updates</h1><p>Technical notes, product guides and industry updates from our team.</p></div></section>
<section><div class="wrap">
    <?php if ( have_posts() ) : ?>
        <div class="grid grid-3">
            <?php $index = 0; while ( have_posts() ) : the_post(); hachemicals_render_post_card( get_post(), $index++ ); endwhile; ?>
        </div>
        <?php the_posts_pagination( array( 'mid_size' => 1, 'prev_text' => 'Previous', 'next_text' => 'Next' ) ); ?>
    <?php else : ?>
        <div class="empty-state" data-reveal><div class="ic" aria-hidden="true">📝</div><h2>No posts published yet</h2><p>This is where articles will appear.</p></div>
    <?php endif; ?>
</div></section>
<?php
get_template_part( 'template-parts/cta', null, array( 'heading' => 'Need a product from one of these guides?', 'text' => "Tell us your requirement and we'll come back with pricing and availability." ) );
get_footer();

