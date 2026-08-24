<?php
/** Metadata, canonical URLs, and JSON-LD. */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

function hachemicals_meta_description() {
    if ( is_front_page() ) {
        return 'UAE supplier of industrial and specialty chemicals and electrical/VFD products for construction, oil and gas, and water treatment. 38+ years in Abu Dhabi.';
    }
    if ( function_exists( 'is_shop' ) && is_shop() ) {
        return 'Browse industrial chemicals, drilling and cementing chemicals, water treatment chemicals, and VFD/electrical equipment from HA International Chemicals.';
    }
    if ( is_singular( array( 'post', 'product' ) ) ) {
        $description = get_post_meta( get_queried_object_id(), '_yoast_wpseo_metadesc', true );
        if ( ! $description ) {
            $description = get_the_excerpt( get_queried_object_id() );
        }
        return wp_trim_words( wp_strip_all_tags( $description ), 26, '' );
    }
    if ( is_page( 'about-us' ) ) {
        return '38+ years supplying industrial chemicals and electrical products across the UAE. Learn about HA International Chemicals Trading LLC.';
    }
    if ( is_page( 'contact-us' ) || is_page( 'elementor-1264' ) ) {
        return 'Contact HA International Chemicals Trading LLC in Abu Dhabi, UAE for product pricing, availability, and technical requirements.';
    }
    return wp_trim_words( wp_strip_all_tags( get_bloginfo( 'description' ) ), 26, '' );
}

function hachemicals_canonical_url() {
    if ( is_front_page() ) {
        return home_url( '/' );
    }
    if ( function_exists( 'is_shop' ) && is_shop() ) {
        return hachemicals_shop_url();
    }
    if ( is_singular() ) {
        return get_permalink();
    }
    return home_url( add_query_arg( array(), $GLOBALS['wp']->request ?? '' ) );
}

function hachemicals_organization_schema() {
    return array(
        '@context'      => 'https://schema.org',
        '@type'         => 'Organization',
        'name'          => 'HA International Chemicals Trading LLC',
        'alternateName' => 'HA International Chemicals',
        'url'           => home_url( '/' ),
        'logo'          => hachemicals_asset( 'img/HA-international-chemical-llc-01-e1709276380617.webp' ),
        'image'         => hachemicals_asset( 'img/environmental-pollution-factory-exterior-night.webp' ),
        'email'         => HACHEMICALS_EMAIL,
        'telephone'     => HACHEMICALS_PHONE,
        'foundingDate'  => '1986',
        'address'       => array(
            '@type'           => 'PostalAddress',
            'streetAddress'   => 'M02, United Arab Bank Building, Al Danah',
            'addressLocality' => 'Abu Dhabi',
            'addressCountry'  => 'AE',
        ),
        'areaServed'    => array(
            array( '@type' => 'Country', 'name' => 'United Arab Emirates' ),
            array( '@type' => 'Place', 'name' => 'GCC' ),
        ),
        'knowsAbout'    => array( 'Industrial chemicals', 'Specialty chemicals', 'Drilling fluid additives', 'Water treatment chemicals', 'Variable frequency drives', 'Electrical installation', 'Cathodic protection' ),
        'contactPoint'  => array(
            array(
                '@type'             => 'ContactPoint',
                'contactType'       => 'sales',
                'telephone'         => HACHEMICALS_PHONE,
                'email'             => HACHEMICALS_EMAIL,
                'areaServed'        => 'AE',
                'availableLanguage' => array( 'English' ),
            ),
        ),
    );
}

function hachemicals_breadcrumb_schema() {
    $items = array( array( 'name' => 'Home', 'url' => home_url( '/' ) ) );
    if ( function_exists( 'is_product' ) && is_product() ) {
        $items[] = array( 'name' => 'Products', 'url' => hachemicals_shop_url() );
        $items[] = array( 'name' => hachemicals_display_title( get_the_title() ), 'url' => get_permalink() );
    } elseif ( is_singular( 'post' ) ) {
        $items[] = array( 'name' => 'Blog', 'url' => home_url( '/blog/' ) );
        $items[] = array( 'name' => get_the_title(), 'url' => get_permalink() );
    } elseif ( is_page() && ! is_front_page() ) {
        $items[] = array( 'name' => get_the_title(), 'url' => get_permalink() );
    } else {
        return null;
    }
    return array(
        '@context'        => 'https://schema.org',
        '@type'           => 'BreadcrumbList',
        'itemListElement' => array_map(
            static function ( $item, $index ) {
                return array( '@type' => 'ListItem', 'position' => $index + 1, 'name' => $item['name'], 'item' => $item['url'] );
            },
            $items,
            array_keys( $items )
        ),
    );
}

function hachemicals_context_schema() {
    if ( is_front_page() ) {
        $faqs = array(
            array( 'What chemicals does HA International Chemicals Trading LLC supply?', 'We supply drilling and cementing chemicals, water treatment chemicals, industrial chemicals, and variable frequency drives.' ),
            array( 'Where is HA International Chemicals Trading LLC based?', 'We are based at ' . HACHEMICALS_ADDRESS . ' and supply customers across the UAE and international markets.' ),
            array( 'Which industries does HA International Chemicals serve?', 'We serve construction, oil and gas, water treatment, manufacturing, and general industrial sectors across the UAE.' ),
            array( 'Does HA International supply drilling fluid additives?', 'Yes. Our range includes Cenosphere, Barite, Bentonite, Drilling Detergent, Drilling Foam, Drilling Starch, and C.M.C HV.' ),
            array( 'Does HA International supply VFDs and electrical products?', 'Yes. We supply MD290 series variable frequency drives and provide electrical installation and technical services.' ),
            array( 'How do I request a quote?', 'Call ' . HACHEMICALS_PHONE . ', email ' . HACHEMICALS_EMAIL . ', or use our quote form with your product and specification details.' ),
        );
        return array(
            '@context'   => 'https://schema.org',
            '@type'      => 'FAQPage',
            'mainEntity' => array_map(
                static function ( $faq ) {
                    return array( '@type' => 'Question', 'name' => $faq[0], 'acceptedAnswer' => array( '@type' => 'Answer', 'text' => $faq[1] ) );
                },
                $faqs
            ),
        );
    }
    if ( function_exists( 'is_product' ) && is_product() ) {
        $product = wc_get_product( get_queried_object_id() );
        if ( ! $product ) {
            return null;
        }
        return array(
            '@context'    => 'https://schema.org',
            '@type'       => 'Product',
            'name'        => hachemicals_display_title( $product->get_name() ),
            'category'    => hachemicals_product_label( $product ),
            'image'       => hachemicals_product_image_url( $product->get_id(), 'full' ),
            'brand'       => array( '@type' => 'Organization', 'name' => 'HA International Chemicals Trading LLC' ),
            'description' => wp_trim_words( wp_strip_all_tags( $product->get_short_description() . ' ' . $product->get_description() ), 70, '' ),
            'url'         => get_permalink( $product->get_id() ),
        );
    }
    if ( is_singular( 'post' ) ) {
        return array(
            '@context'         => 'https://schema.org',
            '@type'            => 'BlogPosting',
            'headline'         => get_the_title(),
            'datePublished'    => get_the_date( DATE_W3C ),
            'dateModified'     => get_the_modified_date( DATE_W3C ),
            'image'            => hachemicals_post_image_url( get_the_ID(), 'full' ),
            'description'      => hachemicals_meta_description(),
            'author'           => array( '@type' => 'Organization', 'name' => 'HA International Chemicals Trading LLC' ),
            'publisher'        => array( '@type' => 'Organization', 'name' => 'HA International Chemicals Trading LLC', 'logo' => array( '@type' => 'ImageObject', 'url' => hachemicals_asset( 'img/HA-international-chemical-llc-01-e1709276380617.webp' ) ) ),
            'mainEntityOfPage' => array( '@type' => 'WebPage', '@id' => get_permalink() ),
        );
    }
    return null;
}

function hachemicals_head_metadata() {
    $description = hachemicals_meta_description();
    $canonical   = hachemicals_canonical_url();
    $title       = wp_get_document_title();
    $image       = hachemicals_asset( 'img/environmental-pollution-factory-exterior-night.webp' );
    if ( is_singular() && has_post_thumbnail() ) {
        $image = get_the_post_thumbnail_url( null, 'full' );
    }
    ?>
    <meta name="description" content="<?php echo esc_attr( $description ); ?>">
    <link rel="canonical" href="<?php echo esc_url( $canonical ); ?>">
    <meta property="og:title" content="<?php echo esc_attr( $title ); ?>">
    <meta property="og:description" content="<?php echo esc_attr( $description ); ?>">
    <meta property="og:type" content="<?php echo is_singular( 'post' ) ? 'article' : 'website'; ?>">
    <meta property="og:url" content="<?php echo esc_url( $canonical ); ?>">
    <meta property="og:site_name" content="HA International Chemicals Trading LLC">
    <meta property="og:locale" content="en_AE">
    <meta property="og:image" content="<?php echo esc_url( $image ); ?>">
    <meta name="twitter:card" content="summary_large_image">
    <?php
    $schemas = array_filter( array( hachemicals_organization_schema(), hachemicals_breadcrumb_schema(), hachemicals_context_schema() ) );
    foreach ( $schemas as $schema ) {
        printf( '<script type="application/ld+json">%s</script>' . "\n", wp_json_encode( $schema, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE ) );
    }
}
remove_action( 'wp_head', 'rel_canonical' );
add_action( 'wp_head', 'hachemicals_head_metadata', 3 );
