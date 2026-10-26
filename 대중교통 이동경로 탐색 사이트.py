import streamlit as st
import streamlit.components.v1 as components
from google import genai

# 1. 페이지 기본 설정
st.set_page_config(page_title="대중교통 이동경로 탐색", layout="wide")

# 2. 사이드바: 메뉴 선택 & API Key 입력
st.sidebar.title("📌 대중교통 탐색 메뉴")
menu = st.sidebar.radio(
    "이동할 페이지를 선택하세요:",
    ["🏠 홈 (메인)", "🗺️ 최적 경로 찾기", "🚇 지하철 혼잡도", "🚌 버스 혼잡도"]
)

st.sidebar.divider()
st.sidebar.title("🤖 AI 도우미 설정")
api_key = st.sidebar.text_input("Gemini API Key 입력", type="password")

# AI 대화 기록 초기화
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ==========================================
# 3. 페이지별 HTML 정의 (팀원들 코드 합치기)
# ==========================================

# [내 담당] 메인 페이지 HTML (클릭 이동 효과 없음, 종류 나열만)
home_html = """
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />
  <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    body { font-family: 'Pretendard', sans-serif; }
  </style>
</head>
<body class="bg-slate-50 text-slate-800 p-6">

  <!-- 메인 히어로 -->
  <div class="bg-gradient-to-r from-indigo-600 to-purple-600 text-white p-10 rounded-2xl text-center mb-8">
    <h1 class="text-3xl font-extrabold mb-2">빠르고 편리한 대중교통 이동경로 탐색</h1>
    <p class="text-indigo-100">왼쪽 사이드바 메뉴를 사용해 각 서비스로 이동하거나, 하단 Gemini AI에게 물어보세요!</p>
  </div>

  <!-- 서비스 종류 나열 (버튼 효과 없음) -->
  <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
    <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
      <div class="w-12 h-12 bg-indigo-50 text-indigo-600 rounded-xl flex items-center justify-center text-xl mb-4">
