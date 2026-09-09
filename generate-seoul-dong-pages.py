from collections import defaultdict
import json
from pathlib import Path
import re
import shutil
from urllib.request import urlopen


DATA_URL = (
    "https://raw.githubusercontent.com/vuski/admdongkor/master/"
    "ver20260201/HangJeongDong_ver20260201.geojson"
)
DISTRICT_SLUGS = {
    "강남구": "gangnamgu", "강동구": "gangdonggu", "강북구": "gangbukgu",
    "강서구": "gangseogu", "관악구": "gwanakgu", "광진구": "gwangjingu",
    "구로구": "gurogu", "금천구": "geumcheongu", "노원구": "nowongu",
    "도봉구": "dobonggu", "동대문구": "dongdaemungu", "동작구": "dongjakgu",
    "마포구": "mapogu", "서대문구": "seodaemungu", "서초구": "seochogu",
    "성동구": "seongdonggu", "성북구": "seongbukgu", "송파구": "songpagu",
    "양천구": "yangcheongu", "영등포구": "yeongdeungpogu", "용산구": "yongsangu",
    "은평구": "eunpyeonggu", "종로구": "jongnogu", "중구": "junggu",
    "중랑구": "jungnanggu",
}
LEGACY_SEODAEMUN_SLUGS = (
    "chunghyeondong", "cheonyeondong", "bugahyeondong", "sinchondong",
    "yeonhuidong", "hongje1dong", "hongje2dong", "hongje3dong",
    "hongeun1dong", "hongeun2dong", "namgajwa1dong", "namgajwa2dong",
    "bukgajwa1dong", "bukgajwa2dong",
)

ROOT = Path(__file__).resolve().parent
DISTRICT_PAGE = ROOT / "regions" / "seoul-district.html"


def load_seoul_dongs():
    with urlopen(DATA_URL, timeout=60) as response:
        data = json.load(response)

    districts = defaultdict(list)
    for feature in data["features"]:
        properties = feature["properties"]
        code = str(properties.get("adm_cd2", ""))
        name = properties.get("adm_nm", "")
        if not code.startswith("11") or not name.startswith("서울특별시 "):
            continue
        _, district, dong = name.split(" ", 2)
        districts[district].append({"name": dong, "code": code})

    for dongs in districts.values():
        dongs.sort(key=lambda item: item["code"])
    if set(districts) != set(DISTRICT_SLUGS):
        missing = set(DISTRICT_SLUGS) - set(districts)
        extra = set(districts) - set(DISTRICT_SLUGS)
        raise RuntimeError(f"Unexpected Seoul districts. Missing={missing}, extra={extra}")
    return dict(districts)


def update_district_page(districts):
    html = DISTRICT_PAGE.read_text(encoding="utf-8")
    section = (
        '<section class="section" id="dongGuide" hidden><div class="section-head"><div>'
        '<p class="eyebrow"><span></span> SEOUL LOCAL GUIDE</p>'
        '<h2>설치할 행정동을<br><em>선택해주세요.</em></h2></div>'
        '<p><span id="dongDistrictName">서울</span> 행정동별 스마트무인자판기 설치 안내와 무료 견적 상담을 확인할 수 있습니다.</p>'
        '</div><div class="region-grid" id="dongGrid"></div></section>'
    )
    if 'id="dongGuide"' in html:
        html = re.sub(
            r'<section class="section" id="dongGuide".*?</section>',
            section,
            html,
            count=1,
        )
    else:
        html = html.replace('<section class="cta">', section + '<section class="cta">', 1)

    html = re.sub(r'<script>const area=.*?</script>', '', html, count=1)
    navigation = {
        district: {
            "slug": DISTRICT_SLUGS[district],
            "dongs": dongs,
        }
        for district, dongs in districts.items()
    }
    script = (
        '<script>const area=new URLSearchParams(location.search).get("area")||"서울";'
        'document.title=area+" 스마트무인자판기 설치 안내 | 수행코치";'
        'document.querySelectorAll("#areaName,#areaHeading,#areaCallout").forEach(element=>{element.textContent=area;});'
        f'const seoulDongs={json.dumps(navigation, ensure_ascii=False, separators=(",", ":"))};'
        'const selected=seoulDongs[area];if(selected){'
        'document.querySelector("#dongDistrictName").textContent=area;'
        'document.querySelector("#dongGrid").innerHTML=selected.dongs.map(dong=>'
        '`<a class="region-card" href="seoul/${selected.slug}/${dong.code}/"><span><b>${dong.name}</b><small>${area} ${dong.name} 설치 안내</small></span><span>↗</span></a>`).join("");'
        'document.querySelector("#dongGuide").hidden=false;}</script>'
    )
    html = html.replace('</body>', script + '</body>', 1)
    DISTRICT_PAGE.write_text(html, encoding="utf-8")


PAGE_TEMPLATE = '''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="서울특별시 {district} {dong} 스마트무인자판기 설치 비용과 무료 견적 상담 안내"><title>{district} {dong} 스마트무인자판기 설치 안내 | 수행코치</title><link rel="canonical" href="https://suhaengcoach.kr/regions/seoul/{district_slug}/{code}/"><link rel="stylesheet" href="../../../../installation.css"></head><body><header class="site-header"><a class="brand" href="../../../../index.html"><span class="brand-mark">S</span><span>수행코치 <small>VENDING STUDIO</small></span></a><nav class="main-nav"><a href="../../../seoul.html">서울 지역 안내</a><a href="../../../../index.html#consult">상담 문의</a></nav></header><main><section class="hero"><div class="hero-copy"><p class="eyebrow"><span></span> SEOUL LOCAL INSTALLATION GUIDE</p><h1>{district} {dong}<br><em>무인자판기</em><br>설치 안내</h1><p>{district} {dong}의 오피스·상업시설·교육시설·주거공간에 맞춰 상품 구성과 운영 동선을 설계합니다.</p></div><div class="hero-image"><img src="../../../../1234.png" alt="{district} {dong}에 설치 가능한 스마트 무인자판기"><div class="hero-label"><strong>{dong} 지역 상담</strong><span>무료 견적 안내</span></div></div></section><section class="section keyword-guide"><div class="section-head"><div><p class="eyebrow"><span></span> VENDING SOLUTION</p><h2>{dong} 공간별 자판기<br><em>맞춤 운영 안내</em></h2></div><p>설치 장소의 이용 시간과 고객 흐름을 확인해 음료·간식·생활용품 등 적합한 상품군을 제안합니다. 공간 규모와 예상 수요에 따라 냉장 자판기부터 여러 상품을 한 기기에 구성하는 멀티자판기까지 안내하며, 결제 방식과 재고 보충 동선도 함께 설계합니다.</p></div></section><section class="section process"><div class="section-head"><div><p class="eyebrow"><span></span> LOCAL INSTALLATION</p><h2>{dong} 설치 상담<br><em>진행 안내</em></h2></div><p>설치 장소 사진과 주소를 보내주시면 입지 조건을 확인해 가능한 모델과 운영 방향을 안내해드립니다.</p></div><div class="steps"><article><b>01</b><strong>입지 상담</strong><p>공간과 고객 흐름 확인</p></article><article><b>02</b><strong>맞춤 견적</strong><p>기기·상품·결제 안내</p></article><article><b>03</b><strong>설치 세팅</strong><p>결제 연결과 상품 진열</p></article><article><b>04</b><strong>운영 안내</strong><p>재고·매출 관리</p></article></div></section><section class="cta"><h2>{dong} 무료 설치 상담<br><em>받아보세요.</em></h2><a class="button" href="../../../../index.html#consult">상담 신청하기 <span>→</span></a></section></main><footer class="site-footer"><a href="../../../seoul-district.html?area={district_encoded}">← {district} 행정동 선택</a><p>수행코치 VENDING STUDIO</p></footer></body></html>'''


def generate_pages(districts):
    from urllib.parse import quote

    for slug in LEGACY_SEODAEMUN_SLUGS:
        legacy_path = ROOT / "regions" / "seoul" / "seodaemungu" / slug
        if legacy_path.exists():
            shutil.rmtree(legacy_path)

    created = 0
    for district, dongs in districts.items():
        district_slug = DISTRICT_SLUGS[district]
        for dong in dongs:
            page_path = ROOT / "regions" / "seoul" / district_slug / dong["code"] / "index.html"
            page_path.parent.mkdir(parents=True, exist_ok=True)
            page_path.write_text(
                PAGE_TEMPLATE.format(
                    district=district,
                    district_slug=district_slug,
                    district_encoded=quote(district),
                    dong=dong["name"],
                    code=dong["code"],
                ),
                encoding="utf-8",
            )
            created += 1
    return created


districts = load_seoul_dongs()
update_district_page(districts)
created = generate_pages(districts)
print(f"Updated Seoul navigation and generated {created} pages across {len(districts)} districts.")
