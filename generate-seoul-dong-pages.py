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


def build_solution_section(district, dong=None):
    area = f"{district} {dong}" if dong else district
    heading = f"{dong} 설치 전" if dong else f"{district} 설치를 위한"
    return (
        '<!-- VENDING CONTENT START -->'
        '<section class="section keyword-guide"><div class="section-head"><div>'
        '<p class="eyebrow"><span></span> VENDING SOLUTION</p>'
        f'<h2>{heading}<br><em>4가지 핵심 설계</em></h2></div>'
        f'<p>{area}의 공간과 이용 고객을 먼저 살펴보고, 필요한 상품과 기기 구성을 정합니다. '
        '설치 이후에도 관리하기 편하도록 결제 방식과 재고 보충 동선까지 함께 안내합니다.</p>'
        '</div><div class="steps"><article><b>01</b><strong>공간 분석</strong><p>설치 면적과 전원,<br>고객 이동 동선 확인</p></article>'
        '<article><b>02</b><strong>상품 구성</strong><p>음료·간식·생활용품 중<br>수요에 맞는 품목 제안</p></article>'
        '<article><b>03</b><strong>기기·결제</strong><p>상품 크기에 맞는 기기와<br>카드 결제 방식 선택</p></article>'
        '<article><b>04</b><strong>운영 동선</strong><p>재고 보충과 매출 확인이<br>편리한 관리 방법 안내</p></article></div></section>'
        '<section class="section vending-use-cases"><div class="section-head"><div>'
        '<p class="eyebrow"><span></span> SPACE &amp; PRODUCT GUIDE</p>'
        f'<h2>{area} 공간에 맞는<br><em>자판기 상품 구성</em></h2></div>'
        '<p>같은 무인자판기라도 설치 장소에 따라 잘 팔리는 상품과 필요한 기능이 달라집니다. 주요 이용 시간과 고객 목적을 기준으로 공간별 구성을 구체화합니다.</p></div>'
        '<div class="keyword-card-grid">'
        '<article><span>WORK</span><h3>오피스·공장·물류센터</h3><p>출근 시간과 교대 근무 수요에 맞춰 커피, 냉장 음료, 간식, 간편식을 구성합니다. 휴게 공간에서는 빠르게 고르고 결제할 수 있는 진열과 동선이 중요합니다.</p><small>음료 자판기 · 간식 자판기 · 간편식</small></article>'
        '<article><span>LIVING</span><h3>아파트·학교·학원</h3><p>생활권 이용자가 자주 찾는 음료와 스낵, 문구, 위생용품, 소형 생활용품을 함께 제안합니다. 어린이와 학생이 이용하는 공간은 상품 높이와 안전한 진열도 확인합니다.</p><small>생활용품 자판기 · 문구 · 스낵</small></article>'
        '<article><span>STAY</span><h3>병원·호텔·숙박시설</h3><p>보호자와 투숙객이 늦은 시간에도 구매할 수 있도록 생수, 간편식, 여행용품, 위생용품 중심으로 구성합니다. 로비와 객실층 등 설치 위치별 수요도 나눠 살펴봅니다.</p><small>병원 자판기 · 호텔 자판기 · 여행용품</small></article>'
        '<article><span>LEISURE</span><h3>골프장·헬스장·세차장</h3><p>골프용품과 기능성 음료, 단백질 간식, 세정제와 타월처럼 방문 목적이 분명한 상품을 판매합니다. 전문용품은 포장 크기와 보관 조건에 맞는 칸 구성이 필요합니다.</p><small>골프장 자판기 · 세차용품 자판기</small></article>'
        '</div></section>'
        '<section class="section vending-machine-guide"><div class="section-head"><div>'
        '<p class="eyebrow"><span></span> MACHINE &amp; OPERATION</p><h2>상품부터 결제까지<br><em>운영에 맞는 기기 선택</em></h2></div>'
        f'<p>{area}에서 판매할 품목이 정해지면 보관 온도, 상품 크기, 결제 수단과 관리 방식을 기준으로 기기를 선택합니다. 초기 설치비용뿐 아니라 재고 보충과 장기 운영의 편의성까지 함께 비교합니다.</p></div>'
        '<div class="keyword-card-grid">'
        '<article><span>01</span><h3>냉장 음료 자판기</h3><p>캔·페트병 음료와 유제품처럼 일정한 온도 관리가 필요한 상품에 적합합니다. 판매 품목의 용량과 진열 수량을 확인해 내부 칸을 구성합니다.</p><small>커피 · 생수 · 탄산음료 · 냉장식품</small></article>'
        '<article><span>02</span><h3>간식·디저트 자판기</h3><p>스낵, 베이커리, 디저트와 간편식은 포장이 눌리거나 걸리지 않도록 배출 방식과 칸 너비를 맞춥니다. 유통기한과 회전율을 고려한 소량 진열도 가능합니다.</p><small>간식 · 디저트 · 베이커리 · 간편식</small></article>'
        '<article><span>03</span><h3>멀티·생활용품 자판기</h3><p>크기가 다른 상품을 한 기기에서 판매할 때는 멀티자판기 구성이 효율적입니다. 생활용품, 지역 특산물, 골프용품 등 비정형 상품도 규격에 맞춰 검토합니다.</p><small>멀티자판기 · 생활용품 · 지역 특산물</small></article>'
        '<article><span>04</span><h3>스마트 결제·운영 관리</h3><p>카드와 간편결제 사용 환경을 확인하고, 재고 보충 주기와 매출 확인 방법을 운영자에게 안내합니다. 무인 운영 시간과 관리 인력에 맞는 방식을 선택합니다.</p><small>카드결제 · 간편결제 · 재고관리 · 매출확인</small></article>'
        '</div></section><!-- VENDING CONTENT END -->'
    )


def update_district_page(districts):
    html = DISTRICT_PAGE.read_text(encoding="utf-8")
    if 'gyeonggi-content.css' not in html:
        html = html.replace('</head>', '<link rel="stylesheet" href="../gyeonggi-content.css"></head>', 1)
    html, solution_count = re.subn(
        r'(?:<!-- VENDING CONTENT START -->.*?<!-- VENDING CONTENT END -->|<section class="section keyword-guide">.*?</section>)',
        build_solution_section('<span class="solutionAreaName">서울</span>'),
        html,
        count=1,
        flags=re.DOTALL,
    )
    if solution_count != 1:
        raise RuntimeError("Could not update Seoul district solution content")
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
        'document.querySelectorAll("#areaName,#areaHeading,#areaCallout,.solutionAreaName").forEach(element=>{element.textContent=area;});'
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


PAGE_TEMPLATE = PAGE_TEMPLATE.replace(
    '</head>',
    '<link rel="stylesheet" href="../../../../gyeonggi-content.css"></head>',
    1,
)
PAGE_TEMPLATE, solution_template_count = re.subn(
    r'<section class="section keyword-guide">.*?</section>',
    "{solution_section}",
    PAGE_TEMPLATE,
    count=1,
)
if solution_template_count != 1:
    raise RuntimeError("Could not prepare Seoul detail-page solution template")


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
                    solution_section=build_solution_section(district, dong["name"]),
                ),
                encoding="utf-8",
            )
            created += 1
    return created


districts = load_seoul_dongs()
update_district_page(districts)
created = generate_pages(districts)
print(f"Updated Seoul navigation and generated {created} pages across {len(districts)} districts.")
