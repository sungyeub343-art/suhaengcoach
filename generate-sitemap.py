from datetime import date as date_type
from pathlib import Path
import re
import runpy
import subprocess
from urllib.parse import quote
from xml.etree.ElementTree import Element, ElementTree, SubElement, indent


ROOT = Path(__file__).resolve().parent
SITE_URL = "https://suhaengcoach.kr"
EXCLUDED_FILES = {"naverd3e30b29bcc94d6ebc62de63a329c28c.html"}
CANONICAL_PATTERN = re.compile(
    r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']',
    re.IGNORECASE,
)

# 검색 제외(noindex)·canonical 규칙을 먼저 적용해야 사이트맵에 정확한 주소만 들어간다.
runpy.run_path(str(ROOT / "apply-seo-rules.py"), run_name="__main__")


def last_modified_dates():
    """git 커밋 기록에서 파일별 마지막 수정일을 읽는다."""
    log = subprocess.run(
        ["git", "-c", "core.quotepath=false", "log", "--format=%x00%cs", "--name-only"],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8", check=True,
    ).stdout
    dates = {}
    date = None
    for line in log.splitlines():
        if line.startswith("\x00"):
            date = line[1:]
        elif line and line not in dates:
            dates[line] = date
    # 아직 커밋하지 않은 변경 파일은 오늘 날짜로 본다.
    status = subprocess.run(
        ["git", "-c", "core.quotepath=false", "status", "--porcelain", "--untracked-files=all"],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8", check=True,
    ).stdout
    today = date_type.today().isoformat()
    for line in status.splitlines():
        dates[line[3:].strip('"')] = today
    return dates


def public_url(path):
    relative_path = path.relative_to(ROOT).as_posix()
    if relative_path == "index.html":
        return f"{SITE_URL}/"
    if relative_path.endswith("/index.html"):
        relative_path = relative_path.removesuffix("index.html")
    return f"{SITE_URL}/{quote(relative_path, safe='/')}"


modified = last_modified_dates()
urls = {}
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
    url = canonical.group(1) if canonical else public_url(page_path)
    urls[url] = max(urls.get(url, ""), modified.get(page_path.relative_to(ROOT).as_posix(), ""))

urlset = Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
for url in sorted(urls, key=lambda value: (value != f"{SITE_URL}/", value)):
    url_element = SubElement(urlset, "url")
    SubElement(url_element, "loc").text = url
    if urls[url]:
        SubElement(url_element, "lastmod").text = urls[url]

indent(urlset, space="  ")
ElementTree(urlset).write(ROOT / "sitemap.xml", encoding="utf-8", xml_declaration=True)
print(f"Generated sitemap.xml with {len(urls)} URLs.")