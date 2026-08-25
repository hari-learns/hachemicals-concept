<?php
/** Front page matching the approved concept. */
get_header();
$featured = hachemicals_get_products( 'chemical', 8 );
$all      = hachemicals_get_products();
$installation_capabilities = array(
    array( 'label' => 'Electrical Equipment Installation', 'image' => 'installation-electrical.webp' ),
    array( 'label' => 'Earthing & Cathodic Protection', 'image' => 'installation-earthing-cathodic.webp' ),
    array( 'label' => 'ELV & Telecommunication Installation', 'image' => 'installation-elv-telecom.webp' ),
);
?>
<section class="hero">
    <div class="hero__slides">
        <div class="hero__slide is-active"><img class="hero__img" src="<?php echo esc_url( hachemicals_asset( 'img/environmental-pollution-factory-exterior-night.webp' ) ); ?>" alt="" fetchpriority="high"></div>
        <div class="hero__slide"><img class="hero__img" src="<?php echo esc_url( hachemicals_asset( 'img/distant-shot-port-with-boats-loaded-with-cargo-shipment-during-nighttime.webp' ) ); ?>" alt="" loading="lazy"></div>
    </div>
    <div class="wrap">
        <div>
            <div class="eyebrow on-dark">Abu Dhabi, UAE · Since 1986</div>
            <h1>Leading Chemical Supplier in the <em>UAE</em></h1>
            <p class="lead">Premium chemical solutions — industrial and specialty chemicals plus electrical and VFD equipment for construction, oil &amp; gas, water treatment, and manufacturing.</p>
            <div class="cta-row">
                <a class="btn btn-primary" href="<?php echo esc_url( hachemicals_shop_url() ); ?>" data-ripple>Discover More <span class="arw" aria-hidden="true">→</span></a>
                <a class="btn btn-ghost" href="<?php echo esc_url( hachemicals_quote_url() ); ?>" data-ripple>Get a Free Quote</a>
            </div>
        </div>
        <div class="hero-stats">
            <div><b>38+</b><span>Years in the Trade</span></div>
            <div><b><?php echo esc_html( count( $all ) ); ?></b><span>Products Stocked</span></div>
            <div><b>UAE</b><span>&amp; International Reach</span></div>
            <div><b>24h</b><span>Quote Turnaround</span></div>
        </div>
    </div>
    <div class="hero__dots">
        <button class="is-active" aria-label="Slide 1"></button>
        <button aria-label="Slide 2"></button>
    </div>
</section>

<section>
    <div class="wrap">
        <div class="section-head">
            <div><div class="eyebrow" data-reveal>What We Supply</div><h2 data-reveal="wipe">Featured chemicals &amp; materials</h2></div>
            <a class="btn btn-outline" href="<?php echo esc_url( hachemicals_shop_url() ); ?>" data-reveal data-ripple>View All Products <span class="arw" aria-hidden="true">→</span></a>
        </div>
        <div class="grid grid-4">
            <?php foreach ( $featured as $index => $product ) { hachemicals_render_product_card( $product, $index ); } ?>
        </div>
    </div>
</section>

<section class="bg-surface">
    <div class="wrap">
        <div class="section-head"><div><div class="eyebrow" data-reveal>Industries We Serve</div><h2 data-reveal="wipe">Built for demanding sectors</h2></div></div>
        <div class="industry-row" data-reveal>
            <article class="industry-card industry-card--construction"><div class="industry-card__media"><img src="<?php echo esc_url( hachemicals_asset( 'img/sector-construction.webp' ) ); ?>" alt="UAE construction site with high-rise development and cranes" loading="lazy"></div><h4>Construction</h4></article>
            <article class="industry-card"><div class="industry-card__media"><img src="<?php echo esc_url( hachemicals_asset( 'img/sector-oil-gas.webp' ) ); ?>" alt="Modern oil and gas processing facility" loading="lazy"></div><h4>Oil &amp; Gas</h4></article>
            <article class="industry-card"><div class="industry-card__media"><img src="<?php echo esc_url( hachemicals_asset( 'img/sector-water-treatment.webp' ) ); ?>" alt="Industrial water treatment and filtration facility" loading="lazy"></div><h4>Water Treatment</h4></article>
            <article class="industry-card"><div class="industry-card__media"><img src="<?php echo esc_url( hachemicals_asset( 'img/sector-manufacturing.webp' ) ); ?>" alt="Clean automated manufacturing facility" loading="lazy"></div><h4>Manufacturing</h4></article>
        </div>
    </div>
</section>

<section>
    <div class="wrap about-grid">
        <div>
            <div class="eyebrow" data-reveal>We Trade You Gain</div>
            <h2 data-reveal="wipe">The Best Prices For You</h2>
            <p class="lede" data-reveal style="--i:1">HA International Chemicals Trading LLC is a leading chemical trading company in the UAE, specializing in the supply and distribution of high-quality industrial chemicals, specialty chemicals, and electrical products for diverse industries.</p>
            <p class="lede" data-reveal style="--i:2">With 38 years of experience, we have built a strong reputation for reliability, quality, and customer satisfaction, serving businesses across the UAE and international markets. Our commitment to excellence, timely delivery, and competitive pricing makes us a trusted partner for construction, manufacturing, water treatment, oil &amp; gas, and industrial sectors. We deliver premium products and dependable solutions tailored to meet modern industry demands.</p>
        </div>
        <div class="shot" data-reveal="right"><img src="<?php echo esc_url( hachemicals_asset( 'img/img_bg_business_Home01-STE4HQX-e1686194116880.webp' ) ); ?>" alt="HA International Chemicals operations" loading="lazy"></div>
    </div>
</section>

<section class="bg-navy">
    <div class="wrap">
        <div class="section-head section-head--wide"><div><div class="eyebrow on-dark" data-reveal>Installation Capabilities</div><h2 data-reveal="wipe">Electromechanical equipment installation</h2></div></div>
        <div class="installation-grid">
            <?php foreach ( $installation_capabilities as $index => $capability ) : ?>
                <article class="installation-card" data-reveal style="--i:<?php echo esc_attr( $index ); ?>">
                    <img src="<?php echo esc_url( hachemicals_asset( 'img/' . $capability['image'] ) ); ?>" alt="" loading="lazy" aria-hidden="true">
                    <h3><?php echo esc_html( $capability['label'] ); ?></h3>
                </article>
            <?php endforeach; ?>
        </div>
    </div>
</section>

<section>
    <div class="wrap">
        <div class="section-head"><div><div class="eyebrow" data-reveal>What Else We Do</div><h2 data-reveal="wipe">Committed to exceptional service</h2><p data-reveal style="--i:1">We offer an extensive selection of electrical products and chemicals, catering to various industries' needs.</p></div></div>
        <div class="grid grid-3">
            <div class="feature" data-reveal><div class="num">01</div><div><h4>Timely Delivery</h4><p>Our team of experienced professionals possesses in-depth knowledge and technical expertise in the electrical and chemical fields.</p></div></div>
            <div class="feature" data-reveal style="--i:1"><div class="num">02</div><div><h4>Quality Assurance</h4><p>At HA International Chemicals Trading LLC, quality is our top priority. We partner with reputable manufacturers and suppliers to ensure that all our products meet strict quality standards and comply with safety regulations.</p></div></div>
            <div class="feature" data-reveal style="--i:2"><div class="num">03</div><div><h4>Extensive Product Range</h4><p>From cutting-edge electrical equipment to premium-grade chemicals, we've got you covered.</p></div></div>
            <div class="feature" data-reveal style="--i:3"><div class="num">04</div><div><h4>Technical Expertise</h4><p>We can assist you in finding the right products that best suit your specific requirements.</p></div></div>
            <div class="feature" data-reveal style="--i:4"><div class="num">05</div><div><h4>Competitive Pricing</h4><p>Direct sourcing relationships keep our pricing sharp without compromising on quality.</p></div></div>
            <div class="feature" data-reveal style="--i:5"><div class="num">06</div><div><h4>38+ Years Trading</h4><p>Four decades of relationships across UAE construction, industrial, and energy sectors.</p></div></div>
        </div>
    </div>
</section>

<section class="bg-surface">
    <div class="wrap">
        <div class="section-head"><div><div class="eyebrow" data-reveal>Common Questions</div><h2 data-reveal="wipe">What buyers ask us</h2></div></div>
        <div class="faq-grid">
            <div class="faq-item" data-reveal><h3>What chemicals does HA International Chemicals Trading LLC supply?</h3><p>We supply drilling and cementing chemicals including Cenosphere, Barite, Bentonite, Drilling Detergent, Drilling Foam, Drilling Starch and C.M.C HV; water treatment chemicals including Ferric Chloride, Aluminium Sulphate and Calcium Chloride; and industrial chemicals including Caustic Soda Prills, Citric Acid, DEA, Butyl Glycol, Biocide, Ammonium Chloride and Ammonium Bisulfite.</p></div>
            <div class="faq-item" data-reveal style="--i:1"><h3>Where is HA International Chemicals Trading LLC based?</h3><p>We are based at <?php echo esc_html( HACHEMICALS_ADDRESS ); ?>, and supply customers across the UAE and international markets.</p></div>
            <div class="faq-item" data-reveal style="--i:2"><h3>Which industries does HA International Chemicals serve?</h3><p>We serve construction, oil and gas, water treatment, manufacturing and general industrial sectors across the UAE.</p></div>
            <div class="faq-item" data-reveal><h3>Does HA International supply drilling fluid additives for oil and gas?</h3><p>Yes. Our oil and gas range includes Cenosphere for lightweight cementing, Barite for weighting drilling fluids, Bentonite, Drilling Detergent, Drilling Foam, Drilling Starch and C.M.C HV.</p></div>
            <div class="faq-item" data-reveal style="--i:1"><h3>Does HA International supply VFDs and electrical products?</h3><p>Yes. We supply MD290 series variable frequency drives and provide electrical installation, earthing systems, cathodic protection, ELV installation and telecommunication installation services.</p></div>
            <div class="faq-item" data-reveal style="--i:2"><h3>How do I request a quote from HA International Chemicals?</h3><p>Call <?php echo esc_html( HACHEMICALS_PHONE ); ?>, email <?php echo esc_html( HACHEMICALS_EMAIL ); ?>, or message us on WhatsApp. Tell us the product, quantity and any specification details and we will respond with pricing and availability.</p></div>
        </div>
    </div>
</section>
<?php
get_template_part(
    'template-parts/cta',
    null,
    array(
        'heading' => 'Need a chemical or spec sheet fast?',
        'text'    => "Send us your requirement and we'll come back with pricing and availability, usually within one business day.",
    )
);
get_footer();
