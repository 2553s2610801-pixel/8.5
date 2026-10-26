import streamlit as st

# 페이지 기본 설정
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
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 10px;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #4B5563;
        text-align: center;
        margin-bottom: 30px;
    }
    .feature-card {
        background-color: #F3F4F6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #3B82F6;
        margin-bottom: 20px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 메인 헤더
st.markdown(
    '<div class="main-header">🚇 스마트 대중교통 길찾기 플랫폼</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-header">가장 빠르고 쾌적한 이동을 위한 통합 대중교통 안내 서비스입니다.</div>',
    unsafe_allow_html=True,
)

st.divider()

# 서비스 소개 섹션 (팀원들이 담당한 기능 소개)
st.subheader("✨ 주요 기능 소개")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🚀 빠른 길찾기")
    st.markdown(
        """
        <div class="feature-card">
        출발지와 목적지를 입력하면 최적의 경로와 소요 시간을 실시간으로 안내합니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown("### 🚇 지하철 혼잡도")
    st.markdown(
        """
        <div class="feature-card">
        실시간 지하철 칸별 혼잡도를 미리 확인하고 쾌적하게 탑승할 수 있습니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown("### 🚌 버스 혼잡도")
    st.markdown(
        """
        <div class="feature-card">
        탑승하려는 버스의 실시간 잔여 좌석과 혼잡 상황을 한눈에 파악합니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

# AI 문의사항 답변 섹션 (API 키 없이 Streamlit 내장 기능으로 작동)
st.subheader("💬 AI 서비스 안내 & 문의사항")
st.write(
    "궁금한 점이 있으신가요? 아래 채팅창에 질문을 남겨주시면 안내해 드립니다!"
)

# 세션 스테이트를 이용한 대화 기록 저장
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "안녕하세요! 대중교통 이동경로 탐색 서비스 홈입니다. 무엇을 도와드릴까요?",
        }
    ]

# 이전 대화 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 받기
if prompt := st.chat_input("질문을 입력하세요 (예: 혼잡도 서비스는 어디서 보나요?)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 간단한 규칙 기반 자동 응답 로직 (API 키 불필요)
    response = ""
    prompt_lower = prompt.lower()

    if "길찾기" in prompt or "경로" in prompt:
        response = (
            "빠른 길찾기 기능은 상단 메뉴 혹은 팀원이 구현한 페이지에서 출발지와"
            " 목적지를 입력하여 이용하실 수 있습니다!"
        )
    elif "지하철" in prompt:
        response = (
            "지하철 혼잡도 페이지에서는 각 열차의 실시간 혼잡도를 색상별로"
            " 확인하여 여유로운 칸을 골라 탈 수 있습니다."
        )
    elif "버스" in prompt:
        ...  # 버스 관련 응답
        response = (
            "버스 혼잡도 기능은 실시간으로 연동되어 잔여 좌석과 혼잡 상태를"
            " 제공합니다."
        )
    else:
        response = (
            f"'{prompt}'에 대한 답변입니다. 저희 플랫폼은 빠른 길찾기, 지하철"
            " 혼잡도, 버스 혼잡도 기능을 제공하고 있습니다. 추가 문의사항은"
            " 관리자에게 연락주세요!"
        )
