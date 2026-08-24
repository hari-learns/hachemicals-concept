<?php
get_header();
?>
<div class="notfound"><div class="code">404</div><h1>Page not found</h1><p>The page you're looking for has moved or doesn't exist.</p><a class="btn btn-primary" href="<?php echo esc_url( home_url( '/' ) ); ?>" data-ripple>Back to Home <span class="arw" aria-hidden="true">→</span></a></div>
<?php get_footer(); ?>

