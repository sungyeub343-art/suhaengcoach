from pathlib import Path

MARKER = "keyword-guide"
KEYWORD_SECTION = '''<section class="section keyword-guide"><div class="section-head"><div><p class="eyebrow"><span></span> VENDING SOLUTION</p><h2>자판기 설치·렌탈·운영<br><em>상담 안내</em></h2></div><p>스마트 자판기와 무인판매기 설치를 검토하신다면 자판기 구매·렌탈·임대, 설치 비용과 운영 방식을 함께 안내해드립니다. 사무실·학교·병원·아파트·학원·상가·헬스장 등 공간에 맞춰 음료 자판기, 간식 자판기, 커피 자판기, 식품 자판기와 냉장 자판기를 구성하고, 카드결제 자판기·키오스크 자판기·무인결제 자판기 세팅까지 지원합니다.</p></div></section>'''
REDIRECT_KEYWORD_SECTION = '''<section class="keyword-guide"><h2>자판기 설치·렌탈·운영 상담 안내</h2><p>스마트 자판기와 무인판매기 설치를 검토하신다면 자판기 구매·렌탈·임대, 설치 비용과 운영 방식을 함께 안내해드립니다. 사무실·학교·병원·아파트·학원·상가·헬스장 등 공간에 맞춰 음료 자판기, 간식 자판기, 커피 자판기, 식품 자판기와 냉장 자판기를 구성하고, 카드결제 자판기·키오스크 자판기·무인결제 자판기 세팅까지 지원합니다.</p></section>'''

updated = 0
for path in Path("regions").rglob("*.html"):
    html = path.read_text(encoding="utf-8-sig")
    if MARKER in html:
        while html.count(REDIRECT_KEYWORD_SECTION) > 1:
            html = html.replace(REDIRECT_KEYWORD_SECTION, "", 1)
            updated += 1
            path.write_text(html, encoding="utf-8")
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