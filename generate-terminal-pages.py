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


AREA_NAME_OVERRIDES = {
    ("gyeongbuk", "gunwi"): "군위군",
}


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


landing = '''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="전국 카드단말기 설치·구매·개통 상담과 이동식 카드단말기, 테이블오더, 무인키오스크 판매 안내"><title>카드단말기 설치·판매·개통 | 더세이브 수행코치</title><link rel="stylesheet" href="../installation.css"><link rel="stylesheet" href="terminal.css"></head><body><header class="site-header"><a class="brand" href="../index.html"><span class="brand-mark">S</span><span>더세이브 수행코치 <small>VENDING STUDIO</small></span></a><nav class="main-nav"><a href="../installation.html">무인자판기</a><a href="../index.html#consult">상담 문의</a></nav></header><main><section class="hero"><div class="hero-copy"><p class="eyebrow"><span></span> PAYMENT SOLUTION</p><h1>공간과 현장에 맞는<br><em>단말기</em>를<br>설계합니다.</h1><p>카드단말기 설치·구매·개통부터 이동식 카드단말기, 테이블오더, 무인키오스크까지 매장과 현장의 결제 흐름에 맞는 상품을 안내합니다.</p></div><div class="hero-image"><img src="../1234.png" alt="카드단말기와 무인 결제 솔루션 설치 상담"><div class="hero-label"><strong>전국 단말기 상담</strong><span>시군구별 설치 안내</span></div></div></section><section class="section terminal-products"><div class="section-head"><div><p class="eyebrow"><span></span> TERMINAL PRODUCTS</p><h2>필요한 결제를<br><em>더 간편하게.</em></h2></div><p>업종과 이용 방식, 설치 장소를 확인해 결제 단말기와 주문 시스템을 맞춤으로 구성합니다.</p></div><div class="terminal-grid">{products}</div></section><section class="section terminal-guide"><div class="section-head"><div><p class="eyebrow"><span></span> TERMINAL BUYING GUIDE</p><h2>카드단말기 설치부터<br><em>구매·개통까지.</em></h2></div><p>신규 사업자와 소상공인이 매장 운영에 필요한 결제 환경을 한 번에 준비할 수 있도록 상담합니다.</p></div><div class="guide-grid"><article><span>01</span><h3>사업자 맞춤 카드단말기</h3><p>개인사업자·법인사업자 여부와 업종, 월 결제량을 확인해 유선·무선 카드단말기와 POS 단말기를 제안합니다. 카드가맹점 신청과 신규 개통에 필요한 절차도 함께 안내합니다.</p></article><article><span>02</span><h3>이동식·휴대용 현장 결제</h3><p>배달, 출장, 방문판매, 행사장, 플리마켓과 푸드트럭에는 휴대용 카드단말기나 블루투스·모바일 결제 단말기처럼 이동이 편한 구성을 안내합니다.</p></article><article><span>03</span><h3>매장 주문·결제 자동화</h3><p>음식점, 카페, 병원, 학원 등에는 테이블오더와 무인키오스크를 매장 동선에 맞춰 구성합니다. 주문·결제와 포스 연동 여부까지 확인해 설치를 돕습니다.</p></article></div></section><section class="section terminal-faq"><div class="section-head"><div><p class="eyebrow"><span></span> FREQUENTLY ASKED QUESTIONS</p><h2>단말기 설치 전<br><em>궁금한 점.</em></h2></div><p>가격만 비교하기보다 업종과 사용 환경, 필요한 기능을 함께 확인해야 알맞은 단말기를 선택할 수 있습니다.</p></div><div class="faq-list"><details><summary>카드단말기 가격과 설치 비용은 어떻게 결정되나요?</summary><p>유선·무선 여부, 통신 방식, 영수증 출력과 POS 연동 같은 기능, 구매 또는 임대 조건에 따라 달라집니다. 상담 시 사용 장소와 필요한 기능을 확인한 뒤 적합한 구성과 비용을 안내합니다.</p></details><details><summary>신규 사업자도 카드단말기 신청과 개통이 가능한가요?</summary><p>개인사업자와 법인사업자 모두 신청할 수 있습니다. 사업자 정보와 영업 형태를 확인해 카드가맹점 등록, 단말기 개통과 설치에 필요한 준비 사항을 안내합니다.</p></details><details><summary>카드결제 수수료나 월 사용료도 상담할 수 있나요?</summary><p>카드결제 수수료는 사업자 유형과 카드사 정책 등에 따라 달라질 수 있으며, 단말기 통신비와 월 사용료는 선택한 상품 조건에 따라 달라집니다. 계약 전에 적용 조건을 구체적으로 확인해드립니다.</p></details><details><summary>테이블오더와 키오스크 중 무엇이 적합한가요?</summary><p>테이블에서 추가 주문이 많은 음식점은 테이블오더가 편리하고, 입구나 카운터에서 주문과 결제를 한 번에 처리하려면 무인키오스크가 적합합니다. 고객 동선과 기존 포스기 연동 여부를 기준으로 제안합니다.</p></details></div></section><section class="section"><div class="section-head"><div><p class="eyebrow"><span></span> LOCAL TERMINAL GUIDE</p><h2>설치할 지역을<br><em>선택해주세요.</em></h2></div><p>지역을 선택하면 해당 시·군·구의 카드단말기·포스기·테이블오더·키오스크 판매 및 설치 상담 페이지로 연결됩니다.</p></div><div class="region-grid">{regions}</div></section><section class="cta" id="consult"><h2>우리 지역 단말기 상담을<br><em>시작해보세요.</em></h2><a class="button" href="../index.html#consult">무료 상담받기 <span>→</span></a></section></main><footer class="site-footer"><a href="../installation.html">← 무인자판기 설치 안내</a><p>더세이브 수행코치 VENDING STUDIO</p></footer></body></html>'''

landing = landing.replace(
    '<meta name="description" content="전국 카드단말기 설치·구매·개통 상담과 이동식 카드단말기, 테이블오더, 무인키오스크 판매 안내">',
    '<meta name="description" content="카드단말기 설치·신청·개통과 가격 상담. 유선·무선·휴대용 카드단말기, 포스기, 테이블오더, 키오스크를 업종과 매장 환경에 맞춰 안내합니다."><link rel="canonical" href="https://suhaengcoach.kr/terminal/">',
)

terminal_keyword_content = '''<section class="section terminal-compare"><div class="section-head"><div><p class="eyebrow"><span></span> TERMINAL COMPARISON</p><h2>유선·무선·휴대용,<br><em>어떤 단말기가 맞을까요?</em></h2></div><p>카드단말기는 가격보다 결제 장소, 이동 여부, 통신 환경과 기존 포스기 연동을 먼저 확인해야 운영 중 불편을 줄일 수 있습니다.</p></div><div class="compare-table" role="region" aria-label="카드단말기 종류 비교" tabindex="0"><table><thead><tr><th>구분</th><th>추천 환경</th><th>주요 장점</th><th>확인할 점</th></tr></thead><tbody><tr><th>유선 카드단말기</th><td>카운터가 고정된 음식점·카페·소매점</td><td>안정적인 통신과 영수증 출력, 포스기 연동</td><td>인터넷 회선과 설치 위치</td></tr><tr><th>무선 카드단말기</th><td>테이블 결제·넓은 매장·야외 좌석</td><td>매장 안에서 자유롭게 이동하며 결제</td><td>통신 음영과 충전 방식</td></tr><tr><th>휴대용 카드단말기</th><td>배달·출장·방문판매·플리마켓</td><td>현장에서 카드와 간편결제 처리</td><td>데이터 통신과 사용 시간</td></tr><tr><th>POS·키오스크</th><td>상품·메뉴·주문 관리가 필요한 매장</td><td>결제와 주문, 매출 관리를 한 흐름으로 연결</td><td>프로그램·주방·프린터 연동</td></tr></tbody></table></div></section><section class="section terminal-use-cases"><div class="section-head"><div><p class="eyebrow"><span></span> BUSINESS TYPE GUIDE</p><h2>업종에 따라 달라지는<br><em>결제 환경 설계</em></h2></div><p>같은 카드단말기라도 주문 방식과 고객 동선이 다르면 필요한 기능도 달라집니다. 실제 운영 장면을 기준으로 구성을 제안합니다.</p></div><div class="keyword-card-grid"><article><span>FOOD</span><h3>음식점·카페</h3><p>카운터 결제에는 유선 단말기와 포스기를, 추가 주문이 잦은 매장에는 테이블오더를 검토합니다. 주방 프린터, 메뉴 관리와 분할 결제 가능 여부도 함께 확인합니다.</p><small>포스기 · 테이블오더 · 주방 프린터</small></article><article><span>RETAIL</span><h3>편의점·소매점</h3><p>바코드 스캐너, 상품 등록과 재고 관리가 필요하면 POS 연동형 구성이 효율적입니다. 현금영수증, 간편결제와 영수증 출력 방식까지 운영에 맞춥니다.</p><small>카드단말기 · POS · 바코드 스캐너</small></article><article><span>MOBILE</span><h3>배달·출장·행사</h3><p>전원과 인터넷이 고정되지 않은 현장에는 LTE 무선 또는 휴대용 카드단말기가 적합합니다. 이동 거리, 하루 결제 건수와 배터리 사용 시간을 기준으로 선택합니다.</p><small>무선 단말기 · 이동식 결제 · 간편결제</small></article><article><span>SELF</span><h3>병원·학원·무인매장</h3><p>접수와 수납을 줄이려면 키오스크를, 반복 주문을 줄이려면 테이블오더를 검토합니다. 화면 크기, 설치 높이와 직원 호출 동선까지 함께 설계합니다.</p><small>키오스크 · 셀프결제 · 비대면 주문</small></article></div></section><section class="section terminal-functions"><div class="section-head"><div><p class="eyebrow"><span></span> PAYMENT &amp; CONNECTION</p><h2>결제 기능과 연동까지<br><em>빠짐없이 확인합니다.</em></h2></div><p>설치 후 바로 사용할 수 있도록 필요한 결제 수단과 주변 기기, 통신 환경을 상담 단계에서 점검합니다.</p></div><div class="feature-list"><article><b>01</b><div><h3>카드·간편결제</h3><p>신용카드와 체크카드, 삼성페이 등 필요한 간편결제 지원 여부를 확인합니다.</p></div></article><article><b>02</b><div><h3>POS·프린터 연동</h3><p>기존 포스기, 영수증 프린터, 주방 주문서와 연결 가능한 구성을 살펴봅니다.</p></div></article><article><b>03</b><div><h3>유선·LTE 통신</h3><p>매장 인터넷과 이동 환경에 맞춰 안정적인 승인 통신 방식을 선택합니다.</p></div></article><article><b>04</b><div><h3>매출·상품 관리</h3><p>매출 조회, 메뉴 수정과 상품 관리가 필요한 경우 적합한 프로그램을 안내합니다.</p></div></article></div></section><section class="section terminal-opening"><div class="section-head"><div><p class="eyebrow"><span></span> OPENING CHECKLIST</p><h2>카드단말기 신청과 개통,<br><em>이렇게 준비하세요.</em></h2></div><p>신규 사업자 카드가맹점 등록은 업종과 사업 형태에 따라 확인 내용이 달라질 수 있습니다. 상담 후 필요한 항목을 정확히 안내합니다.</p></div><div class="opening-layout"><div class="opening-copy"><h3>상담 전에 알려주시면 더 빠릅니다</h3><ul><li>사업자등록 여부와 개인·법인 구분</li><li>매장 업종, 주소와 오픈 예정일</li><li>유선 인터넷과 와이파이 설치 여부</li><li>기존 POS·프린터·키오스크 사용 여부</li><li>매장 결제인지 배달·출장 결제인지</li></ul></div><div class="opening-steps"><article><span>01</span><h3>사용 환경 상담</h3><p>업종, 장소, 예상 결제 방식과 필요한 기능을 확인합니다.</p></article><article><span>02</span><h3>기기·비용 안내</h3><p>구매·임대 조건과 통신비, 부가 서비스 비용을 구분해 안내합니다.</p></article><article><span>03</span><h3>가맹 신청·개통</h3><p>사업자 형태에 맞는 준비사항을 확인하고 카드가맹점 신청을 진행합니다.</p></article><article><span>04</span><h3>설치·사용 안내</h3><p>승인 테스트 후 결제, 취소, 영수증과 정산 확인 방법을 설명합니다.</p></article></div></div></section>'''

landing = landing.replace(
    '<section class="section terminal-guide">',
    terminal_keyword_content + '<section class="section terminal-guide">',
)

region_landing = '''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{region} 시·군·구별 이동식 카드단말기·테이블오더·무인키오스크 판매 및 설치 안내"><title>{region} 단말기 판매·설치 안내 | 더세이브 수행코치</title><link rel="stylesheet" href="../../installation.css"><link rel="stylesheet" href="../terminal.css"></head><body><header class="site-header"><a class="brand" href="../../index.html"><span class="brand-mark">S</span><span>더세이브 수행코치 <small>VENDING STUDIO</small></span></a><nav class="main-nav"><a href="../../terminal/">단말기 상품</a><a href="../../index.html#consult">상담 문의</a></nav></header><main><section class="hero"><div class="hero-copy"><p class="eyebrow"><span></span> {region} TERMINAL GUIDE</p><h1>{region} 지역에 맞는<br><em>단말기</em><br>상담 안내</h1><p>{region}의 매장·행사·출장 현장에 맞춰 이동식 카드단말기, 휴대용 단말기, 테이블오더, 무인키오스크를 제안합니다.</p></div><div class="hero-image"><img src="../../1234.png" alt="{region} 단말기 설치 상담"><div class="hero-label"><strong>{region} 단말기 상담</strong><span>시·군·구별 맞춤 안내</span></div></div></section><section class="section terminal-products"><div class="section-head"><div><p class="eyebrow"><span></span> LOCAL TERMINAL PRODUCTS</p><h2>{region}에 필요한<br><em>결제 솔루션</em></h2></div><p>사업 형태와 고객 동선에 맞춰 단말기 상품, 설치 위치, 사용 방법을 안내합니다.</p></div><div class="terminal-grid">{products}</div></section><section class="section"><div class="section-head"><div><p class="eyebrow"><span></span> CITY & COUNTY GUIDE</p><h2>상담할 지역을<br><em>선택해주세요.</em></h2></div><p>{region} 시·군·구별 페이지에서 매장과 현장에 맞는 단말기 상담을 확인할 수 있습니다.</p></div><div class="region-grid">{areas}</div></section><section class="cta" id="consult"><h2>{region} 단말기 상담을<br><em>시작해보세요.</em></h2><a class="button" href="../../index.html#consult">무료 상담받기 <span>→</span></a></section></main><footer class="site-footer"><a href="../../terminal/">← 단말기 지역 선택</a><p>더세이브 수행코치 VENDING STUDIO</p></footer></body></html>'''

page = '''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{region} {area} 이동식 카드단말기·휴대용 단말기·테이블오더·무인키오스크 판매 및 설치 안내"><title>{region} {area} 단말기 판매·설치 안내 | 더세이브 수행코치</title><link rel="stylesheet" href="../../../installation.css"><link rel="stylesheet" href="../../terminal.css"></head><body><header class="site-header"><a class="brand" href="../../../index.html"><span class="brand-mark">S</span><span>더세이브 수행코치 <small>VENDING STUDIO</small></span></a><nav class="main-nav"><a href="../../">{region} 단말기 안내</a><a href="../../../index.html#consult">상담 문의</a></nav></header><main><section class="hero"><div class="hero-copy"><p class="eyebrow"><span></span> {region} {area} TERMINAL GUIDE</p><h1>{region} {area}<br><em>단말기</em><br>판매·설치 안내</h1><p>{region} {area} 지역의 매장, 행사, 출장 현장에 맞춰 이동식 카드단말기와 휴대용 단말기를 비롯해 테이블오더·무인키오스크를 안내합니다.</p></div><div class="hero-image"><img src="../../../1234.png" alt="{region} {area} 단말기 설치 상담"><div class="hero-label"><strong>{area} 단말기 상담</strong><span>무료 견적 안내</span></div></div></section><section class="section terminal-products"><div class="section-head"><div><p class="eyebrow"><span></span> LOCAL PAYMENT SOLUTION</p><h2>{area}에 맞는<br><em>단말기 구성</em></h2></div><p>사용 장소와 결제량을 확인해 필요한 상품과 설치 방법을 맞춤으로 제안합니다.</p></div><div class="terminal-grid">{products}</div></section><section class="section process"><p class="eyebrow"><span></span> INSTALLATION PROCESS</p><h2>{area} 단말기 상담<br><em>간단하게 진행됩니다.</em></h2><div class="steps"><article><b>01</b><strong>현장 상담</strong><p>업종과 사용 장소 확인</p></article><article><b>02</b><strong>상품 제안</strong><p>단말기·주문 시스템 구성</p></article><article><b>03</b><strong>설치 세팅</strong><p>결제 연결과 사용 안내</p></article><article><b>04</b><strong>운영 지원</strong><p>문의와 관리 방법 안내</p></article></div></section><section class="cta" id="consult"><h2>{area} 단말기 상담을<br><em>시작해보세요.</em></h2><a class="button" href="../../../index.html#consult">무료 상담받기 <span>→</span></a></section></main><footer class="site-footer"><a href="../../">← {region} 단말기 지역 선택</a><p>더세이브 수행코치 VENDING STUDIO</p></footer></body></html>'''


def local_terminal_content(location):
    name = escape(location)
    return f'''<section class="section terminal-compare"><div class="section-head"><div><p class="eyebrow"><span></span> LOCAL TERMINAL COMPARISON</p><h2>{name} 매장에 맞는<br><em>카드단말기 선택</em></h2></div><p>결제 장소와 이동 여부, 통신 환경, 기존 포스기 연동을 기준으로 비교하면 설치 후 불편과 불필요한 비용을 줄일 수 있습니다.</p></div><div class="compare-table" role="region" aria-label="{name} 카드단말기 종류 비교" tabindex="0"><table><thead><tr><th>구분</th><th>추천 환경</th><th>주요 장점</th><th>확인할 점</th></tr></thead><tbody><tr><th>유선 카드단말기</th><td>카운터가 고정된 음식점·카페·소매점</td><td>안정적인 통신과 영수증 출력, 포스기 연동</td><td>인터넷 회선과 설치 위치</td></tr><tr><th>무선 카드단말기</th><td>테이블 결제·넓은 매장·야외 좌석</td><td>매장 안에서 이동하며 편리하게 결제</td><td>통신 음영과 충전 방식</td></tr><tr><th>휴대용 카드단말기</th><td>배달·출장·방문판매·플리마켓</td><td>장소가 바뀌는 현장에서 카드 결제</td><td>데이터 통신과 사용 시간</td></tr><tr><th>POS·키오스크</th><td>상품·메뉴·주문 관리가 필요한 매장</td><td>결제와 주문, 매출 관리를 한 번에 연결</td><td>프로그램·주방·프린터 연동</td></tr></tbody></table></div></section><section class="section terminal-use-cases"><div class="section-head"><div><p class="eyebrow"><span></span> BUSINESS TYPE GUIDE</p><h2>{name} 업종별<br><em>결제 솔루션 안내</em></h2></div><p>같은 단말기라도 주문 방식과 고객 동선이 다르면 필요한 기능도 달라집니다. 실제 운영 장면을 기준으로 구성을 제안합니다.</p></div><div class="keyword-card-grid"><article><span>FOOD</span><h3>음식점·카페</h3><p>카운터 결제에는 유선 단말기와 포스기를, 추가 주문이 잦은 매장에는 테이블오더를 검토합니다. 주방 프린터와 메뉴 연동 여부도 확인합니다.</p><small>포스기 · 테이블오더 · 주방 프린터</small></article><article><span>RETAIL</span><h3>편의점·소매점</h3><p>상품 등록과 재고 관리가 필요하면 POS 연동형 구성이 효율적입니다. 바코드 스캐너, 현금영수증과 간편결제 지원 여부를 함께 살펴봅니다.</p><small>카드단말기 · POS · 바코드 스캐너</small></article><article><span>MOBILE</span><h3>배달·출장·행사</h3><p>전원과 인터넷이 고정되지 않은 현장에는 LTE 무선 또는 휴대용 카드단말기가 적합합니다. 결제 건수와 배터리 사용 시간을 기준으로 선택합니다.</p><small>무선 단말기 · 이동식 결제 · 간편결제</small></article><article><span>SELF</span><h3>병원·학원·무인매장</h3><p>접수와 수납을 줄이려면 키오스크를, 반복 주문을 줄이려면 테이블오더를 검토합니다. 화면 크기와 설치 높이, 직원 동선까지 함께 봅니다.</p><small>키오스크 · 셀프결제 · 비대면 주문</small></article></div></section><section class="section terminal-functions"><div class="section-head"><div><p class="eyebrow"><span></span> PAYMENT &amp; CONNECTION</p><h2>결제부터 매출 관리까지<br><em>필요한 기능을 연결합니다.</em></h2></div><p>{name} 현장의 통신 상태와 사용 중인 장비를 확인해 결제 수단, POS와 주변 기기 연동 범위를 정리합니다.</p></div><div class="feature-list"><article><b>01</b><div><h3>카드·간편결제</h3><p>신용카드와 체크카드, 삼성페이 등 필요한 결제 수단의 지원 여부를 확인합니다.</p></div></article><article><b>02</b><div><h3>POS·프린터 연동</h3><p>기존 포스기, 영수증 프린터와 주방 주문서 연결 가능 여부를 살펴봅니다.</p></div></article><article><b>03</b><div><h3>유선·LTE 통신</h3><p>매장 인터넷과 이동 환경에 맞춰 안정적인 승인 통신 방식을 선택합니다.</p></div></article><article><b>04</b><div><h3>매출·상품 관리</h3><p>매출 조회, 메뉴 수정과 상품 관리에 필요한 프로그램을 안내합니다.</p></div></article></div></section><section class="section terminal-opening"><div class="section-head"><div><p class="eyebrow"><span></span> OPENING CHECKLIST</p><h2>{name} 카드단말기<br><em>신청·개통 준비</em></h2></div><p>신규 사업자와 기존 매장 모두 사업 형태와 설치 환경을 먼저 확인하면 상담부터 개통까지 더 정확하게 진행할 수 있습니다.</p></div><div class="opening-layout"><div class="opening-copy"><h3>상담 전에 확인해주세요</h3><ul><li>사업자등록 여부와 개인·법인 구분</li><li>업종, 설치 주소와 오픈 예정일</li><li>유선 인터넷과 와이파이 설치 여부</li><li>기존 POS·프린터·키오스크 사용 여부</li><li>매장 결제 또는 배달·출장 결제 여부</li></ul></div><div class="opening-steps"><article><span>01</span><h3>사용 환경 상담</h3><p>업종, 장소와 필요한 결제 기능을 확인합니다.</p></article><article><span>02</span><h3>기기·비용 안내</h3><p>구매·임대 조건과 통신비를 구분해 안내합니다.</p></article><article><span>03</span><h3>가맹 신청·개통</h3><p>사업자 형태에 맞는 준비사항을 확인합니다.</p></article><article><span>04</span><h3>설치·사용 안내</h3><p>승인 테스트와 결제·취소 방법을 설명합니다.</p></article></div></div></section><section class="section terminal-faq"><div class="section-head"><div><p class="eyebrow"><span></span> LOCAL TERMINAL FAQ</p><h2>{name} 단말기 설치 전<br><em>자주 묻는 질문</em></h2></div><p>설치 비용과 개통 기간은 선택한 기기, 통신 방식과 카드가맹점 심사 조건에 따라 달라질 수 있습니다.</p></div><div class="faq-list"><details><summary>신규 사업자도 카드단말기를 신청할 수 있나요?</summary><p>개인사업자와 법인사업자 모두 신청할 수 있습니다. 사업자 정보와 영업 형태를 확인한 후 카드가맹점 등록과 개통에 필요한 준비사항을 안내합니다.</p></details><details><summary>카드단말기 가격과 월 비용은 어떻게 정해지나요?</summary><p>유선·무선 여부, 통신 방식, POS 연동 기능과 구매·임대 조건에 따라 달라집니다. 계약 전 기기 비용과 통신비, 부가 서비스 조건을 구분해 확인하는 것이 좋습니다.</p></details><details><summary>기존 포스기와 새 카드단말기를 연결할 수 있나요?</summary><p>사용 중인 POS 프로그램과 연결 방식에 따라 가능 여부가 달라집니다. 기존 장비의 모델과 프로그램 정보를 확인해 호환 가능한 구성을 안내합니다.</p></details><details><summary>설치 전에 어떤 정보를 보내야 하나요?</summary><p>사업자등록 여부, 업종, 설치 주소, 오픈 예정일, 인터넷 환경과 필요한 결제 방식을 알려주시면 상담이 빠릅니다.</p></details></div></section>'''


region_landing = region_landing.replace(
    '<section class="section"><div class="section-head"><div><p class="eyebrow"><span></span> CITY & COUNTY GUIDE',
    '{local_content}<section class="section"><div class="section-head"><div><p class="eyebrow"><span></span> CITY & COUNTY GUIDE',
)
page = page.replace(
    '<section class="section process">',
    '{local_content}<section class="section process">',
    1,
)

for template_name in ("landing", "region_landing", "page"):
    globals()[template_name] = globals()[template_name].replace(
        "terminal.css\"", "terminal.css?v=20260916\""
    )

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
        area = AREA_NAME_OVERRIDES.get(
            (group, slug), area_name(source.read_text(encoding="utf-8-sig"))
        )
        target = output / group / slug
        target.mkdir(parents=True, exist_ok=True)
        (target / "index.html").write_text(page.format(region=region, area=area, products=product_cards(), local_content=local_terminal_content(f"{region} {area}")), encoding="utf-8")
        areas.append(f'<a class="region-card" href="{slug}/"><span><b>{escape(area)} 단말기</b><small>{escape(area)} 판매·설치 안내</small></span><span>↗</span></a>')
        created += 1
    for area, slug in EXTRA_AREAS.get(group, {}).items():
        target = output / group / slug
        target.mkdir(parents=True, exist_ok=True)
        (target / "index.html").write_text(page.format(region=region, area=area, products=product_cards(), local_content=local_terminal_content(f"{region} {area}")), encoding="utf-8")
        areas.append(f'<a class="region-card" href="{slug}/"><span><b>{escape(area)} 단말기</b><small>{escape(area)} 판매·설치 안내</small></span><span>↗</span></a>')
        created += 1
    (output / group).mkdir(parents=True, exist_ok=True)
    (output / group / "index.html").write_text(region_landing.format(region=region, products=product_cards(), local_content=local_terminal_content(region), areas="".join(areas)), encoding="utf-8")
print(f"Generated {created} 시군구 단말기 pages.")
