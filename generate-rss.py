from datetime import datetime, timezone
from email.utils import format_datetime
from html import unescape
from pathlib import Path
import re
import subprocess
from xml.etree.ElementTree import Element, ElementTree, SubElement, indent


ROOT = Path(__file__).resolve().parent
SITE_URL = "https://suhaengcoach.kr"
FEED_DIRS = ("guides", "solutions")
TITLE = re.compile(r"<title>(.*?)</title>", re.DOTALL)
DESCRIPTION = re.compile(r'<meta\s+name="description"\s+content="([^"]*)"')
CANONICAL = re.compile(r'<link\s+rel="canonical"\s+href="([^"]+)"')


def published_at(page_path):
    """파일이 처음 커밋된 시각. 아직 커밋 전이면 현재 시각."""
    output = subprocess.run(
        ["git", "log", "--diff-filter=A", "--format=%cI", "--", page_path.relative_to(ROOT).as_posix()],
        cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout.split()
    return datetime.fromisoformat(output[-1]) if output else datetime.now(timezone.utc)


items = []
for directory in FEED_DIRS:
    for page_path in (ROOT / directory).glob("*.html"):
        page_html = page_path.read_text(encoding="utf-8")
        items.append({
            "title": unescape(TITLE.search(page_html).group(1).strip()),
            "description": unescape(DESCRIPTION.search(page_html).group(1)),
            "link": CANONICAL.search(page_html).group(1),
            "date": published_at(page_path),
        })
items.sort(key=lambda item: item["date"], reverse=True)

rss = Element("rss", version="2.0")
channel = SubElement(rss, "channel")
SubElement(channel, "title").text = "더세이브 수행코치 무인자판기 가이드"
SubElement(channel, "link").text = f"{SITE_URL}/"
SubElement(channel, "description").text = "무인자판기 설치 비용, 창업, 카드결제, 업종별 설치 안내"
SubElement(channel, "language").text = "ko"
SubElement(channel, "lastBuildDate").text = format_datetime(items[0]["date"])
for item in items:
    entry = SubElement(channel, "item")
    SubElement(entry, "title").text = item["title"]
    SubElement(entry, "link").text = item["link"]
    SubElement(entry, "guid").text = item["link"]
    SubElement(entry, "description").text = item["description"]
    SubElement(entry, "pubDate").text = format_datetime(item["date"])

indent(rss, space="  ")
ElementTree(rss).write(ROOT / "rss.xml", encoding="utf-8", xml_declaration=True)
print(f"Generated rss.xml with {len(items)} items.")
