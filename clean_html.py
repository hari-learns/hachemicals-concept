"""Strip leftover AI-chat / Tailwind formatting cruft from product HTML,
re-tag it with our own semantic classes (.spec-table, .benefits-list, etc)."""
import re
from bs4 import BeautifulSoup

KEEP_TAGS = {"p", "strong", "em", "b", "i", "ul", "ol", "li", "table",
             "thead", "tbody", "tr", "th", "td", "h3", "h4", "br", "a"}

# Leftovers from an abandoned payment integration pasted into a product
# description on their live site: raw checkout URLs shown as body text plus
# orphaned JS. The /wpay/ endpoint 404s, and the link hardcodes amount=50 —
# a customer clicking it would be paying an arbitrary $50 for a VFD.
JUNK_LINK_PATTERNS = ("/wpay/pay", "paypal.com/ncp/payment")
JUNK_TEXT = ("</script>", "});", "{", "}")

# Several product descriptions fake their lists: one <p> holding "✔ item<br>
# ✔ item<br>…" rather than a <ul>. No list styling can reach those, so they get
# rebuilt into real lists. The marker character also tells us which kind of list
# it is — ticks for features/benefits, diamonds for applications.
GREEN_MARKS = "✔✅✓☑❖"
BLUE_MARKS = "🔹🔷◆◇▪🔸"
ALL_MARKS = GREEN_MARKS + BLUE_MARKS
# headings that mean "this list is about where the product is used"
APPLICATION_WORDS = ("application", "used in", "industr", "use case", "suitable for")

# Text left behind by the embedded quote forms once their markup is removed.
FORM_TEXT_SIGNATURES = (
    "ak_js", "setAttribute", "document.createElement", "wpforms",
    "Please enable JavaScript",
)


def _list_classes(variant):
    return ["benefits-list"] + (["is-applications"] if variant == "blue" else [])


def _variant_from_heading(tag):
    """Look back for the nearest heading to decide what kind of list this is."""
    for prev in tag.find_all_previous(["h2", "h3", "h4"], limit=2):
        text = prev.get_text(" ", strip=True).lower()
        if any(w in text for w in APPLICATION_WORDS):
            return "blue"
        return "green"
    return "green"


def _split_on_br(tag):
    """Group a tag's children into the runs separated by <br>."""
    groups, current = [], []
    for child in list(tag.children):
        if getattr(child, "name", None) == "br":
            groups.append(current)
            current = []
        else:
            current.append(child)
    groups.append(current)
    return groups


def _promote_marker_paragraphs(soup):
    """Turn "<p>✔ a<br>✔ b</p>" into a real <ul>, coloured by marker type."""
    from bs4 import NavigableString

    for p in list(soup.find_all("p")):
        groups = [g for g in _split_on_br(p)
                  if "".join(str(x) for x in g).strip()]
        if not groups:
            continue

        leading = []
        for g in groups:
            text = "".join(
                x if isinstance(x, str) else x.get_text() for x in g
            ).lstrip()
            leading.append(text[0] if text else "")

        # only rebuild when every run is marker-prefixed — otherwise it's prose
        if not all(ch in ALL_MARKS for ch in leading):
            continue

        variant = "blue" if any(ch in BLUE_MARKS for ch in leading) else "green"
        ul = soup.new_tag("ul")
        ul["class"] = _list_classes(variant)

        for g in groups:
            li = soup.new_tag("li")
            stripped = False
            for node in g:
                if not stripped and isinstance(node, NavigableString):
                    text = str(node).lstrip()
                    if text and text[0] in ALL_MARKS:
                        node = NavigableString(text[1:].lstrip())
                        stripped = True
                    elif not text:
                        continue
                li.append(node)
            if li.get_text(strip=True):
                ul.append(li)

        if ul.find("li"):
            p.replace_with(ul)


def _remove_embedded_forms(soup):
    """Drop the Contact Form 7 quote form embedded in 18 product descriptions.

    On their live site WordPress renders this as a working form. Here only the
    labels survive — the inputs are injected server-side — so it degrades to
    orphaned text like "Company Name / Quantity Required" plus an Akismet
    timestamp script. Our product pages carry their own quote box instead.

    Must run before the unwrap pass, which would strip the classes we match on.
    """
    for el in soup.select(
        '[class*="wpcf7"], [id*="wpcf7"], '      # Contact Form 7 (13 products)
        '[class*="wpforms"], [id*="wpforms"], '  # WPForms (5 products)
        '[class*="akismet"], .screen-reader-response, '
        'form, fieldset, script, noscript, style'
    ):
        el.decompose()

    # inline plugin scripts and their no-JS notices leak as bare text nodes
    for node in list(soup.find_all(string=True)):
        if any(sig in node for sig in FORM_TEXT_SIGNATURES):
            node.extract()


def _strip_stray_markers(soup):
    from bs4 import NavigableString

    for node in list(soup.find_all(string=True)):
        text = str(node)
        if not any(ch in text for ch in ALL_MARKS):
            continue
        # a marker opening the run takes its trailing space with it, so
        # "✅ Key Features:" doesn't become " Key Features:"
        text = re.sub(rf"^\s*[{ALL_MARKS}]\s*", "", text)
        for ch in ALL_MARKS:
            text = text.replace(ch, "")
        text = re.sub(r" {2,}", " ", text)
        node.replace_with(NavigableString(text))


def clean(html: str) -> str:
    if not html or not html.strip():
        return ""
    soup = BeautifulSoup(html, "html.parser")

    _remove_embedded_forms(soup)

    for tag in soup.find_all(True):
        if tag.name not in KEEP_TAGS:
            tag.unwrap()
            continue
        keep_attrs = {}
        if tag.name == "a" and tag.get("href"):
            keep_attrs["href"] = tag["href"]
        tag.attrs = keep_attrs

    for table in soup.find_all("table"):
        table["class"] = "spec-table"

    _promote_marker_paragraphs(soup)

    for ul in soup.find_all("ul"):
        if ul.get("class"):
            continue  # already classed by the promotion pass
        ul["class"] = _list_classes(_variant_from_heading(ul))

    # strip the abandoned payment-integration leftovers
    for a in soup.find_all("a"):
        href = a.get("href", "")
        if any(pat in href for pat in JUNK_LINK_PATTERNS):
            a.decompose()

    for node in list(soup.find_all(string=True)):
        if node.strip() in JUNK_TEXT:
            node.extract()

    # Safety net for markers the promotion pass correctly left alone — ones
    # decorating a heading ("✅ Key Features:") or sitting inline mid-sentence.
    # Those aren't list items, but the raw emoji shouldn't reach the page.
    _strip_stray_markers(soup)

    # drop empty paragraphs (e.g. the stray &nbsp; ones)
    for p in soup.find_all("p"):
        if not p.get_text(strip=True):
            p.decompose()

    return str(soup)
