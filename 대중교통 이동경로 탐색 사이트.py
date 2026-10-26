import streamlit as st

# 페이지 기본 설정 (반드시 코드 최상단에 위치해야 에러가 나지 않습니다)
st.set_page_config(
    page_title="대중교통 이동경로 탐색 - 홈",
    page_icon="🚇",
    layout="wide",
)

# 커스텀 CSS 스타일링
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.3rem;
        font-weight: 700;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 5px;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4B5563;
        text-align: center;
        margin-bottom: 25px;
    }
    .feature-card {
        background-color: #F8FAFC;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #3B82F6;
        margin-bottom: 15px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 메인 헤더
st.markdown(
    '<div class="main-header">🚇 스마트 대중교통 이동경로 탐색 플랫폼</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-header">가장 빠르고 쾌적한 이동을 위한 통합 대중교통 안내 서비스입니다.</div>',
    unsafe_allow_html=True,
)

st.divider()

# 서비스 소개 섹션 (팀원들이 담당한 기능 소개)
st.subheader("✨ 주요 기능 안내")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🚀 빠른 길찾기")
    st.markdown(
        """
        <div class="feature-card">
        출발지와 목적지를 입력하면 최적의 대중교통 경로와 예상 소요 시간을 실시간으로 안내합니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
