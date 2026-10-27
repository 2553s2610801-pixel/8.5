
import streamlit as st
import requests
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime

st.set_page_config(
    page_title="전국 버스 도로 혼잡도",
    page_icon="🚌",
    layout="wide",
)

API_URL = "https://openapi.its.go.kr/trafficInfo"

# 지역별 조회 범위: 경도 최소/최대, 위도 최소/최대
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


def get_secret_key():
    """Streamlit Secrets에서 API 키를 읽는다."""
    try:
        return str(st.secrets.get("ITS_API_KEY", "")).strip()
    except Exception:
        return ""


def parse_traffic_xml(xml_text):
    """XML 응답에서 도로 소통정보를 추출한다."""
    root = ET.fromstring(xml_text)

    result_code = root.findtext(".//header/resultCode")
    result_msg = root.findtext(".//header/resultMsg")

    # 오류 응답도 정상 데이터로 오인하지 않도록 확인한다.
    if result_code not in (None, "0"):
        raise ValueError(
            f"교통 API 응답 오류: {result_msg or result_code}"
        )

    rows = []

    for item in root.findall(".//item"):
        def get_text(*names):
            for name in names:
                value = item.findtext(name)
                if value and value.strip():
                    return value.strip()
            return ""

        road_name = get_text("roadName", "roadNm", "linkName")
        speed_text = get_text("speed", "avgSpeed")
        travel_time_text = get_text("travelTime")
        link_id = get_text("linkId", "linkNo")
        created_date = get_text("createdDate", "collectTime")

        try:
            speed = float(speed_text)
        except (ValueError, TypeError):
            continue

        if speed < 0:
            continue

        if speed <= 20:
            status = "🔴 정체"
            color = "#ffcccc"
        elif speed <= 40:
            status = "🟡 서행"
            color = "#fff0b3"
        else:
            status = "🟢 원활"
            color = "#c9f2d0"

        rows.append({
            "도로명": road_name or "이름 미제공",
            "현재 속도(km/h)": speed,
            "혼잡 상태": status,
            "링크 ID": link_id,
            "통행시간(분)": travel_time_text,
            "수집 시각": created_date,
            "_색상": color,
        })

    return rows


@st.cache_data(ttl=60, show_spinner=False)
def fetch_traffic(api_key, region):
    """선택한 지역의 도로 교통정보를 조회한다."""
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
        API_URL,
        params=params,
        timeout=20,
    )
    response.raise_for_status()

    return parse_traffic_xml(response.text)


st.title("🚌 전국 버스 도로 혼잡도")
st.caption(
    "실시간 도로 소통정보를 확인하고 "
    "교통 체증에 따른 버스 지연 가능성을 추정합니다."
)

with st.sidebar:
    st.header("조회 설정")
    region = st.selectbox(
        "조회 지역",
        list(REGIONS.keys()),
        index=1,
        help="전국 조회는 데이터가 많거나 API 제한에 걸릴 수 있습니다.",
    )

    st.markdown("---")
    st.subheader("API 설정")

    secret_key = get_secret_key()

    if secret_key:
        api_key = secret_key
        st.success("Secrets에 등록된 API 키를 사용합니다.")
    else:
        api_key = st.text_input(
            "ITS API 키",
            type="password",
            help="공공데이터포털 또는 ITS에서 발급받은 키",
        )
        st.caption(
            "배포할 때는 API 키를 Secrets에 등록하는 것을 권장합니다."
        )

    refresh = st.button("🔄 교통정보 새로 조회", use_container_width=True)

    st.markdown("---")
    st.caption("교통정보는 API 제공 범위와 갱신 주기에 따라 달라집니다.")

if refresh:
    st.cache_data.clear()

if not api_key:
    st.info(
        "왼쪽 메뉴에 ITS API 키를 입력하거나, "
        "배포 환경의 Secrets에 ITS_API_KEY를 등록해 주세요."
    )
    st.markdown(
        "[국가교통정보센터 API 안내](https://www.its.go.kr/opendata/intro)"
    )
    st.stop()

try:
    with st.spinner(f"{region} 지역의 교통정보를 조회하는 중..."):
        rows = fetch_traffic(api_key, region)
except requests.exceptions.Timeout:
    st.error("교통정보 서버 응답 시간이 초과되었습니다. 잠시 후 다시 시도해 주세요.")
    st.stop()
except requests.exceptions.HTTPError as e:
    st.error(f"교통정보 서버 HTTP 오류: {e}")
    st.stop()
except requests.exceptions.RequestException as e:
    st.error(f"네트워크 오류가 발생했습니다: {e}")
    st.stop()
except ET.ParseError:
    st.error("API 응답을 XML로 해석할 수 없습니다. API 키와 응답 형식을 확인해 주세요.")
    st.stop()
except ValueError as e:
    st.error(str(e))
    st.stop()
except Exception as e:
    st.error(f"예상하지 못한 오류가 발생했습니다: {e}")
    st.stop()

if not rows:
    st.warning(
        "조회된 도로 정보가 없습니다. 다른 지역을 선택하거나 "
        "API 이용 승인, 요청 범위, 응답 데이터를 확인해 주세요."
    )
    st.stop()

df = pd.DataFrame(rows)
df = df.drop_duplicates(
    subset=["도로명", "링크 ID", "현재 속도(km/h)"]
).reset_index(drop=True)

# 상단 요약
total = len(df)
congested = int((df["현재 속도(km/h)"] <= 20).sum())
slow = int(
    (
        (df["현재 속도(km/h)"] > 20)
        & (df["현재 속도(km/h)"] <= 40)
    ).sum()
)
smooth = int((df["현재 속도(km/h)"] > 40).sum())

st.caption(
    f"조회 지역: {region} · 화면 조회 시각: "
    f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
)

c1, c2, c3, c4 = st.columns(4)
c1.metric("조회 도로 구간", f"{total:,}개")
c2.metric("🔴 정체", f"{congested:,}개")
c3.metric("🟡 서행", f"{slow:,}개")
c4.metric("🟢 원활", f"{smooth:,}개")

st.markdown("### 🛣️ 도로 혼잡도")

search = st.text_input(
    "도로명 검색",
    placeholder="예: 강남대로",
)

view_df = df.copy()

if search.strip():
    view_df = view_df[
        view_df["도로명"].str.contains(
            search.strip(),
            case=False,
            na=False,
            regex=False,
        )
    ]

if view_df.empty:
    st.warning("검색 조건에 맞는 도로가 없습니다.")
else:
    display_df = view_df[
        [
            "도로명",
            "현재 속도(km/h)",
            "혼잡 상태",
            "통행시간(분)",
            "수집 시각",
        ]
    ].copy()

    def color_status(row):
        speed = row["현재 속도(km/h)"]
        if speed <= 20:
            color = "#ffcccc"
        elif speed <= 40:
            color = "#fff0b3"
        else:
            color = "#c9f2d0"
        return [f"background-color: {color}"] * len(row)

    st.dataframe(
        display_df.style.apply(color_status, axis=1),
        use_container_width=True,
        hide_index=True,
    )

    st.download_button(
        "조회 결과 CSV 다운로드",
        data=display_df.to_csv(index=False).encode("utf-8-sig"),
        file_name="traffic_data.csv",
        mime="text/csv",
    )

st.markdown("---")
st.markdown("### ⏱️ 버스 지연 시간 추정")

st.write(
    "버스 노선의 평소 소요 시간과 해당 노선에 영향을 주는 도로의 "
    "현재 평균 속도를 입력해 지연 가능성을 계산합니다."
)

road_names = sorted(
    view_df["도로명"].dropna().astype(str).unique().tolist()
)

if road_names:
    selected_road = st.selectbox("비교할 도로", road_names)
    road_rows = view_df[view_df["도로명"] == selected_road]
    current_speed = float(
        road_rows["현재 속도(km/h)"].mean()
    )

    col1, col2 = st.columns(2)

    with col1:
        normal_minutes = st.number_input(
            "평소 버스 이동 시간(분)",
            min_value=1,
            max_value=600,
            value=30,
        )

    with col2:
        normal_speed = st.number_input(
            "평소 해당 도로 주행 속도(km/h)",
            min_value=1.0,
            max_value=120.0,
            value=40.0,
            step=1.0,
        )

    st.metric("선택 도로 현재 평균 속도", f"{current_speed:.1f} km/h")

    if st.button("예상 지연 시간 계산", type="primary"):
        # 단순 비례 추정치이며, 실제 버스 도착예정정보는 아니다.
        estimated_minutes = normal_minutes * normal_speed / max(
            current_speed, 1.0
        )
        delay = max(0.0, estimated_minutes - normal_minutes)

        result1, result2 = st.columns(2)
        result1.metric("예상 이동 시간", f"{estimated_minutes:.1f}분")
        result2.metric("예상 추가 지연", f"{delay:.1f}분")

        if current_speed <= 20:
            st.error("🔴 정체 구간입니다. 지연 가능성이 높을 수 있습니다.")
        elif current_speed <= 40:
            st.warning("🟡 서행 구간입니다. 지연 가능성을 확인하세요.")
        else:
            st.success("🟢 도로 흐름이 비교적 원활합니다.")

        st.caption(
            "주의: 이 결과는 현재 도로 속도가 평소 속도보다 "
            "낮아졌다고 가정한 단순 추정치입니다. "
            "신호 대기, 정류장 정차, 다른 도로 구간, 버스전용차로, "
            "실제 버스 위치를 반영하지 않으므로 실제 도착 시간과 다를 수 있습니다."
        )
else:
    st.info("지연 시간을 계산할 도로가 없습니다. 다른 검색 조건을 선택해 주세요.")

st.markdown("---")
st.caption(
    "혼잡도 기준(현재 속도): 20km/h 이하 정체 · "
    "20 초과~40km/h 이하 서행 · 40km/h 초과 원활. "
    "이는 앱에서 사용하는 단순 분류 기준이며 공식 혼잡 판정과 다를 수 있습니다."
)
