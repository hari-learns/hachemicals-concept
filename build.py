#!/usr/bin/env python3
"""Static concept-site generator for HA International Chemicals Trading LLC.
Reads scraped src_data/*.json, writes a self-contained static site to ./site."""
import json, os, re, shutil
from clean_html import clean

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "site")
PROD = json.load(open(os.path.join(ROOT, "src_data/products.json")))

PHONE = "+971 50 228 7866"
PHONE_LINK = "+971502287866"
WHATSAPP = "https://wa.me/971502287866"
EMAIL = "sales@hachemicals.com"
ADDRESS = "M02, United Arab Bank Building, Al Danah, Abu Dhabi, UAE"
HOURS = "Mon – Sat, 10:00 – 18:30 (Sunday closed)"

NAV = [
    ("index.html", "Home"),
    ("products.html", "Products"),
    ("services.html", "Services"),
    ("about-us.html", "About"),
    ("contact-us.html", "Contact"),
]

# ---- image filename fixups (source URLs -> local /assets/img/*) ----
def img(name):
    return f"assets/img/{name}"

CHEM_IMG = {
    "cenosphere": "cenosphere.png",
    "drilling-detergent": "DRILLING-DETERGENT.png",
    "fly-ash-1-4-ton-bag": "FLYASH.png",
    "ferric-chloride": "ferric-chloride.png",
    "dea": "DEA.png",
    "defoam-silicon-based": "silicon-defomer.png",
}
PLACEHOLDER = "placeholder.png"

def product_img(p):
    if p["images"]:
        fname = re.sub(r"\?.*$", "", p["images"][0].split("/")[-1])
        local = os.path.join(ROOT, "build_src/img", fname)
        if os.path.exists(local):
            return img(fname)
    return img(PLACEHOLDER)


def base(title, description, body, active="", canonical="", extra_head="", body_class=""):
    nav_links = "\n".join(
        f'<a href="{href}"{" class=\"active\"" if href==active else ""}>{label}</a>'
        for href, label in NAV
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="https://hachemicals-concept.example/{canonical}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
{extra_head}
</head>
<body class="{body_class}">
<div class="topbar"><div class="wrap">
  <div><a href="mailto:{EMAIL}">{EMAIL}</a><span class="sep">|</span>{HOURS}</div>
  <div><a href="tel:{PHONE_LINK}">Dial us: {PHONE}</a></div>
</div></div>
<header class="site">
  <div class="wrap">
    <a href="index.html" class="logo">
      <span class="mark">HA</span>
      <span>HA International<small>Chemicals Trading LLC</small></span>
    </a>
    <nav class="main" id="mainNav">
      {nav_links}
    </nav>
    <div class="header-cta">
      <a class="btn btn-primary" href="contact-us.html">Get a Quote</a>
      <button class="menu-toggle" id="menuToggle" aria-label="Menu"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>
{body}
<footer class="site">
  <div class="wrap">
    <div class="fgrid">
      <div>
        <div class="flogo">HA International Chemicals Trading LLC</div>
        <p style="max-width:38ch;color:#8890A0;font-size:14px">Trusted UAE supplier of industrial &amp; specialty chemicals and electrical products for construction, oil &amp; gas, and water treatment — serving the region for over four decades.</p>
      </div>
      <div>
        <h4>Company</h4>
        <a href="about-us.html">About Us</a>
        <a href="services.html">Services</a>
        <a href="products.html">Products</a>
        <a href="contact-us.html">Contact</a>
      </div>
      <div>
        <h4>Categories</h4>
        <a href="products.html#chemicals">Industrial Chemicals</a>
        <a href="products.html#vfd">VFDs &amp; Electrical</a>
      </div>
      <div>
        <h4>Get in Touch</h4>
        <a href="tel:{PHONE_LINK}">{PHONE}</a>
        <a href="mailto:{EMAIL}">{EMAIL}</a>
        <a href="{WHATSAPP}" target="_blank" rel="noopener">WhatsApp Us</a>
        <a href="#" style="color:#8890A0">{ADDRESS}</a>
      </div>
    </div>
    <div class="fbottom">
      <span>© 2026 HA International Chemicals Trading LLC. All rights reserved.</span>
      <span>Design concept — not the live site.</span>
    </div>
  </div>
</footer>
<script src="script.js"></script>
</body>
</html>"""


def category_badge(cat):
    return "VFD &amp; Electrical" if cat == "VFD" else "Industrial Chemical"


def product_card(p):
    return f"""<a class="card" href="product/{p['slug']}.html">
  <div class="thumb"><img src="{product_img(p)}" alt="{p['name']}" loading="lazy"></div>
  <div class="body">
    <span class="tag">{category_badge(p['category'])}</span>
    <h3>{p['name']}</h3>
    <span class="go">View specs &amp; request quote →</span>
  </div>
</a>"""


# ---------------------------------------------------------------- HOMEPAGE
def build_home():
    chem = [p for p in PROD if p["category"] != "VFD"][:8]
    featured_cards = "\n".join(product_card(p) for p in chem)
    body = f"""
<section class="hero">
  <div class="wrap">
    <div>
      <div class="eyebrow" style="color:#FF9457">Since 1986 · Abu Dhabi, UAE</div>
      <h1>Industrial chemicals &amp; electrical solutions, <em>delivered on time.</em></h1>
      <p class="lead">HA International Chemicals Trading LLC supplies drilling, cementing, and water-treatment chemicals, plus electrical &amp; VFD equipment, to construction, oil &amp; gas, and industrial clients across the UAE.</p>
      <div class="cta-row">
        <a class="btn btn-primary" href="products.html">Browse Products</a>
        <a class="btn btn-ghost" href="contact-us.html">Request a Quote</a>
      </div>
    </div>
    <div class="hero-stats">
      <div><b>38+</b><span>Years in the Trade</span></div>
      <div><b>26+</b><span>Products Stocked</span></div>
      <div><b>UAE</b><span>&amp; International Reach</span></div>
      <div><b>24h</b><span>Quote Turnaround</span></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head">
      <div>
        <div class="eyebrow">What We Supply</div>
        <h2>Featured chemicals &amp; materials</h2>
      </div>
      <a class="btn btn-dark" href="products.html">View All Products</a>
    </div>
    <div class="grid grid-4">
      {featured_cards}
    </div>
  </div>
</section>

<section class="bg-surface">
  <div class="wrap">
    <div class="section-head">
      <div>
        <div class="eyebrow">Industries We Serve</div>
        <h2>Built for demanding sectors</h2>
      </div>
    </div>
    <div class="industry-row">
      <div><div class="ic">🏗️</div><h4>Construction</h4></div>
      <div><div class="ic">🛢️</div><h4>Oil &amp; Gas</h4></div>
      <div><div class="ic">💧</div><h4>Water Treatment</h4></div>
      <div><div class="ic">⚙️</div><h4>Manufacturing</h4></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head">
      <div><div class="eyebrow">Why HA International</div><h2>Reliability, at industrial scale</h2></div>
    </div>
    <div class="grid grid-3">
      <div class="feature"><div class="num">01</div><div><h4>Quality Assurance</h4><p>We partner only with reputable manufacturers, so every batch meets strict quality &amp; safety standards.</p></div></div>
      <div class="feature"><div class="num">02</div><div><h4>Extensive Range</h4><p>From drilling additives to VFDs — one supplier for chemical and electrical procurement.</p></div></div>
      <div class="feature"><div class="num">03</div><div><h4>Technical Expertise</h4><p>Our team helps you match the right product to your operating conditions before you order.</p></div></div>
      <div class="feature"><div class="num">04</div><div><h4>Timely Delivery</h4><p>Site schedules don't wait — our logistics are built around getting materials there on time.</p></div></div>
      <div class="feature"><div class="num">05</div><div><h4>Competitive Pricing</h4><p>Direct sourcing relationships keep our pricing sharp without compromising on quality.</p></div></div>
      <div class="feature"><div class="num">06</div><div><h4>38+ Years Trading</h4><p>Four decades of relationships across UAE construction, industrial, and energy sectors.</p></div></div>
    </div>
  </div>
</section>

<section class="cta-band">
  <div class="wrap">
    <h2>Need a chemical or spec sheet fast?</h2>
    <p>Send us your requirement and we'll come back with pricing and availability, usually within one business day.</p>
    <a class="btn btn-dark" href="contact-us.html">Get a Free Quote</a>
  </div>
</section>
"""
    html = base(
        "HA International Chemicals Trading LLC — Chemical & Electrical Supplier, UAE",
        "UAE supplier of industrial & specialty chemicals and electrical/VFD products for construction, oil & gas, and water treatment. 38+ years in Abu Dhabi.",
        body, active="index.html", canonical="",
    )
    write("index.html", html)


# ---------------------------------------------------------------- PRODUCTS LISTING
def build_products():
    chem = [p for p in PROD if p["category"] != "VFD"]
    vfd = [p for p in PROD if p["category"] == "VFD"]
    body = f"""
<section class="page-hero">
  <div class="wrap">
    <div class="eyebrow" style="color:#FF9457">Catalogue</div>
    <h1>Products</h1>
    <p>{len(PROD)} chemicals and electrical products, stocked and ready to quote.</p>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="cat-strip">
      <a href="#chemicals" class="cat-pill active">Industrial Chemicals ({len(chem)})</a>
      <a href="#vfd" class="cat-pill">VFDs &amp; Electrical ({len(vfd)})</a>
    </div>
    <h2 id="chemicals" style="font-size:22px;margin-bottom:20px">Industrial Chemicals</h2>
    <div class="grid grid-4" style="margin-bottom:64px">
      {"".join(product_card(p) for p in chem)}
    </div>
    <h2 id="vfd" style="font-size:22px;margin-bottom:20px">VFDs &amp; Electrical</h2>
    <div class="grid grid-4">
      {"".join(product_card(p) for p in vfd)}
    </div>
  </div>
</section>
<section class="cta-band">
  <div class="wrap">
    <h2>Can't find what you need?</h2>
    <p>Our catalogue keeps growing — tell us the chemical or spec you're after and we'll source it.</p>
    <a class="btn btn-dark" href="contact-us.html">Ask Our Team</a>
  </div>
</section>
"""
    html = base(
        "Products — Industrial Chemicals & VFDs | HA International Chemicals",
        "Browse HA International's full catalogue: drilling & cementing chemicals, water treatment chemicals, and VFDs/electrical equipment.",
        body, active="products.html", canonical="products.html",
    )
    write("products.html", html)


# ---------------------------------------------------------------- PRODUCT DETAIL
def build_product_pages():
    os.makedirs(os.path.join(OUT, "product"), exist_ok=True)
    for p in PROD:
        short = clean(p["short_description"])
        full = clean(p["description"])
        related = [r for r in PROD if r["category"] == p["category"] and r["slug"] != p["slug"]][:4]
        schema = {
            "@context": "https://schema.org",
            "@type": "Product",
            "name": p["name"],
            "category": category_badge(p["category"]).replace("&amp;", "&"),
            "brand": {"@type": "Organization", "name": "HA International Chemicals Trading LLC"},
            "description": re.sub("<[^>]+>", " ", short + full)[:500].strip(),
            "offers": {
                "@type": "Offer",
                "availability": "https://schema.org/InStock",
                "priceCurrency": "AED",
                "url": f"https://hachemicals-concept.example/product/{p['slug']}.html",
                "seller": {"@type": "Organization", "name": "HA International Chemicals Trading LLC"},
            },
        }
        body = f"""
<div class="breadcrumb"><div class="wrap"><a href="index.html">Home</a> / <a href="products.html">Products</a> / {p['name']}</div></div>
<section class="pd-grid wrap">
  <div class="pd-media">
    <div class="frame"><img src="../{product_img(p)}" alt="{p['name']}"></div>
    <div class="quote-box">
      <h4>Request pricing</h4>
      <p>Get a quote with current pricing, MOQ, and lead time for {p['name']}.</p>
      <a class="btn btn-primary" href="../contact-us.html?product={p['slug']}" style="width:100%;justify-content:center">Request a Quote</a>
    </div>
  </div>
  <div class="pd-info">
    <span class="tag">{category_badge(p['category'])}</span>
    <h1>{p['name']}</h1>
    <div class="pd-body">
      {short}
      {full}
    </div>
    <div class="pd-actions">
      <a class="btn btn-dark" href="tel:{PHONE_LINK}">Call {PHONE}</a>
      <a class="btn btn-ghost" style="border-color:var(--line);color:var(--ink)" href="{WHATSAPP}" target="_blank" rel="noopener">WhatsApp</a>
    </div>
  </div>
</section>
{"".join([f'''
<section class="bg-surface related">
  <div class="wrap">
    <h2>Related products</h2>
    <div class="grid grid-4">{"".join(product_card(r) for r in related)}</div>
  </div>
</section>''']) if related else ""}
"""
        html = base(
            f"{p['name']} — HA International Chemicals",
            re.sub("<[^>]+>", " ", short)[:155].strip() or f"{p['name']} supplied by HA International Chemicals Trading LLC, UAE.",
            body, active="products.html", canonical=f"product/{p['slug']}.html",
            extra_head=f'<script type="application/ld+json">{json.dumps(schema)}</script>',
        )
        # product pages are one directory deep, fix relative asset paths
        html = html.replace('href="styles.css"', 'href="../styles.css"')
        html = html.replace('src="script.js"', 'src="../script.js"')
        html = html.replace('href="index.html"', 'href="../index.html"')
        html = html.replace('href="products.html', 'href="../products.html')
        html = html.replace('href="services.html"', 'href="../services.html"')
        html = html.replace('href="about-us.html"', 'href="../about-us.html"')
        html = html.replace('href="contact-us.html"', 'href="../contact-us.html"')
        html = html.replace('src="assets/img', 'src="../assets/img')
        html = html.replace('href="product/', 'href="../product/')
        write(f"product/{p['slug']}.html", html)


# ---------------------------------------------------------------- ABOUT
def build_about():
    body = f"""
<section class="page-hero">
  <div class="wrap">
    <div class="eyebrow" style="color:#FF9457">About Us</div>
    <h1>Four decades in the trade.</h1>
    <p>Your trusted partner in chemicals, engineering products, and electrical solutions across the UAE.</p>
  </div>
</section>
<section>
  <div class="wrap about-grid">
    <div>
      <div class="eyebrow">Our Story</div>
      <h2>A legacy built on reliability</h2>
      <p style="color:var(--muted)">HA International Chemicals Trading LLC is a leading chemical trading company in the UAE, under the patronage of Mr. Adel Saif Amer Hasan Aljaberi, specialising in the supply and distribution of high-quality industrial chemicals, specialty chemicals, and electrical products for diverse industries.</p>
      <p style="color:var(--muted)">With a legacy spanning over four decades, we've built a reputation for reliability, quality, and customer satisfaction — serving businesses across the UAE and international markets, from construction and manufacturing to water treatment and oil &amp; gas.</p>
      <div class="stat-row">
        <div><b>38+</b><span>Years Experience</span></div>
        <div><b>26+</b><span>Products Stocked</span></div>
        <div><b>2</b><span>Business Lines</span></div>
      </div>
    </div>
    <img src="assets/img/img_about_Home01-7DPAR8H.jpg" alt="HA International Chemicals warehouse operations">
  </div>
</section>
<section class="bg-surface">
  <div class="wrap">
    <div class="section-head"><div><div class="eyebrow">What Drives Us</div><h2>Quality, range, and expertise</h2></div></div>
    <div class="grid grid-3">
      <div class="feature"><div class="num">01</div><div><h4>Quality Assurance</h4><p>We partner with reputable manufacturers to ensure every product meets strict quality standards and safety regulations.</p></div></div>
      <div class="feature"><div class="num">02</div><div><h4>Extensive Product Range</h4><p>From cutting-edge electrical equipment to premium-grade chemicals — one supplier, broad coverage.</p></div></div>
      <div class="feature"><div class="num">03</div><div><h4>Technical Expertise</h4><p>Our team's in-depth knowledge across electrical and chemical fields helps you find the right fit, first time.</p></div></div>
    </div>
  </div>
</section>
<section class="cta-band">
  <div class="wrap">
    <h2>Work with a supplier that shows up on time.</h2>
    <p>Tell us what your project needs — we'll quote it fast.</p>
    <a class="btn btn-dark" href="contact-us.html">Get a Free Quote</a>
  </div>
</section>
"""
    html = base(
        "About Us — HA International Chemicals Trading LLC",
        "38+ years supplying industrial chemicals and electrical products across the UAE. Learn about HA International Chemicals Trading LLC.",
        body, active="about-us.html", canonical="about-us.html",
    )
    write("about-us.html", html)


# ---------------------------------------------------------------- SERVICES
SERVICES = [
    ("Electrical Installation", "From residential to industrial facilities, our team delivers cutting-edge electrical installation solutions matched to your project's requirements — component selection through to precise wiring."),
    ("VFD Supply & Support", "Variable frequency drives sized and specified for your motors and process, backed by technical guidance on selection and commissioning."),
    ("Chemical Supply for Drilling & Cementing", "Cenosphere, defoamers, drilling detergents, foams, and starches supplied for downhole and cementing operations across oil &amp; gas projects."),
    ("Water Treatment Chemicals", "Ferric chloride, aluminium sulphate, calcium chloride, and related chemistries for municipal and industrial water treatment."),
    ("Bulk & Project Supply", "Volume orders for construction and industrial projects, with logistics planned around your site schedule."),
    ("Technical Consultation", "Our team helps match the right chemical or electrical product to your operating conditions before you commit to an order."),
]

def build_services():
    items = "".join(f"""<div class="service-item"><div class="ic">{i+1:02d}</div><div><h3>{t}</h3><p>{d}</p></div></div>""" for i,(t,d) in enumerate(SERVICES))
    body = f"""
<section class="page-hero">
  <div class="wrap">
    <div class="eyebrow" style="color:#FF9457">Services</div>
    <h1>What we do</h1>
    <p>Committed to providing exceptional product and service across chemicals and electrical supply.</p>
  </div>
</section>
<section>
  <div class="wrap" style="max-width:880px">
    {items}
  </div>
</section>
<section class="cta-band">
  <div class="wrap">
    <h2>Have a project spec in hand?</h2>
    <p>Send it over and we'll respond with pricing, availability, and lead time.</p>
    <a class="btn btn-dark" href="contact-us.html">Get a Free Quote</a>
  </div>
</section>
"""
    html = base(
        "Services — HA International Chemicals Trading LLC",
        "Electrical installation, VFD supply, and industrial chemical supply for drilling, cementing, and water treatment across the UAE.",
        body, active="services.html", canonical="services.html",
    )
    write("services.html", html)


# ---------------------------------------------------------------- CONTACT
def build_contact():
    body = f"""
<section class="page-hero">
  <div class="wrap">
    <div class="eyebrow" style="color:#FF9457">Contact</div>
    <h1>Let's talk about your requirement</h1>
    <p>Feel free to write our team anytime — we usually respond within one business day.</p>
  </div>
</section>
<section>
  <div class="wrap contact-grid">
    <div>
      <div class="contact-card"><h4>Phone</h4><a href="tel:{PHONE_LINK}">{PHONE}</a></div>
      <div class="contact-card"><h4>Email</h4><a href="mailto:{EMAIL}">{EMAIL}</a></div>
      <div class="contact-card"><h4>Address</h4><p>{ADDRESS}</p></div>
      <div class="contact-card"><h4>Hours</h4><p>{HOURS}</p></div>
    </div>
    <form class="contact-card" style="background:#fff">
      <h4 style="margin-bottom:20px">Request a Quote</h4>
      <div class="form-row">
        <div class="field"><label>First Name</label><input type="text" placeholder="John"></div>
        <div class="field"><label>Last Name</label><input type="text" placeholder="Smith"></div>
      </div>
      <div class="form-row">
        <div class="field"><label>Email</label><input type="email" placeholder="you@company.com"></div>
        <div class="field"><label>Mobile No.</label><input type="tel" placeholder="+971 ..."></div>
      </div>
      <div class="field" style="margin-bottom:16px"><label>What do you need?</label><textarea rows="5" placeholder="Product, quantity, and any spec details..."></textarea></div>
      <button type="submit" class="btn btn-primary" style="width:100%;justify-content:center">Send Request</button>
    </form>
  </div>
</section>
"""
    html = base(
        "Contact Us — HA International Chemicals Trading LLC",
        "Get in touch with HA International Chemicals Trading LLC in Abu Dhabi, UAE — request a quote by phone, email, or WhatsApp.",
        body, active="contact-us.html", canonical="contact-us.html",
    )
    write("contact-us.html", html)


# ---------------------------------------------------------------- 404
def build_404():
    body = """
<div class="notfound">
  <div class="code">404</div>
  <h1>Page not found</h1>
  <p style="color:#9AA3AF;margin-bottom:24px">The page you're looking for has moved or doesn't exist.</p>
  <a class="btn btn-primary" href="index.html">Back to Home</a>
</div>
"""
    html = base("Page Not Found — HA International Chemicals", "Page not found.", body, canonical="404.html")
    write("404.html", html)


def write(relpath, content):
    dest = os.path.join(OUT, relpath)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    open(dest, "w", encoding="utf-8").write(content)


def copy_assets():
    if os.path.exists(os.path.join(OUT, "assets")):
        shutil.rmtree(os.path.join(OUT, "assets"))
    shutil.copytree(os.path.join(ROOT, "build_src/img"), os.path.join(OUT, "assets/img"))
    shutil.copy(os.path.join(ROOT, "styles.css"), os.path.join(OUT, "styles.css"))
    shutil.copy(os.path.join(ROOT, "script.js"), os.path.join(OUT, "script.js"))


if __name__ == "__main__":
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    build_home()
    build_products()
    build_product_pages()
    build_about()
    build_services()
    build_contact()
    build_404()
    copy_assets()
    print("Build complete ->", OUT)
