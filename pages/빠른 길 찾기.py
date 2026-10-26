import streamlit as st
import hashlib

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

# 출발지/도착지 입력에 따른 시간 및 경로 계산 함수
def calculate_route_time(start, end):
    if not start or not end:
        return None, None
    if start.strip() == end.strip():
        return 0, "동일한 위치입니다."
    
    # 두 장소 이름을 기반으로 고유한 시간(10분 ~ 75분 사이) 계산
    combined = f"{start.strip()}_{end.strip()}"
    hash_val = int(hashlib.md5(combined.encode('utf-8')).hexdigest(), 16)
    minutes = 10 + (hash_val % 66)
    
    # 소요 시간에 따른 수단 안내
    if minutes < 20:
        transport = "도보 또는 버스 이용"
    elif minutes < 45:
        transport = "지하철 최단 경로 이용"
    else:
        transport = "지하철 환승 + 버스 이용"
        
    return minutes, transport

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

        st.markdown('<div class="card-yellow"><h2>⭐ 즐겨찾기</h2><p>자주 가는 장소를 저장해보세요</p></div>',
