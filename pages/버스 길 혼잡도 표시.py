
import random
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="버스길 혼잡도",
    page_icon="🚌",
    layout="wide",
)

# 가상의 도로 데이터
ROAD_DATA = {
    "서울": [
        ("강남대로", 3.2),
        ("테헤란로", 2.8),
        ("올림픽대로", 5.5),
        ("세종대로", 2.4),
        ("송파대로", 3.1),
        ("영동대로", 2.6),
    ],
    "부산": [
        ("중앙대로", 4.2),
        ("해운대로", 3.5),
        ("수영로", 2.7),
        ("가야대로", 3.8),
        ("충렬대로", 3.1),
    ],
    "대전": [
        ("대덕대로", 3.4),
        ("계룡로", 3.0),
        ("한밭대로", 4.1),
        ("중앙로", 2.2),
    ],
    "인천": [
        ("경인로", 4.3),
        ("인주대로", 3.6),
        ("송도바이오대로", 3.2),
        ("아암대로", 4.0),
    ],
    "대구": [
        ("달구벌대로", 4.5),
        ("동대구로", 3.2),
        ("신천대로", 4.0),
        ("중앙대로", 2.5),
    ],
    "광주": [
        ("무진대로", 3.8),
        ("상무대로", 3.4),
        ("북문대로", 2.9),
    ],
    "울산": [
        ("삼산로", 2.8),
        ("산업로", 5.2),
        ("문수로", 3.6),
    ],
    "세종": [
        ("한누리대로", 4.0),
        ("도움3로", 2.5),
        ("절재로", 2.8),
    ],
    "제주": [
        ("연삼로", 4.2),
        ("노연로", 2.7),
        ("중앙로", 3.0),
    ],
}

COLORS = {
    "원활": "#16A34A",
    "서행": "#EAB308",
    "정체": "#DC2626",
}

EMOJIS = {
    "원활": "🟢",
    "서행": "🟡",
    "정체": "🔴",
}


def make_traffic(region, seed):
    """가상 도로 속도와 혼잡도 생성."""
    rng = random.Random(seed)
    rows = []

    for road, distance in ROAD_DATA[region]:
        speed = rng.randint(8, 65)

        if speed >= 40:
            status = "원활"
        elif speed >= 20:
            status = "서행"
        else:
            status = "정체"

        # 가상의 일반적인 주행 속도와 현재 속도의 차이를 이용한
        # 참고용 지연 시간 계산
        normal_speed = 40
        normal_minutes = distance / normal_speed * 60
        current_minutes = distance / speed * 60
        delay = max(0, round(current_minutes - normal_minutes))

        rows.append({
            "도로명": road,
            "거리(km)": distance,
            "속도(km/h)": speed,
            "혼잡도": status,
            "예상 지연(분)": delay,
        })

    return pd.DataFrame(rows)


st.title("🚌 버스길 혼잡도")
st.caption("가상 교통정보로 확인하는 도로 혼잡도 시뮬레이터")

st.warning(
    "⚠️ 시뮬레이션 모드입니다. 화면에 표시되는 도로 속도와 "
    "예상 지연 시간은 모두 가상 데이터이며 실제 교통 상황이 아닙니다."
)

with st.sidebar:
    st.header("교통 상황 설정")

    region = st.selectbox(
        "지역 선택",
        list(ROAD_DATA.keys()),
    )

    st.write("**혼잡도 색상 기준**")
    st.markdown("🟢 원활: 40km/h 이상")
    st.markdown("🟡 서행: 20~39km/h")
    st.markdown("🔴 정체: 20km/h 미만")

    if "seed" not in st.session_state:
        st.session_state.seed = 100

    if st.button("🔄 가상 교통정보 새로고침", use_container_width=True):
        st.session_state.seed += 1

    st.caption("새로고침을 누르면 가상 교통 상황이 바뀝니다.")

df = make_traffic(region, st.session_state.seed)

# 요약 수치
total = len(df)
smooth = int((df["혼잡도"] == "원활").sum())
slow = int((df["혼잡도"] == "서행").sum())
jam = int((df["혼잡도"] == "정체").sum())

st.subheader(f"📍 {region} 도로 상황")

c1, c2, c3, c4 = st.columns(4)
c1.metric("전체 도로", f"{total}개")
c2.metric("🟢 원활", f"{smooth}개")
c3.metric("🟡 서행", f"{slow}개")
c4.metric("🔴 정체", f"{jam}개")

st.markdown("---")
st.subheader("🚦 도로별 혼잡도")

for _, row in df.iterrows():
    status = row["혼잡도"]
    color = COLORS[status]
    emoji = EMOJIS[status]

    st.markdown(
        f"""
        <div style="
            border-left: 8px solid {color};
            border-radius: 10px;
            padding: 14px;
            margin-bottom: 10px;
            background-color: rgba(128,128,128,0.08);
        ">
            <div style="font-size: 19px; font-weight: bold;">
                {emoji} {row['도로명']}
            </div>
            <div style="margin-top: 8px;">
                <span style="color:{color}; font-weight:bold;">
                    {status}
                </span>
                &nbsp; | &nbsp; 속도 {row['속도(km/h)']} km/h
                &nbsp; | &nbsp; 거리 {row['거리(km)']} km
            </div>
            <div style="margin-top: 6px;">
                버스 지연 예상: 약 {row['예상 지연(분)']}분
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")
st.subheader("🚌 버스 지연 위험 분석")

jam_ratio = jam / total if total else 0
slow_ratio = (jam + slow) / total if total else 0

if jam_ratio >= 0.4:
    st.error(
        "정체 위험 높음: 가상 데이터에서 정체 도로 비율이 높습니다. "
        "이 도로들을 지나는 버스는 지연될 가능성이 있습니다."
    )
elif slow_ratio >= 0.4:
    st.warning(
        "주의: 서행 또는 정체 도로가 있습니다. "
        "버스 도착이 늦어질 수 있는 상황을 가정합니다."
    )
else:
    st.success(
        "대체로 원활: 가상 데이터상 도로 흐름이 양호합니다."
    )

average_delay = round(df["예상 지연(분)"].mean(), 1)
st.metric("도로별 예상 지연 평균", f"{average_delay}분")

st.caption(
    "지연 시간은 가상 도로 거리와 속도로 계산한 참고용 값입니다. "
    "실제 버스 도착 시간이나 실제 교통정보를 의미하지 않습니다."
)

with st.expander("📋 가상 교통정보 표 보기"):
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.download_button(
        "가상 데이터 CSV 다운로드",
        data=df.to_csv(index=False).encode("utf-8-sig"),
        file_name=f"{region}_가상교통정보.csv",
        mime="text/csv",
    )
