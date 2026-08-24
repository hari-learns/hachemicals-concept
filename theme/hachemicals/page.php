<?php
/** Safe fallback for non-core pages. */
get_header();
while ( have_posts() ) : the_post(); ?>
<section class="page-hero"><div class="wrap"><div class="eyebrow on-dark">HA International Chemicals</div><h1><?php the_title(); ?></h1></div></section>
<section><div class="wrap post-wrap pd-body"><?php the_content(); ?></div></section>
<?php endwhile; get_footer(); ?>

