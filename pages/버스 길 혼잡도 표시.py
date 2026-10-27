
import streamlit as st
import requests
import pandas as pd
import folium
import xml.etree.ElementTree as ET

from streamlit_folium import st_folium

st.set_page_config(
    page_title="전국 버스 도로 혼잡도",
    page_icon="🚌",
    layout="wide",
)

ITS_URL = "https://openapi.its.go.kr/trafficInfo"

REGIONS = {
    "전국": (124.5, 131.9, 33.0, 38.7),
    "서울": (126.7, 127.2, 37.4, 37.7),
    "부산": (128.8, 129.3, 34.9, 35.3),
    "대구": (128.4, 128.8, 35.7, 36.0),
    "인천": (126.4, 126.8, 37.3, 37.6),
    "광주": (126.7, 127.0, 35.0, 35.3),
    "대전": (127.3, 127.5, 36.2, 36.5),
    "울산": (129.1, 129.5, 35.4, 35.7),
    "세종": (127.1, 127.4, 36.4, 36.7),
    "경기": (126.4, 127.8, 36.9, 38.1),
    "강원": (127.0, 129.4, 37.0, 38.6),
    "충북": (127.3, 128.2, 36.4, 37.3),
    "충남": (125.9, 127.4, 35.9, 37.1),
    "전북": (126.4, 127.6, 35.3, 36.2),
    "전남": (125.0, 127.8, 34.0, 35.3),
    "경북": (128.0, 129.6, 35.5, 37.2),
    "경남": (127.5, 129.3, 34.7, 35.9),
    "제주": (126.1, 126.9, 33.1, 33.6),
}


def get_api_key():
    try:
        return str(st.secrets.get("ITS_API_KEY", "")).strip()
    except Exception:
        return ""


def fetch_traffic(api_key, region):
    min_x, max_x, min_y, max_y = REGIONS[region]

    params = {
        "apiKey": api_key,
        "type": "all",
        "minX": min_x,
        "maxX": max_x,
        "minY": min_y,
        "maxY": max_y,
        "getType": "xml",
    }

    response = requests.get(
        ITS_URL,
        params=params,
        timeout=25,
    )
    response.raise_for_status()

    root = ET.fromstring(response.content)

    result_code = root.findtext(".//header/resultCode")
    result_msg = root.findtext(".//header/resultMsg")

    if result_code not in (None, "0"):
        raise ValueError(
            f"ITS API 오류: {result_msg or result_code}"
        )

    rows = []

    for item in root.findall(".//item"):
        road = item.findtext("roadName", default="").strip()
        link_id = item.findtext("linkId", default="").strip()
        speed_text = item.findtext("speed", default="").strip()

        try:
            speed = float(speed_text)
        except (ValueError, TypeError):
            continue

        if speed < 0:
            continue

        if speed <= 20:
            status = "정체"
            color = "red"
        elif speed <= 40:
            status = "서행"
            color = "orange"
        else:
            status = "원활"
            color = "green"

        rows.append({
            "도로명": road or "이름 미제공",
            "링크 ID": link_id,
            "현재 속도(km/h)": speed,
            "상태": status,
            "색상": color,
            "수집 시각": item.findtext(
                "createdDate", default=""
            ),
        })

    return pd.DataFrame(rows)


def read_route(file):
    """사용자가 제공한 노선 CSV를 검증한다."""
    df = pd.read_csv(file)

    required = {
        "stop_order",
        "stop_name",
        "latitude",
        "longitude",
        "road_name",
    }

    missing = required - set(df.columns)

    if missing:
        raise ValueError(
            "CSV에 필요한 열이 없습니다: "
            + ", ".join(sorted(missing))
        )

    df = df.copy()

    for col in ["latitude", "longitude", "stop_order"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(
        subset=["latitude", "longitude", "stop_order"]
    )

    if len(df) < 2:
        raise ValueError(
            "좌표가 유효한 정류장이 최소 2개 필요합니다."
        )

    if not df["latitude"].between(33, 39).all():
        raise ValueError("위도 범위가 올바르지 않습니다.")

    if not df["longitude"].between(124, 132).all():
        raise ValueError("경도 범위가 올바르지 않습니다.")

    df["road_name"] = df["road_name"].fillna("").astype(str)
    df["stop_name"] = df["stop_name"].fillna("정류장").astype(str)

    return df.sort_values("stop_order").reset_index(drop=True)


def match_traffic(road_name, traffic):
    """도로명으로 교통정보를 연결한다."""
    if not road_name or traffic.empty:
        return None

    matched = traffic[
        traffic["도로명"].str.strip() == road_name.strip()
    ]

    if matched.empty:
        return None

    # 같은 도로명이 여러 번 있으면 평균 속도를 사용한다.
    return float(matched["현재 속도(km/h)"].mean())


def speed_color(speed):
    if speed is None:
        return "blue"
    if speed <= 20:
        return "red"
    if speed <= 40:
        return "orange"
    return "green"


st.title("🚌 전국 버스 도로 혼잡도")
st.write(
    "실시간 도로 소통정보를 확인하고, "
    "좌표가 있는 버스 노선을 지도에 표시합니다."
)

with st.sidebar:
    st.header("조회 설정")
    region = st.selectbox("지역", list(REGIONS.keys()), index=1)

    api_key = get_api_key()

    if not api_key:
        api_key = st.text_input(
            "ITS API 키",
            type="password",
        )

    st.caption(
        "전국 범위 조회는 데이터 양과 API 이용 한도에 "
        "영향을 받을 수 있습니다."
    )

st.subheader("1. 실시간 도로 소통정보")

if not api_key:
    st.info(
        "ITS API 키를 입력하거나 Streamlit Secrets에 "
        "ITS_API_KEY를 등록하세요."
    )
    traffic = pd.DataFrame()
else:
    if st.button("🔄 교통정보 새로 조회", type="primary"):
        st.cache_data.clear()

    try:
        with st.spinner("교통정보를 조회하고 있습니다..."):
            traffic = fetch_traffic(api_key, region)

        if traffic.empty:
            st.warning(
                "교통정보가 없습니다. API 승인, 요청 지역 및 "
                "응답 데이터를 확인하세요."
            )
        else:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("도로 구간", f"{len(traffic):,}")

            c2.metric(
                "🔴 정체",
                int((traffic["현재 속도(km/h)"] <= 20).sum()),
            )
            c3.metric(
                "🟡 서행",
                int(
                    (
                        (traffic["현재 속도(km/h)"] > 20)
                        & (traffic["현재 속도(km/h)"] <= 40)
                    ).sum()
                ),
            )
            c4.metric(
                "🟢 원활",
                int((traffic["현재 속도(km/h)"] > 40).sum()),
            )

            st.dataframe(
                traffic[
                    [
                        "도로명",
                        "링크 ID",
                        "현재 속도(km/h)",
                        "상태",
                        "수집 시각",
                    ]
                ],
                use_container_width=True,
                hide_index=True,
            )

    except requests.RequestException as e:
        st.error(f"교통정보 연결 오류: {e}")
        traffic = pd.DataFrame()
    except ET.ParseError:
        st.error("교통정보 응답을 해석할 수 없습니다.")
        traffic = pd.DataFrame()
    except ValueError as e:
        st.error(str(e))
        traffic = pd.DataFrame()
    except Exception as e:
        st.error(f"예상하지 못한 오류: {e}")
        traffic = pd.DataFrame()

st.divider()
st.subheader("2. 버스 노선 지도")

st.write(
    "노선 좌표 CSV를 올려 주세요. "
    "정류장 좌표와 해당 구간 도로명을 이용해 지도에 표시합니다."
)

st.download_button(
    "노선 CSV 양식 다운로드",
    data=(
        "stop_order,stop_name,latitude,longitude,road_name\n"
        "1,정류장 A,36.8151,127.1139,도로명 입력\n"
        "2,정류장 B,36.8200,127.1200,도로명 입력\n"
    ).encode("utf-8-sig"),
    file_name="bus_route_template.csv",
    mime="text/csv",
)

uploaded = st.file_uploader(
    "버스 노선 CSV 업로드",
    type=["csv"],
)

route = None

if uploaded is not None:
    try:
        route = read_route(uploaded)
    except Exception as e:
        st.error(f"노선 파일을 읽을 수 없습니다: {e}")

if route is not None:
    center_lat = route["latitude"].mean()
    center_lon = route["longitude"].mean()

    map_view = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=13,
        control_scale=True,
    )

    # 정류장 좌표를 이용해 노선을 연결한다.
    # 도로 좌표가 아니라 정류장 사이 직선이므로,
    # 실제 도로 경로와 다를 수 있다.
    for i in range(len(route) - 1):
        current = route.iloc[i]
        next_stop = route.iloc[i + 1]

        road_name = str(current["road_name"]).strip()
        speed = match_traffic(road_name, traffic)
        color = speed_color(speed)

        if speed is None:
            label = "실시간 속도 미연결"
        else:
            label = f"현재 속도: {speed:.1f} km/h"

        folium.PolyLine(
            locations=[
                [current["latitude"], current["longitude"]],
                [next_stop["latitude"], next_stop["longitude"]],
            ],
            color=color,
            weight=6,
            opacity=0.85,
            tooltip=(
                f"{road_name or '도로명 미입력'} | {label}"
            ),
        ).add_to(map_view)

    for _, stop in route.iterrows():
        folium.CircleMarker(
            location=[stop["latitude"], stop["longitude"]],
            radius=5,
            color="blue",
            fill=True,
            fill_opacity=0.9,
            tooltip=f"{stop['stop_order']}. {stop['stop_name']}",
            popup=(
                f"정류장: {stop['stop_name']}<br>"
                f"도로명: {stop['road_name']}"
            ),
        ).add_to(map_view)

    st_folium(
        map_view,
        use_container_width=True,
        height=550,
        key="bus_route_map",
    )

    st.caption(
        "빨강: 속도 20km/h 이하 · "
        "노랑: 20 초과~40km/h 이하 · "
        "초록: 40km/h 초과 · "
        "파랑: 교통정보 연결 안 됨. "
        "정류장 사이 선은 직선이며 실제 도로 형상은 아닙니다."
    )

    st.subheader("3. 지연 시간 참고")

    normal_minutes = st.number_input(
        "평소 노선 소요 시간(분)",
        min_value=1,
        max_value=600,
        value=30,
    )

    normal_speed = st.number_input(
        "평소 도로 속도(km/h)",
        min_value=1.0,
        max_value=120.0,
        value=40.0,
    )

    matched_speeds = []

    for _, stop in route.iloc[:-1].iterrows():
        speed = match_traffic(str(stop["road_name"]), traffic)
        if speed is not None:
            matched_speeds.append(speed)

    if matched_speeds:
        current_speed = sum(matched_speeds) / len(matched_speeds)

        estimated = normal_minutes * normal_speed / max(
            current_speed, 1
        )
        delay = max(0, estimated - normal_minutes)

        a, b = st.columns(2)
        a.metric("단순 예상 소요 시간", f"{estimated:.1f}분")
        b.metric("예상 추가 지연", f"{delay:.1f}분")

        st.caption(
            "참고용 추정치입니다. 버스 위치, 정류장 정차, "
            "신호, 버스전용차로와 실제 경로를 반영하지 않으며 "
            "공식 도착예정시간이 아닙니다."
        )
    else:
        st.info(
            "노선의 도로명과 실시간 교통정보가 연결되지 않아 "
            "지연 시간을 계산할 수 없습니다."
        )
else:
    st.info(
        "노선 CSV를 업로드하면 정류장 지도와 혼잡도 표시가 나타납니다. "
        "실제 노선 자동 검색은 별도의 버스 노선 API 연결이 필요합니다."
    )
