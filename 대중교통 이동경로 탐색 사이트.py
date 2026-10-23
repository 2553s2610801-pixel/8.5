import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="대중교통 이동경로 탐색", layout="wide")

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
      <a href="index.html" class="flex items-center space-x-3 text-xl font-bold hover:text-indigo-200 transition">
        <i class="fa-solid fa-bus-simple text-2xl"></i>
        <span>대중교통 탐색</span>
      </a>
      <nav class="flex space-x-1 md:space-x-4 mt-2 sm:mt-0 text-sm md:text-base">
        <a href="index.html" class="px-3 py-2 rounded-lg bg-indigo-700 font-semibold text-white">홈</a>
        <a href="route.html" class="px-3 py-2 rounded-lg hover:bg-indigo-500 transition">최적 경로 찾기</a>
        <a href="subway-congestion.html" class="px-3 py-2 rounded-lg hover:bg-indigo-500 transition">지하철 혼잡도</a>
        <a href="bus-congestion.html" class="px-3 py-2 rounded-lg hover:bg-indigo-500 transition">버스 혼잡도</a>
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
          <span>상단 메뉴 및 아래의 기능 카드를 눌러 원하시는 페이지로 편리하게 이동하실 수 있습니다.</span>
        </li>
        <li class="flex items-start gap-2">
          <i class="fa-solid fa-check text-emerald-500 mt-1"></i>
          <span><strong>최적 경로 찾기:</strong> 출발지와 도착지를 입력하여 버스 및 지하철의 환승 최적 경로를 조회합니다.</span>
        </li>
        <li class="flex items-start gap-2">
          <i class="fa-solid fa-check text-emerald-500 mt-1"></i>
          <span><strong>지하철 & 버스 혼잡도:</strong> 실시간 통계 데이터를 기반으로 각 칸 및 노선의 혼잡 상태를 미리 파악할 수 있습니다.</span>
        </li>
      </ul>
    </section>

    <!-- 원하시는 기능을 선택하세요 -->
    <section>
      <div class="text-center mb-8">
        <h2 class="text-2xl md:text-3xl font-bold text-slate-900">원하시는 기능을 선택하세요</h2>
        <p class="text-slate-500 mt-1">버튼을 클릭하면 해당 페이지로 바로 이동합니다.</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">

        <!-- 기능 카드 1: 최적 경로 찾기 -->
        <a href="route.html" class="group bg-white rounded-2xl p-6 shadow-sm border border-slate-200 hover:shadow-xl hover:border-indigo-400 transition-all duration-300 flex flex-col justify-between">
          <div>
            <div class="w-14 h-14 bg-indigo-50 text-indigo-600 rounded-2xl flex items-center justify-center text-2xl mb-4 group-hover:scale-110 transition-transform">
              <i class="fa-solid fa-route"></i>
            </div>
            <h3 class="text-xl font-bold text-slate-900 mb-2 group-hover:text-indigo-600 transition">
              최적 경로 찾기
            </h3>
            <p class="text-slate-500 text-sm leading-relaxed mb-6">
              출발지와 도착지를 검색하여 최소 시간, 최소 환승 대중교통 이동 경로를 빠르게 찾아드립니다.
            </p>
          </div>
          <div class="flex items-center font-semibold text-indigo-600 text-sm group-hover:translate-x-1 transition-transform">
            <span>페이지로 이동</span>
            <i class="fa-solid fa-arrow-right ml-2 text-xs"></i>
          </div>
        </a>

        <!-- 기능 카드 2: 지하철 혼잡도 확인 -->
        <a href="subway-congestion.html" class="group bg-white rounded-2xl p-6 shadow-sm border border-slate-200 hover:shadow-xl hover:border-indigo-400 transition-all duration-300 flex flex-col justify-between">
          <div>
            <div class="w-14 h-14 bg-blue-50 text-blue-600 rounded-2xl flex items-center justify-center text-2xl mb-4 group-hover:scale-110 transition-transform">
              <i class="fa-solid fa-train-subway"></i>
            </div>
            <h3 class="text-xl font-bold text-slate-900 mb-2 group-hover:text-indigo-600 transition">
              지하철 혼잡도 확인
            </h3>
            <p class="text-slate-500 text-sm leading-relaxed mb-6">
              호선별, 지하철 칸별 실시간 및 시간대별 여유/혼잡 상태를 사전에 확인하여 쾌적하게 이동해보세요.
            </p>
          </div>
          <div class="flex items-center font-semibold text-blue-600 text-sm group-hover:translate-x-1 transition-transform">
            <span>페이지로 이동</span>
            <i class="fa-solid fa-arrow-right ml-2 text-xs"></i>
          </div>
        </a>

        <!-- 기능 카드 3: 버스 혼잡도 표시 -->
        <a href="bus-congestion.html" class="group bg-white rounded-2xl p-6 shadow-sm border border-slate-200 hover:shadow-xl hover:border-indigo-400 transition-all duration-300 flex flex-col justify-between">
          <div>
            <div class="w-14 h-14 bg-emerald-50 text-emerald-600 rounded-2xl flex items-center justify-center text-2xl mb-4 group-hover:scale-110 transition-transform">
              <i class="fa-solid fa-bus"></i>
            </div>
            <h3 class="text-xl font-bold text-slate-900 mb-2 group-hover:text-indigo-600 transition">
              버스 혼잡도 표시
            </h3>
            <p class="text-slate-500 text-sm leading-relaxed mb-6">
              노선별 버스의 현재 좌석 여유 상태(여유/보통/혼잡) 및 도착 예정 정보를 실시간으로 확인합니다.
            </p>
          </div>
          <div class="flex items-center font-semibold text-emerald-600 text-sm group-hover:translate-x-1 transition-transform">
            <span>페이지로 이동</span>
            <i class="fa-solid fa-arrow-right ml-2 text-xs"></i>
          </div>
        </a>

      </div>
    </section>

  </main>

  <!-- 푸터 -->
  <footer class="bg-slate-900 text-slate-400 py-8 border-t border-slate-800 mt-auto">
    <div class="max-w-6xl mx-auto px-4 text-center text-sm space-y-2">
      <p class="font-medium text-slate-300">대중교통 이동경로 탐색 서비스</p>
      <p>© 2026 Public Transport Route Finder. All rights reserved.</p>
    </div>
  </footer>

</body>
</html>
"""

components.html(html_code, height=900, scrolling=True)
