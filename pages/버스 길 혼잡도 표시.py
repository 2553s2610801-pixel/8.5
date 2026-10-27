import streamlit as st
import requests
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo

st.set_page_config(
    page_title="버스길 교통 신호등",
    page_icon="🚌",
    layout="wide"
)

API_URL = "https://openapi.its.go.kr/trafficInfo"

# 지역별 조회 범위: 경도·위도
REGIONS = {
    "서울": (126.80, 127.20, 37.40, 37.70),
    "부산": (128.90, 129.25, 35.05, 35.25),
    "인천": (126.35, 126.80, 37.35, 37.65),
    "대구": (128.45, 128.75, 35.75, 36.00),
    "광주": (126.75, 127.00, 35.05, 35.25),
    "대전": (127.25, 127.50, 36.25, 36.45),
    "울산": (129.15, 129.40, 35.45, 35.65),
    "세종": (127.15, 127.35, 36.45, 36.65),
    "제주": (126.15, 126.70, 33.20, 33.60),
}

COLORS = {
    "원활": "#16A34A",
    "서행": "#EAB308",
    "정체": "#DC2626",
    "정보 없음": "#64748B",
}


def get_congestion(speed):
    """속도를 기준으로 혼잡 단계를 구분한다."""
    if speed is None or speed < 0:
        return "정보 없음"
    if speed >= 40:
        return "원활"
    if speed >= 20:
        return "서행"
    return "정체"


def fetch_traffic(region, api_key):
    """ITS API에서 선택한 지역의 도로 교통정보를 가져온다."""
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

    try:
        response = requests.get(
            API_URL,
            params=params,
            timeout=20,
        )
        response.raise_for_status()

        # 잘못된 XML 응답도 예외 처리한다.
        root = ET.fromstring(response.content)

        result_code = root.findtext(".//header/resultCode")
        result_msg = root.findtext(".//header/resultMsg")

        if result_code not in (None, "0"):
            raise ValueError(
                f"API 응답 오류: {result_msg or result_code}"
            )

        rows = []

        for item in root.findall(".//body/items/item"):
            road_name = (
                item.findtext("roadName") or "도로명 없음"
            ).strip()

            speed_text = item.findtext("speed")
            time_text = item.findtext("travelTime")

            try:
                speed = float(speed_text)
                if speed < 0:
                    speed = None
            except (TypeError, ValueError):
                speed = None

            try:
                travel_time = float(time_text)
                if travel_time < 0:
                    travel_time = None
            except (TypeError, ValueError):
                travel_time = None

            rows.append({
                "도로명": road_name,
                "속도(km/h)": speed,
                "통행시간(분)": (
                    travel_time if travel_time is not None else None
                ),
                "혼잡도": get_congestion(speed),
                "구간 ID": item.findtext("linkId") or "-",
                "수집 시각": item.findtext("createdDate") or "-",
            })

        return rows

    except requests.exceptions.Timeout:
        raise RuntimeError(
            "교통정보 서버 응답 시간이 초과되었습니다. 잠시 후 다시 시도해 주세요."
        )
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(
            f"교통정보 서버 HTTP 오류가 발생했습니다: {e}"
        )
    except requests.exceptions.RequestException as e:
        raise RuntimeError(
            f"네트워크 연결에 실패했습니다: {e}"
        )
    except ET.ParseError:
        raise RuntimeError(
            "서버 응답을 해석할 수 없습니다. API 응답 형식을 확인해 주세요."
        )


def estimate_delay(df):
    """
    참고용 지연 위험 추정.
    실제 버스 도착시간 예측이 아님을 화면에 명시한다.
    """
    if df.empty:
        return 0

    slow_count = int(
        df["혼잡도"].isin(["서행", "정체"]).sum()
    )
    jam_count = int((df["혼잡도"] == "정체").sum())

    # 도로 정보 개수만으로 계산하는 단순 참고 지표
    return min(30, slow_count + jam_count * 2)


st.title("🚌 버스길 교통 신호등")
st.caption(
    "도로의 실시간 속도를 신호등 색상으로 확인하고 "
    "버스 지연 위험을 참고하세요."
)

st.info(
    "이 앱은 도로 교통정보를 보여줍니다. "
    "버스 전용차로, 개별 버스 노선 및 실제 버스 도착정보와 "
    "직접 연결된 것은 아닙니다. 지연 추정치는 참고용입니다."
)

with st.sidebar:
    st.header("🔎 교통정보 설정")

    region = st.selectbox(
        "조회 지역",
        list(REGIONS.keys()),
        index=0,
    )

    road_filter = st.text_input(
        "도로명 검색 (선택)",
        placeholder="예: 강남대로",
    )

    st.markdown("---")
    st.subheader("🔑 API 설정")
    st.caption(
        "ITS 국가교통정보센터에서 발급받은 API 키를 "
        "Streamlit Secrets에 등록해 주세요."
    )

    try:
        api_key = st.secrets.get("ITS_API_KEY", "")
    except Exception:
        api_key = ""

    if not api_key:
        api_key = st.text_input(
            "API 키",
            type="password",
            help="임시 테스트용 입력란입니다. 공개 저장소에 키를 올리지 마세요.",
        )

    refresh = st.button(
        "🔄 실시간 교통정보 조회",
        type="primary",
        use_container_width=True,
    )

    st.caption(
        "색상 기준: 원활 40km/h 이상 · "
        "서행 20~40km/h 미만 · 정체 20km/h 미만"
    )

# 조회 버튼을 눌렀을 때만 API를 호출한다.
if refresh:
    if not api_key.strip():
        st.error(
            "API 키가 없습니다. 사이드바에 키를 입력하거나 "
            "Secrets에 ITS_API_KEY를 등록해 주세요."
        )
    else:
        with st.spinner(f"{region} 지역 교통정보를 조회 중입니다..."):
            try:
                rows = fetch_traffic(region, api_key.strip())
                st.session_state["traffic_rows"] = rows
                st.session_state["traffic_region"] = region
                st.session_state["traffic_time"] = datetime.now(
                    ZoneInfo("Asia/Seoul")
                ).strftime("%Y-%m-%d %H:%M:%S")
                st.session_state.pop("traffic_error", None)
            except Exception as e:
                st.session_state["traffic_error"] = str(e)

if st.session_state.get("traffic_error"):
    st.error(st.session_state["traffic_error"])

rows = st.session_state.get("traffic_rows", [])
loaded_region = st.session_state.get("traffic_region", "")

if not rows:
    st.subheader("교통정보를 확인해 보세요")
    st.write(
        "1. 왼쪽에서 지역을 선택합니다.\n"
        "2. API 키를 등록합니다.\n"
        "3. **실시간 교통정보 조회** 버튼을 누릅니다."
    )
    st.markdown(
        "[ITS 국가교통정보센터 오픈데이터 안내]"
        "(https://www.its.go.kr/opendata/intro)"
    )
    st.stop()

if region != loaded_region:
    st.warning(
        f"현재 표시된 정보는 {loaded_region} 조회 결과입니다. "
        "새 지역을 보려면 조회 버튼을 눌러 주세요."
    )

df = pd.DataFrame(rows)

if road_filter.strip():
    df = df[
        df["도로명"].str.contains(
            road_filter.strip(),
            case=False,
            na=False,
            regex=False,
        )
    ].copy()

st.subheader(f"📍 {loaded_region} 도로 상황")
st.caption(
    f"마지막 조회 시각: "
    f"{st.session_state.get('traffic_time', '알 수 없음')}"
)

if df.empty:
    st.warning("검색 조건에 맞는 도로 정보가 없습니다.")
    st.stop()

total = len(df)
green = int((df["혼잡도"] == "원활").sum())
yellow = int((df["혼잡도"] == "서행").sum())
red = int((df["혼잡도"] == "정체").sum())
unknown = int((df["혼잡도"] == "정보 없음").sum())

c1, c2, c3, c4 = st.columns(4)
c1.metric("🟢 원활", f"{green}개")
c2.metric("🟡 서행", f"{yellow}개")
c3.metric("🔴 정체", f"{red}개")
c4.metric("전체 구간", f"{total}개")

st.markdown("---")
st.subheader("🚦 도로별 혼잡도")

# 각 도로를 신호등 카드로 표시
for _, row in df.iterrows():
    status = row["혼잡도"]
    color = COLORS.get(status, COLORS["정보 없음"])
    speed = row["속도(km/h)"]
    speed_label = (
        f"{speed:g} km/h"
        if pd.notna(speed)
        else "속도 정보 없음"
    )

    travel_time = row["통행시간(분)"]
    time_label = (
        f"{travel_time:g}분"
        if pd.notna(travel_time)
        else "정보 없음"
    )

    st.markdown(
        f"""
        <div style="
            border-left: 8px solid {color};
            border-radius: 8px;
            padding: 12px 16px;
            margin: 8px 0;
            background-color: rgba(128,128,128,0.08);
        ">
            <div style="font-size: 18px; font-weight: 700;">
                {row['도로명']}
            </div>
            <div style="margin-top: 6px;">
                <span style="
                    color: {color};
                    font-weight: 700;
                ">● {status}</span>
                &nbsp; | &nbsp; 속도: {speed_label}
                &nbsp; | &nbsp; 통행시간: {time_label}
            </div>
            <div style="font-size: 12px; opacity: 0.7; margin-top: 4px;">
                구간 ID: {row['구간 ID']}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")
st.subheader("🚌 버스 지연 위험 참고")

delay = estimate_delay(df)
jam_ratio = red / total if total else 0

if total == 0:
    st.info("분석할 도로 정보가 없습니다.")
elif jam_ratio >= 0.3:
    st.error(
        "정체 구간 비율이 높습니다. 해당 도로를 지나는 버스의 "
        "지연 가능성을 주의해서 확인하세요."
    )
elif yellow + red > 0:
    st.warning(
        "서행 또는 정체 구간이 있습니다. 버스 도착이 "
        "평소보다 늦어질 가능성이 있습니다."
    )
else:
    st.success(
        "조회된 도로는 대체로 원활합니다. "
        "다만 버스 운행 상황에 따라 도착시간은 달라질 수 있습니다."
    )

st.metric(
    "단순 지연 위험 참고 지표",
    f"{delay}점",
    help=(
        "서행 구간 수 + 정체 구간 수×2로 계산하며 30점으로 제한합니다. "
        "분 단위의 실제 지연시간이나 검증된 예측값이 아닙니다."
    ),
)

st.caption(
    "주의: 조회 결과는 API가 반환한 도로 구간 기준입니다. "
    "버스 노선에 포함된 도로만 필터링한 결과가 아니며, "
    "도로 속도 기준과 지연 위험 지표는 참고용입니다."
)

with st.expander("📋 표로 보기 / CSV 저장"):
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
    )

    csv = df.to_csv(
        index=False,
        encoding="utf-8-sig",
    )
    st.download_button(
        "CSV 다운로드",
        data=csv,
        file_name=f"{loaded_region}_교통정보.csv",
        mime="text/csv",
    )
