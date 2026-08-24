<?php
/** About page. */
get_header();
$photos = array(
    '710_3730-2-EDITED-1.webp', '710_3734-EDITED.webp', '710_3738-1.webp',
    '710_3745-2-1.webp', '710_3748-2-1.webp', '710_3749-3-1.webp', '710_3755-2-1.webp',
);
$installation_capabilities = array(
    'Electrical Equipment Installation',
    'Earthing & Cathodic Protection',
    'ELV & Telecommunication Installation',
);
?>
<section class="page-hero"><div class="wrap"><div class="eyebrow on-dark">About Us</div><h1>Four decades in the trade.</h1><p>Your trusted partner in the world of chemicals, engineering products and services.</p></div></section>
<section><div class="wrap about-grid">
    <div>
        <div class="eyebrow" data-reveal>Get to Know HA International</div>
        <h2 data-reveal="wipe">Chemical supply and electromechanical expertise</h2>
        <h4 data-reveal style="--i:1;font-family:var(--mono);font-size:12.5px;letter-spacing:.08em;color:var(--grey);text-transform:uppercase">Committed to providing our customers with exceptional product and service.</h4>
        <p class="lede" data-reveal style="--i:2">Your trusted partner in the world of chemicals, engineering products and services. Under the patronage of <strong>Mr. Adel Saif Amer Hasan Aljaberi</strong>, with a legacy of excellence and innovation spanning over 4 decades, we are committed to delivering superior solutions to meet the dynamic needs of industries in the region.</p>
        <p class="lede" data-reveal style="--i:3">We understand that the journey to this ideal future is multifaceted, requiring dedication, vision, and a clear sense of direction. At HA International Chemicals Trading LLC, we strive to stay at the forefront of technological advancements while nurturing a deep-rooted sense of responsibility towards our planet. We are acutely aware that progress is not merely measured in profit margins but in the positive change we bring to our world.</p>
        <div class="counter-row" style="margin-top:34px"><div data-reveal><b data-count="38">0</b><span>Years of Experience</span></div></div>
    </div>
    <div class="shot" data-reveal="right"><img src="<?php echo esc_url( hachemicals_asset( 'img/img_about_Home01-7DPAR8H.webp' ) ); ?>" alt="HA International Chemicals warehouse operations" loading="lazy"></div>
</div></section>
<section class="bg-navy"><div class="wrap">
    <div class="section-head"><div><div class="eyebrow on-dark" data-reveal>Installation Capabilities</div><h2 data-reveal="wipe">Electromechanical equipment installation</h2></div></div>
    <div class="counter-row"><?php foreach ( $installation_capabilities as $index => $capability ) : ?><div data-reveal style="--i:<?php echo esc_attr( $index ); ?>"><b aria-hidden="true"><?php echo esc_html( sprintf( '%02d', $index + 1 ) ); ?></b><span><?php echo esc_html( $capability ); ?></span></div><?php endforeach; ?></div>
</div></section>
<section><div class="wrap">
    <div class="section-head"><div><div class="eyebrow" data-reveal>Our Operations</div><h2 data-reveal="wipe">Inside the business</h2></div></div>
    <div class="photo-strip"><?php foreach ( $photos as $index => $photo ) : ?><figure data-reveal="scale" style="--i:<?php echo esc_attr( $index ); ?>"><img src="<?php echo esc_url( hachemicals_asset( 'img/' . $photo ) ); ?>" alt="HA International Chemicals facility" loading="lazy"></figure><?php endforeach; ?></div>
</div></section>
<section class="bg-surface"><div class="wrap">
    <div class="section-head"><div><div class="eyebrow" data-reveal>What Drives Us</div><h2 data-reveal="wipe">Quality, range, and expertise</h2></div></div>
    <div class="grid grid-3">
        <div class="feature" data-reveal><div class="num">01</div><div><h4>Quality Assurance</h4><p>At HA International Chemicals Trading LLC, quality is our top priority. We partner with reputable manufacturers and suppliers to ensure that all our products meet strict quality standards and comply with safety regulations.</p></div></div>
        <div class="feature" data-reveal style="--i:1"><div class="num">02</div><div><h4>Extensive Product Range</h4><p>We offer an extensive selection of electrical products and chemicals, catering to various industries' needs.</p></div></div>
        <div class="feature" data-reveal style="--i:2"><div class="num">03</div><div><h4>Technical Expertise</h4><p>Our team of experienced professionals possesses in-depth knowledge and technical expertise in the electrical and chemical fields.</p></div></div>
    </div>
</div></section>
<?php
get_template_part( 'template-parts/cta', null, array( 'heading' => 'Work with a supplier that shows up on time.', 'text' => "Tell us what your project needs — we'll quote it fast." ) );
get_footer();
