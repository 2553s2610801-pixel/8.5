import streamlit as st
import streamlit.components.v1 as components
from google import genai

st.set_page_config(page_title="대중교통 이동경로 탐색", layout="wide")

# 사이드바: API Key 입력 (AI 작동용)
st.sidebar.title("🤖 AI 설정")
api_key = st.sidebar.text_input("Gemini API Key 입력", type="password")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 원본 HTML/CSS 디자인 그대로 유지 (버튼 이동 기능만 제거)
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
      <a href="#" class="flex items-center space-x-3 text-xl font-bold hover:text-indigo-200 transition">
        <i class="fa-solid fa-bus-simple text-2xl"></i>
        <span>대중교통 탐색</span>
      </a>
      <nav class="flex space-x-1 md:space-x-4 mt-2 sm:mt-0 text-sm md:text-base">
        <a href="#" class="px-3 py-2 rounded-lg bg-indigo-700 font-semibold text-white">홈</a>
        <a href="#" class="px-3 py-2 rounded-lg hover:bg-indigo-500 transition cursor-default">최적 경로 찾기</a>
        <a href="#" class="px-3 py-2 rounded-lg hover:bg-indigo-500 transition cursor-default">지하철 혼잡도</a>
        <a href="#" class="px-3 py-2 rounded-lg
