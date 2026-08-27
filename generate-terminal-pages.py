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


landing = '''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="전국 카드단말기 설치·구매·개통 상담과 이동식 카드단말기, 테이블오더, 무인키오스크 판매 안내"><title>카드단말기 설치·판매·개통 | 수행코치</title><link rel="stylesheet" href="../installation.css"><link rel="stylesheet" href="terminal.css"></head><body><header class="site-header"><a class="brand" href="../index.html"><span class="brand-mark">S</span><span>수행코치 <small>VENDING STUDIO</small></span></a><nav class="main-nav"><a href="../installation.html">무인자판기</a><a href="../index.html#consult">상담 문의</a></nav></header><main><section class="hero"><div class="hero-copy"><p class="eyebrow"><span></span> PAYMENT SOLUTION</p><h1>공간과 현장에 맞는<br><em>단말기</em>를<br>설계합니다.</h1><p>카드단말기 설치·구매·개통부터 이동식 카드단말기, 테이블오더, 무인키오스크까지 매장과 현장의 결제 흐름에 맞는 상품을 안내합니다.</p></div><div class="hero-image"><img src="../1234.png" alt="카드단말기와 무인 결제 솔루션 설치 상담"><div class="hero-label"><strong>전국 단말기 상담</strong><span>시군구별 설치 안내</span></div></div></section><section class="section terminal-products"><div class="section-head"><div><p class="eyebrow"><span></span> TERMINAL PRODUCTS</p><h2>필요한 결제를<br><em>더 간편하게.</em></h2></div><p>업종과 이용 방식, 설치 장소를 확인해 결제 단말기와 주문 시스템을 맞춤으로 구성합니다.</p></div><div class="terminal-grid">{products}</div></section><section class="section terminal-guide"><div class="section-head"><div><p class="eyebrow"><span></span> TERMINAL BUYING GUIDE</p><h2>카드단말기 설치부터<br><em>구매·개통까지.</em></h2></div><p>신규 사업자와 소상공인이 매장 운영에 필요한 결제 환경을 한 번에 준비할 수 있도록 상담합니다.</p></div><div class="guide-grid"><article><span>01</span><h3>사업자 맞춤 카드단말기</h3><p>개인사업자·법인사업자 여부와 업종, 월 결제량을 확인해 유선·무선 카드단말기와 POS 단말기를 제안합니다. 카드가맹점 신청과 신규 개통에 필요한 절차도 함께 안내합니다.</p></article><article><span>02</span><h3>이동식·휴대용 현장 결제</h3><p>배달, 출장, 방문판매, 행사장, 플리마켓과 푸드트럭에는 휴대용 카드단말기나 블루투스·모바일 결제 단말기처럼 이동이 편한 구성을 안내합니다.</p></article><article><span>03</span><h3>매장 주문·결제 자동화</h3><p>음식점, 카페, 병원, 학원 등에는 테이블오더와 무인키오스크를 매장 동선에 맞춰 구성합니다. 주문·결제와 포스 연동 여부까지 확인해 설치를 돕습니다.</p></article></div></section><section class="section terminal-faq"><div class="section-head"><div><p class="eyebrow"><span></span> FREQUENTLY ASKED QUESTIONS</p><h2>단말기 설치 전<br><em>궁금한 점.</em></h2></div><p>가격만 비교하기보다 업종과 사용 환경, 필요한 기능을 함께 확인해야 알맞은 단말기를 선택할 수 있습니다.</p></div><div class="faq-list"><details><summary>카드단말기 가격과 설치 비용은 어떻게 결정되나요?</summary><p>유선·무선 여부, 통신 방식, 영수증 출력과 POS 연동 같은 기능, 구매 또는 임대 조건에 따라 달라집니다. 상담 시 사용 장소와 필요한 기능을 확인한 뒤 적합한 구성과 비용을 안내합니다.</p></details><details><summary>신규 사업자도 카드단말기 신청과 개통이 가능한가요?</summary><p>개인사업자와 법인사업자 모두 신청할 수 있습니다. 사업자 정보와 영업 형태를 확인해 카드가맹점 등록, 단말기 개통과 설치에 필요한 준비 사항을 안내합니다.</p></details><details><summary>카드결제 수수료나 월 사용료도 상담할 수 있나요?</summary><p>카드결제 수수료는 사업자 유형과 카드사 정책 등에 따라 달라질 수 있으며, 단말기 통신비와 월 사용료는 선택한 상품 조건에 따라 달라집니다. 계약 전에 적용 조건을 구체적으로 확인해드립니다.</p></details><details><summary>테이블오더와 키오스크 중 무엇이 적합한가요?</summary><p>테이블에서 추가 주문이 많은 음식점은 테이블오더가 편리하고, 입구나 카운터에서 주문과 결제를 한 번에 처리하려면 무인키오스크가 적합합니다. 고객 동선과 기존 포스기 연동 여부를 기준으로 제안합니다.</p></details></div></section><section class="section"><div class="section-head"><div><p class="eyebrow"><span></span> LOCAL TERMINAL GUIDE</p><h2>설치할 지역을<br><em>선택해주세요.</em></h2></div><p>지역을 선택하면 해당 시·군·구의 카드단말기·포스기·테이블오더·키오스크 판매 및 설치 상담 페이지로 연결됩니다.</p></div><div class="region-grid">{regions}</div></section><section class="cta" id="consult"><h2>우리 지역 단말기 상담을<br><em>시작해보세요.</em></h2><a class="button" href="../index.html#consult">무료 상담받기 <span>→</span></a></section></main><footer class="site-footer"><a href="../installation.html">← 무인자판기 설치 안내</a><p>수행코치 VENDING STUDIO</p></footer></body></html>'''

region_landing = '''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{region} 시·군·구별 이동식 카드단말기·테이블오더·무인키오스크 판매 및 설치 안내"><title>{region} 단말기 판매·설치 안내 | 수행코치</title><link rel="stylesheet" href="../../installation.css"><link rel="stylesheet" href="../terminal.css"></head><body><header class="site-header"><a class="brand" href="../../index.html"><span class="brand-mark">S</span><span>수행코치 <small>VENDING STUDIO</small></span></a><nav class="main-nav"><a href="../../terminal/">단말기 상품</a><a href="../../index.html#consult">상담 문의</a></nav></header><main><section class="hero"><div class="hero-copy"><p class="eyebrow"><span></span> {region} TERMINAL GUIDE</p><h1>{region} 지역에 맞는<br><em>단말기</em><br>상담 안내</h1><p>{region}의 매장·행사·출장 현장에 맞춰 이동식 카드단말기, 휴대용 단말기, 테이블오더, 무인키오스크를 제안합니다.</p></div><div class="hero-image"><img src="../../1234.png" alt="{region} 단말기 설치 상담"><div class="hero-label"><strong>{region} 단말기 상담</strong><span>시·군·구별 맞춤 안내</span></div></div></section><section class="section terminal-products"><div class="section-head"><div><p class="eyebrow"><span></span> LOCAL TERMINAL PRODUCTS</p><h2>{region}에 필요한<br><em>결제 솔루션</em></h2></div><p>사업 형태와 고객 동선에 맞춰 단말기 상품, 설치 위치, 사용 방법을 안내합니다.</p></div><div class="terminal-grid">{products}</div></section><section class="section"><div class="section-head"><div><p class="eyebrow"><span></span> CITY & COUNTY GUIDE</p><h2>상담할 지역을<br><em>선택해주세요.</em></h2></div><p>{region} 시·군·구별 페이지에서 매장과 현장에 맞는 단말기 상담을 확인할 수 있습니다.</p></div><div class="region-grid">{areas}</div></section><section class="cta" id="consult"><h2>{region} 단말기 상담을<br><em>시작해보세요.</em></h2><a class="button" href="../../index.html#consult">무료 상담받기 <span>→</span></a></section></main><footer class="site-footer"><a href="../../terminal/">← 단말기 지역 선택</a><p>수행코치 VENDING STUDIO</p></footer></body></html>'''

page = '''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{region} {area} 이동식 카드단말기·휴대용 단말기·테이블오더·무인키오스크 판매 및 설치 안내"><title>{region} {area} 단말기 판매·설치 안내 | 수행코치</title><link rel="stylesheet" href="../../../installation.css"><link rel="stylesheet" href="../../terminal.css"></head><body><header class="site-header"><a class="brand" href="../../../index.html"><span class="brand-mark">S</span><span>수행코치 <small>VENDING STUDIO</small></span></a><nav class="main-nav"><a href="../../">{region} 단말기 안내</a><a href="../../../index.html#consult">상담 문의</a></nav></header><main><section class="hero"><div class="hero-copy"><p class="eyebrow"><span></span> {region} {area} TERMINAL GUIDE</p><h1>{region} {area}<br><em>단말기</em><br>판매·설치 안내</h1><p>{region} {area} 지역의 매장, 행사, 출장 현장에 맞춰 이동식 카드단말기와 휴대용 단말기를 비롯해 테이블오더·무인키오스크를 안내합니다.</p></div><div class="hero-image"><img src="../../../1234.png" alt="{region} {area} 단말기 설치 상담"><div class="hero-label"><strong>{area} 단말기 상담</strong><span>무료 견적 안내</span></div></div></section><section class="section terminal-products"><div class="section-head"><div><p class="eyebrow"><span></span> LOCAL PAYMENT SOLUTION</p><h2>{area}에 맞는<br><em>단말기 구성</em></h2></div><p>사용 장소와 결제량을 확인해 필요한 상품과 설치 방법을 맞춤으로 제안합니다.</p></div><div class="terminal-grid">{products}</div></section><section class="section process"><p class="eyebrow"><span></span> INSTALLATION PROCESS</p><h2>{area} 단말기 상담<br><em>간단하게 진행됩니다.</em></h2><div class="steps"><article><b>01</b><strong>현장 상담</strong><p>업종과 사용 장소 확인</p></article><article><b>02</b><strong>상품 제안</strong><p>단말기·주문 시스템 구성</p></article><article><b>03</b><strong>설치 세팅</strong><p>결제 연결과 사용 안내</p></article><article><b>04</b><strong>운영 지원</strong><p>문의와 관리 방법 안내</p></article></div></section><section class="cta" id="consult"><h2>{area} 단말기 상담을<br><em>시작해보세요.</em></h2><a class="button" href="../../../index.html#consult">무료 상담받기 <span>→</span></a></section></main><footer class="site-footer"><a href="../../">← {region} 단말기 지역 선택</a><p>수행코치 VENDING STUDIO</p></footer></body></html>'''

output = ROOT / "terminal"
output.mkdir(exist_ok=True)
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
