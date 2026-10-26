import streamlit as st
import streamlit.components.v1 as components

# 페이지 기본 설정
st.set_page_config(page_title="대중교통 이동경로 탐색", layout="wide")

# ==========================================
# 사이드바: Gemini API Key 입력 (선택)
# ==========================================
st.sidebar.title("🤖 AI 문의 설정")
api_key = st.sidebar.text_input("Gemini API Key (선택)", type="password", help="API 키를 넣으면 AI 대답 기능이 활성화됩니다.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ==========================================
# 원본 HTML 레이아웃 (버튼 이동 기능만 제거)
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
      <nav class="flex space-x-1 md:space-x-4 mt-2 sm:mt-0 text-sm md:text-base">
        <span class="px-3 py-2 rounded-lg bg-indigo-700 font-semibold text-white">홈</span>
        <span class="px-3 py-2 rounded-lg text-indigo-200">최적 경로 찾기</span>
        <span class="px-3 py-2 rounded-lg text-indigo-200">지하철 혼잡도</span>
        <span class="px-3 py-2 rounded-lg text-indigo-200">버스 혼잡도</span>
      </nav>
    </div>
  </header>

  <!-- 메인 히어로 섹션 -->
  <section class="bg-gradient-to-r from-indigo-600 to-purple-600 text-white py-16 px-4">
    <div class="max-w-4xl mx-auto text-center space-y-4">
      <h1 class="text-3xl md:text-5xl font-extrabold tracking-tight">
        빠르고 편리한 대중교통 이동경로 탐색
      </h1>
      <p class="text-indigo-100 text-base md:text-lg max-w-2xl mx-auto">
        실시간 이동 경로 검색부터 지하철 및 버스의 혼잡도 정보까지 한눈에 확인하고 가장 스마트한 출퇴근길을 찾아보세요!
      </p>
    </div>
  </section>

  <main class="max-w-6xl mx-auto px-4 py-12 flex-grow space-y-12">

    <!-- 이용 안내사항 카드 -->
    <section class="bg-white rounded-2xl p-6 md:p-8 shadow-sm border border-slate-200">
      <h2 class="text-xl font-bold text-slate-900 mb-4 flex items-center gap-2">
        <i class="fa-solid fa-bullhorn text-indigo-600"></i>
        이용 안내사항
      </h2>
      <ul class="space-y-3 text-slate-600 text-sm md:text-base">
        <li class="flex items-start gap-2">
          <i class="fa-solid fa-check text-emerald-500 mt-1"></i>
          <span>본 사이트는 대중교통 안내 및 이동경로 관련 주요 정보를 종합 제공합니다.</span>
        </li>
