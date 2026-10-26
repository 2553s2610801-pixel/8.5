import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# 1. Streamlit 페이지 설정
# ==========================================
st.set_page_config(
    page_title="대중교통 이동경로 탐색",
    page_icon="🚌",
    layout="wide"
)

# 사이드바: AI 기능용 API Key 입력
st.sidebar.title("🤖 AI 설정")
st.sidebar.markdown("Gemini API 키를 입력하면 대중교통 AI 도우미가 활성화됩니다.")
api_key = st.sidebar.text_input("Gemini API Key", type="password", help="Google AI Studio에서 발급받은 API 키를 입력하세요.")

# 대화 기록 세션 초기화
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ==========================================
# 2. 메인 페이지 HTML UI (홈 / 안내)
# ==========================================
html_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>대중교통 이동경로 탐색 사이트</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />
  <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    body {
      font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
    }
  </style>
</head>
<body class="bg-slate-50 text-slate-800 min-h-screen flex flex-col">

  <!-- 상단 헤더 / 내비게이션 바 -->
  <header class="bg-indigo-600 text-white shadow-lg sticky top-0 z-50">
    <div class="max-w-6xl mx-auto px-4 py-4 flex flex-wrap justify-between items-center">
      <div class="flex items-center space-x-3 text-xl font-bold">
        <i class="fa-solid fa-bus-simple text-2xl"></i>
        <span>대중교통 이동경로 탐색</span>
      </div>
      <nav class="flex space-x-1 md:space-x-3 mt-2 sm:mt-0 text-sm md:text-base">
        <span class="px-3 py-2 rounded-lg bg-indigo-700 font-semibold text-white">홈</span>
        <span class="px-3 py-2 rounded-lg text-indigo-100">빠른 길 찾기</span>
        <span class="px-3 py-2 rounded-lg text-indigo-100">지하철 혼잡도</span>
        <span class="px-3 py-2 rounded-lg text-indigo-100">버스 혼잡도</span>
      </nav>
    </div>
  </header>

  <!-- 메인 히어로 섹션 -->
  <section class="bg-gradient-to-r from-indigo-600 to-purple-600 text-white py-14 px-4">
    <div class="max-w-4xl mx-auto text-center space-y-4">
      <h1 class="text-3xl md:text-5xl font-extrabold tracking-tight">
        빠르고 편리한 대중교통 이동경로 탐색
      </h1>
      <p class="text-indigo-100 text-base md:text-lg max-w-2xl mx-auto">
        실시간 이동 경로 검색부터 지하철 및 버스의 혼잡도 정보까지 한눈에 확인하고 가장 스마트한 출퇴근길을 찾아보세요!
      </p>
    </div>
  </section>

  <main class="max-w-6xl mx-auto px-4 py-10 flex-grow space-y-10">

    <!-- 서비스 이용 안내 카드 -->
    <section class="bg-white rounded-2xl p-6 md:p-8 shadow-sm border border-slate-200">
      <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2">
        <i class="fa-solid fa-bullhorn text-indigo-600"></i>
        이용 안내사항
      </h2>
      <ul class="space-y-3 text-slate-600 text-sm md:text-base">
        <li class="flex items-start gap-2">
          <i class="fa-solid fa-check text-emerald-500 mt-1"></i>
          <span>본 사이트는 대중교통 경로 검색 및 수단별 혼잡도 정보를 통합하여 제공하는 메인 플랫폼입니다.</span>
        </li>
        <li class="flex items-start gap-2">
          <i class="fa-solid fa-check text-emerald-500 mt-1"></i>
          <span>아래의 기능 안내 카드에서 제공되는 주요 서비스 종류를 파악하실 수 있습니다.</span>
        </li>
        <li class="flex items-start gap-2">
          <i class="fa-solid fa-check text-emerald-500 mt-1"></i>
          <span>궁금한 점이나 대중교통 문의사항은 하단의 <strong>AI 대중교통 문의 도우미</strong>를 이용해보세요!</span>
        </li>
      </ul>
    </section>

    <!-- 사이트 기능 종류 설명 (정적 나열) -->
    <section>
      <div class="text-center mb-8">
        <h2 class="text-2xl md:text-3xl font-bold text-slate-900">제공 기능 안내</h2>
        <p class="text-slate-500 mt-1">사이트에서 취급하는 주요 기능 종류입니다.</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">

        <!-- 기능 1: 빠른 길 찾기 -->
        <div class="bg-white rounded-2xl p-6 shadow-sm border border-slate-200 flex flex-col justify-between">
          <div>
            <div class="w-14 h-14 bg-indigo-50 text-indigo-600 rounded-2xl flex items-center justify-center text-2xl mb-4">
              <i class="fa-solid fa-route"></i>
            </div>
            <h3 class="text-xl font-bold text-slate-900 mb-2">
              빠른 길 찾기
            </h3>
            <p class="text-slate-500 text-sm leading-relaxed">
              출발지와 도착지를 검색하여 최소 시간, 최소 환승 대중교통 이동 경로를 빠르게 확인하는 기능입니다.
            </p>
          </div>
        </div>

        <!-- 기능 2: 지하철 혼잡도 -->
        <div class="bg-white rounded-2xl p-6 shadow-sm border border-slate-200 flex flex-col justify-between">
          <div>
            <div class="w-14 h-14 bg-blue-50 text-blue-600 rounded-2xl flex items-center justify-center text-2xl mb-4">
              <i class="fa-solid fa-train-subway"></i>
            </div>
            <h3 class="text-xl font-bold text-slate-900 mb-2">
              지하철 혼잡도
            </h3>
            <p class="text-slate-500 text-sm leading-relaxed">
              호선별, 지하철 칸별 실시간 및 시간대별 여유/혼잡 상태를 사전에 확인하여 쾌적하게 이동할 수 있습니다.
            </p>
          </div>
        </div>

        <!-- 기능 3: 버스 혼잡도 -->
        <div class="bg-white rounded-2xl p-6 shadow-sm border border-slate-200 flex flex-col justify-between">
          <div>
            <div class="w-14 h-14 bg-emerald-50 text-emerald-600 rounded-2xl flex items-center justify-center text-2xl mb-4">
              <i class="fa-solid fa-bus"></i>
            </div>
            <h3 class="text-xl font-bold text-slate-900 mb-2">
              버스 혼잡도
            </h3>
            <p class="text-slate-500 text-sm leading-relaxed">
              노선별 버스의 현재 좌석 여유 상태(여유/보통/혼잡) 및 도착 예정 정보를 실시간으로 파악합니다.
            </p>
          </div>
        </div>

      </div>
    </section>

  </main>

  <!-- 푸터 -->
  <footer class="bg-slate-900 text-slate-400 py-6 border-t border-slate-800 mt-auto">
    <div class="max-w-6xl mx-auto px-4 text-center text-sm space-y-1">
      <p class="font-medium text-slate-300">대중교통 이동경로 탐색 서비스</p>
      <p>© 2026 Public Transport Route Finder. All rights reserved.</p>
    </div>
  </footer>

</body>
</html>
"""

# HTML 랜딩 페이지 화면에 출력
components.html(html_code, height=850, scrolling=True)


# ==========================================
# 3. Gemini AI 문의사항 응답 챗봇
# ==========================================
st.divider()
st.subheader("💬 AI 대중교통 문의 응답 도우미 (Gemini)")

# 이전 대화 내용 출력
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 처리
if user_prompt := st.chat_input("대중교통 이동경로, 지하철/버스 혼잡도, 환승 방법 등 문의사항을 질문해 보세요!"):
    # 사용자 질문 등록
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # AI 답변 생성
    with st.chat_message("assistant"):
        if not api_key:
            info_msg = "💡 **AI 질문 기능을 사용하시려면 왼쪽 사이드바에 Gemini API Key를 입력해 주세요.**"
            st.warning(info_msg)
            st.session_state.chat_history.append({"role": "assistant", "content": info_msg})
        else:
            try:
                from google import genai
                client = genai.Client(api_key=api_key)
                
                # AI 역할 부여 (대중교통 전용 도우미)
                prompt_with_context = (
                    "당신은 '대중교통 이동경로 탐색 사이트'의 친절한 AI 안내원입니다. "
                    "사용자의 질문에 대해 대중교통 이용 팁, 경로 안내, 혼잡도 관리법 등을 알기 쉽고 정확하게 답변하세요.\n\n"
                    f"사용자 문의: {user_prompt}"
                )
                
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt_with_context
                )
                
                st.markdown(response.text)
                st.session_state.chat_history.append({"role": "assistant", "content": response.text})
            except Exception as e:
                err_msg = f"❌ AI 응답 생성 실패: {str(e)}"
                st.error(err_msg)
                st.session_state.chat_history.append({"role": "assistant", "content": err_msg})
