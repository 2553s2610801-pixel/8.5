import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="길 찾기 대장",
    page_icon="🗺️",
    layout="centered"
)

# 세션 상태 초기화 (현재 보고 있는 화면 관리)
if "page" not in st.session_state:
    st.session_state.page = "home"
if "recent_searches" not in st.session_state:
    st.session_state.recent_searches = ["강남역", "홍대입구역", "서울역"]
if "favorites" not in st.session_state:
    st.session_state.favorites = ["우리집 (역삼동)", "회사 (판교)", "학교 (신촌)"]

# 커스텀 CSS 적용
st.markdown("""
    <style>
    .header-box {
        background-color: #8FD8FA;
        padding: 20px;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 25px;
    }
    .header-box h1 {
        color: #000000;
        font-size: 36px;
        font-weight: 800;
        margin: 0;
    }
    .card-blue { background-color: #EBF3FF; padding: 20px; border-radius: 12px; text-align: center; }
    .card-green { background-color: #EAF7E8; padding: 20px; border-radius: 12px; text-align: center; }
    .card-purple { background-color: #F2ECFB; padding: 20px; border-radius: 12px; text-align: center; }
    .card-yellow { background-color: #FFF9E5; padding: 20px; border-radius: 12px; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# 페이지 이동 함수
def go_to(page_name):
    st.session_state.page = page_name

# --- 1. 홈 화면 ---
if st.session_state.page == "home":
    st.markdown('<div class="header-box"><h1>길 찾기 대장</h1></div>', unsafe_allow_html=True)

    # 검색창
    search_col1, search_col2 = st.columns([4, 1])
    with search_col1:
        query = st.text_input("검색", placeholder="장소, 주소, 버스, 지하철 검색", label_visibility="collapsed")
    with search_col2:
        if st.button("검색", type="primary", use_container_width=True):
            if query:
                st.session_state.recent_searches.insert(0, query)
                st.success(f"🔍 '{query}' 검색 완료!")

    st.write("")

    # 2x2 카드 버튼 영역
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="card-blue"><h2>📍 빠른 길 찾기</h2><p>최단 시간 경로를 알려드려요</p></div>', unsafe_allow_html=True)
        if st.button("빠른 길 찾기 열기", key="btn_fast", use_container_width=True):
            go_to("fast_route")
            st.rerun()

        st.write("")

        st.markdown('<div class="card-purple"><h2>🕒 최근 검색</h2><p>이전에 찾은 경로를 다시 확인해요</p></div>', unsafe_allow_html=True)
        if st.button("최근 검색 기록 보기", key="btn_recent", use_container_width=True):
            go_to("recent")
            st.rerun()

    with col2:
        st.markdown('<div class="card-green"><h2>🚌 대중교통</h2><p>지하철, 버스 경로를 확인해보세요</p></div>', unsafe_allow_html=True)
        if st.button("대중교통 안내 열기", key="btn_transit", use_container_width=True):
            go_to("transit")
            st.rerun()

        st.write("")

        st.markdown('<div class="card-yellow"><h2>⭐ 즐겨찾기</h2><p>자주 가는 장소를 저장해보세요</p></div>', unsafe_allow_html=True)
        if st.button("즐겨찾기 목록 보기", key="btn_fav", use_container_width=True):
            go_to("favorites")
            st.rerun()

# --- 2. 상세 페이지들 ---
else:
    if st.button("⬅️ 메인 홈으로 돌아가기"):
        go_to("home")
        st.rerun()

    st.divider()

    if st.session_state.page == "fast_route":
        st.title("📍 빠른 길 찾기")
        start = st.text_input("출발지 입력", value="서울역")
        end = st.text_input("도착지 입력", value="강남역")
        if st.button("최적 경로 검색", type="primary"):
            st.success(f"<b>{start}</b> ➡️ <b>{end}</b> 최단 경로: 약 28분 소요 (지하철 2호선 이용)", icon="🚗")

    elif st.session_state.page == "transit":
        st.title("🚌 대중교통 & 🚇 지하철 혼잡도")
        st.subheader("실시간 지하철 혼잡도")
        line = st.selectbox("노선 선택", ["1호선", "2호선", "3호선", "4호선", "9호선"])
        station = st.text_input("역 이름 입력", value="강남역")
        st.info(f"💡 {line} **{station}** 현재 혼잡도: **보통 (65%)**")

    elif st.session_state.page == "recent":
        st.title("🕒 최근 검색 기록")
        for item in st.session_state.recent_searches:
            st.write(f"- 🔍 {item}")

    elif st.session_state.page == "favorites":
        st.title("⭐ 즐겨찾기 장소")
        for fav in st.session_state.favorites:
            st.write(f"- 📌 {fav}")
