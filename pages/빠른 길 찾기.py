import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="길 찾기 대장",
    page_icon="🗺️",
    layout="centered"
)

# 2. 세션 상태 초기화
if "page" not in st.session_state:
    st.session_state.page = "home"
if "recent_searches" not in st.session_state:
    st.session_state.recent_searches = ["성환역", "평택역", "서울역"]
if "favorites" not in st.session_state:
    st.session_state.favorites = ["성환역 (1호선)", "평택역 (1호선)", "강남역 (2호선)"]

# 3. 서울교통공사 및 수도권 전철 DB (성환역, 평택역 포함)
SUBWAY_STATIONS = [
    # 1호선 주요 역 (성환, 평택 연선 포함)
    "성환역", "평택역", "두정역", "천안역", "지제역", "평택지제역", "서정리역", 
    "오산역", "수원역", "금정역", "신도림역", "용산역", "서울역", "시청역", "종로3가역", "청량리역",
    
    # 주요 환승 및 거점 역
    "강남역", "홍대입구역", "잠실역", "고속터미널역", "사당역", "신촌역", 
    "건대입구역", "삼성역", "판교역", "합정역", "여의도역", "김포공항역"
]

# 실제 전철 구간별 소요시간(분) 및 경로 안내
REAL_ROUTES = {
    # 1호선 성환역 ↔ 평택역 (실제 약 6분 소요)
    ("성환역", "평택역"): (6, "수도권 전철 1호선 직행 (약 1정거장)"),
    ("평택역", "성환역"): (6, "수도권 전철 1호선 직행 (약 1정거장)"),
    
    # 1호선 성환/평택 주요 구간
    ("성환역", "천안역"): (10, "수도권 전철 1호선 직행"),
    ("천안역", "성환역"): (10, "수도권 전철 1호선 직행"),
    ("성환역", "서울역"): (75, "수도권 전철 1호선 (또는 ITX-마음/무궁화호 이용 시 약 50분)"),
    ("평택역", "서울역"): (68, "수도권 전철 1호선 (또는 ITX-새마을/무궁화호 이용 시 약 45분)"),
    
    # 주요 광역 경로
    ("서울역", "강남역"): (30, "4호선 사당역 환승 ➡️ 2호선 강남역"),
    ("강남역", "서울역"): (30, "2호선 사당역 환승 ➡️ 4호선 서울역"),
    ("홍대입구역", "잠실역"): (39, "2호선 직행"),
    ("서울역", "홍대입구역"): (8, "공항철도 직행"),
    ("강남역", "판교역"): (15, "신분당선 직행")
}

def clean_station_name(name):
    name = name.strip()
    if name and not name.endswith("역"):
        name += "역"
    return name

def find_subway_route(start_raw, end_raw):
    start = clean_station_name(start_raw)
    end = clean_station_name(end_raw)
    
    # 노선도 DB 검증 ('호날두' 등 미등록 검색어 차단)
    if start not in SUBWAY_STATIONS or end not in SUBWAY_STATIONS:
        invalid_list = []
        if start not in SUBWAY_STATIONS:
            invalid_list.append(f"'{start_raw}'")
        if end not in SUBWAY_STATIONS:
            invalid_list.append(f"'{end_raw}'")
        return False, f"⚠️ 입력하신 {', '.join(invalid_list)}은(는) 전철 노선도에 등록되지 않은 역입니다. 올바른 역명을 입력해 주세요."
    
    if start == end:
        return False, "⚠️ 출발역과 도착역이 동일합니다. 서로 다른 역을 입력해 주세요."
    
    # 실제 구간 데이터 우선 조회
    if (start, end) in REAL_ROUTES:
        duration, route_desc = REAL_ROUTES[(start, end)]
        return True, {"start": start, "end": end, "time": duration, "route": route_desc}
    
    # 일반 계산 경로
    idx_s = SUBWAY_STATIONS.index(start)
    idx_e = SUBWAY_STATIONS.index(end)
    station_cnt = abs(idx_s - idx_e)
    est_time = station_cnt * 5 + 3
    
    return True, {"start": start, "end": end, "time": est_time, "route": f"{start} ➡️ 수도권 전철 최단 경로 ➡️ {end}"}

# CSS 스타일링
st.markdown("""
    <style>
    .header-box {
        background-color: #8FD8FA;
        padding: 20px;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 25px;
    }
    .header-box h1 { color: #000; font-size
