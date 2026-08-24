<?php
/** Site header. */
?><!doctype html>
<html <?php language_attributes(); ?>>
<head>
    <meta charset="<?php bloginfo( 'charset' ); ?>">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="theme-color" content="#13223C">
    <?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>
<a class="screen-reader-text" href="#main-content"><?php esc_html_e( 'Skip to content', 'hachemicals' ); ?></a>
<div class="topbar"><div class="wrap">
    <div><a href="mailto:<?php echo esc_attr( HACHEMICALS_EMAIL ); ?>"><?php echo esc_html( HACHEMICALS_EMAIL ); ?></a><span class="sep">|</span><?php echo esc_html( HACHEMICALS_HOURS ); ?></div>
    <div><a href="tel:<?php echo esc_attr( HACHEMICALS_PHONE_LINK ); ?>">Dial us: <?php echo esc_html( HACHEMICALS_PHONE ); ?></a></div>
</div></div>
<header class="site">
    <div class="wrap">
        <a href="<?php echo esc_url( home_url( '/' ) ); ?>" class="logo" aria-label="HA International Chemicals Trading LLC — home">
            <img src="<?php echo esc_url( hachemicals_asset( 'img/HA-international-chemical-llc-01-e1709276380617.webp' ) ); ?>" alt="HA International Chemicals Trading LLC" width="160" height="52">
        </a>
        <nav class="main" id="mainNav" aria-label="Primary navigation">
            <?php
            if ( has_nav_menu( 'primary' ) ) {
                wp_nav_menu(
                    array(
                        'theme_location' => 'primary',
                        'container'      => false,
                        'items_wrap'     => '%3$s',
                        'depth'          => 1,
                        'fallback_cb'    => false,
                    )
                );
            } else {
                hachemicals_primary_navigation_fallback();
            }
            ?>
            <a class="mobile-nav-quote" href="<?php echo esc_url( hachemicals_quote_url() ); ?>">Get a Free Quote</a>
        </nav>
        <div class="header-cta">
            <a class="btn btn-primary" href="<?php echo esc_url( hachemicals_quote_url() ); ?>" data-ripple>Get a Quote</a>
            <button class="menu-toggle" id="menuToggle" aria-label="Toggle menu" aria-controls="mainNav" aria-expanded="false">
                <span></span><span></span><span></span>
            </button>
        </div>
    </div>
</header>
<main id="main-content">
