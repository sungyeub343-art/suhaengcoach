$regions = @{
  'busan' = '중구,서구,동구,영도구,부산진구,동래구,남구,북구,해운대구,사하구,금정구,강서구,연제구,수영구,사상구,기장군'
  'daegu' = '중구,동구,서구,남구,북구,수성구,달서구,달성군,군위군'
  'incheon' = '중구,동구,미추홀구,연수구,남동구,부평구,계양구,서구,강화군,옹진군'
  'gwangju' = '동구,서구,남구,북구,광산구'
  'daejeon' = '동구,중구,서구,유성구,대덕구'
  'ulsan' = '중구,남구,동구,북구,울주군'
  'sejong' = '조치원읍,연기면,연동면,부강면,금남면,장군면,연서면,전의면,전동면,소정면,한솔동,새롬동,나성동,도담동,아름동,종촌동,고운동,보람동,대평동,다정동,해밀동,반곡동,소담동'
  'chungbuk' = '청주시,충주시,제천시,보은군,옥천군,영동군,증평군,진천군,괴산군,음성군,단양군'
  'chungnam' = '천안시,공주시,보령시,아산시,서산시,논산시,계룡시,당진시,금산군,부여군,서천군,청양군,홍성군,예산군,태안군'
  'jeonbuk' = '전주시,군산시,익산시,정읍시,남원시,김제시,완주군,진안군,무주군,장수군,임실군,순창군,고창군,부안군'
  'jeonnam' = '목포시,여수시,순천시,나주시,광양시,담양군,곡성군,구례군,고흥군,보성군,화순군,장흥군,강진군,해남군,영암군,무안군,함평군,영광군,장성군,완도군,진도군,신안군'
  'gangwon' = '춘천시,원주시,강릉시,동해시,태백시,속초시,삼척시,홍천군,횡성군,영월군,평창군,정선군,철원군,화천군,양구군,인제군,고성군,양양군'
  'gyeongbuk' = '포항시,경주시,김천시,안동시,구미시,영주시,영천시,상주시,문경시,경산시,의성군,청송군,영양군,영덕군,청도군,고령군,성주군,칠곡군,예천군,봉화군,울진군,울릉군,군위군'
  'jeju' = '제주시,서귀포시,한림읍,애월읍,구좌읍,조천읍,한경면,대정읍,남원읍,성산읍,안덕면,표선면'
}
$names = @{busan='부산';daegu='대구';incheon='인천';gwangju='광주';daejeon='대전';ulsan='울산';sejong='세종';chungbuk='충북';chungnam='충남';jeonbuk='전북';jeonnam='전남';gangwon='강원';gyeongbuk='경북';jeju='제주'}
New-Item -ItemType Directory -Force -Path 'regions/pages' | Out-Null
$count = 0
foreach ($slug in $regions.Keys) {
  foreach ($area in ($regions[$slug] -split ',')) {
    $safe = [uri]::EscapeDataString($area).Replace('%','-')
    $path = "regions/pages/$slug-$safe.html"
    $region = $names[$slug]
    $html = "<!doctype html><html lang='ko'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'><meta name='description' content='$region $area 스마트무인자판기 설치 안내'><title>$area 스마트무인자판기 설치 안내 | 수행코치</title><link rel='stylesheet' href='../../installation.css'></head><body><header class='site-header'><a class='brand' href='../../index.html'><span class='brand-mark'>S</span><span>수행코치 <small>VENDING STUDIO</small></span></a><nav class='main-nav'><a href='../regional-areas.html?region=$([uri]::EscapeDataString($region))'>$region 지역 안내</a><a href='../../index.html#consult'>상담 문의</a></nav></header><main><section class='hero'><div class='hero-copy'><p class='eyebrow'><span></span> LOCAL INSTALLATION GUIDE</p><h1>$region $area<br><em>무인자판기</em><br>설치 안내</h1><p>$region $area 지역의 오피스·상업시설·공장·주거공간에 맞춰 상품 구성과 운영 동선을 설계합니다.</p></div><div class='hero-image'><img src='../../1234.png' alt='$region $area에 설치 가능한 스마트 무인자판기'><div class='hero-label'><strong>지역 맞춤 상담</strong><span>설치 가능 여부 확인</span></div></div></section><section class='section'><div class='section-head'><div><p class='eyebrow'><span></span> LOCAL SOLUTION</p><h2>$region $area 설치<br><em>운영 포인트</em></h2></div><p>설치 장소 사진과 주소를 바탕으로 고객 유형, 체류 시간, 보충 동선을 확인해 맞춤 제안을 드립니다.</p></div><div class='steps'><article><b>01</b><strong>입지 상담</strong><p>설치 위치와<br>이용 고객 확인</p></article><article><b>02</b><strong>상품 구성</strong><p>음료·간식·간편식<br>맞춤 제안</p></article><article><b>03</b><strong>설치 세팅</strong><p>결제 연결과<br>상품 진열 진행</p></article><article><b>04</b><strong>운영 안내</strong><p>재고·매출 확인을<br>1:1로 안내</p></article></div></section><section class='cta'><h2>무료 설치 상담<br><em>받아보세요.</em></h2><a class='button' href='../../index.html#consult'>상담 신청하기 <span>→</span></a></section></main><footer class='site-footer'><a href='../regional-areas.html?region=$([uri]::EscapeDataString($region))'>← $region 세부 지역 선택</a><p>수행코치 VENDING STUDIO</p></footer></body></html>"
    Set-Content -Path $path -Value $html -Encoding utf8
    $count++
  }
}
Write-Output "Generated $count pages"
python add_regional_keywords.py
