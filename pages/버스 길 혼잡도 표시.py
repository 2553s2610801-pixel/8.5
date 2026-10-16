import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="버스 길 혼잡도",
    page_icon="🚌",
    layout="wide",
)

st.title("🚌 버스 길 혼잡도 확인")
st.write("도로 구간별 혼잡 상태를 색깔로 확인하고 버스 지연 가능성을 살펴보세요.")

st.info(
    "현재 버전은 작동 예시를 위한 가상 데이터입니다. "
    "실제 실시간 교통정보나 버스 도착정보를 제공하지는 않습니다."
)

# 예시 데이터: 실제 교통 API에 연결하면 이 부분을 실제 데이터로 바꿀 수 있습니다.
routes = {
    "1번 버스": [
        {"구간": "천안터미널 → 두정역", "상태": "원활", "지연(분)": 0},
        {"구간": "두정역 → 학교 앞", "상태": "서행", "지연(분)": 4},
        {"구간": "학교 앞 → 종점", "상태": "정체", "지연(분)": 9},
    ],
    "2번 버스": [
        {"구간": "천안역 → 시청", "상태": "서행", "지연(분)": 3},
        {"구간": "시청 → 종합운동장", "상태": "원활", "지연(분)": 0},
        {"구간": "종합운동장 → 종점", "상태": "원활", "지연(분)": 1},
    ],
    "3번 버스": [
        {"구간": "학교 앞 → 시장", "상태": "정체", "지연(분)": 8},
        {"구간": "시장 → 천안역", "상태": "정체", "지연(분)": 6},
        {"구간": "천안역 → 터미널", "상태": "서행", "지연(분)": 3},
    ],
}

colors = {
    "원활": "#16a34a",
    "서행": "#eab308",
    "정체": "#dc2626",
}

route_name = st.selectbox("확인할 버스 노선을 선택하세요", list(routes.keys()))
segments = routes[route_name]
df = pd.DataFrame(segments)

st.subheader(f"📍 {route_name} 도로 구간")
legend = st.columns(3)
for col, status, label in zip(
    legend,
    ["원활", "서행", "정체"],
    ["원활 · 초록색", "서행 · 노란색", "정체 · 빨간색"],
):
    col.markdown(
        f"""
        <div style="padding:12px;border-radius:10px;background:{colors[status]};
        color:#111827;text-align:center;font-weight:700;">{label}</div>
        """,
        unsafe_allow_html=True,
    )

st.write("")

for item in segments:
    color = colors[item["상태"]]
    st.markdown(
        f"""
        <div style="border:1px solid #d1d5db;border-left:10px solid {color};
        border-radius:8px;padding:14px;margin-bottom:10px;">
          <div style="font-size:17px;font-weight:700;">{item["구간"]}</div>
          <div style="margin-top:6px;">혼잡 상태: <b>{item["상태"]}</b>
          &nbsp; | &nbsp; 예상 지연: 약 {item["지연(분)"]}분</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

total_delay = sum(item["지연(분)"] for item in segments)
congested_count = sum(item["상태"] == "정체" for item in segments)

left, middle, right = st.columns(3)
left.metric("노선 구간 수", f"{len(segments)}개")
middle.metric("정체 구간", f"{congested_count}개")
right.metric("예상 지연 합계", f"약 {total_delay}분")

st.subheader("📊 구간별 예상 지연 시간")
chart_df = df.set_index("구간")[["지연(분)"]]
st.bar_chart(chart_df)

with st.expander("구간 데이터를 표로 보기"):
    st.dataframe(df, use_container_width=True, hide_index=True)

st.caption(
    "※ 지연 시간은 설명을 위한 예시값입니다. 실제 교통 상황 및 버스 도착 시간과 다를 수 있습니다."
)
