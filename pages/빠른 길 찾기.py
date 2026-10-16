import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="길 찾기 대장",
    page_icon="🗺️",
    layout="centered"
)

# 커스텀 CSS (이미지 속 디자인 스타일링 적용)
st.markdown("""
    <style>
    /* 상단 타이틀 하늘색 박스 */
    .header-box {
        background-color: #8FD8FA;
        padding: 20px;
        border-radius: 4px;
        text-align: center;
        margin-bottom: 25px;
    }
    .header-box h1 {
        color: #000000;
        font-size: 38px;
        font-weight: 800;
        margin: 0;
        letter-spacing: 2px;
    }

    /* 카드 기본 공통 스타일 */
    .card {
        padding: 30px 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        min-height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin-bottom: 20px;
        transition: transform 0.2s ease;
    }
    .card:hover {
        transform: translateY(-2px);
    }
    .card-icon {
        font-size: 48px;
        margin-bottom: 12px;
    }
    .card-title {
        font-size: 20px;
        font-weight: 700;
        color: #111111;
        margin-bottom: 8px;
    }
    .card-desc {
        font-size: 13px;
        color: #666666;
        margin: 0;
        word-break: keep-all;
    }

    /* 카드별 색상 설정 */
    .card-blue { background-color: #EBF3FF; }
    .card-green { background-color: #EAF7E8; }
    .card-purple { background-color: #F2ECFB; }
    .card-yellow { background-color: #FFF9E5; }
    </style>
""", unsafe_allow_html=True)

# 1. 상단 타이틀
st.markdown("""
    <div class="header-box">
        <h1>길 찾기 대장</h1>
    </div>
""", unsafe_allow_html=True)

# 2. 검색창 영역
search_col1, search_col2 = st.columns([5, 1])

with search_col1:
    search_query = st.text_input("검색", placeholder="장소, 주소, 버스, 지하철 검색", label_visibility="collapsed")

with search_col2:
    search_btn = st.button("검색", type="primary", use_container_width=True)

if search_btn and search_query:
    st.info(f"🔍 '{search_query}' 검색 결과 페이지로 이동합니다.")

st.markdown("<br>", unsafe_allow_html=True)

# 3. 2x2 카드 그리드 영역
col1, col2 = st.columns(2)

with col1:
    # 빠른 길 찾기
    st.markdown("""
        <div class="card card-blue">
            <div class="card-icon">📍</div>
            <div class="card-title">빠른 길 찾기</div>
            <div class="card-desc">최단 시간 경로를 알려드려요</div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("빠른 길 찾기 실행", key="btn_fast", use_container_width=True):
        st.write("👉 빠른 길 찾기 기능이 실행되었습니다.")

    st.markdown("<br>", unsafe_allow_html=True)

    # 최근 검색
    st.markdown("""
        <div class="card card-purple">
            <div class="card-icon">🕒</div>
            <div class="card-title">최근 검색</div>
            <div class="card-desc">이전에 찾은 경로를 다시 확인할 수 있어요</div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("최근 검색 기록 보기", key="btn_recent", use_container_width=True):
        st.write("👉 최근 검색 기록 목록입니다.")

with col2:
    # 대중교통
    st.markdown("""
        <div class="card card-green">
            <div class="card-icon">🚌</div>
            <div class="card-title">대중교통</div>
            <div class="card-desc">지하철, 버스 경로를 확인해보세요</div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("대중교통 경로 확인", key="btn_transit", use_container_width=True):
        st.write("👉 대중교통 경로 안내 페이지입니다.")

    st.markdown("<br>", unsafe_allow_html=True)

    # 즐겨찾기
    st.markdown("""
        <div class="card card-yellow">
            <div class="card-icon">⭐</div>
            <div class="card-title">즐겨찾기</div>
            <div class="card-desc">자주 가는 장소를 저장해보세요</div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("즐겨찾기 목록 열기", key="btn_fav", use_container_width=True):
        st.write("👉 저장된 즐겨찾기 장소들입니다.")
