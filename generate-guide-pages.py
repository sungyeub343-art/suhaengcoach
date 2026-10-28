import json
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "guides"
SITE_URL = "https://suhaengcoach.kr"
OG_IMAGE = f"{SITE_URL}/og-image.jpg"

GUIDES = [
    {
        "slug": "vending-install-cost",
        "short": "설치 비용 가이드",
        "summary": "기기·결제·초기 상품·운영비 구성",
        "title": "무인자판기 설치 비용 | 기기·결제단말기·운영비 구성 정리",
        "description": "무인자판기 설치 비용은 기기 종류, 결제단말기, 초기 상품, 운송·설치, 월 운영비로 나뉩니다. 항목별로 견적이 달라지는 기준을 정리했습니다.",
        "eyebrow": "INSTALLATION COST GUIDE",
        "h1": "무인자판기<br><em>설치 비용</em><br>한눈에 보기",
        "lede": "자판기 견적은 기기 한 대 가격만으로 정해지지 않습니다. 결제단말기, 처음 채울 상품, 운송·설치, 매달 나가는 운영비까지 합쳐야 실제 비용이 보입니다. 항목별로 금액이 달라지는 기준을 정리했습니다.",
        "cards_eyebrow": "COST BREAKDOWN",
        "cards_title": "견적을 구성하는<br><em>다섯 가지 항목</em>",
        "cards_text": "같은 크기의 자판기라도 냉장 여부, 화면 유무, 결제 방식에 따라 견적이 달라집니다.",
        "cards": [
            ("기기 본체", "크기·냉장 여부·터치스크린 유무"),
            ("결제단말기", "카드·간편결제 단말기와 통신 방식"),
            ("초기 상품", "처음 진열할 음료·간식 매입 비용"),
            ("운송·설치", "설치 위치, 층수, 반입 경로"),
        ],
        "steps_eyebrow": "MONTHLY COST",
        "steps_title": "설치 후 매달 나가는<br><em>운영비 확인</em>",
        "steps_text": "초기 비용과 함께 월 고정비를 미리 계산해야 운영 계획을 세울 수 있습니다.",
        "steps": [
            ("전기요금", "냉장 기기는<br>상시 전력 사용"),
            ("결제 수수료", "카드 매출에<br>붙는 수수료"),
            ("통신비", "단말기 통신<br>방식에 따라 발생"),
            ("상품 보충", "매입 비용과<br>보충 동선"),
        ],
        "faq": [
            ("무인자판기 설치 비용은 얼마인가요?", "기기 크기와 냉장 기능, 결제단말기 종류, 설치 장소의 반입 조건에 따라 달라집니다. 설치 장소 사진과 판매할 상품을 알려주시면 조건에 맞는 견적을 안내해드립니다."),
            ("기기 가격 말고 추가로 드는 비용이 있나요?", "결제단말기, 처음 진열할 상품 매입비, 운송·설치비가 초기에 들고, 설치 후에는 전기요금, 카드 결제 수수료, 단말기 통신비, 상품 보충 비용이 매달 발생합니다."),
            ("비용을 줄이려면 어떻게 해야 하나요?", "이용 인원과 판매 상품에 맞는 크기의 기기를 고르는 것이 가장 중요합니다. 필요 이상으로 큰 기기나 쓰지 않을 기능을 빼면 초기 비용과 전기요금을 함께 줄일 수 있습니다."),
        ],
    },
    {
        "slug": "vending-rental-vs-purchase",
        "short": "렌탈 vs 구매 비교",
        "summary": "초기 비용·관리·운영 기간별 선택 기준",
        "title": "무인자판기 렌탈 vs 구매 비교 | 운영 기간별 선택 기준",
        "description": "무인자판기를 렌탈할지 구매할지 고민된다면 초기 비용, 월 납부액, 유지보수 책임, 운영 기간을 비교해보세요. 상황별 선택 기준을 정리했습니다.",
        "eyebrow": "RENTAL OR PURCHASE",
        "h1": "무인자판기<br><em>렌탈과 구매</em><br>무엇이 맞을까요",
        "lede": "렌탈은 초기 부담이 적고, 구매는 오래 운영할수록 유리한 구조입니다. 어느 쪽이 맞는지는 운영 기간, 관리 방식, 설치 장소의 계약 조건에 따라 달라집니다.",
        "cards_eyebrow": "COMPARE",
        "cards_title": "렌탈과 구매<br><em>비교 포인트</em>",
        "cards_text": "계약 전에 아래 네 가지를 기준으로 두 방식을 비교해보세요.",
        "cards": [
            ("초기 비용", "렌탈은 낮고, 구매는 기기값을 한 번에 부담"),
            ("월 고정비", "렌탈은 약정 기간 동안 월 납부액 발생"),
            ("유지보수", "계약 조건에 따라 수리 책임 주체가 다름"),
            ("운영 기간", "길게 운영할수록 구매 쪽 총비용이 유리"),
        ],
        "steps_eyebrow": "HOW TO CHOOSE",
        "steps_title": "상황별로 고르는<br><em>선택 기준</em>",
        "steps_text": "아래 질문에 답해보면 어떤 방식이 맞는지 정리됩니다.",
        "steps": [
            ("운영 기간", "얼마나 오래<br>운영할 계획인가"),
            ("초기 자금", "기기값을 한 번에<br>부담할 수 있는가"),
            ("장소 계약", "설치 장소 계약<br>기간은 얼마인가"),
            ("관리 방식", "고장 대응을 직접<br>할 수 있는가"),
        ],
        "faq": [
            ("처음 시작하는데 렌탈이 나을까요?", "운영이 처음이고 상권 반응을 먼저 확인하고 싶다면 초기 부담이 적은 렌탈이 맞을 수 있습니다. 다만 약정 기간과 중도 해지 조건을 반드시 확인해야 합니다."),
            ("구매가 유리한 경우는 언제인가요?", "설치 장소를 오래 쓸 수 있고 운영 기간이 길게 예상된다면 총비용 면에서 구매가 유리한 경우가 많습니다. 기기를 다른 장소로 옮겨 쓸 수 있다는 점도 장점입니다."),
            ("렌탈 계약 때 꼭 확인할 것은 무엇인가요?", "약정 기간, 중도 해지 위약금, 고장 시 수리 범위와 기간, 약정 종료 후 기기 소유권을 확인하세요."),
        ],
    },
    {
        "slug": "vending-business-profit",
        "short": "창업 수익 구조",
        "summary": "매출 계산법과 빠져나가는 비용 정리",
        "title": "무인자판기 창업 수익 구조 | 매출 계산법과 운영 비용",
        "description": "무인자판기 창업 수익은 이용자 수, 구매율, 객단가로 매출을 계산하고 상품 원가와 수수료, 전기요금, 자리 비용을 빼서 판단합니다. 수익 구조를 정리했습니다.",
        "eyebrow": "VENDING BUSINESS",
        "h1": "무인자판기<br><em>창업 수익</em><br>구조 이해하기",
        "lede": "자판기 수익은 설치 장소에서 결정됩니다. 하루에 지나가는 사람이 얼마나 되는지, 그중 몇 명이 사는지, 한 번에 얼마를 쓰는지로 매출을 추정하고, 여기서 비용을 빼서 남는 금액을 확인해야 합니다.",
        "cards_eyebrow": "REVENUE FORMULA",
        "cards_title": "매출을 만드는<br><em>세 가지 숫자</em>",
        "cards_text": "하루 매출은 이용 가능 인원 × 구매율 × 1회 평균 결제액으로 추정할 수 있습니다.",
        "cards": [
            ("이용 가능 인원", "설치 장소를 하루에 오가는 사람 수"),
            ("구매율", "지나가는 사람 중 실제 구매하는 비율"),
            ("1회 결제액", "한 번 구매할 때 평균 금액"),
            ("판매 상품", "장소와 시간대에 맞는 상품 구성"),
        ],
        "steps_eyebrow": "COST CHECK",
        "steps_title": "매출에서 빠지는<br><em>비용 항목</em>",
        "steps_text": "매출이 같아도 비용 구조에 따라 남는 금액이 크게 달라집니다.",
        "steps": [
            ("상품 원가", "매입가와<br>판매가 차이"),
            ("결제 수수료", "카드·간편결제<br>매출 수수료"),
            ("자리 비용", "임대료 또는<br>매출 배분 계약"),
            ("전기·보충", "전기요금과<br>보충 이동 비용"),
        ],
        "faq": [
            ("무인자판기 한 대로 얼마나 벌 수 있나요?", "설치 장소의 유동 인구와 상품 구성에 따라 차이가 매우 큽니다. 설치 전에 이용 가능 인원과 예상 구매율을 따져보고, 상품 원가와 고정비를 뺀 금액으로 판단하는 것이 안전합니다."),
            ("어떤 장소가 수익이 잘 나나요?", "사람이 오래 머물거나 같은 사람이 자주 오는 곳, 그리고 주변에 편의점이 멀어 대체 구매처가 적은 곳이 유리합니다. 사무실, 헬스장, 공장, 학원처럼 이용자가 정해진 공간이 대표적입니다."),
            ("자리 비용은 어떤 방식으로 계약하나요?", "고정 월 임대료를 내는 방식과 매출의 일정 비율을 장소 제공자와 나누는 방식이 있습니다. 매출이 불확실한 초기에는 매출 배분 방식이 부담이 적습니다."),
        ],
    },
    {
        "slug": "vending-card-payment",
        "short": "카드결제 연결 방법",
        "summary": "단말기·가맹점 등록·통신·정산 안내",
        "title": "무인자판기 카드결제 연결 방법 | 단말기·가맹점 등록·정산",
        "description": "무인자판기에서 카드와 간편결제를 받으려면 결제단말기, 카드 가맹점 등록, 통신 연결, 정산 계좌가 필요합니다. 연결 순서와 확인할 점을 정리했습니다.",
        "eyebrow": "CARD PAYMENT GUIDE",
        "h1": "무인자판기<br><em>카드결제</em><br>연결 방법",
        "lede": "현금 없이 카드와 간편결제로 사는 사람이 대부분이라 카드결제는 사실상 필수입니다. 결제단말기를 다는 것뿐 아니라 가맹점 등록, 통신 연결, 정산 계좌까지 준비해야 결제가 시작됩니다.",
        "cards_eyebrow": "WHAT YOU NEED",
        "cards_title": "카드결제에<br><em>필요한 준비물</em>",
        "cards_text": "아래 네 가지가 모두 갖춰져야 자판기에서 결제가 정상적으로 이뤄집니다.",
        "cards": [
            ("결제단말기", "IC카드·NFC 간편결제 지원 여부 확인"),
            ("가맹점 등록", "사업자등록증으로 카드 가맹점 신청"),
            ("통신 연결", "LTE 모뎀 또는 설치 장소 인터넷"),
            ("정산 계좌", "카드 매출이 입금될 사업자 계좌"),
        ],
        "steps_eyebrow": "SETUP FLOW",
        "steps_title": "카드결제<br><em>연결 순서</em>",
        "steps_text": "보통 아래 순서로 진행되며, 가맹점 심사 기간을 감안해 설치 일정보다 미리 신청하는 것이 좋습니다.",
        "steps": [
            ("사업자 준비", "사업자등록과<br>정산 계좌 준비"),
            ("단말기 선택", "자판기와 호환되는<br>단말기 확인"),
            ("가맹점 신청", "카드사 가맹점<br>등록과 심사"),
            ("결제 테스트", "설치 후 실제<br>결제·정산 확인"),
        ],
        "faq": [
            ("사업자등록 없이 카드결제를 받을 수 있나요?", "카드 가맹점은 사업자 기준으로 등록되기 때문에 일반적으로 사업자등록이 필요합니다. 자판기 운영을 시작하기 전에 사업자등록부터 준비하세요."),
            ("삼성페이나 모바일 결제도 되나요?", "NFC 결제를 지원하는 단말기를 쓰면 휴대폰 간편결제도 받을 수 있습니다. 단말기를 고를 때 지원하는 결제 수단을 확인하세요."),
            ("설치 장소에 인터넷이 없으면 어떻게 하나요?", "LTE 통신 모뎀이 들어간 단말기를 쓰면 설치 장소 인터넷 없이도 결제할 수 있습니다. 이 경우 단말기 통신비가 매달 발생합니다."),
        ],
    },
    {
        "slug": "vending-location-guide",
        "short": "설치 장소 고르는 법",
        "summary": "유동 인구·체류 시간·전원·계약 조건",
        "title": "무인자판기 설치 장소 고르는 법 | 자리 선정 체크리스트",
        "description": "무인자판기 매출은 설치 장소에서 결정됩니다. 유동 인구, 체류 시간, 주변 경쟁 매장, 전원과 공간 조건, 장소 계약 방식까지 자리 선정 기준을 정리했습니다.",
        "eyebrow": "LOCATION GUIDE",
        "h1": "무인자판기<br><em>설치 장소</em><br>고르는 법",
        "lede": "같은 기기와 같은 상품이라도 어디에 두느냐에 따라 매출이 몇 배씩 차이 납니다. 사람이 얼마나 오가는지, 얼마나 머무는지, 근처에 대신 살 곳이 있는지를 먼저 확인해야 합니다.",
        "cards_eyebrow": "LOCATION CHECK",
        "cards_title": "좋은 자리를 고르는<br><em>네 가지 기준</em>",
        "cards_text": "설치를 결정하기 전에 아래 네 가지를 현장에서 직접 확인해보세요.",
        "cards": [
            ("유동 인구", "하루 동안 자판기 앞을 지나는 사람 수"),
            ("체류 시간", "오래 머물거나 자주 오는 이용자인지"),
            ("대체 구매처", "가까운 편의점·매점까지의 거리"),
            ("이용 시간대", "야간·주말에도 사람이 있는지"),
        ],
        "steps_eyebrow": "SITE CONDITION",
        "steps_title": "설치 전에 확인할<br><em>현장 조건</em>",
        "steps_text": "자리가 좋아도 기기를 놓을 수 없는 조건이면 설치가 어렵습니다. 공간과 계약 조건도 함께 확인하세요.",
        "steps": [
            ("설치 면적", "기기 크기와<br>문 여닫는 공간"),
            ("전원", "가까운 콘센트와<br>전기 용량"),
            ("반입 경로", "출입문·엘리베이터<br>크기와 계단"),
            ("장소 계약", "임대료 또는<br>매출 배분 조건"),
        ],
        "faq": [
            ("자판기 매출이 잘 나오는 장소는 어디인가요?", "이용자가 정해져 있고 자주 오는 공간이 유리합니다. 사무실, 공장, 헬스장, 학원, 병원 대기 공간처럼 사람이 머무는 곳이 대표적이며, 근처에 편의점이 멀수록 구매로 이어지기 쉽습니다."),
            ("유동 인구가 많으면 무조건 좋은가요?", "지나가기만 하는 길목보다 잠시라도 머무는 공간이 더 낫습니다. 바로 옆에 편의점이 있으면 유동 인구가 많아도 자판기 매출은 낮을 수 있습니다."),
            ("실외에도 설치할 수 있나요?", "실외는 비와 직사광선, 온도 변화에 노출되고 파손 위험도 있어 실외 설치가 가능한 기기인지 먼저 확인해야 합니다. 가능하면 지붕이 있는 실내나 건물 출입구 안쪽을 권합니다."),
        ],
    },
    {
        "slug": "vending-product-mix",
        "short": "상품 구성·재고 관리",
        "summary": "잘 팔리는 상품 구성과 보충 주기",
        "title": "무인자판기 상품 구성과 재고 관리 | 잘 팔리는 진열 방법",
        "description": "무인자판기 상품은 설치 장소의 이용자와 시간대에 맞춰 구성해야 합니다. 상품 고르는 기준, 칸 배치, 재고 보충 주기와 소비기한 관리 방법을 정리했습니다.",
        "eyebrow": "PRODUCT MIX GUIDE",
        "h1": "무인자판기<br><em>상품 구성과</em><br>재고 관리",
        "lede": "자판기는 칸 수가 정해져 있어서 어떤 상품을 넣느냐가 곧 매출입니다. 이용자가 누구인지에 맞춰 상품을 고르고, 판매 기록을 보면서 안 팔리는 상품을 계속 바꿔주는 것이 핵심입니다.",
        "cards_eyebrow": "PRODUCT PLAN",
        "cards_title": "상품을 고르는<br><em>네 가지 기준</em>",
        "cards_text": "처음에는 많이 팔리는 기본 상품 위주로 채우고, 판매 기록을 보며 조금씩 바꿔가는 것이 안전합니다.",
        "cards": [
            ("이용자 맞춤", "직장인·학생·운동하는 사람 등 이용자층"),
            ("시간대 맞춤", "아침·점심·야간에 필요한 상품"),
            ("가격대 구성", "저가 상품과 객단가 높은 상품 배합"),
            ("보관 조건", "냉장 필요 여부와 상품 규격"),
        ],
        "steps_eyebrow": "STOCK ROUTINE",
        "steps_title": "재고 관리<br><em>기본 루틴</em>",
        "steps_text": "품절된 칸은 매출이 0입니다. 정해진 주기로 보충하고 판매 기록을 확인하세요.",
        "steps": [
            ("판매 확인", "상품별 판매량과<br>품절 칸 확인"),
            ("보충 주기", "잘 팔리는 상품<br>기준으로 일정 설정"),
            ("소비기한", "먼저 들어온 상품을<br>앞쪽에 진열"),
            ("상품 교체", "안 팔리는 상품은<br>다른 상품으로 교체"),
        ],
        "faq": [
            ("처음에는 어떤 상품을 넣는 게 좋나요?", "생수, 커피, 탄산음료, 이온음료처럼 어디서나 꾸준히 팔리는 음료와 대표 과자류부터 시작하는 것이 안전합니다. 이후 판매 기록을 보고 설치 장소에 맞는 상품으로 바꿔가세요."),
            ("재고는 얼마나 자주 채워야 하나요?", "설치 장소의 판매량에 따라 다릅니다. 가장 빨리 팔리는 상품이 품절되기 전에 채울 수 있도록 주기를 잡고, 원격으로 재고를 확인할 수 있는 기기라면 이동 횟수를 줄일 수 있습니다."),
            ("소비기한 관리는 어떻게 하나요?", "새로 넣는 상품은 뒤쪽에, 먼저 들어온 상품은 앞쪽에 진열해 먼저 팔리게 하세요. 보충할 때마다 소비기한이 가까운 상품이 있는지 함께 확인해야 합니다."),
        ],
    },
    {
        "slug": "vending-business-permit",
        "short": "영업신고·인허가 안내",
        "summary": "사업자등록과 식품자동판매기 영업신고",
        "title": "무인자판기 영업신고·사업자등록 | 운영 전 인허가 확인",
        "description": "무인자판기를 운영하려면 사업자등록과 판매 상품에 따른 식품자동판매기영업 신고 여부를 확인해야 합니다. 운영 전 준비할 서류와 확인 순서를 정리했습니다.",
        "eyebrow": "PERMIT GUIDE",
        "h1": "무인자판기<br><em>영업신고와</em><br>사업자등록",
        "lede": "자판기 운영도 사업이기 때문에 사업자등록이 필요하고, 식품을 판매한다면 판매 방식에 따라 식품자동판매기영업 신고 대상인지 확인해야 합니다. 기준은 바뀔 수 있으므로 설치 전에 관할 기관에 꼭 확인하세요.",
        "cards_eyebrow": "WHAT TO PREPARE",
        "cards_title": "운영 전에 확인할<br><em>네 가지</em>",
        "cards_text": "판매하는 상품과 운영 방식에 따라 필요한 절차가 달라집니다.",
        "cards": [
            ("사업자등록", "세무서 또는 홈택스에서 신청"),
            ("영업신고 여부", "판매 식품 종류에 따라 신고 대상 확인"),
            ("장소 사용 동의", "건물주·관리사무소의 설치 동의"),
            ("카드 가맹점", "사업자등록 후 가맹점 등록"),
        ],
        "steps_eyebrow": "PROCESS",
        "steps_title": "인허가<br><em>확인 순서</em>",
        "steps_text": "아래 순서로 준비하면 설치 일정에 맞춰 운영을 시작할 수 있습니다.",
        "steps": [
            ("상품 결정", "판매할 상품과<br>보관 방식 정리"),
            ("관할 기관 확인", "시·군·구청에<br>신고 대상 문의"),
            ("사업자등록", "업종을 정해<br>사업자등록 신청"),
            ("신고·설치", "필요 시 영업신고 후<br>설치·운영 시작"),
        ],
        "faq": [
            ("무인자판기도 영업신고를 해야 하나요?", "식품을 판매하는 자판기는 식품자동판매기영업 신고 대상이 될 수 있습니다. 다만 소비기한이 1개월 이상인 포장 완제품만 판매하는 경우처럼 신고 대상에서 제외되는 경우도 있으므로, 판매할 상품을 정한 뒤 관할 시·군·구청 위생 담당 부서에 확인하세요."),
            ("식품이 아닌 생활용품만 팔아도 사업자등록이 필요한가요?", "판매를 통해 계속 수익을 내는 것이라면 판매 상품과 관계없이 사업자등록이 필요합니다. 카드 가맹점 등록에도 사업자등록증이 필요합니다."),
            ("개인 사업자로 등록하면 되나요?", "처음에는 대부분 개인사업자로 시작합니다. 업종 코드와 과세 유형은 세무서나 홈택스 안내에 따라 판매 상품에 맞게 선택하세요."),
        ],
    },
    {
        "slug": "vending-maintenance-checklist",
        "short": "관리·점검 체크리스트",
        "summary": "청소·온도·결제·배출 점검 방법",
        "title": "무인자판기 관리 방법 | 청소·고장 예방 점검 체크리스트",
        "description": "무인자판기는 정기적으로 청소하고 냉장 온도, 결제단말기, 상품 배출 상태를 점검해야 고장과 매출 손실을 줄일 수 있습니다. 점검 항목과 주기를 정리했습니다.",
        "eyebrow": "MAINTENANCE GUIDE",
        "h1": "무인자판기<br><em>관리·점검</em><br>체크리스트",
        "lede": "무인으로 운영되는 만큼 고장이 나도 바로 알기 어렵습니다. 결제가 안 되거나 상품이 걸리면 그 시간 동안 매출이 멈추기 때문에, 보충하러 갈 때마다 기본 점검을 함께 하는 습관이 중요합니다.",
        "cards_eyebrow": "CHECK POINTS",
        "cards_title": "보충할 때마다<br><em>확인할 항목</em>",
        "cards_text": "아래 네 가지는 매번 짧게 확인해도 큰 고장을 미리 막을 수 있습니다.",
        "cards": [
            ("냉장 온도", "음료가 충분히 시원한지 확인"),
            ("결제 상태", "카드·간편결제가 정상 승인되는지"),
            ("상품 배출", "걸리거나 기울어진 상품이 없는지"),
            ("외관·청결", "유리면·배출구·주변 바닥 청소"),
        ],
        "steps_eyebrow": "ROUTINE",
        "steps_title": "주기별<br><em>관리 루틴</em>",
        "steps_text": "점검 주기를 정해두면 고장을 미리 발견하고 이용자 불편을 줄일 수 있습니다.",
        "steps": [
            ("보충할 때", "온도·결제·배출<br>기본 점검"),
            ("주 단위", "유리면·배출구<br>청소와 판매 기록"),
            ("월 단위", "냉각 장치 통풍구<br>먼지 제거"),
            ("이상 발생 시", "전원·통신 확인 후<br>A/S 접수"),
        ],
        "faq": [
            ("카드결제가 갑자기 안 될 때는 어떻게 하나요?", "먼저 단말기 전원과 통신 연결 상태를 확인하고, 설치 장소 인터넷이나 LTE 신호에 문제가 없는지 살펴보세요. 그래도 안 되면 단말기 업체나 설치 업체에 문의하세요."),
            ("음료가 시원하지 않으면 무엇을 확인해야 하나요?", "기기 뒤쪽 통풍구가 벽에 너무 붙어 있거나 먼지로 막혀 있지 않은지 확인하세요. 문이 제대로 닫히는지도 함께 점검하고, 계속 온도가 오르지 않으면 A/S를 요청하세요."),
            ("상품이 걸려서 안 나올 때는 어떻게 하나요?", "상품 규격이 칸에 맞는지, 진열할 때 기울어지지 않았는지 확인하세요. 같은 칸에서 반복된다면 칸 간격이나 배출 장치 조정이 필요할 수 있습니다."),
        ],
    },
]


def json_ld(data):
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))


def render_guide(guide):
    url = f"{SITE_URL}/guides/{guide['slug']}.html"
    cards = "".join(
        f'<article class="region-card"><span><b>{escape(name)}</b><small>{escape(text)}</small></span></article>'
        for name, text in guide["cards"]
    )
    steps = "".join(
        f"<article><b>{index:02d}</b><strong>{escape(name)}</strong><p>{text}</p></article>"
        for index, (name, text) in enumerate(guide["steps"], start=1)
    )
    faq = "".join(
        f"<details><summary>{escape(question)}</summary><p>{escape(answer)}</p></details>"
        for question, answer in guide["faq"]
    )
    related = "".join(
        f'<a class="region-card" href="{other["slug"]}.html"><span><b>{escape(other["short"])}</b><small>{escape(other["summary"])}</small></span><span>↗</span></a>'
        for other in GUIDES
        if other is not guide
    )
    article_ld = json_ld({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": guide["title"],
        "description": guide["description"],
        "image": OG_IMAGE,
        "mainEntityOfPage": url,
        "author": {"@type": "Organization", "name": "더세이브 수행코치", "url": f"{SITE_URL}/"},
        "publisher": {"@type": "Organization", "name": "더세이브 수행코치", "url": f"{SITE_URL}/"},
    })
    faq_ld = json_ld({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": question, "acceptedAnswer": {"@type": "Answer", "text": answer}}
            for question, answer in guide["faq"]
        ],
    })
    title = escape(guide["title"])
    description = escape(guide["description"])
    return f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{description}">
  <title>{title}</title>
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="article">
  <meta property="og:locale" content="ko_KR">
  <meta property="og:site_name" content="더세이브 수행코치">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{OG_IMAGE}">
  <meta property="og:image:secure_url" content="{OG_IMAGE}">
  <meta property="og:image:type" content="image/jpeg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="음료와 간식이 진열된 무인자판기">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{OG_IMAGE}">
  <link rel="stylesheet" href="../installation.css">
  <script type="application/ld+json">{article_ld}</script>
  <script type="application/ld+json">{faq_ld}</script>
</head>
<body>
  <header class="site-header"><a class="brand" href="../index.html"><span class="brand-mark">S</span><span>더세이브 수행코치 <small>VENDING STUDIO</small></span></a><nav class="main-nav" aria-label="주 메뉴"><a href="../installation.html">제품 설치안내</a><a href="../installation.html#guides">자판기 가이드</a><a href="../installation.html#regions">지역별 안내</a><a href="../index.html#consult">상담 문의</a></nav></header>
  <main>
    <section class="hero"><div class="hero-copy"><p class="eyebrow"><span></span> {guide['eyebrow']}</p><h1>{guide['h1']}</h1><p>{escape(guide['lede'])}</p></div><div class="hero-image"><img src="../1234.png" alt="음료와 간식이 진열된 무인자판기"><div class="hero-label"><strong>무인자판기 가이드</strong><span>설치 전 확인할 내용</span></div></div></section>
    <section class="section"><div class="section-head"><div><p class="eyebrow"><span></span> {guide['cards_eyebrow']}</p><h2>{guide['cards_title']}</h2></div><p>{escape(guide['cards_text'])}</p></div><div class="region-grid">{cards}</div></section>
    <section class="section process"><div class="section-head"><div><p class="eyebrow"><span></span> {guide['steps_eyebrow']}</p><h2>{guide['steps_title']}</h2></div><p>{escape(guide['steps_text'])}</p></div><div class="steps">{steps}</div></section>
    <section class="section"><div class="section-head"><div><p class="eyebrow"><span></span> FAQ</p><h2>자주 묻는<br><em>질문</em></h2></div><p>상담 때 자주 받는 질문을 정리했습니다. 더 궁금한 점은 전화로 문의해주세요.</p></div><div class="faq-list">{faq}</div></section>
    <section class="section"><div class="section-head"><div><p class="eyebrow"><span></span> RELATED GUIDES</p><h2>함께 보면 좋은<br><em>자판기 가이드</em></h2></div><p>설치 전부터 운영까지 필요한 내용을 주제별로 함께 확인해보세요.</p></div><div class="region-grid">{related}<a class="region-card" href="../installation.html#space-guides"><span><b>업종별 설치 안내</b><small>사무실·헬스장·세차장 등 공간별 구성</small></span><span>↗</span></a></div></section>
    <section class="cta"><h2>내 공간에 맞는 견적이<br><em>궁금하신가요?</em></h2><a class="button" href="tel:010-3946-3614">전화 상담 010-3946-3614 <span>→</span></a></section>
  </main>
  <footer class="site-footer"><a href="../installation.html">← 제품·업종별 설치안내</a><p>더세이브 수행코치 VENDING STUDIO</p></footer>
</body>
</html>
"""


OUTPUT_DIR.mkdir(exist_ok=True)
for guide in GUIDES:
    (OUTPUT_DIR / f"{guide['slug']}.html").write_text(render_guide(guide), encoding="utf-8")
print(f"Generated {len(GUIDES)} guide pages.")
