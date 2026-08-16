"""Strip leftover AI-chat / Tailwind formatting cruft from product HTML,
re-tag it with our own semantic classes (.spec-table, .benefits-list, etc)."""
from bs4 import BeautifulSoup

KEEP_TAGS = {"p", "strong", "em", "b", "i", "ul", "ol", "li", "table",
             "thead", "tbody", "tr", "th", "td", "h3", "h4", "br", "a"}


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

    # drop empty paragraphs (e.g. the stray &nbsp; ones)
    for p in soup.find_all("p"):
        if not p.get_text(strip=True):
            p.decompose()

    return str(soup)
