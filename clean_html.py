"""Strip leftover AI-chat / Tailwind formatting cruft from product HTML,
re-tag it with our own semantic classes (.spec-table, .benefits-list, etc)."""
from bs4 import BeautifulSoup

KEEP_TAGS = {"p", "strong", "em", "b", "i", "ul", "ol", "li", "table",
             "thead", "tbody", "tr", "th", "td", "h3", "h4", "br", "a"}

# Leftovers from an abandoned payment integration pasted into a product
# description on their live site: raw checkout URLs shown as body text plus
# orphaned JS. The /wpay/ endpoint 404s, and the link hardcodes amount=50 —
# a customer clicking it would be paying an arbitrary $50 for a VFD.
JUNK_LINK_PATTERNS = ("/wpay/pay", "paypal.com/ncp/payment")
JUNK_TEXT = ("</script>", "});", "{", "}")


def clean(html: str) -> str:
    if not html or not html.strip():
        return ""
    soup = BeautifulSoup(html, "html.parser")

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
    for ul in soup.find_all("ul"):
        ul["class"] = "benefits-list"

    # strip the abandoned payment-integration leftovers
    for a in soup.find_all("a"):
        href = a.get("href", "")
        if any(pat in href for pat in JUNK_LINK_PATTERNS):
            a.decompose()

    for node in list(soup.find_all(string=True)):
        if node.strip() in JUNK_TEXT:
            node.extract()

    # drop empty paragraphs (e.g. the stray &nbsp; ones)
    for p in soup.find_all("p"):
        if not p.get_text(strip=True):
            p.decompose()

    return str(soup)
