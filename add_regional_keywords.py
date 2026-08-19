import re
from pathlib import Path

MARKER = "keyword-guide"
KEYWORD_TEXT = "스마트 무인판매기 설치를 검토하신다면 지역과 공간의 이용 패턴에 맞춰 상품 구성, 설치 위치, 결제 방식과 운영 동선을 함께 설계합니다. 호텔 자판기는 로비와 객실층에 필요한 음료·간식·여행용품을 편리하게 제공하고, 병원 자판기는 보호자와 방문객이 필요한 음료·간편식·생활용품을 쉽게 찾도록 구성합니다. 골프장 자판기는 라운딩 전후의 음료·간식과 골프용품을 중심으로, 디저트 자판기는 카페와 휴게 공간의 이용 시간에 맞춘 디저트 상품을 중심으로 제안합니다. 또한 생활용품 자판기는 아파트·오피스·학교 등 생활권 공간에 필요한 소모품을, 세차용품 자판기는 주유소·세차장 이용객에게 필요한 세정용품과 관리용품을 빠르게 제공하도록 운영합니다. 공간 규모와 예상 수요에 따라 음료 자판기, 간식 자판기, 냉장 자판기부터 여러 상품군을 한 기기에 구성하는 멀티자판기까지 안내하며, 재고 보충과 매출 확인이 편리한 무인자판기 운영을 지원합니다."
KEYWORD_SECTION = f'''<section class="section keyword-guide"><div class="section-head"><div><p class="eyebrow"><span></span> VENDING SOLUTION</p><h2>공간별 자판기 설치·운영<br><em>맞춤 상담 안내</em></h2></div><p>{KEYWORD_TEXT}</p></div></section>'''
REDIRECT_KEYWORD_SECTION = f'''<section class="keyword-guide"><h2>공간별 자판기 설치·운영 상담 안내</h2><p>{KEYWORD_TEXT}</p></section>'''

updated = 0
for path in Path("regions").rglob("*.html"):
    html = path.read_text(encoding="utf-8-sig")
    if MARKER in html:
        section = KEYWORD_SECTION if "<main>" in html else REDIRECT_KEYWORD_SECTION
        replacement, count = re.subn(
            r'<section class="(?:section )?keyword-guide">.*?</section>',
            section,
            html,
            flags=re.DOTALL,
        )
        if count and replacement != html:
            path.write_text(replacement, encoding="utf-8")
            updated += 1
        continue

    if "<main>" in html:
        hero_end = html.find("</section>", html.find("<main>"))
        if hero_end == -1:
            continue
        insertion_point = hero_end + len("</section>")
        section = KEYWORD_SECTION
    else:
        html = html.replace('<meta http-equiv="refresh" content="0;url=', '<meta name="robots" content="index,follow"><meta data-redirect="')
        html = html.replace("%26area=", "&area=")
        insertion_point = html.find("</body>")
        if insertion_point == -1:
            continue
        section = REDIRECT_KEYWORD_SECTION

    path.write_text(
        html[:insertion_point] + section + html[insertion_point:],
        encoding="utf-8",
    )
    updated += 1

print(f"Updated {updated} regional pages.")