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
    st.markdown("### 🚇 지하철 혼잡도")
    st.markdown(
        """
        <div class="feature-card">
        실시간 지하철 칸별 혼잡도를 미리 확인하고, 여유로운 칸을 골라 쾌적하게 탑승할 수 있습니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown("### 🚌 버스 혼잡도")
    st.markdown(
        """
        <div class="feature-card">
        탑승하려는 버스의 실시간 잔여 좌석과 차내 혼잡 상태를 한눈에 파악할 수 있습니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

# AI 문의사항 답변 섹션 (오류 없이 안정적으로 동작하는 스마트 응답 챗봇)
st.subheader("💬 AI 서비스 안내 & 문의사항")
st.write(
    "궁금한 점을 아래 채팅창에 입력해 보세요! 실시간으로 답변해 드립니다."
)

# 세션 스테이트 초기화 (채팅 기록 유지)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "안녕하세요! 대중교통 이동경로 탐색 서비스 홈입니다. 빠른 길찾기, 지하철 혼잡도, 버스 혼잡도에 대해 무엇이든 물어보세요!",
        }
    ]

# 이전 대화 내역 화면에 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 받기 및 즉시 응답 처리
if prompt := st.chat_input("질문을 입력해 주세요 (예: 혼잡도는 어디서 보나요?)"):
    # 1. 사용자 메시지 기록 및 출력
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. 스마트 답변 생성 로직 (키워드 분석)
    query = prompt.lower()
    if any(k in query for k in ["길찾기", "경로", "길", "출발", "목적지"]):
        response = (
            "🚀 **빠른 길찾기** 기능은 출발지와 목적지를 입력하시면 가장 최적의"
            " 대중교통 이동 경로와 소요 시간을 안내해 드립니다. 상단 메뉴나 해당"
            " 페이지에서 이용해 보세요!"
        )
    elif any(k in query for k in ["지하철", "열차", "칸", "역"]):
        response = (
            "🚇 **지하철 혼잡도** 기능은 실시간으로 열차 칸별 혼잡 상태를"
            " 제공합니다. 사람이 덜 붐비는 쾌적한 칸을 미리 확인하고 탑승하실"
            " 수 있습니다."
        )
    elif any(k in query for k in ["버스", "좌석", "잔여"]):
        response = (
            "🚌 **버스 혼잡도** 기능은 실시간 버스 위치와 함께 잔여 좌석 및"
            " 혼잡 상황을 알려주어 편리하게 대중교통을 이용할 수 있도록"
            " 도와줍니다."
        )
    elif any(k in query for k in ["안녕", "반가", "hi", "hello"]):
        response = (
            "안녕하세요! 대중교통 이동경로 탐색 서비스에 오신 것을 환영합니다."
            " 무엇을 도와드릴까요? 😊"
        )
    else:
        response = (
            f"'{prompt}'에 대한 안내입니다. 저희 사이트는 **빠른 길찾기,"
            " 지하철 혼잡도, 버스 혼잡도** 서비스를 제공하고 있습니다."
            " 구체적으로 어떤 기능이 궁금하신가요?"
        )

    # 3. 어시스턴트 응답 기록 및 출력
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )
