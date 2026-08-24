#!/usr/bin/env python3
"""Static concept-site generator for HA International Chemicals Trading LLC.

Reads the scraped src_data/*.json and writes a self-contained static site to
./site. All product and services copy comes from their live site verbatim —
nothing here is invented.
"""
import datetime
import html
import json
import os
import re
import shutil
import sys
from clean_html import clean

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "site")

# `python3 build.py --production` builds for the real domain: indexable,
# canonicals and sitemap on hachemicals.com. The default build is the shareable
# concept, which is noindex so it can never compete with the client's own site
# for their own content.
PRODUCTION = "--production" in sys.argv
SITE_URL = ("https://hachemicals.com" if PRODUCTION
            else "https://hari-learns.github.io/hachemicals-concept")
PROD = json.load(open(os.path.join(ROOT, "src_data/products.json")))
CONTENT = json.load(open(os.path.join(ROOT, "src_data/content.json")))
_posts_path = os.path.join(ROOT, "src_data/posts.json")
POSTS = json.load(open(_posts_path)) if os.path.exists(_posts_path) else []

# WordPress stores titles HTML-encoded ("77 &#8211; 78 %"). That renders fine in
# markup but leaks raw entities into JSON-LD and llms.txt, which are plain text.
# Decode once here so every consumer gets a real en-dash.
for _p in PROD:
    _p["name"] = re.sub(r"\s+", " ", html.unescape(_p["name"])).strip()

PHONE = "+971 50 228 7866"
PHONE_LINK = "+971502287866"
WHATSAPP = "https://wa.me/971502287866"
EMAIL = "sales@hachemicals.com"
ADDRESS = "M02, United Arab Bank Building, Al Danah, Abu Dhabi, United Arab Emirates"
HOURS = "Mon – Sat, 10:00 – 18:30 (Sunday closed)"
LOGO = "HA-international-chemical-llc-01-e1709276380617.webp"

NAV = [
    ("index.html", "Home"),
    ("products.html", "Products"),
    ("electrical-technical-services.html", "VFD"),
    ("services.html", "Services"),
    ("about-us.html", "About"),
    ("blog.html", "Blog"),
    ("contact-us.html", "Contact"),
]

HERO_SLIDES = [
    "environmental-pollution-factory-exterior-night.webp",
    "distant-shot-port-with-boats-loaded-with-cargo-shipment-during-nighttime.webp",
]
FACILITY_PHOTOS = [
    "710_3730-2-EDITED-1.webp", "710_3734-EDITED.webp", "710_3738-1.webp",
    "710_3745-2-1.webp", "710_3748-2-1.webp", "710_3749-3-1.webp",
    "710_3755-2-1.webp",
]

ARW = '<span class="arw">&rarr;</span>'

# Every answer below is verifiable from their own catalogue or contact details.
# Nothing about pricing, MOQ, lead times or certifications — those are unknown,
# and inventing them would put false claims in schema markup.
FAQS = [
    ("What chemicals does HA International Chemicals Trading LLC supply?",
     "We supply drilling and cementing chemicals including Cenosphere, Barite, "
     "Bentonite, Drilling Detergent, Drilling Foam, Drilling Starch and C.M.C HV; "
     "water treatment chemicals including Ferric Chloride, Aluminium Sulphate and "
     "Calcium Chloride; and industrial chemicals including Caustic Soda Prills, "
     "Citric Acid, DEA, Butyl Glycol, Biocide, Ammonium Chloride and Ammonium "
     "Bisulfite."),
    ("Where is HA International Chemicals Trading LLC based?",
     f"We are based at {ADDRESS}, and supply customers across the UAE and "
     "international markets."),
    ("Which industries does HA International Chemicals serve?",
     "We serve construction, oil and gas, water treatment, manufacturing and "
     "general industrial sectors across the UAE."),
    ("Does HA International supply drilling fluid additives for oil and gas?",
     "Yes. Our oil and gas range includes Cenosphere for lightweight cementing, "
     "Barite for weighting drilling fluids, Bentonite, Drilling Detergent, "
     "Drilling Foam, Drilling Starch and C.M.C HV."),
    ("Does HA International supply VFDs and electrical products?",
     "Yes. We supply MD290 series variable frequency drives and provide electrical "
     "installation, earthing systems, cathodic protection, ELV installation and "
     "telecommunication installation services."),
    ("How do I request a quote from HA International Chemicals?",
     f"Call {PHONE}, email {EMAIL}, or message us on WhatsApp. Tell us the product, "
     "quantity and any specification details and we will respond with pricing and "
     "availability."),
]


def asset(name):
    return "assets/img/" + name


def have(name):
    return os.path.exists(os.path.join(ROOT, "assets/img", name))


def product_img(p):
    if p["slug"] == "drilling-strach" and have("drilling-starch-ha.webp"):
        return asset("drilling-starch-ha.webp")
    if p["images"]:
        stem = os.path.splitext(re.sub(r"\?.*$", "", p["images"][0].split("/")[-1]))[0]
        if have(stem + ".webp"):
            return asset(stem + ".webp")
    return asset("placeholder.webp")


def category_badge(cat):
    return "VFD &amp; Electrical" if cat == "VFD" else "Industrial Chemical"


# ---------------------------------------------------------------- shell
def base(title, description, body, active="", canonical="", extra_head="", depth=0):
    up = "../" * depth
    robots = ("index,follow,max-image-preview:large,max-snippet:-1"
              if PRODUCTION else "noindex,nofollow")
    nav_links = "\n      ".join(
        '<a href="{}{}"{}data-ripple>{}</a>'.format(
            up, href, ' class="active" ' if href == active else " ", label
        )
        for href, label in NAV
    )
    # Everything here is verifiable from their own site. knowsAbout/areaServed
    # help search and assistants tie the company to the right subject and place;
    # no geo coordinates because we don't have verified ones and guessing them
    # would put a false location into structured data.
    org_schema = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "HA International Chemicals Trading LLC",
        "alternateName": "HA International Chemicals",
        "url": "https://hachemicals.com/",
        "logo": f"{SITE_URL}/{asset(LOGO)}",
        "image": f"{SITE_URL}/{asset(HERO_SLIDES[0])}",
        "email": EMAIL,
        "telephone": PHONE,
        "foundingDate": "1986",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "M02, United Arab Bank Building, Al Danah",
            "addressLocality": "Abu Dhabi",
            "addressCountry": "AE",
        },
        "areaServed": [
            {"@type": "Country", "name": "United Arab Emirates"},
            {"@type": "Place", "name": "GCC"},
        ],
        "knowsAbout": [
            "Industrial chemicals", "Specialty chemicals",
            "Drilling fluid additives", "Oil well cementing additives",
            "Water treatment chemicals", "Variable frequency drives",
            "Electrical installation", "Cathodic protection",
        ],
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday",
                          "Friday", "Saturday"],
            "opens": "10:00",
            "closes": "18:30",
        }],
        "contactPoint": [{
            "@type": "ContactPoint",
            "contactType": "sales",
            "telephone": PHONE,
            "email": EMAIL,
            "areaServed": "AE",
            "availableLanguage": ["English"],
        }],
        "description": ("UAE supplier of industrial and specialty chemicals and "
                        "electrical products for construction, oil & gas, and "
                        "water treatment."),
    }
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="theme-color" content="#13223C">
<meta name="robots" content="{robots}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE_URL}/{canonical}">
<meta property="og:site_name" content="HA International Chemicals Trading LLC">
<meta property="og:locale" content="en_AE">
<meta property="og:image" content="{SITE_URL}/{asset(HERO_SLIDES[0])}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{SITE_URL}/{asset(HERO_SLIDES[0])}">
<link rel="canonical" href="{SITE_URL}/{canonical}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{up}styles.css">
<script type="application/ld+json">{json.dumps(org_schema)}</script>
{extra_head}
</head>
<body>
<div class="topbar"><div class="wrap">
  <div><a href="mailto:{EMAIL}">{EMAIL}</a><span class="sep">|</span>{HOURS}</div>
  <div><a href="tel:{PHONE_LINK}">Dial us: {PHONE}</a></div>
</div></div>
<header class="site">
  <div class="wrap">
    <a href="{up}index.html" class="logo" aria-label="HA International Chemicals Trading LLC — home">
      <img src="{up}{asset(LOGO)}" alt="HA International Chemicals Trading LLC" width="160" height="52">
    </a>
    <nav class="main" id="mainNav">
      {nav_links}
    </nav>
    <div class="header-cta">
      <a class="btn btn-primary" href="{up}contact-us.html" data-ripple>Get a Quote</a>
      <button class="menu-toggle" id="menuToggle" aria-label="Toggle menu" aria-controls="mainNav">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
</header>
{body}
<footer class="site">
  <div class="wrap">
    <div class="fgrid">
      <div>
        <div class="flogo"><img src="{up}{asset(LOGO)}" alt="HA International Chemicals Trading LLC"></div>
        <p style="max-width:40ch;color:#8890A0;font-size:14px">Trusted UAE supplier of industrial &amp; specialty chemicals and electrical products for construction, oil &amp; gas, and water treatment.</p>
      </div>
      <div>
        <h4>Company</h4>
        <a href="{up}about-us.html">About Us</a>
        <a href="{up}services.html">Services</a>
        <a href="{up}products.html">Products</a>
        <a href="{up}blog.html">Blog</a>
        <a href="{up}contact-us.html">Contact</a>
      </div>
      <div>
        <h4>Categories</h4>
        <a href="{up}products.html#chemicals">Industrial Chemicals</a>
        <a href="{up}electrical-technical-services.html">VFDs &amp; Electrical</a>
      </div>
      <div>
        <h4>Get in Touch</h4>
        <a href="tel:{PHONE_LINK}">{PHONE}</a>
        <a href="mailto:{EMAIL}">{EMAIL}</a>
        <a href="{WHATSAPP}" target="_blank" rel="noopener">WhatsApp Us</a>
        <span style="color:#8890A0;display:block;margin-top:6px">{ADDRESS}</span>
      </div>
    </div>
    <div class="fbottom">
      <span>© 2026 HA International Chemicals Trading LLC. All rights reserved.</span>
      <span>Design concept — not the live site.</span>
    </div>
  </div>
</footer>
<script src="{up}script.js"></script>
</body>
</html>"""


def product_card(p, depth=0, i=0):
    up = "../" * depth
    return f"""<a class="card" href="{up}product/{p['slug']}.html" data-ripple data-reveal="scale" style="--i:{i % 4}">
  <div class="thumb"><img src="{up}{product_img(p)}" alt="{p['name']}" loading="lazy"></div>
  <div class="body">
    <span class="tag">{category_badge(p['category'])}</span>
    <h3>{p['name']}</h3>
    <span class="go">View specs &amp; request quote {ARW}</span>
  </div>
</a>"""


def faq_section():
    """Visible FAQ block. FAQPage schema must mirror on-page content, so this
    renders the same questions it declares in the markup."""
    items = "".join(
        f"""<div class="faq-item" data-reveal style="--i:{n % 3}">
      <h3>{q}</h3>
      <p>{a}</p>
    </div>""" for n, (q, a) in enumerate(FAQS)
    )
    return f"""
<section class="bg-surface">
  <div class="wrap">
    <div class="section-head">
      <div>
        <div class="eyebrow" data-reveal>Common Questions</div>
        <h2 data-reveal="wipe">What buyers ask us</h2>
      </div>
    </div>
    <div class="faq-grid">{items}</div>
  </div>
</section>"""


def faq_schema():
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in FAQS
        ],
    }


def breadcrumb_schema(trail):
    """trail: list of (name, relative_url)."""
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name,
             "item": f"{SITE_URL}/{url}"}
            for i, (name, url) in enumerate(trail)
        ],
    }


def cta_band(heading, text, label="Get a Free Quote", href="contact-us.html", depth=0):
    up = "../" * depth
    return f"""
<section class="cta-band">
  <div class="wrap">
    <h2 data-reveal>{heading}</h2>
    <p data-reveal style="--i:1">{text}</p>
    <div data-reveal style="--i:2"><a class="btn btn-secondary" href="{up}{href}" data-ripple>{label} {ARW}</a></div>
  </div>
</section>"""


# ---------------------------------------------------------------- home
def build_home():
    chem = [p for p in PROD if p["category"] != "VFD"][:8]
    slides = "".join(
        f'<div class="hero__slide{" is-active" if n == 0 else ""}">'
        f'<img class="hero__img" src="{asset(s)}" alt="" '
        f'{"fetchpriority=\"high\"" if n == 0 else "loading=\"lazy\""}></div>'
        for n, s in enumerate(HERO_SLIDES) if have(s)
    )
    dots = "".join(
        f'<button class="{"is-active" if n == 0 else ""}" aria-label="Slide {n+1}"></button>'
        for n, s in enumerate(HERO_SLIDES) if have(s)
    )
    counters = "".join(
        f'<div data-reveal style="--i:{n}"><b data-count="{c["value"]}">0</b><span>{c["label"]}</span></div>'
        for n, c in enumerate(CONTENT["counters"])
    )
    bars = "".join(
        f"""<div class="progress" data-reveal data-progress="{b['value']}" style="--i:{n}">
      <div class="progress__top"><span>{b['label']}</span><span data-progress-num>0%</span></div>
      <div class="progress__track"><div class="progress__fill"></div></div>
    </div>"""
        for n, b in enumerate(CONTENT["progress"])
    )

    body = f"""
<section class="hero">
  <div class="hero__slides">{slides}</div>
  <div class="wrap">
    <div>
      <div class="eyebrow on-dark">Abu Dhabi, UAE · Since 1986</div>
      <h1>Leading Chemical Supplier in the <em>UAE</em></h1>
      <p class="lead">Premium chemical solutions — industrial and specialty chemicals plus electrical and VFD equipment for construction, oil &amp; gas, water treatment, and manufacturing.</p>
      <div class="cta-row">
        <a class="btn btn-primary" href="products.html" data-ripple>Discover More {ARW}</a>
        <a class="btn btn-ghost" href="contact-us.html" data-ripple>Get a Free Quote</a>
      </div>
    </div>
    <div class="hero-stats">
      <div><b>38+</b><span>Years in the Trade</span></div>
      <div><b>{len(PROD)}</b><span>Products Stocked</span></div>
      <div><b>UAE</b><span>&amp; International Reach</span></div>
      <div><b>24h</b><span>Quote Turnaround</span></div>
    </div>
  </div>
  <div class="hero__dots">{dots}</div>
</section>

<section>
  <div class="wrap">
    <div class="section-head">
      <div>
        <div class="eyebrow" data-reveal>What We Supply</div>
        <h2 data-reveal="wipe">Featured chemicals &amp; materials</h2>
      </div>
      <a class="btn btn-outline" href="products.html" data-reveal data-ripple>View All Products {ARW}</a>
    </div>
    <div class="grid grid-4">
      {"".join(product_card(p, 0, n) for n, p in enumerate(chem))}
    </div>
  </div>
</section>

<section class="bg-surface">
  <div class="wrap">
    <div class="section-head">
      <div>
        <div class="eyebrow" data-reveal>Industries We Serve</div>
        <h2 data-reveal="wipe">Built for demanding sectors</h2>
      </div>
    </div>
    <div class="industry-row" data-reveal>
      <article class="industry-card"><div class="industry-card__media"><img src="assets/img/sector-construction.webp" alt="UAE construction site with high-rise development and cranes" loading="lazy"></div><h4>Construction</h4></article>
      <article class="industry-card"><div class="industry-card__media"><img src="assets/img/sector-oil-gas.webp" alt="Modern oil and gas processing facility" loading="lazy"></div><h4>Oil &amp; Gas</h4></article>
      <article class="industry-card"><div class="industry-card__media"><img src="assets/img/sector-water-treatment.webp" alt="Industrial water treatment and filtration facility" loading="lazy"></div><h4>Water Treatment</h4></article>
      <article class="industry-card"><div class="industry-card__media"><img src="assets/img/sector-manufacturing.webp" alt="Clean automated manufacturing facility" loading="lazy"></div><h4>Manufacturing</h4></article>
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
      <div style="margin-top:34px">{bars}</div>
    </div>
    <div class="shot" data-reveal="right">
      <img src="{asset('img_bg_business_Home01-STE4HQX-e1686194116880.webp')}" alt="HA International Chemicals operations" loading="lazy">
    </div>
  </div>
</section>

<section class="bg-navy">
  <div class="wrap">
    <div class="section-head">
      <div>
        <div class="eyebrow on-dark" data-reveal>Industry Achievements</div>
        <h2 data-reveal="wipe">Best construction &amp; building business</h2>
      </div>
    </div>
    <div class="counter-row">{counters}</div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head">
      <div>
        <div class="eyebrow" data-reveal>What Else We Do</div>
        <h2 data-reveal="wipe">Committed to exceptional service</h2>
        <p data-reveal style="--i:1">We offer an extensive selection of electrical products and chemicals, catering to various industries' needs.</p>
      </div>
    </div>
    <div class="grid grid-3">
      <div class="feature" data-reveal style="--i:0"><div class="num">01</div><div><h4>Timely Delivery</h4><p>Our team of experienced professionals possesses in-depth knowledge and technical expertise in the electrical and chemical fields.</p></div></div>
      <div class="feature" data-reveal style="--i:1"><div class="num">02</div><div><h4>Quality Assurance</h4><p>At HA International Chemicals Trading LLC, quality is our top priority. We partner with reputable manufacturers and suppliers to ensure that all our products meet strict quality standards and comply with safety regulations.</p></div></div>
      <div class="feature" data-reveal style="--i:2"><div class="num">03</div><div><h4>Extensive Product Range</h4><p>From cutting-edge electrical equipment to premium-grade chemicals, we've got you covered.</p></div></div>
      <div class="feature" data-reveal style="--i:3"><div class="num">04</div><div><h4>Technical Expertise</h4><p>We can assist you in finding the right products that best suit your specific requirements.</p></div></div>
      <div class="feature" data-reveal style="--i:4"><div class="num">05</div><div><h4>Competitive Pricing</h4><p>Direct sourcing relationships keep our pricing sharp without compromising on quality.</p></div></div>
      <div class="feature" data-reveal style="--i:5"><div class="num">06</div><div><h4>38+ Years Trading</h4><p>Four decades of relationships across UAE construction, industrial, and energy sectors.</p></div></div>
    </div>
  </div>
</section>
{faq_section()}
{cta_band("Need a chemical or spec sheet fast?",
          "Send us your requirement and we'll come back with pricing and availability, usually within one business day.")}
"""
    write("index.html", base(
        "HA International Chemicals Trading LLC — Chemical Supplier in UAE",
        "UAE supplier of industrial & specialty chemicals and electrical/VFD products for construction, oil & gas, and water treatment. 38+ years in Abu Dhabi.",
        body, active="index.html", canonical="",
        extra_head=f'<script type="application/ld+json">{json.dumps(faq_schema())}</script>'))


# ---------------------------------------------------------------- products
def build_products():
    chem = [p for p in PROD if p["category"] != "VFD"]
    vfd = [p for p in PROD if p["category"] == "VFD"]
    body = f"""
<section class="page-hero">
  <div class="wrap">
    <div class="eyebrow on-dark">Catalogue</div>
    <h1>Products</h1>
    <p>{len(PROD)} chemicals and electrical products, stocked and ready to quote.</p>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="cat-strip">
      <a href="#chemicals" class="cat-pill active" data-ripple>Industrial Chemicals ({len(chem)})</a>
      <a href="#vfd" class="cat-pill" data-ripple>VFDs &amp; Electrical ({len(vfd)})</a>
    </div>
    <h2 id="chemicals" style="font-size:24px;margin-bottom:22px" data-reveal="wipe">Industrial Chemicals</h2>
    <div class="grid grid-4" style="margin-bottom:68px">
      {"".join(product_card(p, 0, n) for n, p in enumerate(chem))}
    </div>
    <h2 id="vfd" style="font-size:24px;margin-bottom:22px" data-reveal="wipe">VFDs &amp; Electrical</h2>
    <div class="grid grid-4">
      {"".join(product_card(p, 0, n) for n, p in enumerate(vfd))}
    </div>
  </div>
</section>
{cta_band("Can't find what you need?",
          "Our catalogue keeps growing — tell us the chemical or spec you're after and we'll source it.",
          "Ask Our Team")}
"""
    write("products.html", base(
        "Products — Industrial Chemicals & VFDs | HA International Chemicals",
        "Browse HA International's full catalogue: drilling & cementing chemicals, water treatment chemicals, and VFDs/electrical equipment.",
        body, active="products.html", canonical="products.html"))


# ---------------------------------------------------------------- VFD page
def build_electrical():
    vfd = [p for p in PROD if p["category"] == "VFD"]
    extra = [p for p in PROD if p["category"] != "VFD"][:4]
    body = f"""
<section class="page-hero">
  <div class="wrap">
    <div class="eyebrow on-dark">Electrical &amp; Technical</div>
    <h1>VFD &amp; Electrical Products</h1>
    <p>Variable frequency drives and electrical equipment, supplied and supported by our technical team.</p>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="section-head">
      <div><div class="eyebrow" data-reveal>In Stock</div><h2 data-reveal="wipe">Variable frequency drives</h2></div>
    </div>
    <div class="grid grid-4">
      {"".join(product_card(p, 0, n) for n, p in enumerate(vfd))}
    </div>
  </div>
</section>
<section class="bg-surface">
  <div class="wrap">
    <div class="section-head">
      <div><div class="eyebrow" data-reveal>Also Available</div><h2 data-reveal="wipe">Chemicals from our catalogue</h2></div>
      <a class="btn btn-outline" href="products.html" data-reveal data-ripple>All Products {ARW}</a>
    </div>
    <div class="grid grid-4">
      {"".join(product_card(p, 0, n) for n, p in enumerate(extra))}
    </div>
  </div>
</section>
{cta_band("Need a drive sized for your motor?",
          "Send us the motor rating and duty cycle — we'll specify the right VFD and quote it.",
          "Talk to an Engineer")}
"""
    write("electrical-technical-services.html", base(
        "VFD & Electrical Products — HA International Chemicals",
        "Variable frequency drives and electrical equipment supplied across the UAE by HA International Chemicals Trading LLC.",
        body, active="electrical-technical-services.html",
        canonical="electrical-technical-services.html"))


# ---------------------------------------------------------------- product detail
def build_product_pages():
    for p in PROD:
        short = clean(p["short_description"])
        full = clean(p["description"])
        # spec tables must scroll on their own, never the page body
        merged = (short + full).replace(
            '<table class="spec-table">', '<div class="table-scroll"><table class="spec-table">'
        ).replace("</table>", "</table></div>")

        related = [r for r in PROD if r["category"] == p["category"] and r["slug"] != p["slug"]][:4]
        plain = re.sub(r"\s+", " ", re.sub("<[^>]+>", " ", short + full)).strip()
        schema = {
            "@context": "https://schema.org",
            "@type": "Product",
            "name": p["name"],
            "category": category_badge(p["category"]).replace("&amp;", "&"),
            "image": f"{SITE_URL}/{product_img(p)}",
            "brand": {"@type": "Organization", "name": "HA International Chemicals Trading LLC"},
            "description": plain[:500],
            "offers": {
                "@type": "Offer",
                "availability": "https://schema.org/InStock",
                "priceCurrency": "AED",
                "url": f"{SITE_URL}/product/{p['slug']}.html",
                "seller": {"@type": "Organization",
                           "name": "HA International Chemicals Trading LLC"},
            },
        }
        crumbs = breadcrumb_schema([
            ("Home", ""),
            ("Products", "products.html"),
            (p["name"], f"product/{p['slug']}.html"),
        ])
        related_block = f"""
<section class="bg-surface">
  <div class="wrap">
    <div class="section-head"><div><div class="eyebrow" data-reveal>Related</div><h2 data-reveal="wipe" style="font-size:26px">More {category_badge(p['category'])}s</h2></div></div>
    <div class="grid grid-4">{"".join(product_card(r, 1, n) for n, r in enumerate(related))}</div>
  </div>
</section>""" if related else ""

        body = f"""
<div class="breadcrumb"><div class="wrap"><a href="../index.html">Home</a> / <a href="../products.html">Products</a> / {p['name']}</div></div>
<section class="pd-grid wrap">
  <div class="pd-media">
    <div class="frame" data-reveal="left"><img src="../{product_img(p)}" alt="{p['name']}"></div>
    <div class="quote-box" data-reveal style="--i:1">
      <h4>Request pricing</h4>
      <p>Get a quote with current pricing, MOQ, and lead time for {p['name']}.</p>
      <a class="btn btn-primary" href="../contact-us.html?product={p['slug']}" data-ripple style="width:100%">Request a Quote {ARW}</a>
    </div>
  </div>
  <div class="pd-info">
    <span class="tag" data-reveal>{category_badge(p['category'])}</span>
    <h1 data-reveal style="--i:1">{p['name']}</h1>
    <div class="pd-body" data-reveal style="--i:2">
      {merged}
    </div>
    <div class="pd-actions" data-reveal style="--i:3">
      <a class="btn btn-secondary" href="tel:{PHONE_LINK}" data-ripple>Call {PHONE}</a>
      <a class="btn btn-outline" href="{WHATSAPP}" target="_blank" rel="noopener" data-ripple>WhatsApp</a>
    </div>
  </div>
</section>
{related_block}
"""
        desc = re.sub(r"\s+", " ", re.sub("<[^>]+>", " ", short)).strip()[:155]
        write(f"product/{p['slug']}.html", base(
            f"{p['name']} — HA International Chemicals",
            desc or f"{p['name']} supplied by HA International Chemicals Trading LLC, UAE.",
            body, active="products.html", canonical=f"product/{p['slug']}.html",
            extra_head=(f'<script type="application/ld+json">{json.dumps(schema)}</script>\n'
                        f'<script type="application/ld+json">{json.dumps(crumbs)}</script>'),
            depth=1))


# ---------------------------------------------------------------- services
def build_services():
    intro = CONTENT["services_intro"]
    items = ""
    for n, s in enumerate(CONTENT["services"]):
        paras = "".join(f"<p>{para}</p>" for para in s["paragraphs"])
        items += f"""<div class="service-item" data-reveal style="--i:{n}">
      <div class="ic">{n+1:02d}</div>
      <div><h3>{s['title']}</h3>{paras}</div>
    </div>"""

    body = f"""
<section class="page-hero">
  <div class="wrap">
    <div class="eyebrow on-dark">{intro['eyebrow']}</div>
    <h1>{intro['heading']}</h1>
    <p>{intro['lede']}</p>
  </div>
</section>
<section>
  <div class="wrap" style="max-width:920px">
    <div class="section-head">
      <div><div class="eyebrow" data-reveal>Services Offered</div><h2 data-reveal="wipe">What we do</h2></div>
      <a class="btn btn-outline" href="products.html" data-reveal data-ripple>View Products {ARW}</a>
    </div>
    {items}
  </div>
</section>
{cta_band("Have a project spec in hand?",
          "Send it over and we'll respond with pricing, availability, and lead time.")}
"""
    write("services.html", base(
        "Services — HA International Chemicals Trading LLC",
        "Electrical installation, earthing systems, cathodic protection, ELV and telecommunication installation across the UAE.",
        body, active="services.html", canonical="services.html"))


# ---------------------------------------------------------------- about
def build_about():
    yrs = CONTENT["years_experience"]
    photos = "".join(
        f'<figure data-reveal="scale" style="--i:{n}"><img src="{asset(f)}" alt="HA International Chemicals facility" loading="lazy"></figure>'
        for n, f in enumerate(FACILITY_PHOTOS) if have(f)
    )
    counters = "".join(
        f'<div data-reveal style="--i:{n}"><b data-count="{c["value"]}">0</b><span>{c["label"]}</span></div>'
        for n, c in enumerate(CONTENT["counters"])
    )
    body = f"""
<section class="page-hero">
  <div class="wrap">
    <div class="eyebrow on-dark">About Us</div>
    <h1>Four decades in the trade.</h1>
    <p>Your trusted partner in the world of chemicals, engineering products and services.</p>
  </div>
</section>
<section>
  <div class="wrap about-grid">
    <div>
      <div class="eyebrow" data-reveal>Get to Know HA International</div>
      <h2 data-reveal="wipe">The best industry &amp; factory business</h2>
      <h4 data-reveal style="--i:1;font-family:var(--mono);font-size:12.5px;letter-spacing:.08em;color:var(--grey);text-transform:uppercase">Committed to providing our customers with exceptional product and service.</h4>
      <p class="lede" data-reveal style="--i:2">Your trusted partner in the world of chemicals, engineering products and services. Under the patronage of <strong>Mr. Adel Saif Amer Hasan Aljaberi</strong>, with a legacy of excellence and innovation spanning over 4 decades, we are committed to delivering superior solutions to meet the dynamic needs of industries in the region.</p>
      <p class="lede" data-reveal style="--i:3">We understand that the journey to this ideal future is multifaceted, requiring dedication, vision, and a clear sense of direction. At HA International Chemicals Trading LLC, we strive to stay at the forefront of technological advancements while nurturing a deep-rooted sense of responsibility towards our planet. We are acutely aware that progress is not merely measured in profit margins but in the positive change we bring to our world.</p>
      <div class="counter-row" style="margin-top:34px">
        <div data-reveal><b data-count="{yrs}">0</b><span>Years of Experience</span></div>
      </div>
    </div>
    <div class="shot" data-reveal="right">
      <img src="{asset('img_about_Home01-7DPAR8H.webp')}" alt="HA International Chemicals warehouse operations" loading="lazy">
    </div>
  </div>
</section>

<section class="bg-navy">
  <div class="wrap">
    <div class="section-head">
      <div><div class="eyebrow on-dark" data-reveal>Industry Achievements</div><h2 data-reveal="wipe">Quality, affordable, manufacturing and industrial services</h2></div>
    </div>
    <div class="counter-row">{counters}</div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head">
      <div><div class="eyebrow" data-reveal>Our Operations</div><h2 data-reveal="wipe">Inside the business</h2></div>
    </div>
    <div class="photo-strip">{photos}</div>
  </div>
</section>

<section class="bg-surface">
  <div class="wrap">
    <div class="section-head"><div><div class="eyebrow" data-reveal>What Drives Us</div><h2 data-reveal="wipe">Quality, range, and expertise</h2></div></div>
    <div class="grid grid-3">
      <div class="feature" data-reveal style="--i:0"><div class="num">01</div><div><h4>Quality Assurance</h4><p>At HA International Chemicals Trading LLC, quality is our top priority. We partner with reputable manufacturers and suppliers to ensure that all our products meet strict quality standards and comply with safety regulations.</p></div></div>
      <div class="feature" data-reveal style="--i:1"><div class="num">02</div><div><h4>Extensive Product Range</h4><p>We offer an extensive selection of electrical products and chemicals, catering to various industries' needs.</p></div></div>
      <div class="feature" data-reveal style="--i:2"><div class="num">03</div><div><h4>Technical Expertise</h4><p>Our team of experienced professionals possesses in-depth knowledge and technical expertise in the electrical and chemical fields.</p></div></div>
    </div>
  </div>
</section>
{cta_band("Work with a supplier that shows up on time.",
          "Tell us what your project needs — we'll quote it fast.")}
"""
    write("about-us.html", base(
        "About Us — HA International Chemicals Trading LLC",
        "38+ years supplying industrial chemicals and electrical products across the UAE. Learn about HA International Chemicals Trading LLC.",
        body, active="about-us.html", canonical="about-us.html"))


# ---------------------------------------------------------------- blog
def post_img(p, depth=0):
    up = "../" * depth
    if p.get("image"):
        stem = os.path.splitext(re.sub(r"\?.*$", "", p["image"].split("/")[-1]))[0]
        if have(stem + ".webp"):
            return up + asset(stem + ".webp")
    return up + asset("placeholder.webp")


def pretty_date(iso):
    y, m, d = iso.split("-")
    months = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"]
    return f"{int(d)} {months[int(m) - 1]} {y}"


def post_label(p):
    """Their posts are all filed under "Uncategorized", which reads as a defect
    on the page. Fall back to a neutral label until they categorise them."""
    for c in p.get("categories") or []:
        if c.strip().lower() != "uncategorized":
            return c
    return "Article"


def post_card(p, depth=0, i=0):
    up = "../" * depth
    cat = post_label(p)
    return f"""<a class="card post-card" href="{up}blog/{p['slug']}.html" data-ripple data-reveal="scale" style="--i:{i % 3}">
  <div class="post-thumb"><img src="{post_img(p, depth)}" alt="{p['title']}" loading="lazy"></div>
  <div class="body">
    <span class="tag">{cat} &middot; {pretty_date(p['date'])}</span>
    <h3>{p['title']}</h3>
    <span class="go">Read article {ARW}</span>
  </div>
</a>"""


def build_blog():
    if not POSTS:
        cards = """<div class="empty-state" data-reveal>
      <div class="ic">📝</div><h3>No posts published yet</h3>
      <p>This is where articles will appear.</p>
    </div>"""
    else:
        cards = f'<div class="grid grid-3">{"".join(post_card(p, 0, n) for n, p in enumerate(POSTS))}</div>'

    body = f"""
<section class="page-hero">
  <div class="wrap">
    <div class="eyebrow on-dark">Blog</div>
    <h1>Insights &amp; updates</h1>
    <p>Technical notes, product guides and industry updates from our team.</p>
  </div>
</section>
<section>
  <div class="wrap">
    {cards}
  </div>
</section>
{cta_band("Need a product from one of these guides?",
          "Tell us your requirement and we'll come back with pricing and availability.")}
"""
    write("blog.html", base(
        "Blog — HA International Chemicals Trading LLC",
        "Technical guides on chemical selection and supply in the UAE, from HA International Chemicals Trading LLC.",
        body, active="blog.html", canonical="blog.html"))


def build_post_pages():
    for n, p in enumerate(POSTS):
        article = clean(p["content"]).replace(
            '<table class="spec-table">',
            '<div class="table-scroll"><table class="spec-table">'
        ).replace("</table>", "</table></div>")
        related = [r for r in POSTS if r["slug"] != p["slug"]][:3]
        plain = re.sub(r"\s+", " ", re.sub("<[^>]+>", " ", article)).strip()

        schema = {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": p["title"],
            "datePublished": p["date"],
            "dateModified": p["date"],
            "image": f"{SITE_URL}/{post_img(p).lstrip('./')}",
            "description": plain[:300],
            "author": {"@type": "Organization",
                       "name": "HA International Chemicals Trading LLC"},
            "publisher": {
                "@type": "Organization",
                "name": "HA International Chemicals Trading LLC",
                "logo": {"@type": "ImageObject", "url": f"{SITE_URL}/{asset(LOGO)}"},
            },
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": f"{SITE_URL}/blog/{p['slug']}.html",
            },
        }
        crumbs = breadcrumb_schema([
            ("Home", ""), ("Blog", "blog.html"),
            (p["title"], f"blog/{p['slug']}.html"),
        ])

        related_block = f"""
<section class="bg-surface">
  <div class="wrap">
    <div class="section-head"><div><div class="eyebrow" data-reveal>Keep reading</div><h2 data-reveal="wipe" style="font-size:26px">More guides</h2></div></div>
    <div class="grid grid-3">{"".join(post_card(r, 1, i) for i, r in enumerate(related))}</div>
  </div>
</section>""" if related else ""

        cat = post_label(p)
        body = f"""
<div class="breadcrumb"><div class="wrap"><a href="../index.html">Home</a> / <a href="../blog.html">Blog</a> / {p['title'][:44]}</div></div>
<article>
  <div class="wrap post-wrap">
    <span class="tag" data-reveal>{cat} &middot; {pretty_date(p['date'])}</span>
    <h1 data-reveal style="--i:1">{p['title']}</h1>
    <div class="post-hero" data-reveal style="--i:2"><img src="{post_img(p, 1)}" alt="{p['title']}"></div>
    <div class="pd-body post-body" data-reveal style="--i:3">
      {article}
    </div>
    <div class="pd-actions" data-reveal>
      <a class="btn btn-primary" href="../contact-us.html" data-ripple>Request a Quote {ARW}</a>
      <a class="btn btn-outline" href="../products.html" data-ripple>Browse Products</a>
    </div>
  </div>
</article>
{related_block}
"""
        write(f"blog/{p['slug']}.html", base(
            f"{p['title']} — HA International Chemicals",
            (p.get("excerpt") or plain)[:155],
            body, active="blog.html", canonical=f"blog/{p['slug']}.html",
            extra_head=(f'<script type="application/ld+json">{json.dumps(schema)}</script>\n'
                        f'<script type="application/ld+json">{json.dumps(crumbs)}</script>'),
            depth=1))


# ---------------------------------------------------------------- contact
def build_contact():
    body = f"""
<section class="page-hero">
  <div class="wrap">
    <div class="eyebrow on-dark">Contact</div>
    <h1>Let's talk about your requirement</h1>
    <p>Feel free to write our team anytime — we usually respond within one business day.</p>
  </div>
</section>
<section>
  <div class="wrap contact-grid">
    <div>
      <div class="contact-card" data-reveal style="--i:0"><h4>Phone</h4><a href="tel:{PHONE_LINK}">{PHONE}</a></div>
      <div class="contact-card" data-reveal style="--i:1"><h4>Email</h4><a href="mailto:{EMAIL}">{EMAIL}</a></div>
      <div class="contact-card" data-reveal style="--i:2"><h4>Address</h4><p>{ADDRESS}</p></div>
      <div class="contact-card" data-reveal style="--i:3"><h4>Hours</h4><p>{HOURS}</p></div>
      <div class="contact-card" data-reveal style="--i:4"><h4>WhatsApp</h4><a href="{WHATSAPP}" target="_blank" rel="noopener">Message us on WhatsApp</a></div>
    </div>
    <form class="contact-card" style="background:#fff" data-reveal="right" onsubmit="return false">
      <h4 style="margin-bottom:22px">Request a Quote</h4>
      <div class="form-row">
        <div class="field"><label for="fn">First Name</label><input id="fn" type="text" placeholder="John"></div>
        <div class="field"><label for="ln">Last Name</label><input id="ln" type="text" placeholder="Smith"></div>
      </div>
      <div class="form-row">
        <div class="field"><label for="em">Email</label><input id="em" type="email" placeholder="you@company.com"></div>
        <div class="field"><label for="mo">Mobile No.</label><input id="mo" type="tel" placeholder="+971 ..."></div>
      </div>
      <div class="field" style="margin-bottom:18px"><label for="ms">What do you need?</label><textarea id="ms" rows="5" placeholder="Product, quantity, and any spec details..."></textarea></div>
      <button type="submit" class="btn btn-primary" data-ripple style="width:100%">Send Request {ARW}</button>
      <p style="font-size:12px;color:var(--grey);margin:14px 0 0;text-align:center">Concept demo — this form is not yet wired to a mailbox.</p>
    </form>
  </div>
</section>
"""
    write("contact-us.html", base(
        "Contact Us — HA International Chemicals Trading LLC",
        "Get in touch with HA International Chemicals Trading LLC in Abu Dhabi, UAE — request a quote by phone, email, or WhatsApp.",
        body, active="contact-us.html", canonical="contact-us.html"))


# ---------------------------------------------------------------- 404
def build_404():
    body = f"""
<div class="notfound">
  <div class="code">404</div>
  <h1>Page not found</h1>
  <p>The page you're looking for has moved or doesn't exist.</p>
  <a class="btn btn-primary" href="index.html" data-ripple>Back to Home {ARW}</a>
</div>
"""
    write("404.html", base("Page Not Found — HA International Chemicals",
                           "Page not found.", body, canonical="404.html"))


# ---------------------------------------------------------------- SEO files
TOP_PAGES = [
    ("", "1.0", "weekly"),
    ("products.html", "0.9", "weekly"),
    ("electrical-technical-services.html", "0.8", "monthly"),
    ("services.html", "0.8", "monthly"),
    ("about-us.html", "0.6", "monthly"),
    ("contact-us.html", "0.7", "monthly"),
    ("blog.html", "0.5", "weekly"),
]


def build_sitemap():
    today = datetime.date.today().isoformat()
    urls = []
    for path, priority, freq in TOP_PAGES:
        urls.append((f"{SITE_URL}/{path}", priority, freq))
    for p in PROD:
        urls.append((f"{SITE_URL}/product/{p['slug']}.html", "0.8", "monthly"))
    for p in POSTS:
        urls.append((f"{SITE_URL}/blog/{p['slug']}.html", "0.7", "monthly"))

    entries = "\n".join(
        f"  <url>\n"
        f"    <loc>{loc}</loc>\n"
        f"    <lastmod>{today}</lastmod>\n"
        f"    <changefreq>{freq}</changefreq>\n"
        f"    <priority>{pri}</priority>\n"
        f"  </url>"
        for loc, pri, freq in urls
    )
    write("sitemap.xml",
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          f"{entries}\n</urlset>\n")
    return len(urls)


def build_robots():
    if not PRODUCTION:
        # the concept must never be crawled — it would duplicate the client's
        # own content and compete with their real domain
        write("robots.txt", "User-agent: *\nDisallow: /\n")
        return
    # Assistant crawlers are named explicitly. A blanket allow already covers
    # them, but several of these respect only their own token, and being
    # explicit makes the intent auditable later.
    agents = [
        "GPTBot",            # OpenAI / ChatGPT
        "OAI-SearchBot",     # ChatGPT search
        "ChatGPT-User",      # ChatGPT live browsing
        "ClaudeBot",         # Anthropic
        "anthropic-ai",
        "Claude-Web",
        "PerplexityBot",
        "Google-Extended",   # Gemini grounding
        "Applebot-Extended",
        "CCBot",             # Common Crawl — feeds many models
        "Bingbot",
        "Googlebot",
    ]
    blocks = "\n\n".join(f"User-agent: {a}\nAllow: /" for a in agents)
    write("robots.txt",
          f"User-agent: *\nAllow: /\n\n{blocks}\n\nSitemap: {SITE_URL}/sitemap.xml\n")


def build_llms_txt():
    """Emerging convention: a plain-text brief models can read directly."""
    chem = [p for p in PROD if p["category"] != "VFD"]
    vfd = [p for p in PROD if p["category"] == "VFD"]
    chem_links = "\n".join(
        f"- [{p['name']}]({SITE_URL}/product/{p['slug']}.html)" for p in chem)
    vfd_links = "\n".join(
        f"- [{p['name']}]({SITE_URL}/product/{p['slug']}.html)" for p in vfd)
    faq_lines = "\n\n".join(f"**{q}**\n{a}" for q, a in FAQS)
    post_links = "\n".join(
        f"- [{p['title']}]({SITE_URL}/blog/{p['slug']}.html)" for p in POSTS)

    write("llms.txt", f"""# HA International Chemicals Trading LLC

> Supplier of industrial and specialty chemicals and electrical/VFD products,
> based in Abu Dhabi, United Arab Emirates. Serving construction, oil and gas,
> water treatment and manufacturing sectors across the UAE and international
> markets for over 38 years.

## Contact
- Address: {ADDRESS}
- Phone: {PHONE}
- Email: {EMAIL}
- Hours: {HOURS}

## Industrial Chemicals ({len(chem)} products)
{chem_links}

## VFD & Electrical ({len(vfd)} products)
{vfd_links}

## Services
{chr(10).join('- ' + s['title'] for s in CONTENT['services'])}

## Frequently Asked Questions

{faq_lines}

## Articles
{post_links}

## Pages
- [Home]({SITE_URL}/)
- [Products]({SITE_URL}/products.html)
- [VFD & Electrical]({SITE_URL}/electrical-technical-services.html)
- [Services]({SITE_URL}/services.html)
- [About]({SITE_URL}/about-us.html)
- [Contact]({SITE_URL}/contact-us.html)
""")


# ---------------------------------------------------------------- io
def write(relpath, content):
    dest = os.path.join(OUT, relpath)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(content)


def copy_assets():
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(OUT, "assets"))
    for f in ("styles.css", "script.js"):
        shutil.copy(os.path.join(ROOT, f), os.path.join(OUT, f))


if __name__ == "__main__":
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    build_home()
    build_products()
    build_electrical()
    build_product_pages()
    build_services()
    build_about()
    build_blog()
    build_post_pages()
    build_contact()
    build_404()
    n_urls = build_sitemap()
    build_robots()
    build_llms_txt()
    copy_assets()
    mode = "PRODUCTION (indexable)" if PRODUCTION else "concept (noindex)"
    print(f"Build complete -> {OUT}")
    print(f"  mode: {mode}")
    print(f"  base URL: {SITE_URL}")
    print(f"  {len(PROD)} product pages + 8 top-level pages")
    print(f"  sitemap.xml: {n_urls} URLs · robots.txt · llms.txt")
