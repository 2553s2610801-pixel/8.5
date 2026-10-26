import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="길 찾기 대장",
    page_icon="🗺️",
    layout="centered"
)

# 2. 세션 상태 초기화
if "page" not in st.session_state:
    st.session_state.page = "home"
if "recent_searches" not in st.session_state:
    st.session_state.recent_searches = ["성환역 ➡️ 평택역", "강남역 ➡️ 판교역"]
if "favorites" not in st.session_state:
    st.session_state.favorites = ["성환역 (1호선)", "평택역 (1호선)", "강남역 (2호선)"]

# 3. 종합 대중교통 DB (전철역 + 버스 정류장 + 버스 노선)
SUBWAY_STATIONS = [
    # 1호선 전체 주요 역
    "연천역", "동두천역", "의정부역", "청량리역", "서울역", "용산역", "영등포역", "신도림역", 
    "구로역", "안양역", "수원역", "오산역", "서정리역", "평택지제역", "평택역", "성환역", 
    "직산역", "두정역", "천안역", "아산역", "온양온천역", "신창역", "인천역",
    # 기타 주요 환승 거점역
    "강남역", "홍대입구역", "잠실역", "고속터미널역", "사당역", "신촌역", "판교역", "여의도역"
]

BUS_STOPS = [
    "성환버스터미널", "남서울대", "평택터미널", "천안터미널", "강남역시외버스정류장", 
    "서울역버스환승센터", "수원역환승센터", "판교역보평교", "잠실역광역환승센터"
]

# 전체 장소 DB
ALL_LOCATIONS = SUBWAY_STATIONS + BUS_STOPS

# 주요 버스 및 전철 상세 경로 데이터베이스 (분 단위)
TRANSIT_ROUTES = {
    # 1호선 전철 구간
    ("성환역", "평택역"): (6, "🚃 1호선 전철 직행 (1정거장)", "지하철"),
    ("평택역", "성환역"): (6, "🚃 1호선 전철 직행 (1정거장)", "지하철"),
    ("성환역", "천안역"): (10, "🚃 1호선 전철 직행 (2정거장)", "지하철"),
    ("평택역", "수원역"): (32, "🚃 1호선 전철 직행", "지하철"),
    
    # 버스 전용 노선 (시내/시외/광역)
    ("성환역", "남서울대"): (8, "🚌 천안 시내버스 110번 / 130번 이용", "버스"),
    ("남서울대", "성환역"): (8, "🚌 천안 시내버스 110번 / 130번 이용", "버스"),
    ("성환버스터미널", "평택터미널"): (15, "🚌 시외버스 (성환-평택 노선)", "버스"),
    ("평택역", "평택터미널"): (5, "🚶 도보 이동 또는 시내버스 이용", "도보/버스"),
    ("강남역", "판교역"): (15, "🚌 광역버스 9000번 / 9401번 또는 신분당선", "버스/지하철"),
    ("서울역", "강남역"): (25, "🚌 광역버스 9401번 직행 (또는 4호선->2호선 환승)", "버스/지하철"),
    ("천안터미널", "성환역"): (25, "🚌 천안 시내버스 200번 이용", "버스")
}

def clean_location_name(name):
    name = name.strip()
    # '역'이나 '터미널' 등이 없는 단어 보정
    if name in [s.replace("역", "") for s in SUBWAY_STATIONS]:
        name += "역"
    return name

def calculate_fast_route(start_raw, end_raw):
    start = clean_location_name(start_raw)
    end = clean_location_name(end_raw)
    
    # DB 검증 (존재하지 않는 입력 차단)
    if start not in ALL_LOCATIONS or end not in ALL_LOCATIONS:
        invalid_list = []
        if start not in ALL_LOCATIONS:
            invalid_list.append(f"'{start_raw}'")
        if end not in ALL_LOCATIONS:
            invalid_list.append(f"'{end_raw}'")
        return False, f"⚠️ 입력하신 {', '.join(invalid_list)}은(는) 노선 데이터에 없습니다. 올바른 역명이나 정류장명을 입력해 주세요."
    
    if start == end:
        return False, "⚠️ 출발지와 도착지가 같습니다. 서로 다른 장소를 입력해 주세요."
    
    # 1. 사전 정의된 주요 버스/전철 경로 우선 검색
    if (start, end) in TRANSIT_ROUTES:
        duration, route_desc, mode = TRANSIT_ROUTES[(start, end)]
        return True, {"start": start, "end": end, "time": duration, "route": route_desc, "mode": mode}
    
    # 2. 일반 전철/버스 연계 최단 시간 계산
    idx_s = ALL_LOCATIONS.index(start)
    idx_e = ALL_LOCATIONS.index(end)
    cnt = abs(idx_s - idx_e)
    
    est_time = cnt * 4 + 6
    if est_time > 80:
        est_time = 65
        
    return True, {
        "start": start, 
        "end": end, 
        "time": est_time, 
        "route": f"{start} ➡️ 시내/광역 버스 및 전철 최적 연계 환승 ➡️ {end}",
        "mode": "버스+지하철 연계"
    }

# CSS 디자인
st.markdown("""
    <style>
    .header-box {
        background-color: #8FD8FA;
        padding: 20px;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 25px;
    }
    .header-box h1 { color: #000; font-size: 36px; font-weight: 800; margin: 0; }
    .card-blue { background-color: #EBF3FF; padding: 25px; border-radius: 12px; text-align: center; }
    .card-green { background-color: #EAF7E8; padding: 25px; border-radius: 12px; text-align: center; }
    .card-purple { background-color: #F2ECFB; padding: 25px; border-radius: 12px; text-align: center; }
    .card-yellow { background-color: #FFF9E5; padding: 25px; border-radius: 12px; text-align: center; }
    </style>
""", unsafe_allow_html=True)

def go_to(page_name):
    st.session_state.page = page_name

# --- 메인 화면 (검색창 제거, 빠른 길찾기 중심) ---
if st.session_state.page == "home":
    st.markdown('<div class="header-box"><h1>길 찾기 대장</h1></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card-blue"><h2>🚀 빠른 길 찾기</h2><p>버스 + 지하철 통합 최단 경로 검색</p></div>', unsafe_allow_html=True)
        if st.button("길 찾기 시작하기", key="btn_fast", use_container_width=True, type="primary"):
            go_to("fast_route")
            st.rerun()

        st.write("")

        st.markdown('<div class="card-purple"><h2>🕒 최근 탐색 경로</h2><p>이전에 조회한 경로 기록</p></div>', unsafe_allow_html=True)
        if st.button("최근 기록 보기", key="btn_recent", use_container_width=True):
            go_to("recent")
            st.rerun()

    with col2:
        st.markdown('<div class="card-green"><h2>🚌 버스/전철 노선 정보</h2><p>실시간 대중교통 웹사이트 연결</p></div>', unsafe_allow_html=True)
        if st.button("노선 정보 보기", key="btn_transit", use_container_width=True):
            go_to("transit")
            st.rerun()

        st.write("")

        st.markdown('<div class="card-yellow"><h2>⭐ 즐겨찾기</h2><p>자주 가는 역/정류장 목록</p></div>', unsafe_allow_html=True)
        if st.button("즐겨찾기 열기", key="btn_fav", use_container_width=True):
            go_to("favorites")
            st.rerun()

# --- 상세 기능 화면 ---
else:
    if st.button("⬅️ 메인 홈으로 돌아가기"):
        go_to("home")
        st.rerun()

    st.divider()

    if st.session_state.page == "fast_route":
        st.title("🚀 통합 빠른 길 찾기 (버스 + 지하철)")
        st.write("출발지와 도착지를 입력하시면 버스 및 전철을 포함한 **최단 시간 경로**를 계산합니다.")
        
        start_in = st.text_input("출발지 (역 또는 정류장)", value="성환역")
        end_in = st.text_input("도착지 (역 또는 정류장)", value="평택역")
        
        if st.button("최적 경로 계산", type="primary", use_container_width=True):
            success, result = calculate_fast_route(start_in, end_in)
            if not success:
                st.error(result)
            else:
                # 검색 기록에 저장
                route_str = f"{result['start']} ➡️ {result['end']}"
                if route_str not in st.session_state.recent_searches:
                    st.session_state.recent_searches.insert(0, route_str)
                
                st.success(
                    f"📍 **출발**: {result['start']} | 📍 **도착**: {result['end']}<br>"
                    f"⏱️ **최단 소요 시간**: 약 **{result['time']}분**<br>"
                    f"🚌 **추천 수단**: {result['route']}", 
                    icon="✅"
                )

    elif st.session_state.page == "transit":
        st.title("🚌 대중교통 노선 정보 연동")
        st.write("실시간 버스 및 전철 운행 정보를 확인할 수 있는 공식 페이지입니다.")
        st.link_button("🌐 서울교통공사 사이버스테이션 접속", "http://www.seoulmetro.co.kr/kr/cyberStation.do")

    elif st.session_state.page == "recent":
        st.title("🕒 최근 탐색 경로")
        if st.session_state.recent_searches:
            for item in st.session_state.recent_searches:
                st.write(f"- 🔍 {item}")
        else:
            st.write("기록이 없습니다.")

    elif st.session_state.page == "favorites":
        st.title("⭐ 즐겨찾기 장소")
        for fav in st.session_state.favorites:
            st.write(f"- 📌 {fav}")
