from collections import defaultdict
import json
from pathlib import Path
import re
from urllib.request import urlopen


DATA_URL = (
    "https://raw.githubusercontent.com/vuski/admdongkor/master/"
    "ver20260701/HangJeongDong_ver20260701.geojson"
)
CITY_SLUGS = {
    "가평군": "gapyeong", "고양시": "goyang", "과천시": "gwacheon",
    "광명시": "gwangmyeong", "광주시": "gwangju", "구리시": "guri",
    "군포시": "gunpo", "김포시": "gimpo", "남양주시": "namyangju",
    "동두천시": "dongducheon", "부천시": "bucheon", "성남시": "seongnam",
    "수원시": "suwon", "시흥시": "siheung", "안산시": "ansan",
    "안성시": "anseong", "안양시": "anyang", "양주시": "yangju",
    "양평군": "yangpyeong", "여주시": "yeoju", "연천군": "yeoncheon",
    "오산시": "osan", "용인시": "yongin", "의왕시": "uiwang",
    "의정부시": "uijeongbu", "이천시": "icheon", "파주시": "paju",
    "평택시": "pyeongtaek", "포천시": "pocheon", "하남시": "hanam",
    "화성시": "hwaseong",
}

ROOT = Path(__file__).resolve().parent
REGIONS_DIR = ROOT / "regions"


def load_localities():
    with urlopen(DATA_URL, timeout=60) as response:
        data = json.load(response)

    cities = defaultdict(list)
    for feature in data["features"]:
        properties = feature["properties"]
        if properties.get("sidonm") != "경기도":
            continue

        area_name = properties["adm_nm"].removeprefix("경기도 ")
        city = next((name for name in CITY_SLUGS if area_name.startswith(name)), None)
        if city is None:
            raise RuntimeError(f"Could not match Gyeonggi city for {properties['adm_nm']}")
        cities[city].append({
            "name": area_name.removeprefix(city).strip(),
            "code": str(properties["adm_cd2"]),
        })

    for localities in cities.values():
        localities.sort(key=lambda item: item["code"])

    if set(cities) != set(CITY_SLUGS):
        missing = set(CITY_SLUGS) - set(cities)
        extra = set(cities) - set(CITY_SLUGS)
        raise RuntimeError(f"Unexpected Gyeonggi cities. Missing={missing}, extra={extra}")
    return dict(cities)


def build_solution_section(city, locality=None):
    area = f"{city} {locality}" if locality else city
    heading = f"{locality} 설치 전" if locality else f"{city} 설치를 위한"
    return (
        '<section class="section keyword-guide"><div class="section-head"><div>'
        '<p class="eyebrow"><span></span> VENDING SOLUTION</p>'
        f'<h2>{heading}<br><em>4가지 핵심 설계</em></h2></div>'
        f'<p>{area}의 공간과 이용 고객을 먼저 살펴보고, 필요한 상품과 기기 구성을 정합니다. '
        '설치 이후에도 관리하기 편하도록 결제 방식과 재고 보충 동선까지 함께 안내합니다.</p>'
        '</div><div class="steps"><article><b>01</b><strong>공간 분석</strong>'
        '<p>설치 면적과 전원,<br>고객 이동 동선 확인</p></article>'
        '<article><b>02</b><strong>상품 구성</strong><p>음료·간식·생활용품 중<br>수요에 맞는 품목 제안</p></article>'
        '<article><b>03</b><strong>기기·결제</strong><p>상품 크기에 맞는 기기와<br>카드 결제 방식 선택</p></article>'
        '<article><b>04</b><strong>운영 동선</strong><p>재고 보충과 매출 확인이<br>편리한 관리 방법 안내</p></article></div></section>'
    )


def update_city_pages(cities):
    for city, localities in cities.items():
        city_slug = CITY_SLUGS[city]
        page_path = REGIONS_DIR / f"{city_slug}.html"
        html = page_path.read_text(encoding="utf-8")
        html, solution_count = re.subn(
            r'<section class="section keyword-guide">.*?</section>',
            build_solution_section(city),
            html,
            count=1,
        )
        if solution_count != 1:
            raise RuntimeError(f"Could not update solution content in {page_path.name}")
        cards = "".join(
            f'<a class="region-card" href="gyeonggi/{city_slug}/{locality["code"]}/">'
            f'<span><b>{locality["name"]}</b><small>{city} {locality["name"]} 설치 안내</small></span>'
            '<span>↗</span></a>'
            for locality in localities
        )
        section = (
            '<section class="section" id="localGuide"><div class="section-head"><div>'
            '<p class="eyebrow"><span></span> GYEONGGI LOCAL GUIDE</p>'
            f'<h2>{city} 설치 지역을<br><em>선택해주세요.</em></h2></div>'
            f'<p>{city} 동·읍·면별 스마트무인자판기 설치 안내와 무료 견적 상담을 확인할 수 있습니다.</p>'
            f'</div><div class="region-grid">{cards}</div></section>'
        )

        if 'id="localGuide"' in html:
            html = re.sub(
                r'<section class="section" id="localGuide">.*?</section>',
                section,
                html,
                count=1,
            )
        else:
            marker = '<section class="section process"><p class="eyebrow"><span></span> START WITH A CHAT</p>'
            if marker not in html:
                marker = '<section class="cta">'
            if marker not in html:
                raise RuntimeError(f"Could not find insertion point in {page_path.name}")
            html = html.replace(marker, section + marker, 1)
        page_path.write_text(html, encoding="utf-8")


PAGE_TEMPLATE = '''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="경기도 {city} {locality} 스마트무인자판기 설치 비용과 무료 견적 상담 안내"><title>{city} {locality} 스마트무인자판기 설치 안내 | 수행코치</title><link rel="canonical" href="https://suhaengcoach.kr/regions/gyeonggi/{city_slug}/{code}/"><link rel="stylesheet" href="../../../../installation.css"></head><body><header class="site-header"><a class="brand" href="../../../../index.html"><span class="brand-mark">S</span><span>수행코치 <small>VENDING STUDIO</small></span></a><nav class="main-nav"><a href="../../../{city_slug}.html">{city} 지역 안내</a><a href="../../../../index.html#consult">상담 문의</a></nav></header><main><section class="hero"><div class="hero-copy"><p class="eyebrow"><span></span> GYEONGGI LOCAL INSTALLATION GUIDE</p><h1>{city} {locality}<br><em>무인자판기</em><br>설치 안내</h1><p>{city} {locality}의 오피스·상업시설·교육시설·주거공간에 맞춰 상품 구성과 운영 동선을 설계합니다.</p></div><div class="hero-image"><img src="../../../../1234.png" alt="{city} {locality}에 설치 가능한 스마트 무인자판기"><div class="hero-label"><strong>{locality} 지역 상담</strong><span>무료 견적 안내</span></div></div></section><section class="section keyword-guide"><div class="section-head"><div><p class="eyebrow"><span></span> VENDING SOLUTION</p><h2>{locality} 공간별 자판기<br><em>맞춤 운영 안내</em></h2></div><p>설치 장소의 이용 시간과 고객 흐름을 확인해 음료·간식·생활용품 등 적합한 상품군을 제안합니다. 공간 규모와 예상 수요에 따라 냉장 자판기부터 여러 상품을 한 기기에 구성하는 멀티자판기까지 안내하며, 결제 방식과 재고 보충 동선도 함께 설계합니다.</p></div></section><section class="section process"><div class="section-head"><div><p class="eyebrow"><span></span> LOCAL INSTALLATION</p><h2>{locality} 설치 상담<br><em>진행 안내</em></h2></div><p>설치 장소 사진과 주소를 보내주시면 입지 조건을 확인해 가능한 모델과 운영 방향을 안내해드립니다.</p></div><div class="steps"><article><b>01</b><strong>입지 상담</strong><p>공간과 고객 흐름 확인</p></article><article><b>02</b><strong>맞춤 견적</strong><p>기기·상품·결제 안내</p></article><article><b>03</b><strong>설치 세팅</strong><p>결제 연결과 상품 진열</p></article><article><b>04</b><strong>운영 안내</strong><p>재고·매출 관리 안내</p></article></div></section><section class="cta"><h2>{city} {locality}<br><em>무료 설치 상담</em></h2><a class="button" href="../../../../index.html#consult">상담 신청하기 <span>→</span></a></section></main><footer class="site-footer"><a href="../../../{city_slug}.html">← {city} 동·읍·면 선택</a><p>수행코치 VENDING STUDIO</p></footer><!-- Administrative names and codes: SGIS / vuski/admdongkor, CC BY 4.0 --></body></html>'''
PAGE_TEMPLATE, solution_template_count = re.subn(
    r'<section class="section keyword-guide">.*?</section>',
    "{solution_section}",
    PAGE_TEMPLATE,
    count=1,
)
if solution_template_count != 1:
    raise RuntimeError("Could not prepare detail-page solution template")


def generate_pages(cities):
    created = 0
    for city, localities in cities.items():
        city_slug = CITY_SLUGS[city]
        for locality in localities:
            page_path = REGIONS_DIR / "gyeonggi" / city_slug / locality["code"] / "index.html"
            page_path.parent.mkdir(parents=True, exist_ok=True)
            page_path.write_text(
                PAGE_TEMPLATE.format(
                    city=city,
                    city_slug=city_slug,
                    locality=locality["name"],
                    code=locality["code"],
                    solution_section=build_solution_section(city, locality["name"]),
                ),
                encoding="utf-8",
            )
            created += 1
    return created


localities_by_city = load_localities()
update_city_pages(localities_by_city)
created = generate_pages(localities_by_city)
print(f"Updated 31 Gyeonggi city pages and generated {created} locality pages.")