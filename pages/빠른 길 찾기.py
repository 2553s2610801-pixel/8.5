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
    st.session_state.recent_searches = ["성환역", "평택역", "서울역"]
if "favorites" not in st.session_state:
    st.session_state.favorites = ["성환역 (1호선)", "평택역 (1호선)", "강남역 (2호선)"]

# 3. 수도권 전철 1호선 본선 및 지선 전체 역 데이터베이스
LINE_1_STATIONS = [
    # [경원선 구간] 연천 ~ 회기
    "연천역", "전곡역", "청산역", "초성리역", "소요산역", "동두천역", "보산역", "동두천중앙역", 
    "지행역", "덕정역", "덕계역", "양주역", "녹양역", "가능역", "의정부역", "회룡역", 
    "망월사역", "도봉산역", "도봉역", "방학역", "창동역", "녹천역", "월계역", "광운대역", 
    "석계역", "신이문역", "외대앞역", "회기역",
    
    # [서울 지하철 1호선 구간] 청량리 ~ 서울역
    "청량리역", "제기동역", "신설동역", "동묘앞역", "동대문역", "종로5가역", "종로3가역", 
    "종각역", "시청역", "서울역",
    
    # [경부선 구간] 남영 ~ 천안
    "남영역", "용산역", "노량진역", "대방역", "신길역", "영등포역", "신도림역", "구로역", 
    "가산디지털단지역", "독산역", "금천구청역", "석수역", "관악역", "안양역", "명학역", 
    "금정역", "군포역", "당정역", "의왕역", "성균관대역", "화서역", "수원역", "세류역", 
    "병점역", "세마역", "오산대역", "오산역", "진위역", "송탄역", "서정리역", "평택지제역", 
    "평택역", "성환역", "직산역", "두정역", "천안역",
    
    # [장항선 구간] 봉명 ~ 신창
    "봉명역", "쌍용역", "아산역", "탕정역", "배방역", "온양온천역", "신창역",
    
    # [경인선 지선] 구일 ~ 인천
    "구일역", "개봉역", "오류동역", "온수역", "역곡역", "소사역", "부천역", "중동역", 
    "송내역", "부개역", "부평역", "백운역", "동암역", "간석역", "주안역", "도화역", 
    "제물포역", "도원역", "동인천역", "인천역",
    
    # [기타 지선] 서동탄, 광명
    "서동탄역", "광명역"
]

# 타 노선 주요 환승 거점역 추가
OTHER_MAJOR_STATIONS = [
    "강남역", "홍대입구역", "잠실역", "고속터미널역", "사당역", "신촌역", 
    "건대입구역", "삼성역", "판교역", "합정역", "여의도역", "김포공항역"
]

# 전체 역 통합 DB
SUBWAY_STATIONS = LINE_1_STATIONS + OTHER_MAJOR_STATIONS

# 특정 구간 실제 정확한 소요시간 데이터 매핑 (분 단위)
REAL_ROUTES = {
    # 성환 / 평택 주변 주요 구간
    ("성환역", "평택역"): (6, "1호선 직행 (1정거장)"),
    ("평택역", "성환역"): (6, "1호선 직행 (1정거장)"),
    ("성환역", "직산역"): (4, "1호선 직행"),
    ("직산역", "성환역"): (4, "1호선 직행"),
    ("성환역", "천안역"): (10, "1호선 직행 (2정거장)"),
    ("천안역", "성환역"): (10, "1호선 직행 (2정거장)"),
    ("평택역", "평택지제역"): (4, "1호선 직행"),
    ("평택지제역", "평택역"): (4, "1호선 직행"),
    ("성환역", "수원역"): (38, "1호선 직행"),
    ("평택역", "수원역"): (32, "1호선 직행"),
    ("성환역", "서울역"): (75, "1호선 전철 (ITX-마음/무궁화호 이용 시 약 50분)"),
    ("평택역", "서울역"): (68, "1호선 전철 (ITX-새마을/무궁화호 이용 시 약 45분)"),
    
    # 주요 서울 타 노선 경로
    ("서울역", "강남역"): (30, "4호선 사당역 환승 ➡️ 2호선 강남역"),
    ("강남역", "서울역"): (30, "2호선 사당역 환승 ➡️ 4호선 서울역"),
    ("홍대입구역", "잠실역"): (39, "2호선 직행"),
    ("서울역", "홍대입구역"): (8, "공항철도 직행"),
    ("강남역", "판교역"): (15, "신분당선 직행")
}

def clean_station_name(name):
    name = name.strip()
    if name and not name.endswith("역"):
        name += "역"
    return name

def find_subway_route(start_raw, end_raw):
    start = clean_station_name(start_raw)
    end = clean_station_name(end_raw)
    
    # DB에 없는 역 차단 (호날두, 메시 등 유효하지 않은 입력)
    if start not in SUBWAY_STATIONS or end not in SUBWAY_STATIONS:
        invalid_list = []
        if start not in SUBWAY_STATIONS:
            invalid_list.append(f"'{start_raw}'")
        if end not in SUBWAY_STATIONS:
            invalid_list.append(f"'{end_raw}'")
        return False, f"⚠️ 입력하신 {', '.join(invalid_list)}은(는) 노선도에 등록되지 않은 역입니다. 올바른 역명을 입력해 주세요."
    
    if start == end:
        return False, "⚠️ 출발역과 도착역이 같습니다. 서로 다른 역을 입력해 주세요."
    
    # 1. 실제 사전 등록된 구간 데이터 조회
    if (start, end) in REAL_ROUTES:
        duration, route_desc = REAL_ROUTES[(start, end)]
        return True, {"start": start, "end": end, "time": duration, "route": route_desc}
    
    # 2. 1호선 라인 내에서의 정거장 수 기반 소요시간 자동 계산
    if start in LINE_1_STATIONS and end in LINE_1_STATIONS:
        idx_s = LINE_1_STATIONS.index(start)
        idx_e = LINE_1_STATIONS.index(end)
        station_count = abs(idx_s - idx_e)
        est_time = station_count * 3  # 1호선 평균 정거장 간 2.5~3분 소요
        return True, {"start": start, "end": end, "time": est_time, "route": f"수도권 전철 1호선 직행 (약 {station_count}개 정거장 이동)"}
        
    # 3. 타 노선 환승 계산
    idx_s = SUBWAY_STATIONS.index(start)
    idx_e = SUBWAY_STATIONS.index(end)
    station_cnt = abs(idx_s - idx_e)
    est_time = station_cnt * 4 + 5
    
    return True, {"start": start, "end": end, "time": est_time, "route": f"{start} ➡️ 최단 환승 경로 ➡️ {end}"}

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
    .card-blue { background-color: #EBF3FF; padding: 20px; border-radius: 12px; text-align: center; }
    .card-green { background-color: #EAF7E8; padding: 20px; border-radius: 12px; text-align: center; }
    .card-purple { background-color: #F2ECFB; padding: 20px; border-radius: 12px; text-align: center; }
    .card-yellow { background-color: #FFF9E5; padding: 20px; border-radius: 12px; text-align: center; }
    </style>
""", unsafe_allow_html=True)

def go_to(page_name):
    st.session_state.page = page_name

# 메인 홈 화면
if st.session_state.page == "home":
    st.markdown('<div class="header-box"><h1>길 찾기 대장</h1></div>', unsafe_allow_html=True)

    search_col1, search_col2 = st.columns([4, 1])
    with search_col1:
        query = st.text_input("검색", placeholder="전철역 이름 입력 (예: 성환역, 평택역, 연천역, 신창역)", label_visibility="collapsed")
    with search_col2:
        if st.button("검색", type="primary", use_container_width=True):
            clean_q = clean_station_name(query)
            if clean_q in SUBWAY_STATIONS:
                st.session_state.recent_searches.insert(0, clean_q)
                st.success(f"🔍 '{clean_q}'을(를) 노선도에서 찾았습니다.")
            else:
                st.error(f"❌ '{query}'은(는) 노선도에 없는 역명입니다.")

    st.write("")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card-blue"><h2>📍 빠른 길 찾기</h2><p>1호선 전체 및 주요 역 최단 경로</p></div>', unsafe_allow_html=True)
        if st.button("빠른 길 찾기 실행", key="btn_fast", use_container_width=True):
            go_to("fast_route")
            st.rerun()

        st.write("")

        st.markdown('<div class="card-purple"><h2>🕒 최근 검색</h2><p>이전에 찾았던 역 목록</p></div>', unsafe_allow_html=True)
        if st.button("최근 검색 기록 보기", key="btn_recent", use_container_width=True):
            go_to("recent")
            st.rerun()

    with col2:
        st.markdown('<div class="card-green"><h2>🚌 대중교통</h2><p>수도권 전철 사이버스테이션</p></div>', unsafe_allow_html=True)
        if st.button("사이버스테이션 연결", key="btn_transit", use_container_width=True):
            go_to("transit")
            st.rerun()

        st.write("")

        st.markdown('<div class="card-yellow"><h2>⭐ 즐겨찾기</h2><p>자주 가는 역 목록</p></div>', unsafe_allow_html=True)
        if st.button("즐겨찾기 목록 열기", key="btn_fav", use_container_width=True):
            go_to("favorites")
            st.rerun()

# 상세 서브 페이지
else:
    if st.button("⬅️ 메인 홈으로 돌아가기"):
        go_to("home")
        st.rerun()

    st.divider()

    if st.session_state.page == "fast_route":
        st.title("📍 빠른 길 찾기")
        
        start_in = st.text_input("출발역 입력", value="성환역")
        end_in = st.text_input("도착역 입력", value="평택역")
        
        if st.button("최단 경로 검색", type="primary"):
            success, result = find_subway_route(start_in, end_in)
            if not success:
                st.error(result)
            else:
                st.success(
                    f"🚃 **{result['start']}** ➡️ **{result['end']}**<br>"
                    f"⏱️ **소요 시간**: 약 **{result['time']}분**<br>"
                    f"🛤️ **추천 경로**: {result['route']}", 
                    icon="✅"
                )

    elif st.session_state.page == "transit":
        st.title("🚌 수도권 전철 사이버스테이션")
        st.write("공식 지하철 노선도 사이트로 연결됩니다.")
        st.link_button("🌐 서울교통공사 사이버스테이션 접속하기", "http://www.seoulmetro.co.kr/kr/cyberStation.do")

    elif st.session_state.page == "recent":
        st.title("🕒 최근 검색 기록")
        for item in st.session_state.recent_searches:
            st.write(f"- 🔍 {item}")

    elif st.session_state.page == "favorites":
        st.title("⭐ 즐겨찾기 장소")
        for fav in st.session_state.favorites:
            st.write(f"- 📌 {fav}")
