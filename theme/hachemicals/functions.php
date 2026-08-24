<?php
/**
 * HA International Chemicals child-theme setup and rendering helpers.
 *
 * @package Hachemicals
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

define( 'HACHEMICALS_THEME_VERSION', '1.0.0' );
define( 'HACHEMICALS_PHONE', '+971 50 228 7866' );
define( 'HACHEMICALS_PHONE_LINK', '+971502287866' );
define( 'HACHEMICALS_EMAIL', 'sales@hachemicals.com' );
define( 'HACHEMICALS_ADDRESS', 'M02, United Arab Bank Building, Al Danah, Abu Dhabi, United Arab Emirates' );
define( 'HACHEMICALS_HOURS', 'Mon – Sat, 10:00 – 18:30 (Sunday closed)' );

require_once get_stylesheet_directory() . '/inc/schema.php';

function hachemicals_setup() {
    load_child_theme_textdomain( 'hachemicals', get_stylesheet_directory() . '/languages' );
    add_theme_support( 'title-tag' );
    add_theme_support( 'post-thumbnails' );
    add_theme_support( 'responsive-embeds' );
    add_theme_support( 'html5', array( 'search-form', 'gallery', 'caption', 'style', 'script' ) );
    add_theme_support( 'woocommerce', array( 'thumbnail_image_width' => 640, 'single_image_width' => 900 ) );

    register_nav_menus(
        array(
            'primary' => __( 'Primary navigation', 'hachemicals' ),
        )
    );
}
add_action( 'after_setup_theme', 'hachemicals_setup', 20 );

function hachemicals_asset( $path ) {
    return trailingslashit( get_stylesheet_directory_uri() ) . 'assets/' . ltrim( $path, '/' );
}

function hachemicals_file_version( $relative_path ) {
    $file = get_stylesheet_directory() . '/' . ltrim( $relative_path, '/' );
    return file_exists( $file ) ? (string) filemtime( $file ) : HACHEMICALS_THEME_VERSION;
}

function hachemicals_enqueue_assets() {
    wp_enqueue_style(
        'hachemicals-fonts',
        'https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@500;600&display=swap',
        array(),
        null
    );
    wp_enqueue_style(
        'hachemicals-theme',
        get_stylesheet_uri(),
        array( 'hachemicals-fonts' ),
        hachemicals_file_version( 'style.css' )
    );
    wp_enqueue_script(
        'hachemicals-site',
        hachemicals_asset( 'js/site.js' ),
        array(),
        hachemicals_file_version( 'assets/js/site.js' ),
        true
    );
    wp_script_add_data( 'hachemicals-site', 'strategy', 'defer' );
}
add_action( 'wp_enqueue_scripts', 'hachemicals_enqueue_assets', 30 );

function hachemicals_body_classes( $classes ) {
    $classes[] = 'hachemicals-site';
    if ( function_exists( 'is_shop' ) && ( is_shop() || is_product_taxonomy() ) ) {
        $classes[] = 'hachemicals-catalogue';
    }
    return $classes;
}
add_filter( 'body_class', 'hachemicals_body_classes' );

function hachemicals_page_url( $path ) {
    $path = trim( $path, '/' );
    $page = get_page_by_path( $path );
    return $page ? get_permalink( $page ) : home_url( '/' . $path . '/' );
}

function hachemicals_shop_url() {
    return function_exists( 'wc_get_page_permalink' ) ? wc_get_page_permalink( 'shop' ) : home_url( '/shop/' );
}

function hachemicals_quote_url( $product_slug = '' ) {
    $url = hachemicals_page_url( 'contact-us/elementor-1264' );
    return $product_slug ? add_query_arg( 'product', sanitize_title( $product_slug ), $url ) : $url;
}

function hachemicals_display_title( $title ) {
    return str_ireplace( 'Drilling Strach', 'Drilling Starch', (string) $title );
}

function hachemicals_product_is_vfd( $product ) {
    $product = is_numeric( $product ) && function_exists( 'wc_get_product' ) ? wc_get_product( (int) $product ) : $product;
    if ( ! $product || ! is_a( $product, 'WC_Product' ) ) {
        return false;
    }

    $terms = get_the_terms( $product->get_id(), 'product_cat' );
    if ( is_array( $terms ) ) {
        foreach ( $terms as $term ) {
            if ( preg_match( '/(?:vfd|electrical|drive)/i', $term->slug . ' ' . $term->name ) ) {
                return true;
            }
        }
    }

    return (bool) preg_match( '/(?:\bVFD\b|MD290)/i', $product->get_name() );
}

function hachemicals_product_label( $product ) {
    return hachemicals_product_is_vfd( $product ) ? 'VFD & Electrical' : 'Industrial Chemical';
}

function hachemicals_product_image_url( $product_id, $size = 'large' ) {
    $image = get_the_post_thumbnail_url( $product_id, $size );
    return $image ?: hachemicals_asset( 'img/placeholder.webp' );
}

function hachemicals_post_image_url( $post_id, $size = 'large' ) {
    $image = get_the_post_thumbnail_url( $post_id, $size );
    return $image ?: hachemicals_asset( 'img/placeholder.webp' );
}

/**
 * Strip pasted authoring-tool markup and embedded checkout/form fragments from
 * catalogue copy while preserving every substantive text node and safe link.
 */
function hachemicals_clean_rich_content( $html ) {
    $html = do_shortcode( do_blocks( (string) $html ) );
    if ( '' === trim( wp_strip_all_tags( $html ) ) ) {
        return '';
    }

    if ( ! class_exists( 'DOMDocument' ) ) {
        return wp_kses_post( $html );
    }

    $previous = libxml_use_internal_errors( true );
    $dom      = new DOMDocument( '1.0', 'UTF-8' );
    $dom->loadHTML( '<?xml encoding="utf-8" ?><div id="hachemicals-content">' . $html . '</div>', LIBXML_HTML_NOIMPLIED | LIBXML_HTML_NODEFDTD );
    $xpath = new DOMXPath( $dom );

    foreach ( $xpath->query( '//form|//fieldset|//script|//style|//noscript|//iframe' ) as $node ) {
        $node->parentNode->removeChild( $node );
    }

    $allowed = array( 'p', 'strong', 'em', 'b', 'i', 'ul', 'ol', 'li', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'h2', 'h3', 'h4', 'br', 'a' );
    $nodes   = iterator_to_array( $xpath->query( '//*[@id="hachemicals-content"]//*' ) );
    foreach ( array_reverse( $nodes ) as $node ) {
        $tag = strtolower( $node->nodeName );
        if ( ! in_array( $tag, $allowed, true ) ) {
            while ( $node->firstChild ) {
                $node->parentNode->insertBefore( $node->firstChild, $node );
            }
            $node->parentNode->removeChild( $node );
            continue;
        }

        $href = ( 'a' === $tag ) ? $node->getAttribute( 'href' ) : '';
        while ( $node->attributes && $node->attributes->length ) {
            $node->removeAttributeNode( $node->attributes->item( 0 ) );
        }
        if ( 'a' === $tag && $href && ! preg_match( '#(?:/wpay/pay|paypal\.com/ncp/payment)#i', $href ) ) {
            $node->setAttribute( 'href', esc_url_raw( $href ) );
        } elseif ( 'a' === $tag && $href ) {
            $node->parentNode->removeChild( $node );
            continue;
        }
        if ( 'table' === $tag ) {
            $node->setAttribute( 'class', 'spec-table' );
        }
        if ( 'ul' === $tag ) {
            $node->setAttribute( 'class', 'benefits-list' );
        }
    }

    $wrapper = $dom->getElementById( 'hachemicals-content' );
    $output  = '';
    if ( $wrapper ) {
        foreach ( $wrapper->childNodes as $child ) {
            $output .= $dom->saveHTML( $child );
        }
    }
    libxml_clear_errors();
    libxml_use_internal_errors( $previous );

    $output = preg_replace( '/<table class="spec-table">/i', '<div class="table-scroll"><table class="spec-table">', $output );
    $output = preg_replace( '/<\/table>/i', '</table></div>', $output );
    $output = preg_replace( '/^[\s\x{00A0}]+|[\s\x{00A0}]+$/u', '', $output );

    return wp_kses_post( $output );
}

function hachemicals_primary_navigation_fallback() {
    $items = array(
        array( 'Home', home_url( '/' ), is_front_page() ),
        array( 'Products', hachemicals_shop_url(), function_exists( 'is_shop' ) && ( is_shop() || is_product() || is_product_taxonomy() ) ),
        array( 'VFD', hachemicals_page_url( 'electrical-technical-services' ), is_page( 'electrical-technical-services' ) ),
        array( 'Services', hachemicals_page_url( 'services' ), is_page( 'services' ) ),
        array( 'About', hachemicals_page_url( 'about-us' ), is_page( 'about-us' ) ),
        array( 'Blog', get_option( 'page_for_posts' ) ? get_permalink( (int) get_option( 'page_for_posts' ) ) : home_url( '/blog/' ), is_home() || is_singular( 'post' ) ),
        array( 'Contact', hachemicals_page_url( 'contact-us' ), is_page( 'contact-us' ) || is_page( 'elementor-1264' ) ),
    );
    foreach ( $items as $index => $item ) {
        printf(
            '<a href="%1$s"%2$s style="--n:%3$d">%4$s</a>',
            esc_url( $item[1] ),
            $item[2] ? ' class="active" aria-current="page"' : '',
            (int) $index,
            esc_html( $item[0] )
        );
    }
}

function hachemicals_render_product_card( $product, $index = 0 ) {
    if ( ! $product || ! is_a( $product, 'WC_Product' ) ) {
        return;
    }
    ?>
    <a class="card" href="<?php echo esc_url( get_permalink( $product->get_id() ) ); ?>" data-ripple data-reveal="scale" style="--i:<?php echo esc_attr( $index % 4 ); ?>">
        <div class="thumb"><img src="<?php echo esc_url( hachemicals_product_image_url( $product->get_id(), 'woocommerce_thumbnail' ) ); ?>" alt="<?php echo esc_attr( hachemicals_display_title( $product->get_name() ) ); ?>" loading="lazy"></div>
        <div class="body">
            <span class="tag"><?php echo esc_html( hachemicals_product_label( $product ) ); ?></span>
            <h3><?php echo esc_html( hachemicals_display_title( $product->get_name() ) ); ?></h3>
            <span class="go">View specs &amp; request quote <span class="arw" aria-hidden="true">→</span></span>
        </div>
    </a>
    <?php
}

function hachemicals_render_post_card( $post, $index = 0 ) {
    $post = get_post( $post );
    if ( ! $post ) {
        return;
    }
    $categories = get_the_category( $post->ID );
    $label      = 'Article';
    foreach ( $categories as $category ) {
        if ( 'uncategorized' !== $category->slug ) {
            $label = $category->name;
            break;
        }
    }
    ?>
    <a class="card post-card" href="<?php echo esc_url( get_permalink( $post ) ); ?>" data-ripple data-reveal="scale" style="--i:<?php echo esc_attr( $index % 3 ); ?>">
        <div class="post-thumb"><img src="<?php echo esc_url( hachemicals_post_image_url( $post->ID, 'large' ) ); ?>" alt="<?php echo esc_attr( get_the_title( $post ) ); ?>" loading="lazy"></div>
        <div class="body">
            <span class="tag"><?php echo esc_html( $label ); ?> &middot; <?php echo esc_html( get_the_date( 'j F Y', $post ) ); ?></span>
            <h3><?php echo esc_html( get_the_title( $post ) ); ?></h3>
            <span class="go">Read article <span class="arw" aria-hidden="true">→</span></span>
        </div>
    </a>
    <?php
}

function hachemicals_get_products( $kind = 'all', $limit = -1, $exclude = array() ) {
    if ( ! function_exists( 'wc_get_products' ) ) {
        return array();
    }
    $products = wc_get_products(
        array(
            'status'  => 'publish',
            'limit'   => -1,
            'orderby' => 'menu_order',
            'order'   => 'ASC',
            'exclude' => array_map( 'intval', (array) $exclude ),
            'return'  => 'objects',
        )
    );
    if ( 'vfd' === $kind ) {
        $products = array_values( array_filter( $products, 'hachemicals_product_is_vfd' ) );
    } elseif ( 'chemical' === $kind ) {
        $products = array_values( array_filter( $products, static function ( $product ) { return ! hachemicals_product_is_vfd( $product ); } ) );
    }
    return $limit > -1 ? array_slice( $products, 0, $limit ) : $products;
}

function hachemicals_document_title( $title ) {
    if ( is_front_page() ) {
        return 'HA International Chemicals Trading LLC — Chemical Supplier in UAE';
    }
    if ( function_exists( 'is_shop' ) && is_shop() ) {
        return 'Products — Industrial Chemicals & VFDs | HA International Chemicals';
    }
    return $title;
}
add_filter( 'pre_get_document_title', 'hachemicals_document_title', 20 );

// The quote-only presentation deliberately omits WooCommerce purchase UI while
// leaving products, orders, extensions, and all wp-admin behavior untouched.
function hachemicals_disable_catalogue_purchase_ui() {
    remove_action( 'woocommerce_single_product_summary', 'woocommerce_template_single_price', 10 );
    remove_action( 'woocommerce_single_product_summary', 'woocommerce_template_single_add_to_cart', 30 );
    remove_action( 'woocommerce_after_shop_loop_item', 'woocommerce_template_loop_add_to_cart', 10 );
}
add_action( 'wp', 'hachemicals_disable_catalogue_purchase_ui' );
