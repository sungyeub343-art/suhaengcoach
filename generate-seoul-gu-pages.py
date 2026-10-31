from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import re
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parent
SEOUL_DIR = ROOT / "regions" / "seoul"
DONG_TITLE = re.compile(r"<title>(\S+) (.+?) 스마트무인자판기")
DISTRICT_LINK = re.compile(r'href="\.\./\.\./\.\./seoul-district\.html\?area=[^"]+"')

# 다른 광역시 구 페이지와 같은 템플릿을 쓰기 위해 전국 생성 스크립트의 함수를 불러온다.
spec = spec_from_file_location("nationwide", ROOT / "generate-nationwide-local-pages.py")
nationwide = module_from_spec(spec)
spec.loader.exec_module(nationwide)


def load_districts():
    districts = {}
    for gu_dir in sorted(path for path in SEOUL_DIR.iterdir() if path.is_dir()):
        items = []
        gu_name = None
        for dong_page in sorted(gu_dir.glob("*/index.html")):
            match = DONG_TITLE.search(dong_page.read_text(encoding="utf-8"))
            if not match:
                raise RuntimeError(f"Could not read dong title in {dong_page}")
            gu_name = match.group(1)
            items.append({"name": match.group(2), "code": dong_page.parent.name})
        if not items:
            raise RuntimeError(f"No dong pages found in {gu_dir}")
        districts[gu_dir.name] = (gu_name, items)
    return districts


def link_dong_pages_to_district(gu_dir):
    for dong_page in gu_dir.glob("*/index.html"):
        page_html = dong_page.read_text(encoding="utf-8")
        updated = DISTRICT_LINK.sub('href="../"', page_html)
        if updated != page_html:
            dong_page.write_text(updated, encoding="utf-8")


def update_seoul_landing(districts):
    landing = ROOT / "regions" / "seoul.html"
    page_html = landing.read_text(encoding="utf-8")
    slugs = {name: slug for slug, (name, _) in districts.items()}

    def replace(match):
        name = unquote(match.group(1))
        if name not in slugs:
            raise RuntimeError(f"Unknown Seoul district link: {name}")
        return f'href="seoul/{slugs[name]}/"'

    landing.write_text(
        re.sub(r'href="seoul-district\.html\?area=([^"]+)"', replace, page_html),
        encoding="utf-8",
    )


districts = load_districts()
for slug, (gu_name, items) in districts.items():
    page_html = nationwide.build_city_page("서울특별시", "서울", "seoul", gu_name, slug, items)
    (SEOUL_DIR / slug / "index.html").write_text(page_html, encoding="utf-8")
    link_dong_pages_to_district(SEOUL_DIR / slug)
update_seoul_landing(districts)
print(f"Generated {len(districts)} Seoul district pages.")
