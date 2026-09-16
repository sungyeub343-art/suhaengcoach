from collections import defaultdict
import argparse
import html
import json
from pathlib import Path
import re
from subprocess import run
import sys
from urllib.request import urlopen


DATA_URL = (
    "https://raw.githubusercontent.com/vuski/admdongkor/master/"
    "ver20260201/HangJeongDong_ver20260201.geojson"
)
PROVINCES = {
    "강원특별자치도": ("gangwon", "강원"),
    "경상남도": ("gyeongnam", "경남"),
    "경상북도": ("gyeongbuk", "경북"),
    "광주광역시": ("gwangju", "광주"),
    "대구광역시": ("daegu", "대구"),
    "대전광역시": ("daejeon", "대전"),
    "부산광역시": ("busan", "부산"),
    "세종특별자치시": ("sejong", "세종"),
    "울산광역시": ("ulsan", "울산"),
    "인천광역시": ("incheon", "인천"),
    "전라남도": ("jeonnam", "전남"),
    "전북특별자치도": ("jeonbuk", "전북"),
    "제주특별자치도": ("jeju", "제주"),
    "충청남도": ("chungnam", "충남"),
    "충청북도": ("chungbuk", "충북"),
}
GYEONGNAM_SLUGS = {
    "거제시": "geoje", "거창군": "geochang", "고성군": "goseong",
    "김해시": "gimhae", "남해군": "namhae", "밀양시": "miryang",
    "사천시": "sacheon", "산청군": "sancheong", "양산시": "yangsan",
    "의령군": "uiryeong", "진주시": "jinju", "창녕군": "changnyeong",
    "창원시": "changwon", "통영시": "tongyeong", "하동군": "hadong",
    "함안군": "haman", "함양군": "hamyang", "합천군": "hapcheon",
}
ROOT = Path(__file__).resolve().parent
REGIONS_DIR = ROOT / "regions"


def load_area_slugs():
    area_slugs = {}
    for province_name, (group, _) in PROVINCES.items():
        landing_path = REGIONS_DIR / f"{group}.html"
        landing_html = landing_path.read_text(encoding="utf-8-sig")
        matches = re.findall(
            rf'<a[^>]+href=["\']{group}/([^/"\']+)/["\'][^>]*>.*?<b>([^<]+)</b>',
            landing_html,
            flags=re.DOTALL,
        )
        mappings = {
            html.unescape(name).removesuffix(" 스마트무인자판기").strip(): slug
            for slug, name in matches
        }
        if province_name == "경상북도":
            mappings.pop("군위군", None)
        if province_name == "경상남도":
            mappings = GYEONGNAM_SLUGS
        if province_name == "세종특별자치시":
            mappings = {"세종특별자치시": "sejong-si"}
        if not mappings:
            raise RuntimeError(f"No city or county links found in {landing_path}")
        area_slugs[province_name] = mappings
    return area_slugs


def load_localities(area_slugs):
    with urlopen(DATA_URL, timeout=60) as response:
        data = json.load(response)

    localities = defaultdict(list)
    unmatched = []
    for feature in data["features"]:
        properties = feature["properties"]
        province_name = properties.get("sidonm")
        if province_name not in PROVINCES:
            continue

        full_name = properties["adm_nm"]
        remainder = full_name.removeprefix(province_name).strip()
        if province_name == "세종특별자치시":
            parent = "세종특별자치시"
            locality_name = remainder
        else:
            candidates = area_slugs[province_name]
            parent = next(
                (
                    name
                    for name in sorted(candidates, key=len, reverse=True)
                    if remainder.startswith(name)
                ),
                None,
            )
            if parent is None:
                unmatched.append(full_name)
                continue
            locality_name = remainder.removeprefix(parent).strip()

        localities[(province_name, parent)].append(
            {"name": locality_name, "code": str(properties["adm_cd2"])}
        )

    if unmatched:
        sample = ", ".join(unmatched[:10])
        raise RuntimeError(f"Could not match {len(unmatched)} localities: {sample}")

    expected_parents = {
        (province, area)
        for province, mappings in area_slugs.items()
        for area in mappings
    }
    actual_parents = set(localities)
    if expected_parents != actual_parents:
        missing = sorted(expected_parents - actual_parents)
        extra = sorted(actual_parents - expected_parents)
        raise RuntimeError(f"Unexpected parent areas. Missing={missing}, extra={extra}")

    for items in localities.values():
        items.sort(key=lambda item: item["code"])
    return dict(localities)


def build_solution_section(area):
    return (
        '<!-- VENDING CONTENT START -->'
        '<section class="section keyword-guide"><div class="section-head"><div>'
        '<p class="eyebrow"><span></span> VENDING SOLUTION</p>'
        f'<h2>{area} 설치를 위한<br><em>4가지 핵심 설계</em></h2></div>'
        f'<p>{area}의 공간과 이용 고객을 먼저 살펴보고, 필요한 상품과 기기 구성을 정합니다. '
        '설치 이후에도 관리하기 편하도록 결제 방식과 재고 보충 동선까지 함께 안내합니다.</p>'
        '</div><div class="steps"><article><b>01</b><strong>공간 분석</strong>'
        '<p>설치 면적과 전원,<br>고객 이동 동선 확인</p></article>'
        '<article><b>02</b><strong>상품 구성</strong><p>음료·간식·생활용품 중<br>수요에 맞는 품목 제안</p></article>'
        '<article><b>03</b><strong>기기·결제</strong><p>상품 크기에 맞는 기기와<br>카드 결제 방식 선택</p></article>'
        '<article><b>04</b><strong>운영 동선</strong><p>재고 보충과 매출 확인이<br>편리한 관리 방법 안내</p></article></div></section>'
        '<section class="section vending-use-cases"><div class="section-head"><div>'
        '<p class="eyebrow"><span></span> SPACE &amp; PRODUCT GUIDE</p>'
        f'<h2>{area} 공간에 맞는<br><em>자판기 상품 구성</em></h2></div>'
        '<p>설치 장소에 따라 잘 팔리는 상품과 필요한 기능이 달라집니다. 주요 이용 시간과 고객 목적을 기준으로 공간별 구성을 구체화합니다.</p></div>'
        '<div class="keyword-card-grid">'
        '<article><span>WORK</span><h3>오피스·공장·물류센터</h3><p>출근 시간과 교대 근무 수요에 맞춰 커피, 냉장 음료, 간식, 간편식을 구성합니다. 휴게 공간에서는 빠르게 고르고 결제할 수 있는 진열과 동선이 중요합니다.</p><small>음료 자판기 · 간식 자판기 · 간편식</small></article>'
        '<article><span>LIVING</span><h3>아파트·학교·학원</h3><p>생활권 이용자가 자주 찾는 음료와 스낵, 문구, 위생용품, 소형 생활용품을 함께 제안합니다. 어린이와 학생이 이용하는 공간은 상품 높이와 안전한 진열도 확인합니다.</p><small>생활용품 자판기 · 문구 · 스낵</small></article>'
        '<article><span>STAY</span><h3>병원·호텔·숙박시설</h3><p>보호자와 투숙객이 늦은 시간에도 구매할 수 있도록 생수, 간편식, 여행용품, 위생용품 중심으로 구성합니다. 로비와 객실층 등 설치 위치별 수요도 나눠 살펴봅니다.</p><small>병원 자판기 · 호텔 자판기 · 여행용품</small></article>'
        '<article><span>LEISURE</span><h3>골프장·헬스장·세차장</h3><p>골프용품과 기능성 음료, 단백질 간식, 세정제와 타월처럼 방문 목적이 분명한 상품을 판매합니다. 전문용품은 포장 크기와 보관 조건에 맞는 칸 구성이 필요합니다.</p><small>골프장 자판기 · 세차용품 자판기</small></article>'
        '</div></section>'
        '<section class="section vending-machine-guide"><div class="section-head"><div>'
        '<p class="eyebrow"><span></span> MACHINE &amp; OPERATION</p>'
        '<h2>상품부터 결제까지<br><em>운영에 맞는 기기 선택</em></h2></div>'
        f'<p>{area}에서 판매할 품목이 정해지면 보관 온도, 상품 크기, 결제 수단과 관리 방식을 기준으로 기기를 선택합니다. 초기 설치비용뿐 아니라 장기 운영의 편의성까지 함께 비교합니다.</p></div>'
        '<div class="keyword-card-grid">'
        '<article><span>01</span><h3>냉장 음료 자판기</h3><p>캔·페트병 음료와 유제품처럼 일정한 온도 관리가 필요한 상품에 적합합니다. 판매 품목의 용량과 진열 수량을 확인해 내부 칸을 구성합니다.</p><small>커피 · 생수 · 탄산음료 · 냉장식품</small></article>'
        '<article><span>02</span><h3>간식·디저트 자판기</h3><p>스낵, 베이커리, 디저트와 간편식은 포장이 눌리거나 걸리지 않도록 배출 방식과 칸 너비를 맞춥니다. 유통기한과 회전율도 함께 고려합니다.</p><small>간식 · 디저트 · 베이커리 · 간편식</small></article>'
        '<article><span>03</span><h3>멀티·생활용품 자판기</h3><p>크기가 다른 상품을 한 기기에서 판매할 때는 멀티자판기 구성이 효율적입니다. 생활용품, 지역 특산물, 골프용품 등 비정형 상품도 규격에 맞춰 검토합니다.</p><small>멀티자판기 · 생활용품 · 지역 특산물</small></article>'
        '<article><span>04</span><h3>스마트 결제·운영 관리</h3><p>카드와 간편결제 사용 환경을 확인하고, 재고 보충 주기와 매출 확인 방법을 안내합니다. 무인 운영 시간과 관리 인력에 맞는 방식을 선택합니다.</p><small>카드결제 · 간편결제 · 재고관리 · 매출확인</small></article>'
        '</div></section><!-- VENDING CONTENT END -->'
    )


def update_landing_pages():
    for province_name, (group, short_name) in PROVINCES.items():
        page_path = REGIONS_DIR / f"{group}.html"
        page_html = page_path.read_text(encoding="utf-8-sig")
        if province_name == "경상북도":
            page_html = re.sub(
                r'<a class="region-card" href="gyeongbuk/gunwi/">.*?</a>',
                "",
                page_html,
                count=1,
                flags=re.DOTALL,
            )
        if "gyeonggi-content.css" not in page_html:
            page_html = page_html.replace(
                "</head>", '<link rel="stylesheet" href="../gyeonggi-content.css"></head>', 1
            )
        page_html, count = re.subn(
            r'(?:<!-- VENDING CONTENT START -->.*?<!-- VENDING CONTENT END -->|<section class="section keyword-guide">.*?</section>)',
            build_solution_section(short_name),
            page_html,
            count=1,
            flags=re.DOTALL,
        )
        if count != 1:
            raise RuntimeError(f"Could not enrich {page_path}")
        page_path.write_text(page_html, encoding="utf-8")


def build_local_cards(group, area_slug, area_name, items):
    return "".join(
        f'<a class="region-card" href="{item["code"]}/"><span><b>{item["name"]}</b>'
        f'<small>{area_name} {item["name"]} 설치 안내</small></span><span>↗</span></a>'
        for item in items
    )


def build_city_page(province_name, short_name, group, area_name, area_slug, items):
    cards = build_local_cards(group, area_slug, area_name, items)
    return (
        '<!doctype html><html lang="ko"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<meta name="description" content="{province_name} {area_name} 스마트무인자판기 설치 비용과 행정동별 무료 견적 안내">'
        f'<title>{area_name} 스마트무인자판기 설치 안내 | 더세이브 수행코치</title>'
        f'<link rel="canonical" href="https://suhaengcoach.kr/regions/{group}/{area_slug}/">'
        '<link rel="stylesheet" href="../../../installation.css">'
        '<link rel="stylesheet" href="../../../gyeonggi-content.css"></head><body>'
        '<header class="site-header"><a class="brand" href="../../../index.html"><span class="brand-mark">S</span>'
        '<span>더세이브 수행코치 <small>VENDING STUDIO</small></span></a><nav class="main-nav">'
        f'<a href="../../{group}.html">{short_name} 지역 안내</a><a href="../../../index.html#consult">상담 문의</a></nav></header><main>'
        '<section class="hero"><div class="hero-copy">'
        f'<p class="eyebrow"><span></span> {group.upper()} LOCAL INSTALLATION GUIDE</p>'
        f'<h1>{area_name}<br><em>무인자판기</em><br>설치 안내</h1>'
        f'<p>{area_name}의 산업·교육·상업·주거공간에 맞춰 상품 구성과 운영 동선을 설계합니다.</p></div>'
        f'<div class="hero-image"><img src="../../../1234.png" alt="{area_name}에 설치 가능한 스마트 무인자판기">'
        f'<div class="hero-label"><strong>{area_name} 지역 상담</strong><span>무료 견적 안내</span></div></div></section>'
        f'{build_solution_section(area_name)}'
        '<section class="section" id="localGuide"><div class="section-head"><div>'
        f'<p class="eyebrow"><span></span> {group.upper()} LOCAL GUIDE</p>'
        f'<h2>{area_name} 설치 지역을<br><em>선택해주세요.</em></h2></div>'
        f'<p>{area_name} 동·읍·면별 스마트무인자판기 설치 안내와 무료 견적 상담을 확인할 수 있습니다.</p>'
        f'</div><div class="region-grid">{cards}</div></section>'
        '<section class="section process"><div class="section-head"><div><p class="eyebrow"><span></span> START WITH A CHAT</p>'
        '<h2>설치 상담<br><em>4단계 안내</em></h2></div><p>설치 장소 사진과 주소를 보내주시면 입지 조건을 확인해 운영 방향을 안내합니다.</p></div>'
        '<div class="steps"><article><b>01</b><strong>입지 상담</strong><p>공간과 고객 흐름 확인</p></article>'
        '<article><b>02</b><strong>맞춤 견적</strong><p>기기·상품·결제 안내</p></article>'
        '<article><b>03</b><strong>설치 세팅</strong><p>결제 연결과 상품 진열</p></article>'
        '<article><b>04</b><strong>운영 안내</strong><p>재고·매출 관리 방법</p></article></div></section>'
        f'<section class="cta"><h2>{area_name} 무료 설치 상담</h2><a class="button" href="../../../index.html#consult">상담 신청하기</a></section>'
        f'</main><footer class="site-footer"><a href="../../{group}.html">← {short_name} 지역 선택</a></footer></body></html>'
    )


def build_detail_page(province_name, short_name, group, area_name, area_slug, item):
    locality_name = item["name"]
    code = item["code"]
    full_area = f"{area_name} {locality_name}"
    return (
        '<!doctype html><html lang="ko"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<meta name="description" content="{province_name} {full_area} 스마트무인자판기 설치 비용과 무료 견적 상담 안내">'
        f'<title>{full_area} 스마트무인자판기 설치 안내 | 더세이브 수행코치</title>'
        f'<link rel="canonical" href="https://suhaengcoach.kr/regions/{group}/{area_slug}/{code}/">'
        '<link rel="stylesheet" href="../../../../installation.css">'
        '<link rel="stylesheet" href="../../../../gyeonggi-content.css"></head><body>'
        '<header class="site-header"><a class="brand" href="../../../../index.html"><span class="brand-mark">S</span>'
        '<span>더세이브 수행코치 <small>VENDING STUDIO</small></span></a><nav class="main-nav">'
        f'<a href="../../">{area_name} 지역 안내</a><a href="../../../../index.html#consult">상담 문의</a></nav></header><main>'
        '<section class="hero"><div class="hero-copy">'
        f'<p class="eyebrow"><span></span> {group.upper()} LOCAL INSTALLATION GUIDE</p>'
        f'<h1>{full_area}<br><em>무인자판기</em><br>설치 안내</h1>'
        f'<p>{full_area}의 오피스·상업시설·교육시설·주거공간에 맞춰 상품 구성과 운영 동선을 설계합니다.</p></div>'
        f'<div class="hero-image"><img src="../../../../1234.png" alt="{full_area}에 설치 가능한 스마트 무인자판기">'
        f'<div class="hero-label"><strong>{locality_name} 지역 상담</strong><span>무료 견적 안내</span></div></div></section>'
        f'{build_solution_section(full_area)}'
        '<section class="section process"><div class="section-head"><div><p class="eyebrow"><span></span> LOCAL INSTALLATION</p>'
        f'<h2>{locality_name} 설치 상담<br><em>진행 안내</em></h2></div>'
        '<p>설치 장소 사진과 주소를 보내주시면 입지 조건을 확인해 가능한 모델과 운영 방향을 안내합니다.</p></div>'
        '<div class="steps"><article><b>01</b><strong>입지 상담</strong><p>공간과 고객 흐름 확인</p></article>'
        '<article><b>02</b><strong>맞춤 견적</strong><p>기기·상품·결제 안내</p></article>'
        '<article><b>03</b><strong>설치 세팅</strong><p>결제 연결과 상품 진열</p></article>'
        '<article><b>04</b><strong>운영 안내</strong><p>재고·매출 관리 방법</p></article></div></section>'
        f'<section class="cta"><h2>{full_area} 무료 설치 상담</h2><a class="button" href="../../../../index.html#consult">상담 신청하기</a></section>'
        f'</main><footer class="site-footer"><a href="../../">← {area_name} 지역 안내</a></footer></body></html>'
    )


def generate_pages(area_slugs, localities):
    city_count = 0
    locality_count = 0
    for province_name, (group, short_name) in PROVINCES.items():
        for area_name, area_slug in area_slugs[province_name].items():
            items = localities[(province_name, area_name)]
            city_path = REGIONS_DIR / group / area_slug / "index.html"
            city_path.parent.mkdir(parents=True, exist_ok=True)
            city_path.write_text(
                build_city_page(province_name, short_name, group, area_name, area_slug, items),
                encoding="utf-8",
            )
            city_count += 1
            for item in items:
                detail_path = city_path.parent / item["code"] / "index.html"
                detail_path.parent.mkdir(parents=True, exist_ok=True)
                detail_path.write_text(
                    build_detail_page(province_name, short_name, group, area_name, area_slug, item),
                    encoding="utf-8",
                )
                locality_count += 1
    return city_count, locality_count


def write_legacy_redirects():
    legacy_path = REGIONS_DIR / "gyeongbuk" / "gunwi" / "index.html"
    legacy_path.write_text(
        '<!doctype html><html lang="ko"><head><meta charset="utf-8">'
        '<meta name="robots" content="noindex,follow">'
        '<meta http-equiv="refresh" content="0;url=../../../regions/daegu/gunwigun/">'
        '<link rel="canonical" href="https://suhaengcoach.kr/regions/daegu/gunwigun/">'
        '<title>대구 군위군 설치 안내로 이동 | 더세이브 수행코치</title></head><body>'
        '<p><a href="../../../regions/daegu/gunwigun/">대구 군위군 자판기 설치 안내로 이동</a></p>'
        '</body></html>',
        encoding="utf-8",
    )


def validate_output(area_slugs, localities):
    checked_cities = 0
    checked_localities = 0
    canonical_urls = set()
    for province_name, (group, _) in PROVINCES.items():
        landing_html = (REGIONS_DIR / f"{group}.html").read_text(encoding="utf-8")
        if landing_html.count("<!-- VENDING CONTENT START -->") != 1:
            raise RuntimeError(f"Invalid rich content in {group} landing page")

        for area_name, area_slug in area_slugs[province_name].items():
            items = localities[(province_name, area_name)]
            city_path = REGIONS_DIR / group / area_slug / "index.html"
            city_html = city_path.read_text(encoding="utf-8")
            if city_html.count('id="localGuide"') != 1:
                raise RuntimeError(f"Missing locality navigation in {city_path}")
            if city_html.count('class="region-card"') != len(items):
                raise RuntimeError(f"Wrong locality link count in {city_path}")
            if city_html.count("<!-- VENDING CONTENT START -->") != 1:
                raise RuntimeError(f"Invalid rich content in {city_path}")
            checked_cities += 1

            for item in items:
                detail_path = city_path.parent / item["code"] / "index.html"
                detail_html = detail_path.read_text(encoding="utf-8")
                expected_canonical = (
                    f"https://suhaengcoach.kr/regions/{group}/{area_slug}/{item['code']}/"
                )
                checks = {
                    "canonical": detail_html.count(expected_canonical) == 1,
                    "h1": detail_html.count("<h1>") == 1,
                    "rich content": detail_html.count("<!-- VENDING CONTENT START -->") == 1,
                    "guide image": detail_html.count("자판기_통합.png") == 1,
                }
                failed = [name for name, passed in checks.items() if not passed]
                if failed:
                    raise RuntimeError(f"Invalid {', '.join(failed)} in {detail_path}")
                if expected_canonical in canonical_urls:
                    raise RuntimeError(f"Duplicate canonical URL: {expected_canonical}")
                canonical_urls.add(expected_canonical)
                checked_localities += 1

    print(
        f"Validated output for {checked_cities} city/county pages and "
        f"{checked_localities} locality pages."
    )
    legacy_html = (REGIONS_DIR / "gyeongbuk" / "gunwi" / "index.html").read_text(
        encoding="utf-8"
    )
    if 'content="noindex,follow"' not in legacy_html or "/regions/daegu/gunwigun/" not in legacy_html:
        raise RuntimeError("Invalid legacy Gyeongbuk Gunwi redirect")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Validate mappings without writing pages")
    parser.add_argument(
        "--validate-output", action="store_true", help="Validate previously generated HTML pages"
    )
    args = parser.parse_args()

    area_slugs = load_area_slugs()
    localities = load_localities(area_slugs)
    locality_count = sum(len(items) for items in localities.values())
    print(
        f"Validated {len(localities)} parent areas and {locality_count} localities "
        f"across {len(PROVINCES)} regions."
    )
    if args.validate_output:
        validate_output(area_slugs, localities)
        return
    if args.check:
        return

    update_landing_pages()
    city_count, locality_count = generate_pages(area_slugs, localities)
    write_legacy_redirects()
    run([sys.executable, str(ROOT / "add_regional_keywords.py")], check=True)
    validate_output(area_slugs, localities)
    print(f"Updated {len(PROVINCES)} landing pages and {city_count} city/county pages.")
    print(f"Generated {locality_count} dong/eup/myeon pages.")


if __name__ == "__main__":
    main()