import html
import math
import random
import zlib
from datetime import datetime, timedelta, timezone

import streamlit as st

st.set_page_config(page_title="칸칸 혼잡도", page_icon="🚇", layout="centered")

# ───────────────────────── 시간 (한국 시간) ─────────────────────────
try:
    from zoneinfo import ZoneInfo
    KST = ZoneInfo("Asia/Seoul")
except Exception:
    KST = timezone(timedelta(hours=9))

WEEKDAYS = ["월", "화", "수", "목", "금", "토", "일"]


def now_kst():
    return datetime.now(KST)


# ───────────────────────── 노선 / 역 데이터 ─────────────────────────
DIR_DEFAULT = ["상행", "하행"]

# (노선명, 색상, 칸 수, 방향 목록, 역 목록)
LINE_DEFS = [
    ("1호선", "#0052A4", 10, ["상행 (소요산·청량리 방면)", "하행 (인천·신창 방면)"],
     "소요산 동두천 보산 동두천중앙 지행 덕정 덕계 양주 녹양 가능 의정부 회룡 망월사 도봉산 방학 창동 녹천 월계 광운대 석계 신이문 외대앞 회기 청량리 제기동 신설동 동묘앞 동대문 종로5가 종로3가 종각 시청 서울역 남영 용산 노량진 대방 신길 영등포 신도림 구로 가산디지털단지 독산 금천구청 석수 관악 안양 명학 금정 군포 당정 의왕 성균관대 화서 수원 세류 병점 세마 오산대 오산 진위 송탄 서정리 지제 평택 성환 직산 두정 천안 봉명 쌍용 아산 배방 온양온천 신창 구일 개봉 오류동 온수 역곡 소사 부천 중동 송내 부개 부평 백운 동암 간석 주안 도화 제물포 도원 동인천 인천"),
    ("2호선", "#00A84D", 10, ["내선순환", "외선순환"],
     "시청 을지로입구 을지로3가 을지로4가 동대문역사문화공원 신당 상왕십리 왕십리 한양대 뚝섬 성수 건대입구 구의 강변 잠실나루 잠실 잠실새내 종합운동장 삼성 선릉 역삼 강남 교대 서초 방배 사당 낙성대 서울대입구 봉천 신림 신대방 구로디지털단지 대림 신도림 문래 영등포구청 당산 합정 홍대입구 신촌 이대 아현 충정로 용답 신답 용두 도림천 양천구청 신정네거리 까치산"),
    ("3호선", "#EF7C1C", 10, ["상행 (대화 방면)", "하행 (오금 방면)"],
     "대화 주엽 정발산 마두 백석 대곡 화정 원당 원흥 삼송 지축 구파발 연신내 불광 녹번 홍제 무악재 독립문 경복궁 안국 종로3가 을지로3가 충무로 동대입구 약수 금호 옥수 압구정 신사 잠원 고속터미널 교대 남부터미널 양재 매봉 도곡 대치 학여울 대청 일원 수서 가락시장 경찰병원 오금"),
    ("4호선", "#00A5DE", 10, ["상행 (진접·당고개 방면)", "하행 (오이도 방면)"],
     "진접 오남 별내별가람 당고개 상계 노원 창동 쌍문 수유 미아 미아사거리 길음 성신여대입구 한성대입구 혜화 동대문 동대문역사문화공원 충무로 명동 회현 서울역 숙대입구 삼각지 신용산 이촌 동작 총신대입구 사당 남태령 선바위 경마공원 대공원 과천 정부과천청사 인덕원 평촌 범계 금정 산본 수리산 대야미 반월 상록수 한대앞 중앙 고잔 초지 안산 신길온천 정왕 오이도"),
    ("5호선", "#996CAC", 8, ["상행 (방화 방면)", "하행 (상일동·마천 방면)"],
     "방화 개화산 김포공항 송정 마곡 발산 우장산 화곡 까치산 신정 목동 오목교 양평 영등포구청 영등포시장 신길 여의도 여의나루 마포 공덕 애오개 충정로 서대문 광화문 종로3가 을지로4가 동대문역사문화공원 청구 신금호 행당 왕십리 마장 답십리 장한평 군자 아차산 광나루 천호 강동 길동 굽은다리 명일 고덕 상일동 강일 미사 하남풍산 하남시청 하남검단산 둔촌동 올림픽공원 방이 오금 개롱 거여 마천"),
    ("6호선", "#CD7C2F", 8, ["상행 (응암 방면)", "하행 (봉화산 방면)"],
     "응암 역촌 불광 독바위 연신내 구산 새절 증산 디지털미디어시티 월드컵경기장 마포구청 망원 합정 상수 광흥창 대흥 공덕 효창공원앞 삼각지 녹사평 이태원 한강진 버티고개 약수 청구 신당 동묘앞 창신 보문 안암 고려대 월곡 상월곡 돌곶이 석계 태릉입구 화랑대 봉화산"),
    ("7호선", "#747F00", 8, ["상행 (장암 방면)", "하행 (석남 방면)"],
     "장암 도봉산 수락산 마들 노원 중계 하계 공릉 태릉입구 먹골 중화 상봉 면목 사가정 용마산 중곡 군자 어린이대공원 건대입구 뚝섬유원지 청담 강남구청 학동 논현 반포 고속터미널 내방 이수 남성 숭실대입구 상도 장승배기 신대방삼거리 보라매 신풍 대림 남구로 가산디지털단지 철산 광명사거리 천왕 온수 까치울 부천종합운동장 춘의 신중동 부천시청 상동 삼산체육관 굴포천 부평구청 산곡 석남"),
    ("8호선", "#E6186C", 6, ["상행 (암사 방면)", "하행 (모란 방면)"],
     "암사 천호 강동구청 몽촌토성 잠실 석촌 송파 가락시장 문정 장지 복정 남위례 산성 남한산성입구 단대오거리 신흥 수진 모란"),
    ("9호선", "#B8A77A", 6, ["상행 (개화 방면)", "하행 (중앙보훈병원 방면)"],
     "개화 김포공항 공항시장 신방화 마곡나루 양천향교 가양 증미 등촌 염창 신목동 선유도 당산 국회의사당 여의도 샛강 노량진 노들 흑석 동작 구반포 신반포 고속터미널 사평 신논현 언주 선정릉 삼성중앙 봉은사 종합운동장 삼전 석촌고분 석촌 송파나루 한성백제 올림픽공원 둔촌오륜 중앙보훈병원"),
    ("신분당선", "#D4003B", 6, DIR_DEFAULT,
     "신사 논현 신논현 강남 양재 양재시민의숲 청계산입구 판교 정자 미금 동천 수지구청 성복 상현 광교중앙 광교"),
    ("수인분당선", "#F5A200", 10, DIR_DEFAULT,
     "인천 신포 숭의 인하대 송도 연수 원인재 남동인더스파크 호구포 인천논현 소래포구 월곶 달월 오이도 정왕 신길온천 안산 초지 고잔 중앙 한대앞 사리 야목 어천 오목천 고색 수원 매교 수원시청 매탄권선 망포 영통 청명 상갈 기흥 신갈 구성 보정 죽전 오리 미금 정자 수내 서현 이매 야탑 모란 태평 가천대 복정 수서 대모산입구 개포동 구룡 도곡 한티 선릉 선정릉 강남구청 압구정로데오 서울숲 왕십리"),
    ("경의중앙선", "#77C4A3", 8, DIR_DEFAULT,
     "문산 파주 금촌 금릉 운정 야당 탄현 일산 풍산 백마 곡산 대곡 능곡 행신 강매 화전 수색 디지털미디어시티 가좌 신촌 서울역 홍대입구 공덕 효창공원앞 용산 이촌 서빙고 한남 옥수 응봉 왕십리 청량리 회기 중랑 상봉 망우 양원 구리 도농 양정 덕소 도심 팔당 운길산 양수 신원 국수 아신 오빈 양평 원덕 용문 지평"),
    ("공항철도", "#0090D2", 6, DIR_DEFAULT,
     "서울역 공덕 홍대입구 디지털미디어시티 마곡나루 김포공항 계양 검암 청라국제도시 영종 운서 공항화물청사 인천공항1터미널 인천공항2터미널"),
    ("경춘선", "#0C8E72", 8, DIR_DEFAULT,
     "청량리 회기 중랑 상봉 망우 신내 갈매 별내 퇴계원 사릉 금곡 평내호평 천마산 마석 대성리 청평 상천 가평 굴봉산 백양리 강촌 김유정 남춘천 춘천"),
    ("인천1호선", "#7CA8D5", 6, DIR_DEFAULT,
     "계양 박촌 임학 계산 경인교대입구 작전 갈산 부평구청 부평시장 부평 동수 부평삼거리 간석오거리 인천시청 예술회관 인천터미널 문학경기장 선학 신연수 원인재 동춘 동막 캠퍼스타운 테크노파크 지식정보단지 인천대입구 센트럴파크 국제업무지구"),
    ("부산1호선", "#F06A00", 8, DIR_DEFAULT,
     "다대포해수욕장 다대포항 낫개 신장림 장림 동매 신평 하단 당리 사하 괴정 대티 서대신 동대신 토성 자갈치 남포 중앙 부산역 초량 부산진 좌천 범일 범내골 서면 부전 양정 시청 연산 교대 동래 명륜 온천장 부산대 장전 구서 두실 남산 범어사 노포"),
    ("부산2호선", "#81BF48", 6, DIR_DEFAULT,
     "장산 중동 해운대 동백 벡스코 센텀시티 민락 수영 광안 금련산 남천 경성대부경대 대연 못골 지게골 문현 국제금융센터부산은행 전포 서면 부암 가야 동의대 개금 냉정 주례 감전 사상 덕포 모덕 모라 구남 구명 덕천 수정 화명 율리 동원 금곡 호포 증산 부산대양산캠퍼스 남양산 양산"),
    ("부산3호선", "#BB8C00", 4, DIR_DEFAULT,
     "수영 망미 배산 물만골 연산 거제 종합운동장 사직 만덕 미남 덕천 구포 강서구청 체육공원 대저"),
    ("대구1호선", "#D93F5C", 6, DIR_DEFAULT,
     "설화명곡 화원 대곡 진천 월배 상인 월촌 송현 서부정류장 대명 안지랑 현충로 영대병원 교대 명덕 반월당 중앙로 대구역 칠성시장 신천 동대구 동구청 아양교 동촌 해안 방촌 용계 율하 신기 반야월 각산 안심"),
    ("대구2호선", "#00AA80", 6, DIR_DEFAULT,
     "문양 다사 대실 강창 계명대 성서산업단지 이곡 용산 죽전 감삼 두류 내당 반고개 청라언덕 반월당 경대병원 대구은행 범어 수성구청 만촌 담티 연호 대공원 고산 신매 사월 정평 임당 영남대"),
    ("대전1호선", "#007448", 4, DIR_DEFAULT,
     "반석 지족 노은 월드컵경기장 현충원 구암 유성온천 갑천 월평 갈마 정부청사 시청 탄방 용문 오룡 서대전네거리 중구청 중앙로 대전역 대동 신흥 판암"),
    ("광주1호선", "#009088", 2, DIR_DEFAULT,
     "녹동 소태 학동증심사입구 남광주 문화전당 금남로4가 금남로5가 양동시장 돌고개 농성 화정 쌍촌 운천 상무 김대중컨벤션센터 공항 송정공원 광주송정역 도덕 평동"),
]

REGION = {}
for _rg, _names in [("천안시", "두정 천안 봉명 쌍용 성환 직산"),
                    ("아산시", "아산 배방 온양온천 신창"),
                    ("평택시", "평택 지제 서정리 송탄 진위")]:
    for _n in _names.split():
        REGION[("1호선", _n)] = _rg

ENTRIES = []
for _line, _color, _cars, _dirs, _st in LINE_DEFS:
    for _s in _st.split():
        ENTRIES.append({"line": _line, "color": _color, "cars": _cars,
                        "dirs": _dirs, "station": _s, "custom": False})


def label_of(e):
    if e.get("custom"):
        return f"{e['station']}역 · 직접 입력 (목록에 없음)"
    rg = REGION.get((e["line"], e["station"]))
    return f"{e['station']}역 · {e['line']}" + (f" ({rg})" if rg else "")


# ───────────────────────── 검색 ─────────────────────────
def normalize(q):
    key = (q or "").strip().replace(" ", "")
    if key.endswith("역"):
        key = key[:-1]
    return key[:20]


def search(q):
    key = normalize(q)
    if not key:
        return []
    scored = []
    for idx, e in enumerate(ENTRIES):
        s = e["station"]
        if s == key:
            score = 0
        elif s.startswith(key):
            score = 1
        elif key in s:
            score = 2
        elif key in e["line"] or key in REGION.get((e["line"], s), ""):
            score = 3
        else:
            continue
        scored.append((score, idx, e))
    scored.sort(key=lambda x: (x[0], x[1]))
    res = [x[2] for x in scored[:80]]
    if not res:
        res = [{"line": "기타 노선", "color": "#8c7d87", "cars": 8,
                "dirs": DIR_DEFAULT, "station": key, "custom": True}]
    return res


# ───────────────────────── 혼잡도 계산 (가상 데이터) ─────────────────────────
def crc(s):
    return zlib.crc32(s.encode("utf-8"))


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def time_base(h, weekday):
    if h < 5.5:
        return 0.05
    if weekday:
        rush = max(math.exp(-((h - 8.2) ** 2) / 1.4), math.exp(-((h - 18.3) ** 2) / 2.0))
        mid = 0.35 * math.exp(-((h - 13.0) ** 2) / 12.0)
        base = 0.18 + 0.55 * max(rush, mid)
    else:
        base = 0.15 + 0.30 * math.exp(-((h - 14.0) ** 2) / 12.0)
    if h >= 23.5:
        base *= 0.5
    return base


def station_bias(e):
    return (crc("bias" + e["line"] + e["station"]) % 1000) / 1000.0 * 0.2 - 0.1


def exit_cars(e, dir_idx):
    n = e["cars"]
    r = random.Random(crc(f"exit|{e['line']}|{e['station']}|{dir_idx}"))
    a = r.randint(1, n)
    b = r.randint(1, n)
    if n > 1 and b == a:
        b = a % n + 1
    return sorted(set([a, b]))


def car_loads(e, dir_idx, now, offset):
    h = now.hour + now.minute / 60.0
    base = clamp(time_base(h, now.weekday() < 5) + station_bias(e), 0.04, 0.95)
    bucket = int(now.timestamp() // 300) + offset
    r = random.Random(crc(f"{e['line']}|{e['station']}|{dir_idx}") + bucket)
    exits = exit_cars(e, dir_idx)
    out = []
    for i in range(e["cars"]):
        v = base + (r.random() - 0.5) * 0.30 + (0.20 if (i + 1) in exits else -0.05)
        out.append(int(round(clamp(v, 0.05, 1.0) * 100)))
    return out


def day_trend(e, weekday):
    res = []
    for h in range(5, 24):
        v = clamp(time_base(h + 0.5, weekday) + station_bias(e), 0.04, 0.95)
        res.append((h, int(round(v * 100))))
    return res


def lvl(p):
    return "low" if p < 40 else "mid" if p < 70 else "high"


LV_TXT = {"low": "여유", "mid": "보통", "high": "복잡"}
LV_BG = {"low": "#b2f2bb", "mid": "#ffec99", "high": "#ffc9c9"}
LV_FG = {"low": "#2b6e3b", "mid": "#856404", "high": "#9c2b2b"}
FACE = {"low": "(˶ˆ꒳ˆ˵)", "mid": "(•ᴗ•)", "high": "(>_<)"}
MASCOT = {"low": "🐭", "mid": "🐱", "high": "🐰"}

# ───────────────────────── 스타일 ─────────────────────────
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Jua&family=Gowun+Dodum&display=swap');
.stApp { background: linear-gradient(135deg, #fff0f5 0%, #f0f7ff 100%); }
html, body, [class*="css"] { font-family: 'Gowun Dodum', 'Pretendard', sans-serif; }
.block-container { max-width: 860px; padding-top: 1.6rem; }
.hero { display:flex; align-items:center; gap:14px; margin-bottom:6px; }
.hero .logo { width:62px; height:62px; border-radius:50%; background:#ffe3ec; border:3px solid #ffc2d4;
  display:flex; align-items:center; justify-content:center; font-size:32px; box-shadow: inset 0 -4px 0 #ffa8c0; }
.hero h1 { margin:0; font-family:'Jua', sans-serif; font-size:2rem; color:#5a434d; }
.hero p { margin:2px 0 0; color:#8c7d87; font-weight:700; font-size:.95rem; }
.head { display:flex; align-items:center; gap:10px; flex-wrap:wrap; margin-top:8px; }
.badge { color:#fff; border-radius:999px; padding:4px 14px; font-family:'Jua', sans-serif; }
.stitle { font-family:'Jua', sans-serif; font-size:1.35rem; color:#4a3842; }
.pill { margin-left:auto; border-radius:999px; padding:5px 16px; font-family:'Jua', sans-serif; }
.clock { color:#8c7d87; font-weight:700; font-size:.88rem; margin:4px 0 0; }
.trainwrap { overflow-x:auto; padding:22px 4px 8px; }
.train { display:flex; align-items:flex-end; gap:5px; min-width:420px; position:relative; padding-bottom:14px; }
.train::after { content:""; position:absolute; left:0; right:0; bottom:0; height:6px; border-radius:3px;
  background: repeating-linear-gradient(90deg, #ffd0e0 0 16px, transparent 16px 24px); }
.cap { width:14px; height:60px; background:#6c5b65; margin-bottom:14px; flex:none; }
.cap.l { border-radius:30px 6px 6px 30px; } .cap.r { border-radius:6px 30px 30px 6px; }
.car { flex:1 1 0; min-width:46px; display:flex; flex-direction:column; align-items:center; gap:5px; }
.cno { font-size:.8rem; color:#8c7d87; font-weight:700; }
.cno.best { color:#ff5285; font-family:'Jua', sans-serif; }
.box { width:100%; height:100px; border-radius:20px; border:3px solid rgba(0,0,0,.06); position:relative;
  display:flex; flex-direction:column; align-items:center; justify-content:center; gap:3px;
  box-shadow: inset 0 -6px 0 rgba(0,0,0,.08); }
.box .face { font-size:.8rem; color:#5a434d; }
.box .pct { font-family:'Jua', sans-serif; font-size:1.05rem; color:#333; }
.star { position:absolute; top:-14px; right:-4px; font-size:1.3rem; }
.stair { font-size:.62rem; line-height:1.2; text-align:center; color:#d6527f; font-weight:700; min-height:2.5em; }
.legend { display:flex; gap:14px; flex-wrap:wrap; margin:6px 0 0; font-size:.82rem; color:#7a626f; font-weight:700; }
.legend span i { display:inline-block; width:12px; height:12px; border-radius:50%; margin-right:5px; vertical-align:-1px; }
.bubble { background:#fff5f8; border:3px solid #ffcadb; border-radius:28px; padding:18px 24px; margin-top:14px; }
.bubble .tag { display:inline-block; background:#ff7399; color:#fff; border-radius:999px; padding:3px 12px;
  font-family:'Jua', sans-serif; font-size:.82rem; }
.bubble .big { font-family:'Jua', sans-serif; font-size:1.7rem; color:#4a323d; margin:8px 0 4px; line-height:1.35; }
.bubble .sub { color:#7a626f; font-weight:700; line-height:1.55; }
.card { background:#fff; border:2px dashed #fcd5e4; border-radius:24px; padding:14px 18px; margin-top:12px; }
.card h4 { margin:0 0 8px; font-family:'Jua', sans-serif; color:#6b4d5a; font-size:1.1rem; }
.srow { display:flex; align-items:center; gap:10px; padding:7px 0; border-top:1px solid #fde4ee; flex-wrap:wrap; }
.srow .who { font-size:1.4rem; }
.srow .txt { color:#5a434d; font-weight:700; font-size:.92rem; flex:1; min-width:180px; }
.mini { border-radius:999px; padding:2px 12px; font-weight:700; font-size:.82rem; }
.trend { display:flex; align-items:flex-end; gap:3px; height:96px; min-width:400px; }
.trendwrap { overflow-x:auto; padding-top:4px; }
.tb { flex:1 1 0; display:flex; flex-direction:column; align-items:center; justify-content:flex-end; gap:3px; }
.tb .bar { width:100%; border-radius:6px 6px 2px 2px; }
.tb .hh { font-size:.6rem; color:#8c7d87; font-weight:700; }
.tb.now .bar { outline:2px solid #ff7399; outline-offset:1px; }
.tb.now .hh { color:#ff5285; }
.hint { margin-top:18px; padding:30px 16px; border-radius:26px; background:#fff5f8; border:2px dashed #fcd5e4;
  text-align:center; color:#7a626f; font-weight:700; line-height:1.7; }
.hint .e { font-size:2rem; display:block; margin-bottom:4px; }
.foot { color:#8c7d87; font-size:.8rem; font-weight:700; margin-top:14px; }
.plat { display:flex; gap:5px; min-width:420px; align-items:flex-end; }
.pc { flex:1 1 0; min-width:46px; display:flex; flex-direction:column; align-items:center; gap:4px; }
.ppl { font-size:.7rem; line-height:1.1; text-align:center; min-height:3.4em; display:flex; align-items:flex-end; justify-content:center; flex-wrap:wrap; }
.pbar { width:100%; height:14px; border-radius:7px; }
.pn { font-size:.72rem; color:#8c7d87; font-weight:700; }
.pst { font-size:.62rem; line-height:1.2; font-weight:700; text-align:center; min-height:2.6em; }
.pst.jam { color:#d6527f; } .pst.free { color:#2b8a3e; }
.sum { display:flex; gap:10px; flex-wrap:wrap; margin-bottom:8px; }
.sum .m { flex:1; min-width:120px; background:#fff5f8; border-radius:18px; padding:8px 12px; text-align:center; font-weight:700; color:#5a434d; }
.sum .m b { display:block; font-family:'Jua', sans-serif; font-size:1.3rem; }
div.stButton > button { border-radius:999px; border:2px solid #ffc2d4; background:#fff; color:#5a434d; font-weight:700; }
div.stButton > button:hover { border-color:#ff7399; color:#ff5285; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ───────────────────────── 세션 상태 ─────────────────────────
st.session_state.setdefault("q", "")
st.session_state.setdefault("prefer", None)
st.session_state.setdefault("favs", [])      # [(역, 노선)]
st.session_state.setdefault("offset", 0)


def set_query(text, prefer=None):
    st.session_state["q"] = text
    st.session_state["prefer"] = prefer


def clear_prefer():
    st.session_state["prefer"] = None


def bump_refresh():
    st.session_state["offset"] += 1


def toggle_fav(station, line):
    favs = st.session_state["favs"]
    item = (station, line)
    if item in favs:
        favs.remove(item)
    else:
        favs.append(item)
    st.session_state["favs"] = favs[:12]


# ───────────────────────── 화면 조각 ─────────────────────────
def render_header(e, dir_idx, avg, now):
    lv = lvl(avg)
    st.markdown(
        f'<div class="head"><span class="badge" style="background:{e["color"]}">{html.escape(e["line"])}</span>'
        f'<span class="stitle">{html.escape(e["station"])}역 · {html.escape(e["dirs"][dir_idx])}</span>'
        f'<span class="pill" style="background:{LV_BG[lv]};color:{LV_FG[lv]}">전체 {LV_TXT[lv]} · 약 {avg}%</span></div>'
        f'<p class="clock">🕒 {now.strftime("%Y-%m-%d")} ({WEEKDAYS[now.weekday()]}) {now.strftime("%H:%M:%S")} 기준</p>',
        unsafe_allow_html=True,
    )


def render_train(loads, exits, best):
    cars = []
    for i, p in enumerate(loads):
        n = i + 1
        lv = lvl(p)
        star = '<span class="star">⭐</span>' if n == best else ""
        stair = "🪜 계단·에스컬<br>레이터 근처" if n in exits else ""
        best_cls = " best" if n == best else ""
        cars.append(
            f'<div class="car"><span class="cno{best_cls}">{n}호차</span>'
            f'<div class="box" style="background:{LV_BG[lv]}">{star}'
            f'<span class="face">{FACE[lv]}</span><span class="pct">{p}%</span></div>'
            f'<span class="stair">{stair}</span></div>'
        )
    st.markdown(
        '<div class="trainwrap"><div class="train"><div class="cap l"></div>'
        + "".join(cars)
        + '<div class="cap r"></div></div></div>'
        '<div class="legend"><span><i style="background:#b2f2bb"></i>여유 (40% 미만)</span>'
        '<span><i style="background:#ffec99"></i>보통 (40~69%)</span>'
        '<span><i style="background:#ffc9c9"></i>복잡 (70% 이상)</span></div>',
        unsafe_allow_html=True,
    )


def render_recommend(loads, best, exits):
    lv_list = [lvl(p) for p in loads]
    low = [i + 1 for i, v in enumerate(lv_list) if v == "low"]
    high = [i + 1 for i, v in enumerate(lv_list) if v == "high"]
    if low:
        big = f"{', '.join(map(str, low))}호차가<br>완전 여유로워요! ✨"
        mood = "low"
    elif "mid" in lv_list:
        big = f"{best}호차가<br>그나마 제일 한산해요 🌿"
        mood = "mid"
    else:
        big = "모든 칸이 복잡해요 🥺<br>다음 열차를 기다려볼까요?"
        mood = "high"
    jam = [n for n in exits if lv_list[n - 1] == "high"]
    if jam:
        sub = f"{', '.join(map(str, jam))}호차는 계단·에스컬레이터 앞이라 특히 붐벼요. 한두 칸만 옮겨 보세요!"
    elif high:
        sub = f"{', '.join(map(str, high))}호차가 꽉 찼어요. 다른 칸을 노려 보세요!"
    else:
        sub = "대부분의 칸이 넓고 여유로워요. 편하게 타세요!"
    st.markdown(
        f'<div class="bubble"><span class="tag">{MASCOT[mood]} 칸칸이의 추천!</span>'
        f'<div class="big">{big}</div><div class="sub">{sub}</div></div>',
        unsafe_allow_html=True,
    )


def render_stairs(loads, exits):
    rows = []
    n_cars = len(loads)
    for n in exits:
        p = loads[n - 1]
        lv = lvl(p)
        people = max(3, int(round(p * 0.45)))
        near = [m for m in range(max(1, n - 2), min(n_cars, n + 2) + 1) if m != n and m not in exits]
        if near:
            alt = min(near, key=lambda m: loads[m - 1])
            tip = f"가까운 {alt}호차({loads[alt - 1]}%)가 더 여유로워요."
        else:
            tip = "주변 칸으로 조금만 이동해 보세요."
        rows.append(
            f'<div class="srow"><span class="who">🪜🚶</span>'
            f'<span class="txt">{n}호차 · 계단·에스컬레이터 앞에 약 {people}명이 몰려 있어요. {tip}</span>'
            f'<span class="mini" style="background:{LV_BG[lv]};color:{LV_FG[lv]}">{LV_TXT[lv]} {p}%</span></div>'
        )
    st.markdown(
        '<div class="card"><h4>🪜 계단·에스컬레이터 쏠림</h4>' + "".join(rows) + "</div>",
        unsafe_allow_html=True,
    )


def render_trend(e, now):
    weekday = now.weekday() < 5
    data = day_trend(e, weekday)
    bars = []
    for h, v in data:
        lv = lvl(v)
        cls = "tb now" if h == now.hour else "tb"
        bars.append(
            f'<div class="{cls}"><div class="bar" style="height:{max(6, int(v * 0.8))}px;background:{LV_BG[lv]}"></div>'
            f'<span class="hh">{h}</span></div>'
        )
    future = [(h, v) for h, v in data if h > now.hour and 6 <= h <= 22]
    tip = ""
    if future:
        bh, bv = min(future, key=lambda x: x[1])
        tip = (f'<div style="color:#7a626f;font-weight:700;margin-top:6px">'
               f'오늘 지금 이후엔 <b>{bh}시</b>쯤이 가장 한산해요 (약 {bv}%) 🌿</div>')
    kind = "평일" if weekday else "주말"
    st.markdown(
        f'<div class="card"><h4>📈 시간대별 혼잡도 ({kind} 기준)</h4>'
        f'<div class="trendwrap"><div class="trend">{"".join(bars)}</div></div>{tip}</div>',
        unsafe_allow_html=True,
    )



def access_kinds(e, dir_idx, exits):
    r = random.Random(crc(f"kind|{e['line']}|{e['station']}|{dir_idx}"))
    kinds = ["계단", "에스컬레이터"]
    r.shuffle(kinds)
    return {n: kinds[i % 2] for i, n in enumerate(exits)}


def spread_plan(loads):
    """혼잡한 칸(70% 이상)의 승객을 가까운 여유 칸으로 나눴을 때의 예상 결과"""
    after = loads[:]
    moves = []
    n = len(after)
    order = sorted([i for i, p in enumerate(after) if p >= 70], key=lambda i: -after[i])
    for i in order:
        excess = after[i] - 60
        cands = sorted([j for j in range(n) if j != i and abs(j - i) <= 3 and after[j] < 60],
                       key=lambda j: (after[j], abs(j - i)))
        for j in cands:
            if excess <= 0:
                break
            mv = min(excess, 60 - after[j])
            if mv <= 0:
                continue
            after[i] -= mv
            after[j] += mv
            excess -= mv
            moves.append((i + 1, j + 1, mv))
    return after, moves


def render_platform(loads, exits, kinds):
    cells = []
    for i, p in enumerate(loads):
        n = i + 1
        lv = lvl(p)
        people = "🚶" * max(1, int(round(p / 20.0)))
        if n in exits:
            note = f'<span class="pst jam">🪜 {kinds.get(n, "계단")}<br>(몰림)</span>'
        elif lv == "low":
            note = '<span class="pst free">🌿 한산<br>(여기로!)</span>'
        else:
            note = '<span class="pst"></span>'
        cells.append(
            f'<div class="pc"><div class="ppl">{people}</div>'
            f'<div class="pbar" style="background:{LV_BG[lv]}"></div>'
            f'<span class="pn">{n}호차</span>{note}</div>'
        )
    st.markdown(
        '<div class="card"><h4>🚉 승강장 한눈에 보기</h4>'
        '<div class="trainwrap"><div class="plat">' + "".join(cells) + "</div></div>"
        '<div style="color:#8c7d87;font-size:.8rem;font-weight:700">'
        "🚶 = 승강장에서 기다리는 사람 (많을수록 붐벼요) · 🪜 = 계단/에스컬레이터 위치 · 🌿 = 한산한 칸</div></div>",
        unsafe_allow_html=True,
    )


def render_spread(loads):
    after, moves = spread_plan(loads)
    before_max, after_max = max(loads), max(after)
    high_n = len([p for p in loads if p >= 70])
    low_n = len([p for p in loads if p < 40])
    rows = []
    for a, b, mv in moves[:5]:
        rows.append(
            f'<div class="srow"><span class="who">🚶➡️</span>'
            f'<span class="txt">{a}호차({loads[a - 1]}%) 앞에 계신 분들은 {b}호차({loads[b - 1]}%)로 이동해 보세요!</span>'
            f'<span class="mini" style="background:#e7f5ff;color:#1c5d99">약 {mv}%p 분산</span></div>'
        )
    if rows:
        body = "".join(rows)
    elif high_n == 0:
        body = '<div class="sub" style="color:#7a626f;font-weight:700">지금은 승객이 고르게 퍼져 있어요. 가까운 칸에 타셔도 좋아요! 🌸</div>'
    else:
        body = '<div class="sub" style="color:#7a626f;font-weight:700">가까운 곳에 여유 칸이 없어요. 다음 열차도 고려해 보세요.</div>'
    st.markdown(
        '<div class="card"><h4>🤝 승객 분산 안내</h4>'
        f'<div class="sum"><div class="m"><b>{high_n}칸</b>복잡한 칸</div>'
        f'<div class="m"><b>{low_n}칸</b>한산한 칸</div>'
        f'<div class="m"><b>{before_max}% → {after_max}%</b>분산 후 최대 혼잡도</div></div>'
        + body + "</div>",
        unsafe_allow_html=True,
    )


# ───────────────────────── 메인 ─────────────────────────
st.markdown(
    '<div class="hero"><div class="logo">🐭</div><div><h1>칸칸 혼잡도</h1>'
    "<p>복잡복잡 싫어! 폭닥하고 여유로운 칸으로 타요 ( •̀ω•́ )✨</p></div></div>",
    unsafe_allow_html=True,
)

st.text_input(
    "역 이름 검색",
    key="q",
    placeholder="예: 두정, 천안, 강남, 해운대, 반월당",
    on_change=clear_prefer,
)

query = st.session_state["q"]

try:
    cands = search(query)
except Exception:
    cands = []
    st.error("검색 중 문제가 생겼어요. 다시 입력해 주세요.")

if not cands:
    st.markdown(
        '<div class="hint"><span class="e">🌸 🚇 🌸</span>역 이름을 입력하면 칸별 혼잡도를 알려드려요!<br>'
        "노선 이름(예: 2호선)으로도 검색할 수 있어요.</div>",
        unsafe_allow_html=True,
    )
    st.caption("자주 찾는 역")
    popular = [("서울역", "1호선"), ("강남", "2호선"), ("홍대입구", "2호선"),
               ("잠실", "2호선"), ("두정", "1호선"), ("천안", "1호선")]
    cols = st.columns(3)
    for i, (s, ln) in enumerate(popular):
        lab = f"{s}역 · {ln}"
        rg = REGION.get((ln, s))
        if rg:
            lab += f" ({rg})"
        cols[i % 3].button(lab, key=f"pop{i}", use_container_width=True,
                           on_click=set_query, args=(s, lab))
else:
    labels = [label_of(c) for c in cands]
    idx = 0
    prefer = st.session_state.get("prefer")
    if prefer in labels:
        idx = labels.index(prefer)

    c1, c2 = st.columns(2)
    with c1:
        pick = st.selectbox("검색 결과", labels, index=idx)
    entry = cands[labels.index(pick)] if pick in labels else cands[0]
    with c2:
        dir_idx = st.selectbox("방향", list(range(len(entry["dirs"]))),
                               format_func=lambda i: entry["dirs"][i])

    fav_item = (entry["station"], entry["line"])
    b1, b2 = st.columns(2)
    with b1:
        st.button("🔄 실시간 새로고침", use_container_width=True, on_click=bump_refresh)
    with b2:
        if not entry.get("custom"):
            is_fav = fav_item in st.session_state["favs"]
            st.button("💔 즐겨찾기 해제" if is_fav else "💖 즐겨찾기 추가", use_container_width=True,
                      on_click=toggle_fav, args=fav_item)

    try:
        now = now_kst()
        loads = car_loads(entry, dir_idx, now, st.session_state["offset"])
        exits = exit_cars(entry, dir_idx)
        best = loads.index(min(loads)) + 1
        avg = int(round(sum(loads) / len(loads)))

        render_header(entry, dir_idx, avg, now)
        render_train(loads, exits, best)
        render_recommend(loads, best, exits)
        kinds = access_kinds(entry, dir_idx, exits)
        render_platform(loads, exits, kinds)
        render_stairs(loads, exits)
        render_spread(loads)
        render_trend(entry, now)
    except Exception:
        st.error("혼잡도를 표시하는 중 문제가 생겼어요. 새로고침을 눌러 다시 시도해 주세요. 🥺")

favs = st.session_state["favs"]
if favs:
    st.caption("💖 즐겨찾기")
    fcols = st.columns(3)
    for i, (s, ln) in enumerate(favs):
        lab = f"{s}역 · {ln}"
        rg = REGION.get((ln, s))
        if rg:
            lab += f" ({rg})"
        fcols[i % 3].button(lab, key=f"fav{i}", use_container_width=True,
                            on_click=set_query, args=(s, lab))

st.markdown(
    '<p class="foot">※ 이 앱의 혼잡도는 시간대·역 이름으로 만든 <b>가상(시뮬레이션) 데이터</b>라 실제 혼잡도와 다를 수 있어요. '
    "새로고침은 5분 단위로 값이 바뀌는 방식이에요.</p>",
    unsafe_allow_html=True,
)
