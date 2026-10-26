import math
import random
import zlib
from datetime import datetime
from zoneinfo import ZoneInfo

import streamlit as st

st.set_page_config(page_title="지하철 칸별 혼잡도 확인", page_icon="🚇", layout="centered")

CAR_COUNT = 7

# ───────────────────────── 데이터 ─────────────────────────
LINES = {
    "1": {"color": "#0052A4",
          "dirs": ["상행 (소요산·청량리 방면)", "하행 (인천·신창 방면)"],
          "st": "소요산 동두천 보산 동두천중앙 지행 덕정 덕계 양주 녹양 가능 의정부 회룡 망월사 도봉산 방학 창동 녹천 월계 광운대 석계 신이문 외대앞 회기 청량리 제기동 신설동 동묘앞 동대문 종로5가 종로3가 종각 시청 서울역 남영 용산 노량진 대방 신길 영등포 신도림 구로 가산디지털단지 독산 금천구청 석수 관악 안양 명학 금정 군포 당정 의왕 성균관대 화서 수원 세류 병점 세마 오산대 오산 진위 송탄 서정리 지제 평택 성환 직산 두정 천안 봉명 쌍용 아산 배방 온양온천 신창 구일 개봉 오류동 온수 역곡 소사 부천 중동 송내 부개 부평 백운 동암 간석 주안 도화 제물포 도원 동인천 인천"},
    "2": {"color": "#00A84D",
          "dirs": ["내선순환", "외선순환"],
          "st": "시청 을지로입구 을지로3가 을지로4가 동대문역사문화공원 신당 상왕십리 왕십리 한양대 뚝섬 성수 건대입구 구의 강변 잠실나루 잠실 잠실새내 종합운동장 삼성 선릉 역삼 강남 교대 서초 방배 사당 낙성대 서울대입구 봉천 신림 신대방 구로디지털단지 대림 신도림 문래 영등포구청 당산 합정 홍대입구 신촌 이대 아현 충정로 용답 신답 용두 도림천 양천구청 신정네거리 까치산"},
    "3": {"color": "#EF7C1C",
          "dirs": ["상행 (대화 방면)", "하행 (오금 방면)"],
          "st": "대화 주엽 정발산 마두 백석 대곡 화정 원당 원흥 삼송 지축 구파발 연신내 불광 녹번 홍제 무악재 독립문 경복궁 안국 종로3가 을지로3가 충무로 동대입구 약수 금호 옥수 압구정 신사 잠원 고속터미널 교대 남부터미널 양재 매봉 도곡 대치 학여울 대청 일원 수서 가락시장 경찰병원 오금"},
    "4": {"color": "#00A5DE",
          "dirs": ["상행 (진접·당고개 방면)", "하행 (오이도 방면)"],
          "st": "진접 오남 별내별가람 당고개 상계 노원 창동 쌍문 수유 미아 미아사거리 길음 성신여대입구 한성대입구 혜화 동대문 동대문역사문화공원 충무로 명동 회현 서울역 숙대입구 삼각지 신용산 이촌 동작 총신대입구 사당 남태령 선바위 경마공원 대공원 과천 정부과천청사 인덕원 평촌 범계 금정 산본 수리산 대야미 반월 상록수 한대앞 중앙 고잔 초지 안산 신길온천 정왕 오이도"},
    "5": {"color": "#996CAC",
          "dirs": ["상행 (방화 방면)", "하행 (상일동·마천 방면)"],
          "st": "방화 개화산 김포공항 송정 마곡 발산 우장산 화곡 까치산 신정 목동 오목교 양평 영등포구청 영등포시장 신길 여의도 여의나루 마포 공덕 애오개 충정로 서대문 광화문 종로3가 을지로4가 동대문역사문화공원 청구 신금호 행당 왕십리 마장 답십리 장한평 군자 아차산 광나루 천호 강동 길동 굽은다리 명일 고덕 상일동 강일 미사 하남풍산 하남시청 하남검단산 둔촌동 올림픽공원 방이 오금 개롱 거여 마천"},
    "6": {"color": "#CD7C2F",
          "dirs": ["상행 (응암 방면)", "하행 (봉화산 방면)"],
          "st": "응암 역촌 불광 독바위 연신내 구산 새절 증산 디지털미디어시티 월드컵경기장 마포구청 망원 합정 상수 광흥창 대흥 공덕 효창공원앞 삼각지 녹사평 이태원 한강진 버티고개 약수 청구 신당 동묘앞 창신 보문 안암 고려대 월곡 상월곡 돌곶이 석계 태릉입구 화랑대 봉화산"},
    "7": {"color": "#747F00",
          "dirs": ["상행 (장암 방면)", "하행 (석남 방면)"],
          "st": "장암 도봉산 수락산 마들 노원 중계 하계 공릉 태릉입구 먹골 중화 상봉 면목 사가정 용마산 중곡 군자 어린이대공원 건대입구 뚝섬유원지 청담 강남구청 학동 논현 반포 고속터미널 내방 이수 남성 숭실대입구 상도 장승배기 신대방삼거리 보라매 신풍 대림 남구로 가산디지털단지 철산 광명사거리 천왕 온수 까치울 부천종합운동장 춘의 신중동 부천시청 상동 삼산체육관 굴포천 부평구청 산곡 석남"},
    "8": {"color": "#E6186C",
          "dirs": ["상행 (암사 방면)", "하행 (모란 방면)"],
          "st": "암사 천호 강동구청 몽촌토성 잠실 석촌 송파 가락시장 문정 장지 복정 남위례 산성 남한산성입구 단대오거리 신흥 수진 모란"},
    "9": {"color": "#B8A77A",
          "dirs": ["상행 (개화 방면)", "하행 (중앙보훈병원 방면)"],
          "st": "개화 김포공항 공항시장 신방화 마곡나루 양천향교 가양 증미 등촌 염창 신목동 선유도 당산 국회의사당 여의도 샛강 노량진 노들 흑석 동작 구반포 신반포 고속터미널 사평 신논현 언주 선정릉 삼성중앙 봉은사 종합운동장 삼전 석촌고분 석촌 송파나루 한성백제 올림픽공원 둔촌오륜 중앙보훈병원"},
}
for _l in LINES.values():
    _l["stations"] = _l["st"].split()

REGION = {}
for _r, _s in [("천안시", "두정 천안 봉명 쌍용 성환 직산"),
               ("아산시", "아산 배방 온양온천 신창"),
               ("평택시", "평택 지제 서정리 송탄 진위")]:
    for _n in _s.split():
        REGION[("1", _n)] = _r

LEVEL_TXT = {"low": "여유", "mid": "보통", "high": "복잡"}
FACE = {"low": "( ˶ˆ⤙ˆ˵ )", "mid": "( •̀ω•́ )", "high": "( 😭 )"}
LEVEL_BG = {"low": "#b2f2bb", "mid": "#ffec99", "high": "#ffc9c9"}
LEVEL_FG = {"low": "#2b6e3b", "mid": "#856404", "high": "#9c2b2b"}


# ───────────────────────── 로직 ─────────────────────────
def crc(s: str) -> int:
    return zlib.crc32(s.encode("utf-8"))


def exit_cars(line: str, station: str):
    r = random.Random(crc("exit" + line + station))
    a = r.randint(1, CAR_COUNT)
    b = r.randint(1, CAR_COUNT)
    if b == a:
        b = a % CAR_COUNT + 1
    return sorted([a, b])


def congestion(line: str, station: str, dir_idx: int, offset: int):
    """가상 데이터: 시간대 + 역 이름 기반으로 만든 값 (실제 혼잡도 아님)"""
    now = datetime.now(ZoneInfo("Asia/Seoul"))
    h = now.hour + now.minute / 60
    weekday = now.weekday() < 5
    if weekday:
        rush = max(math.exp(-((h - 8.3) ** 2) / 1.5), math.exp(-((h - 18.3) ** 2) / 2))
    else:
        rush = 0.25
    base = 0.25 + 0.5 * rush
    bucket = int(now.timestamp() // 300) + offset
    r = random.Random(crc(f"{line}{station}{dir_idx}") + bucket)
    near = exit_cars(line, station)
    out = []
    for i in range(CAR_COUNT):
        v = base + (r.random() - 0.5) * 0.55 + (0.22 if (i + 1) in near else -0.04)
        out.append(round(min(1.0, max(0.05, v)) * 100))
    return out


def level(p: int) -> str:
    return "low" if p < 40 else "mid" if p < 70 else "high"


# ───────────────────────── 스타일 ─────────────────────────
st.markdown(
    """
<style>
.stApp { background: linear-gradient(135deg, #fff0f5, #f0f7ff); }
h1 { color: #5a434d !important; }
.badge { display:inline-block; color:#fff; border-radius:999px; padding:3px 12px; font-weight:700; }
.lvl { display:inline-block; border-radius:999px; padding:5px 16px; font-weight:700; }
.car-no { text-align:center; font-size:.85rem; color:#8c7d87; font-weight:700; }
.car-no.best { color:#ff5285; }
.box { height:110px; border-radius:22px; border:3px solid rgba(0,0,0,.06);
       display:flex; flex-direction:column; align-items:center; justify-content:center;
       position:relative; box-shadow: inset 0 -6px 0 rgba(0,0,0,.08); }
.box .face { font-size:1rem; }
.box .pct { font-size:1.1rem; font-weight:800; color:#333; }
.star { position:absolute; top:-12px; right:-4px; font-size:1.3rem; }
.near { font-size:.68rem; text-align:center; color:#8a707c; font-weight:700; min-height:2.4em; margin-top:4px; }
.bubble { background:#fff5f8; border:3px solid #ffcadb; border-radius:26px; padding:20px 26px; margin-top:12px; }
.tag { background:#ff7399; color:#fff; border-radius:999px; padding:3px 12px; font-size:.8rem; font-weight:700; }
.big { font-size:1.7rem; font-weight:800; color:#4a323d; margin:8px 0 4px; line-height:1.35; }
.sub { color:#7a626f; font-weight:600; }
@media (max-width: 640px) { .box { height:78px; } .box .face { font-size:.6rem; } .box .pct { font-size:.8rem; } }
</style>
""",
    unsafe_allow_html=True,
)

# ───────────────────────── 화면 ─────────────────────────
st.title("🐰 지하철 칸별 혼잡도 확인")
st.caption("복잡복잡 싫어! 쾌적하고 여유로운 칸으로 타요 ( •̀ω•́ )✨")

if "query" not in st.session_state:
    st.session_state.query = None
if "offset" not in st.session_state:
    st.session_state.offset = 0

with st.form("search"):
    line = st.radio("노선 선택", list(LINES.keys()), horizontal=True,
                    format_func=lambda n: f"{n}호선")
    stations = LINES[line]["stations"]

    def fmt(s):
        rg = REGION.get((line, s))
        return f"{s}역 ({rg})" if rg else f"{s}역"

    station = st.selectbox("역 선택 (입력해서 검색할 수 있어요)", stations, format_func=fmt)
    direction = st.selectbox("방향", range(len(LINES[line]["dirs"])),
                             format_func=lambda i: LINES[line]["dirs"][i])
    submitted = st.form_submit_button("확인 💖", use_container_width=True)

if submitted:
    st.session_state.offset = 0
    st.session_state.query = (line, station, direction)

q = st.session_state.query
if not q:
    st.info("🌸 노선과 역, 방향을 고르고 **확인**을 눌러 보세요! 다음 열차의 칸별 혼잡도를 알려드려요.")
else:
    ln, stn, d = q
    data = congestion(ln, stn, d, st.session_state.offset)
    lv = [level(p) for p in data]
    avg = round(sum(data) / len(data))
    best = data.index(min(data)) + 1
    near = exit_cars(ln, stn)

    st.markdown(
        f'<span class="badge" style="background:{LINES[ln]["color"]}">{ln}호선</span> '
        f'**{stn}역 · {LINES[ln]["dirs"][d]}** &nbsp; '
        f'<span class="lvl" style="background:{LEVEL_BG[level(avg)]};color:{LEVEL_FG[level(avg)]}">'
        f'전체 {LEVEL_TXT[level(avg)]} (약 {avg}%)</span>',
        unsafe_allow_html=True,
    )

    if st.button("🔄 실시간 새로고침"):
        st.session_state.offset += 1
        st.rerun()

    cols = st.columns(CAR_COUNT, gap="small")
    for i, col in enumerate(cols):
        n = i + 1
        star = '<span class="star">⭐</span>' if n == best else ""
        stair = "🪜 계단/에스컬<br>레이터 근처" if n in near else ""
        col.markdown(
            f'<div class="car-no {"best" if n == best else ""}">{n}호차</div>'
            f'<div class="box" style="background:{LEVEL_BG[lv[i]]}">{star}'
            f'<span class="face">{FACE[lv[i]]}</span><span class="pct">{data[i]}%</span></div>'
            f'<div class="near">{stair}</div>',
            unsafe_allow_html=True,
        )

    low = [i + 1 for i, v in enumerate(lv) if v == "low"]
    high = [i + 1 for i, v in enumerate(lv) if v == "high"]
    if low:
        rec = f"{', '.join(map(str, low))}호차<br>완전 여유있어요! ✨"
    elif "mid" in lv:
        rec = f"{best}호차가<br>그나마 제일 한산해요 🌿"
    else:
        rec = "모든 칸이 복잡해요 🥺<br>다음 열차를 기다려볼까요?"

    jam = [n for n in near if lv[n - 1] == "high"]
    if jam:
        warn = f"{', '.join(map(str, jam))}호차는 계단/에스컬레이터 앞이라 밀려요! 조금 이동해서 여유있는 칸을 노려봐요."
    elif high:
        warn = f"{', '.join(map(str, high))}호차가 꽉 찼어요. 쾌적한 다른 칸으로 이동해주세요!"
    else:
        warn = "우와~ 대부분의 칸이 넓고 여유로워요!"

    st.markdown(
        f'<div class="bubble"><span class="tag">치이카와 추천!</span>'
        f'<div class="big">{rec}</div><div class="sub">{warn}</div></div>',
        unsafe_allow_html=True,
    )

    now = datetime.now(ZoneInfo("Asia/Seoul")).strftime("%H:%M:%S")
    st.caption(f"{now} 기준 · 시간대와 역 이름으로 만든 가상 데이터예요 (실제 혼잡도 아님)")
