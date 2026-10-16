import streamlit as st

st.set_page_config(page_title="지하철 혼잡도", page_icon="🚇")

# CSS 전체가 반드시 st.markdown(""" ... """, unsafe_allow_html=True) 안에 있어야 합니다.
st.markdown("""
    <style>
    .main {
        min-height: 100vh;
    }
    .stApp {
        background-color: #f8f9fa;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚇 지하철 혼잡도 안내")
st.write("지하철 실시간 혼잡도 정보를 확인하는 페이지입니다.")
