<?php
/** Site footer. */
?>
</main>
<footer class="site">
    <div class="wrap">
        <div class="fgrid">
            <div>
                <div class="flogo"><img src="<?php echo esc_url( hachemicals_asset( 'img/HA-international-chemical-llc-01-e1709276380617.webp' ) ); ?>" alt="HA International Chemicals Trading LLC"></div>
                <p style="max-width:40ch;color:#8890A0;font-size:14px">Trusted UAE supplier of industrial &amp; specialty chemicals and electrical products for construction, oil &amp; gas, and water treatment.</p>
            </div>
            <div>
                <h4>Company</h4>
                <a href="<?php echo esc_url( hachemicals_page_url( 'about-us' ) ); ?>">About Us</a>
                <a href="<?php echo esc_url( hachemicals_page_url( 'services' ) ); ?>">Services</a>
                <a href="<?php echo esc_url( hachemicals_shop_url() ); ?>">Products</a>
                <a href="<?php echo esc_url( home_url( '/blog/' ) ); ?>">Blog</a>
                <a href="<?php echo esc_url( hachemicals_page_url( 'contact-us' ) ); ?>">Contact</a>
            </div>
            <div>
                <h4>Categories</h4>
                <a href="<?php echo esc_url( hachemicals_shop_url() . '#chemicals' ); ?>">Industrial Chemicals</a>
                <a href="<?php echo esc_url( hachemicals_page_url( 'electrical-technical-services' ) ); ?>">VFDs &amp; Electrical</a>
            </div>
            <div>
                <h4>Get in Touch</h4>
                <a href="tel:<?php echo esc_attr( HACHEMICALS_PHONE_LINK ); ?>"><?php echo esc_html( HACHEMICALS_PHONE ); ?></a>
                <a href="mailto:<?php echo esc_attr( HACHEMICALS_EMAIL ); ?>"><?php echo esc_html( HACHEMICALS_EMAIL ); ?></a>
                <a href="https://wa.me/971502287866" target="_blank" rel="noopener">WhatsApp Us</a>
                <span style="color:#8890A0;display:block;margin-top:6px"><?php echo esc_html( HACHEMICALS_ADDRESS ); ?></span>
            </div>
        </div>
        <div class="fbottom">
            <span>© <?php echo esc_html( gmdate( 'Y' ) ); ?> HA International Chemicals Trading LLC. All rights reserved.</span>
            <span>Abu Dhabi, United Arab Emirates</span>
        </div>
    </div>
</footer>
<?php wp_footer(); ?>
</body>
</html>

