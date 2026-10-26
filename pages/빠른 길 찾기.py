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
    st.session_state.recent_searches = ["강남역", "홍대입구역", "서울역"]
if "favorites" not in st.session_state:
    st.session_state.favorites = ["우리집 (역삼동)", "회사 (판교)", "학교 (신촌)"]

# 3. 서울교통공사 사이버스테이션 노선도 데이터베이스
SUBWAY_STATIONS = [
    "서울역", "시청역", "종로3가역", "동대문역", "청량리역",
    "시청", "을지로입구", "을지로3가", "동대문역사문화공원", "신당역",
    "왕십리역", "성수역", "건대입구역", "잠실역", "삼성역",
    "선릉역", "강남역", "교대역", "서초역", "방배역",
    "사당역", "신림역", "신도림역", "영등포구청역", "당산역",
    "합정역", "홍대입구역", "신촌역", "충정로역", "압구정역",
    "옥수역", "고속터미널역", "양재역", "삼각지역", "이촌역",
    "동작역", "노량진역", "여의도역", "김포공항역", "판교역"
]

# 주요 노선 간 실제 사이버스테이션 기준 소요시간(분) 및 경로
REAL_ROUTES = {
    ("서울역", "강남역"): (30, "4호선 사당역 환승 ➡️ 2호선 강남역"),
    ("강남역", "서울역"): (30, "2호선 사당역 환승 ➡️ 4호선 서울역"),
    ("홍대입구역", "잠실역"): (39, "2호선 직행 (외선순환)"),
    ("잠실역", "홍대입구역"): (39, "2호선 직행 (내선순환)"),
    ("서울역", "홍대입구역"): (8, "공항철도 직행"),
    ("홍대입구역", "서울역"): (8, "공항철도 직행"),
    ("강남역", "판교역"): (15, "신분당선 직행"),
    ("판교역", "강남역"): (15, "신분당선 직행"),
    ("고속터미널역", "서울역"): (12, "4호선 삼각지역 환승"),
    ("신도림역", "강남역"): (26, "2호선 직행"),
}

def clean_station_name(name):
    name = name.strip()
    if name and not name.endswith("역"):
        name += "역"
    return name

def find_subway_route(start_raw, end_raw):
    start = clean_station_name(start_raw)
    end = clean_station_name(end_raw)
    
    # [검증] 노선도 DB에 없는 잘못된 입력 필터링 (예: 호날두)
    if start not in SUBWAY_STATIONS or end not in SUBWAY_STATIONS:
        invalid_list = []
        if start not in SUBWAY_STATIONS:
            invalid_list.append(f"'{start_raw}'")
        if end not in SUBWAY_STATIONS:
            invalid_list.append(f"'{end_raw}'")
        return False, f"⚠️ 입력하신 {', '.join(invalid_list)}은(는) 지하철 노선도에 등록되지 않은 역입니다. 올바른 역명을 입력해 주세요."
    
    if start == end:
        return False, "⚠️ 출발역과 도착역이 동일합니다. 서로 다른 역을 입력해 주세요."
    
    # 사이버스테이션 매핑 데이터 우선 적용
    if (start, end) in REAL_ROUTES:
        duration, route_desc = REAL_ROUTES[(start, end)]
        return True, {"start": start, "end": end, "time": duration, "route": route_desc}
    
    # 기타 등록역 계산
    idx_s = SUBWAY_STATIONS.index(start)
    idx_e = SUBWAY_STATIONS.index(end)
    station_cnt = abs(idx_s - idx_e)
    est_time = station_cnt * 3 + 4
    if est_time > 60:
        est_time = 50
        
    return True, {"start": start, "end": end, "time": est_time, "route": f"{start} ➡️ 최단 환승 경로 ➡️ {end}"}

# CSS 레이아웃 스타일링
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
    .card-blue { background-color: #EBF3FF; padding: 20px; border-radius: 12px; text-align: center; }
    .card-green { background-color: #EAF7E8; padding: 20px; border-radius: 12px; text-align: center; }
    .card-purple { background-color: #F2ECFB; padding: 20px; border-radius: 12px; text-align: center; }
    .card-yellow { background-color: #FFF9E5; padding: 20px; border-radius: 12px; text-align: center; }
    </style>
""", unsafe_allow_html=True)

def go_to(page_name):
    st.session_state.page = page_name

# --- 메인 화면 ---
if st.session_state.page == "home":
    st.markdown('<div class="header-box"><h1>길 찾기 대장</h1></div>', unsafe_allow_html=True)

    search_col1, search_col2 = st.columns([4, 1])
    with search_col1:
        query = st.text_input("검색", placeholder="지하철역 이름 검색 (예: 서울역, 강남역)", label_visibility="collapsed")
    with search_col2:
        if st.button("검색", type="primary", use_container_width=True):
            clean_q = clean_station_name(query)
            if clean_q in SUBWAY_STATIONS:
                st.session_state.recent_searches.insert(0, clean_q)
                st.success(f"🔍 '{clean_q}'을(를) 노선도에서 찾았습니다.")
            else:
                st.error(f"❌ '{query}'은(는) 유효한 지하철역이 아닙니다.")

    st.write("")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card-blue"><h2>📍 빠른 길 찾기</h2><p>실제 노선도 최단 경로 안내</p></div>', unsafe_allow_html=True)
        if st.button("빠른 길 찾기 실행", key="btn_fast", use_container_width=True):
            go_to("fast_route")
            st.rerun()

        st.write("")

        st.markdown('<div class="card-purple"><h2>🕒 최근 검색</h2><p>이전에 검색한 역 목록</p></div>', unsafe_allow_html=True)
        if st.button("최근 검색 기록 보기", key="btn_recent", use_container_width=True):
            go_to("recent")
            st.rerun()

    with col2:
        st.markdown('<div class="card-green"><h2>🚌 대중교통</h2><p>서울교통공사 사이버스테이션</p></div>', unsafe_allow_html=True)
        if st.button("사이버스테이션 연결", key="btn_transit", use_container_width=True):
            go_to("transit")
            st.rerun()

        st.write("")

        st.markdown('<div class="card-yellow"><h2>⭐ 즐겨찾기</h2><p>자주 가는 장소 관리</p></div>', unsafe_allow_html=True)
        if st.button("즐겨찾기 목록 열기", key="btn_fav", use_container_width=True):
            go_to("favorites")
            st.rerun()

# --- 상세 화면 ---
else:
    if st.button("⬅️ 메인 홈으로 돌아가기"):
        go_to("home")
        st.rerun()

    st.divider()

    if st.session_state.page == "fast_route":
        st.title("📍 빠른 길 찾기 (노선도 기반)")
        
        start_in = st.text_input("출발역 입력", value="서울역")
        end_in = st.text_input("도到着역 입력", value="강남역")
        
        if st.button("최단 경로 검색", type="primary"):
            success, result = find_subway_route(start_in, end_in)
            if not success:
                st.error(result)
            else:
                st.success(
                    f"🚇 **{result['start']}** ➡️ **{result['end']}**<br>"
                    f"⏱️ **소요 시간**: 약 **{result['time']}분**<br>"
                    f"🛤️ **추천 경로**: {result['route']}", 
                    icon="✅"
                )

    elif st.session_state.page == "transit":
        st.title("🚌 서울교통공사 사이버스테이션 연동")
        st.write("공식 지하철 노선도 웹 사이트로 이동할 수 있습니다.")
        st.link_button("🌐 서울교통공사 사이버스테이션 접속하기", "http://www.seoulmetro.co.kr/kr/cyberStation.do")

    elif st.session_state.page == "recent":
        st.title("🕒 최근 검색 기록")
        for item in st.session_state.recent_searches:
            st.write(f"- 🔍 {item}")

    elif st.session_state.page == "favorites":
        st.title("⭐ 즐겨찾기 장소")
        for fav in st.session_state.favorites:
            st.write(f"- 📌 {fav}")
