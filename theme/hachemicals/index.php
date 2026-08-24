<?php
/** Required theme fallback. */
get_header();
?>
<section class="page-hero"><div class="wrap"><div class="eyebrow on-dark">HA International Chemicals</div><h1><?php bloginfo( 'name' ); ?></h1></div></section>
<section><div class="wrap">
<?php if ( have_posts() ) : ?><div class="grid grid-3"><?php $index = 0; while ( have_posts() ) : the_post(); hachemicals_render_post_card( get_post(), $index++ ); endwhile; ?></div><?php else : ?><div class="empty-state"><h2>No content found</h2></div><?php endif; ?>
</div></section>
<?php get_footer(); ?>

