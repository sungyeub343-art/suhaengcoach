from pathlib import Path
import re
from urllib.parse import quote
from xml.etree.ElementTree import Element, ElementTree, SubElement, indent


ROOT = Path(__file__).resolve().parent
SITE_URL = "https://suhaengcoach.kr"
EXCLUDED_FILES = {"naverd3e30b29bcc94d6ebc62de63a329c28c.html"}
CANONICAL_PATTERN = re.compile(
    r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']',
    re.IGNORECASE,
)


def public_url(path):
    relative_path = path.relative_to(ROOT).as_posix()
    if relative_path == "index.html":
        return f"{SITE_URL}/"
    if relative_path.endswith("/index.html"):
        relative_path = relative_path.removesuffix("index.html")
    return f"{SITE_URL}/{quote(relative_path, safe='/')}"


urls = set()
for page_path in ROOT.rglob("*.html"):
    if page_path.name in EXCLUDED_FILES or ".git" in page_path.parts:
        continue

    html = page_path.read_text(encoding="utf-8-sig", errors="ignore")
    if "<meta data-redirect=" in html or re.search(
        r'<meta\s+name=["\']robots["\'][^>]*content=["\'][^"\']*noindex',
        html,
        re.IGNORECASE,
    ):
        continue
    canonical = CANONICAL_PATTERN.search(html)
    urls.add(canonical.group(1) if canonical else public_url(page_path))

urlset = Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
for url in sorted(urls, key=lambda value: (value != f"{SITE_URL}/", value)):
    url_element = SubElement(urlset, "url")
    SubElement(url_element, "loc").text = url

indent(urlset, space="  ")
ElementTree(urlset).write(ROOT / "sitemap.xml", encoding="utf-8", xml_declaration=True)
print(f"Generated sitemap.xml with {len(urls)} URLs.")