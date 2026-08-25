<?php
/** Services page preserving the approved concept copy. */
get_header();
$services = array(
    array(
        'title' => 'Electrical installation',
        'image' => hachemicals_asset( 'img/service-electrical.webp' ),
        'alt'   => 'Technician installing industrial electrical switchgear',
        'paragraphs' => array(
            'At HA International Chemicals Trading LLC, we pride ourselves on being at the forefront of electrical installation services. With our team of experienced professionals and a commitment to quality, we offer cutting-edge solutions that meet your unique requirements and surpass your expectations.',
            'Whether you are embarking on a residential project, setting up a commercial space, or building industrial facilities, the expertise of skilled electrical installers is indispensable. From selecting the right components to precise wiring and adherence to safety codes, a well-executed electrical installation guarantees uninterrupted power supply and peace of mind.',
            'Discover the power of seamless electrical installation with us – where precision, efficiency, and safety converge to illuminate the world around us. Let’s electrify your vision together!',
        ),
    ),
    array(
        'title' => 'Earthing systems',
        'image' => hachemicals_asset( 'img/service-earthing.webp' ),
        'alt'   => 'Industrial equipment bonded to a copper earthing system',
        'paragraphs' => array(
            'Electrical earthing installation is a crucial system that ensures safety and protects both people and equipment from the hazards of electrical faults. Grounding, commonly known as earthing, refers to the process of establishing a low-resistance path between electrical circuits and the earth’s surface. By doing so, it effectively dissipates fault currents and prevents electric shock, fire, and damage to sensitive equipment.',
            'Proper electrical earthing installation requires the expertise of skilled professionals who understand the complexities of electrical systems and safety standards. The process involves careful planning, accurate measurements, and the use of high-quality materials to ensure a reliable and effective grounding system.',
            'At HA International Chemicals Trading LLC, we specialize in electrical earthing installation services, providing comprehensive solutions for residential, commercial, and industrial applications. Our experienced team of engineers and technicians ensure that your electrical system meets the highest safety standards, complying with local regulations and industry best practices.',
        ),
    ),
    array(
        'title' => 'Cathodic protection',
        'image' => hachemicals_asset( 'img/service-cathodic.webp' ),
        'alt'   => 'Cathodic protection equipment installed on an industrial pipeline',
        'paragraphs' => array(
            'We take pride in being industry leaders in providing top-notch cathodic protection installation services. Whether you are a large industrial facility or a small residential property owner, we have the expertise and experience to safeguard your valuable assets against the relentless forces of corrosion. Protecting your assets from corrosion is not just a matter of necessity; it’s a smart investment in the longevity and reliability of your infrastructure. We combine our technical expertise with a passion for innovation to deliver unparalleled cathodic protection solutions that stand the test of time.',
        ),
    ),
    array(
        'title' => 'ELV installation',
        'image' => hachemicals_asset( 'img/service-elv.webp' ),
        'alt'   => 'Organized extra-low-voltage control and communications rack',
        'paragraphs' => array(
            'We are proud to be your go-to experts for ELV (Extra-Low Voltage) installation services. As technology continues to advance rapidly, ELV systems have become an integral part of modern buildings and facilities. Our team of skilled professionals is equipped with the knowledge and expertise to deliver cutting-edge ELV installations that cater to your specific needs. Investing in the right ELV systems is essential for modern buildings and facilities, as they not only enhance security but also improve efficiency and convenience. We take pride in delivering ELV installations that set new standards in the industry.',
        ),
    ),
    array(
        'title' => 'Telecommunication installation',
        'image' => content_url( 'uploads/2025/05/october-2018-building-construction-skyscrapers-dubai1.jpg' ),
        'alt'   => 'High-rise installation project with tower cranes in Dubai',
        'paragraphs' => array(
            'Dedicated to revolutionizing the way people connect through our top-of-the-line telecommunication installation services. With the world becoming increasingly interconnected, a robust and efficient telecommunication infrastructure is essential for businesses and individuals alike. Our team of highly skilled professionals is committed to delivering cutting-edge solutions that empower you with seamless communication and connectivity. You can rest assured that your telecommunication needs are in the hands of professionals who are passionate about creating reliable and efficient communication networks. Whether you’re a small business looking to enhance your internal communication or a large enterprise seeking a robust data center solution, we have the expertise to turn your vision into reality.',
        ),
    ),
);
?>
<section class="page-hero"><div class="wrap">
    <div class="eyebrow on-dark">Electromechanical Services</div>
    <h1>Industrial Equipment Installation Expertise</h1>
    <p>Electrical installation, earthing systems, cathodic protection, ELV, and telecommunication installation delivered by experienced technical professionals.</p>
</div></section>
<section class="services-showcase"><div class="wrap">
    <div class="section-head section-head--wide"><div><div class="eyebrow" data-reveal>Installation Capabilities</div><h2 data-reveal="wipe">Electromechanical Installation Services</h2></div><a class="btn btn-outline" href="<?php echo esc_url( hachemicals_shop_url() ); ?>" data-reveal data-ripple>View Products <span class="arw" aria-hidden="true">→</span></a></div>
    <?php foreach ( $services as $index => $service ) : ?>
        <article class="service-item<?php echo 1 === $index % 2 ? ' service-item--media-left' : ''; ?>" data-reveal style="--i:<?php echo esc_attr( $index ); ?>">
            <div class="service-item__copy">
                <div class="ic"><?php echo esc_html( str_pad( (string) ( $index + 1 ), 2, '0', STR_PAD_LEFT ) ); ?></div>
                <div><h3><?php echo esc_html( $service['title'] ); ?></h3><?php foreach ( $service['paragraphs'] as $paragraph ) : ?><p><?php echo esc_html( $paragraph ); ?></p><?php endforeach; ?></div>
            </div>
            <figure class="service-item__media"><img src="<?php echo esc_url( $service['image'] ); ?>" alt="<?php echo esc_attr( $service['alt'] ); ?>" width="1280" height="854" loading="lazy"></figure>
        </article>
    <?php endforeach; ?>
</div></section>
<?php
get_template_part( 'template-parts/cta', null, array( 'heading' => 'Have a project spec in hand?', 'text' => "Send it over and we'll respond with pricing, availability, and lead time." ) );
get_footer();
