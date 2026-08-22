from html import escape
from pathlib import Path
import re

ROOT = Path(__file__).parent
REGIONS = {
    "busan": "부산", "chungbuk": "충북", "chungnam": "충남", "daegu": "대구",
    "daejeon": "대전", "gangwon": "강원", "gwangju": "광주", "gyeongbuk": "경북",
    "incheon": "인천", "jeju": "제주", "jeonbuk": "전북", "jeonnam": "전남",
    "sejong": "세종", "ulsan": "울산", "seoul": "서울", "gyeonggi": "경기", "gyeongnam": "경남",
}
EXTRA_AREAS = {
    "seoul": {
        "강남구": "gangnamgu", "강동구": "gangdonggu", "강북구": "gangbukgu", "강서구": "gangseogu", "관악구": "gwanakgu",
        "광진구": "gwangjingu", "구로구": "gurogu", "금천구": "geumcheongu", "노원구": "nowongu", "도봉구": "dobonggu",
        "동대문구": "dongdaemungu", "동작구": "dongjakgu", "마포구": "mapogu", "서대문구": "seodaemungu", "서초구": "seochogu",
        "성동구": "seongdonggu", "성북구": "seongbukgu", "송파구": "songpagu", "양천구": "yangcheongu", "영등포구": "yeongdeungpogu",
        "용산구": "yongsangu", "은평구": "eunpyeonggu", "종로구": "jongnogu", "중구": "junggu", "중랑구": "jungnanggu",
    },
    "gyeonggi": {
        "가평군": "gapyeong", "고양시": "goyang", "과천시": "gwacheon", "광명시": "gwangmyeong", "광주시": "gwangju", "구리시": "guri", "군포시": "gunpo", "김포시": "gimpo", "남양주시": "namyangju", "동두천시": "dongducheon", "부천시": "bucheon", "성남시": "seongnam", "수원시": "suwon", "시흥시": "siheung", "안산시": "ansan", "안성시": "anseong", "안양시": "anyang", "양주시": "yangju", "양평군": "yangpyeong", "여주시": "yeoju", "연천군": "yeoncheon", "오산시": "osan", "용인시": "yongin", "의왕시": "uiwang", "의정부시": "uijeongbu", "이천시": "icheon", "파주시": "paju", "평택시": "pyeongtaek", "포천시": "pocheon", "하남시": "hanam", "화성시": "hwaseong",
    },
    "gyeongnam": {
        "거제시": "geoje", "거창군": "geochang", "고성군": "goseong", "김해시": "gimhae", "남해군": "namhae", "밀양시": "miryang", "사천시": "sacheon", "산청군": "sancheong", "양산시": "yangsan", "의령군": "uiryeong", "진주시": "jinju", "창녕군": "changnyeong", "창원시": "changwon", "통영시": "tongyeong", "하동군": "hadong", "함안군": "haman", "함양군": "hamyang", "합천군": "hapcheon",
    },
}
PRODUCTS = [
    ("이동식 카드단말기", "행사장·플리마켓·방문 판매처럼 장소가 바뀌는 현장에서 빠르게 결제할 수 있는 휴대형 단말기"),
    ("휴대용 단말기", "배달·출장·현장 접수에 필요한 카드·간편결제를 한 손에 처리하는 실사용 중심 단말기"),
    ("테이블오더", "매장 테이블에서 메뉴 선택과 주문·결제를 간편하게 연결하는 비대면 주문 시스템"),
    ("무인키오스크", "매장·병원·학원·공공시설에서 주문과 결제를 자동화하는 셀프 결제 키오스크"),
]


def area_name(page):
    match = re.search(r"<title>(.*?) 스마트무인자판기", page)
    if match:
        return re.sub(r"\s+", " ", match.group(1)).strip().split()[-1]
    return "해당 지역"


def product_cards():
    return "".join(
        f'<article class="terminal-card"><span class="terminal-number">0{index}</span>'
        f'<h3>{escape(name)}</h3><p>{escape(description)}</p>'
        f'<a href="#consult">상담 문의 <span>↗</span></a></article>'
        for index, (name, description) in enumerate(PRODUCTS, 1)
    )


def region_cards():
    cards = []
    for group, region in REGIONS.items():
        area_count = len(EXTRA_AREAS.get(group, {})) or len(list((ROOT / "regions" / group).glob("*/index.html")))
        cards.append(
            f'<a class="region-card" href="{group}/"><span><b>{region} 단말기 설치</b>'
            f'<small>{area_count}개 시·군·구별 상담 안내</small></span><span>↗</span></a>'
        )
    return "".join(cards)


landing = '''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="전국 이동식 카드단말기·휴대용 단말기·테이블오더·무인키오스크 설치 및 판매 안내"><title>단말기 설치·판매 | 수행코치</title><link rel="stylesheet" href="../installation.css"><link rel="stylesheet" href="terminal.css"></head><body><header class="site-header"><a class="brand" href="../index.html"><span class="brand-mark">S</span><span>수행코치 <small>VENDING STUDIO</small></span></a><nav class="main-nav"><a href="../installation.html">무인자판기</a><a href="../index.html#consult">상담 문의</a></nav></header><main><section class="hero"><div class="hero-copy"><p class="eyebrow"><span></span> PAYMENT SOLUTION</p><h1>공간과 현장에 맞는<br><em>단말기</em>를<br>설계합니다.</h1><p>이동식 카드단말기, 휴대용 단말기, 테이블오더, 무인키오스크까지 매장과 현장의 결제 흐름에 맞는 상품을 안내합니다.</p></div><div class="hero-image"><img src="../1234.png" alt="수행코치 단말기 결제 솔루션"><div class="hero-label"><strong>전국 단말기 상담</strong><span>시군구별 설치 안내</span></div></div></section><section class="section terminal-products"><div class="section-head"><div><p class="eyebrow"><span></span> TERMINAL PRODUCTS</p><h2>필요한 결제를<br><em>더 간편하게.</em></h2></div><p>업종과 이용 방식, 설치 장소를 확인해 결제 단말기와 주문 시스템을 맞춤으로 구성합니다.</p></div><div class="terminal-grid">{products}</div></section><section class="section"><div class="section-head"><div><p class="eyebrow"><span></span> LOCAL TERMINAL GUIDE</p><h2>설치할 지역을<br><em>선택해주세요.</em></h2></div><p>지역을 선택하면 해당 시·군·구의 단말기 판매·설치 상담 페이지로 연결됩니다.</p></div><div class="region-grid">{regions}</div></section><section class="cta" id="consult"><h2>우리 지역 단말기 상담을<br><em>시작해보세요.</em></h2><a class="button" href="../index.html#consult">무료 상담받기 <span>→</span></a></section></main><footer class="site-footer"><a href="../installation.html">← 무인자판기 설치 안내</a><p>수행코치 VENDING STUDIO</p></footer></body></html>'''

region_landing = '''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{region} 시·군·구별 이동식 카드단말기·테이블오더·무인키오스크 판매 및 설치 안내"><title>{region} 단말기 판매·설치 안내 | 수행코치</title><link rel="stylesheet" href="../../installation.css"><link rel="stylesheet" href="../terminal.css"></head><body><header class="site-header"><a class="brand" href="../../index.html"><span class="brand-mark">S</span><span>수행코치 <small>VENDING STUDIO</small></span></a><nav class="main-nav"><a href="../../terminal/">단말기 상품</a><a href="../../index.html#consult">상담 문의</a></nav></header><main><section class="hero"><div class="hero-copy"><p class="eyebrow"><span></span> {region} TERMINAL GUIDE</p><h1>{region} 지역에 맞는<br><em>단말기</em><br>상담 안내</h1><p>{region}의 매장·행사·출장 현장에 맞춰 이동식 카드단말기, 휴대용 단말기, 테이블오더, 무인키오스크를 제안합니다.</p></div><div class="hero-image"><img src="../../1234.png" alt="{region} 단말기 설치 상담"><div class="hero-label"><strong>{region} 단말기 상담</strong><span>시·군·구별 맞춤 안내</span></div></div></section><section class="section terminal-products"><div class="section-head"><div><p class="eyebrow"><span></span> LOCAL TERMINAL PRODUCTS</p><h2>{region}에 필요한<br><em>결제 솔루션</em></h2></div><p>사업 형태와 고객 동선에 맞춰 단말기 상품, 설치 위치, 사용 방법을 안내합니다.</p></div><div class="terminal-grid">{products}</div></section><section class="section"><div class="section-head"><div><p class="eyebrow"><span></span> CITY & COUNTY GUIDE</p><h2>상담할 지역을<br><em>선택해주세요.</em></h2></div><p>{region} 시·군·구별 페이지에서 매장과 현장에 맞는 단말기 상담을 확인할 수 있습니다.</p></div><div class="region-grid">{areas}</div></section><section class="cta" id="consult"><h2>{region} 단말기 상담을<br><em>시작해보세요.</em></h2><a class="button" href="../../index.html#consult">무료 상담받기 <span>→</span></a></section></main><footer class="site-footer"><a href="../../terminal/">← 단말기 지역 선택</a><p>수행코치 VENDING STUDIO</p></footer></body></html>'''

page = '''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{region} {area} 이동식 카드단말기·휴대용 단말기·테이블오더·무인키오스크 판매 및 설치 안내"><title>{region} {area} 단말기 판매·설치 안내 | 수행코치</title><link rel="stylesheet" href="../../../installation.css"><link rel="stylesheet" href="../../terminal.css"></head><body><header class="site-header"><a class="brand" href="../../../index.html"><span class="brand-mark">S</span><span>수행코치 <small>VENDING STUDIO</small></span></a><nav class="main-nav"><a href="../../">{region} 단말기 안내</a><a href="../../../index.html#consult">상담 문의</a></nav></header><main><section class="hero"><div class="hero-copy"><p class="eyebrow"><span></span> {region} {area} TERMINAL GUIDE</p><h1>{region} {area}<br><em>단말기</em><br>판매·설치 안내</h1><p>{region} {area} 지역의 매장, 행사, 출장 현장에 맞춰 이동식 카드단말기와 휴대용 단말기를 비롯해 테이블오더·무인키오스크를 안내합니다.</p></div><div class="hero-image"><img src="../../../1234.png" alt="{region} {area} 단말기 설치 상담"><div class="hero-label"><strong>{area} 단말기 상담</strong><span>무료 견적 안내</span></div></div></section><section class="section terminal-products"><div class="section-head"><div><p class="eyebrow"><span></span> LOCAL PAYMENT SOLUTION</p><h2>{area}에 맞는<br><em>단말기 구성</em></h2></div><p>사용 장소와 결제량을 확인해 필요한 상품과 설치 방법을 맞춤으로 제안합니다.</p></div><div class="terminal-grid">{products}</div></section><section class="section process"><p class="eyebrow"><span></span> INSTALLATION PROCESS</p><h2>{area} 단말기 상담<br><em>간단하게 진행됩니다.</em></h2><div class="steps"><article><b>01</b><strong>현장 상담</strong><p>업종과 사용 장소 확인</p></article><article><b>02</b><strong>상품 제안</strong><p>단말기·주문 시스템 구성</p></article><article><b>03</b><strong>설치 세팅</strong><p>결제 연결과 사용 안내</p></article><article><b>04</b><strong>운영 지원</strong><p>문의와 관리 방법 안내</p></article></div></section><section class="cta" id="consult"><h2>{area} 단말기 상담을<br><em>시작해보세요.</em></h2><a class="button" href="../../../index.html#consult">무료 상담받기 <span>→</span></a></section></main><footer class="site-footer"><a href="../../">← {region} 단말기 지역 선택</a><p>수행코치 VENDING STUDIO</p></footer></body></html>'''

output = ROOT / "terminal"
output.mkdir(exist_ok=True)
(output / "terminal.css").write_text("", encoding="utf-8")
(output / "index.html").write_text(landing.format(products=product_cards(), regions=region_cards()), encoding="utf-8")
created = 0
for group, region in REGIONS.items():
    source_dirs = sorted((ROOT / "regions" / group).glob("*/"))
    if group in EXTRA_AREAS:
        source_dirs = []
    areas = []
    for source_dir in source_dirs:
        source = source_dir / "index.html"
        if not source.exists():
            continue
        slug = source_dir.name
        area = area_name(source.read_text(encoding="utf-8-sig"))
        target = output / group / slug
        target.mkdir(parents=True, exist_ok=True)
        (target / "index.html").write_text(page.format(region=region, area=area, products=product_cards()), encoding="utf-8")
        areas.append(f'<a class="region-card" href="{slug}/"><span><b>{escape(area)} 단말기</b><small>{escape(area)} 판매·설치 안내</small></span><span>↗</span></a>')
        created += 1
    for area, slug in EXTRA_AREAS.get(group, {}).items():
        target = output / group / slug
        target.mkdir(parents=True, exist_ok=True)
        (target / "index.html").write_text(page.format(region=region, area=area, products=product_cards()), encoding="utf-8")
        areas.append(f'<a class="region-card" href="{slug}/"><span><b>{escape(area)} 단말기</b><small>{escape(area)} 판매·설치 안내</small></span><span>↗</span></a>')
        created += 1
    (output / group).mkdir(parents=True, exist_ok=True)
    (output / group / "index.html").write_text(region_landing.format(region=region, products=product_cards(), areas="".join(areas)), encoding="utf-8")
print(f"Generated {created} 시군구 단말기 pages.")
