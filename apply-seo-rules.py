"""검색 노출 규칙을 모든 페이지에 적용한다.

- 지역명만 바뀌는 동·읍·면 페이지와 단말기 세부 지역 페이지는 유사 문서로 판단되기 쉬워
  noindex,follow 로 검색 결과에서 제외하고 링크만 따라가게 한다.
- 주소 파라미터(?area=)로 내용이 바뀌는 템플릿 페이지와 새 주소로 대체된 예전 페이지도
  검색 결과에서 제외한다.
- 검색에 노출되는 페이지 중 canonical 이 없는 페이지에는 자기 주소를 canonical 로 넣는다.

generate-sitemap.py 가 실행될 때 먼저 실행되므로, 페이지를 다시 생성해도 규칙이 유지된다.
"""
from pathlib import Path
import re
from urllib.parse import quote


ROOT = Path(__file__).resolve().parent
SITE_URL = "https://suhaengcoach.kr"
NOINDEX_META = '<meta name="robots" content="noindex,follow">'
TEMPLATE_PAGES = {
    "regional-area.html",
    "regional-areas.html",
    "regions/seoul-district.html",
    "regions/gyeongnam-city.html",
    # regions/gwangju/gwangsangu/ 로 대체된 예전 광산구 페이지
    "regions/gwangju/gwangsan/index.html",
}
SKIPPED_FILES = {"naverd3e30b29bcc94d6ebc62de63a329c28c.html"}
ROBOTS_META = re.compile(r'<meta\s+name=["\']robots["\'][^>]*>', re.IGNORECASE)
CHARSET_META = re.compile(r'<meta\s+charset=["\']?utf-8["\']?\s*/?>', re.IGNORECASE)


def public_url(relative_path):
    if relative_path == "index.html":
        return f"{SITE_URL}/"
    if relative_path.endswith("/index.html"):
        relative_path = relative_path.removesuffix("index.html")
    return f"{SITE_URL}/{quote(relative_path, safe='/')}"


def should_noindex(parts):
    relative_path = "/".join(parts)
    if relative_path in TEMPLATE_PAGES:
        return True
    # regions/<광역>/<시군구>/<행정동코드>/index.html
    if parts[0] == "regions" and len(parts) == 5 and parts[3].isdigit():
        return True
    # terminal/<광역>/<시군구>/index.html
    return parts[0] == "terminal" and len(parts) == 4


def insert_after_charset(page_html, tag):
    match = CHARSET_META.search(page_html)
    if match:
        return page_html[: match.end()] + tag + page_html[match.end() :]
    return page_html.replace("<head>", f"<head>{tag}", 1)


def apply_rules(page_path):
    parts = page_path.relative_to(ROOT).parts
    page_html = page_path.read_text(encoding="utf-8-sig")
    updated = page_html
    if "<meta data-redirect=" in updated:
        return False

    if should_noindex(parts):
        if ROBOTS_META.search(updated):
            updated = ROBOTS_META.sub(NOINDEX_META, updated, count=1)
        else:
            updated = insert_after_charset(updated, NOINDEX_META)
    elif "noindex" not in updated and 'rel="canonical"' not in updated:
        canonical = f'<link rel="canonical" href="{public_url("/".join(parts))}">'
        updated = updated.replace("</title>", f"</title>{canonical}", 1)

    if updated == page_html:
        return False
    page_path.write_text(updated, encoding="utf-8")
    return True


changed = 0
for page_path in ROOT.rglob("*.html"):
    if ".git" in page_path.parts or page_path.name in SKIPPED_FILES:
        continue
    changed += apply_rules(page_path)
print(f"Applied SEO rules to {changed} pages.")
