
import streamlit as st
import random
from datetime import datetime

st.set_page_config(
    page_title="버스 도로 혼잡도 표시",
    page_icon="🚌",
    layout="wide"
)

st.title("🚌 버스 도로 혼잡도 표시")
st.write("버스 노선의 도로 혼잡도를 확인하고 예상 지연 시간을 알려주는 웹사이트입니다.")

st.divider()

# 버스 노선 데이터
routes = {
    "천안 1번 버스": [
        "천안터미널 → 종합운동장",
        "종합운동장 → 두정역",
        "두정역 → 천안역",
        "천안역 → 천안터미널"
    ],
    "서울 143번 버스": [
        "정릉 → 성신여대입구",
        "성신여대입구 → 종로",
        "종로 → 명동",
        "명동 → 고속터미널"
    ],
    "부산 1003번 버스": [
        "기장 → 송정",
        "송정 → 해운대",
        "해운대 → 광안리",
        "광안리 → 부산역"
    ]
}

# 노선 선택
selected_route = st.selectbox(
    "버스 노선을 선택하세요.",
    list(routes.keys())
)

# 새로고침 버튼
if st.button("🔄 교통정보 새로고침"):
    st.session_state.pop("traffic_data", None)

# 가상 교통정보 생성
if (
    "traffic_data" not in st.session_state
    or st.session_state.get("selected_route") != selected_route
):
    traffic_data = []

    for road in routes[selected_route]:
        cars = random.randint(8, 95)
        congestion = int(cars / 95 * 100)

        if congestion >= 70:
            level = "심한 정체"
            color = "red"
            delay = random.randint(5, 12)

        elif congestion >= 40:
            level = "약간 정체"
            color = "orange"
            delay = random.randint(2, 5)

        else:
            level = "원활"
            color = "green"
            delay = random.randint(0, 2)

        traffic_data.append({
            "road": road,
            "cars": cars,
            "congestion": congestion,
            "level": level,
            "color": color,
            "delay": delay
        })

    st.session_state.traffic_data = traffic_data
    st.session_state.selected_route = selected_route

traffic_data = st.session_state.traffic_data

# 전체 혼잡도 계산
average = sum(
    x["congestion"] for x in traffic_data
) // len(traffic_data)

total_delay = sum(
    x["delay"] for x in traffic_data
)

normal_time = len(traffic_data) * 10
estimated_time = normal_time + total_delay

st.subheader("📊 전체 교통 상황")

col1, col2, col3 = st.columns(3)

col1.metric("평균 혼잡도", f"{average}%")
col2.metric("예상 지연 시간", f"{total_delay}분")
col3.metric("예상 소요 시간", f"{estimated_time}분")

if average >= 70:
    st.error("현재 노선은 교통 정체가 심합니다.")

elif average >= 40:
    st.warning("현재 일부 구간에서 교통 정체가 발생하고 있습니다.")

else:
    st.success("현재 교통 상황은 대체로 원활합니다.")

st.divider()

# 혼잡도 안내
st.subheader("🚦 혼잡도 색상 안내")

col1, col2, col3 = st.columns(3)

col1.markdown("🔴 **빨간색: 심한 정체**")
col2.markdown("🟡 **노란색: 약간 정체**")
col3.markdown("🟢 **초록색: 원활**")

st.divider()

# 구간별 혼잡도 표시
st.subheader("🛣️ 구간별 도로 혼잡도")

for i, data in enumerate(traffic_data, 1):

    with st.container(border=True):

        st.write(f"**구간 {i}. {data['road']}**")

        st.progress(data["congestion"] / 100)

        if data["color"] == "red":
            st.error(
                f"🔴 심한 정체 | 혼잡도 {data['congestion']}%"
            )

        elif data["color"] == "orange":
            st.warning(
                f"🟡 약간 정체 | 혼잡도 {data['congestion']}%"
            )

        else:
            st.success(
                f"🟢 원활 | 혼잡도 {data['congestion']}%"
            )

        col1, col2 = st.columns(2)

        col1.metric("가상 차량 수", f"{data['cars']}대")
        col2.metric("예상 지연 시간", f"{data['delay']}분")

st.divider()

# 버스 도착 시간 예측
st.subheader("🚌 버스 도착 시간 예측")

st.write(f"기본 예상 소요 시간: {normal_time}분")
st.write(f"교통 정체로 인한 예상 지연: {total_delay}분")

st.info(
    f"교통 상황을 고려한 예상 소요 시간은 약 {estimated_time}분입니다."
)

st.caption(
    "※ 본 프로그램은 학교 프로젝트 시연을 위한 가상 교통정보를 사용합니다. "
    "실제 실시간 교통정보와는 차이가 있을 수 있습니다."
)

st.caption(
    f"마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
)
