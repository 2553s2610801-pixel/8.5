import streamlit as st

st.set_page_config(page_title="길 찾기 대장", page_icon="🧭", layout="centered")

# ---------- 상태 ----------
if "recent" not in st.session_state:
    st.session_state.recent = []
if "favorites" not in st.session_state:
    st.session_state.favorites = []
if "page" not in st.session_state:
    st.session_state.page = "home"

# ---------- 스타일 ----------
st.markdown("""
<style>
.block-container {max-width: 560px; padding-top: 1.5rem;}
.title-box {
    background:#8fd6ee; border:8px solid #e3effc; border-radius:14px;
    text-align:center; padding:22px 0; margin-bottom:18px;
}
.title-box h1 {margin:0; font-size:2.4rem; font-weight:900; color:#111;}
.card {
    border-radius:12px; padding:22px 10px; text-align:center;
    height:170px; margin-bottom:8px;
}
.card .icon {font-size:2.6rem;}
.card .name {font-weight:800; font-size:1.1rem; margin-top:6px; color:#111;}
.card .desc {font-size:0.8rem; color:#555; margin-top:4px;}
.blue {background:#e6f0fd;} .green {background:#e5f4e3;}
.purple {background:#ece8fb;} .yellow {background:#fff3d6;}
div.stButton > button {width:100%; border-radius:8px;}
</style>
""", unsafe_allow_html=True)

# ---------- 제목 ----------
st.markdown('<div class="title-box"><h1>길 찾기 대장</h1></div>', unsafe_allow_html=True)

# ---------- 검색창 ----------
c1, c2 = st.columns([5, 1])
query = c1.text_input("검색", placeholder="목적지를 입력하세요", label_visibility="collapsed")
if c2.button("검색", type="primary"):
    if query.strip():
        if query not in st.session_state.recent:
            st.session_state.recent.insert(0, query)
        st.session_state.page = "result"
        st.session_state.query = query
    else:
        st.warning("검색어를 입력해주세요.")

# ---------- 카드 ----------
def card(icon, name, desc, color, key, page):
    st.markdown(
        f'<div class="card {color}"><div class="icon">{icon}</div>'
        f'<div class="name">{name}</div><div class="desc">{desc}</div></div>',
        unsafe_allow_html=True,
    )
    if st.button("열기", key=key):
        st.session_state.page = page

if st.session_state.page == "home" or True:
    a, b = st.columns(2)
    with a:
        card("📍", "빠른 길 찾기", "최단 시간 경로를<br>알려드려요", "blue", "k1", "fast")
    with b:
        card("🚌", "대중교통", "지하철, 버스 경로를<br>확인해보세요", "green", "k2", "transit")
    a, b = st.columns(2)
    with a:
        card("🕒", "최근 검색", "이전에 찾은 경로를<br>다시 확인할 수 있어요", "purple", "k3", "recent")
    with b:
        card("⭐", "즐겨찾기", "자주 가는 장소를<br>저장해보세요", "yellow", "k4", "fav")

st.divider()

# ---------- 페이지별 내용 ----------
page = st.session_state.page

if page == "result":
    q = st.session_state.get("query", "")
    st.subheader(f"'{q}' 검색 결과")
    st.info("여기에 지도/경로 API 결과를 연결하세요. (예: 카카오맵, 네이버, TMAP API)")
    if st.button("⭐ 즐겨찾기에 추가"):
        if q not in st.session_state.favorites:
            st.session_state.favorites.append(q)
            st.success("추가했어요!")

elif page == "fast":
    st.subheader("빠른 길 찾기")
    st.text_input("출발지")
    st.text_input("도착지")
    st.button("최단 경로 찾기")

elif page == "transit":
    st.subheader("대중교통")
    st.radio("교통수단", ["지하철", "버스", "지하철+버스"], horizontal=True)
    st.text_input("출발지", key="t1")
    st.text_input("도착지", key="t2")
    st.button("경로 확인")

elif page == "recent":
    st.subheader("최근 검색")
    if st.session_state.recent:
        for r in st.session_state.recent:
            st.write(f"🕒 {r}")
    else:
        st.caption("아직 검색 기록이 없어요.")

elif page == "fav":
    st.subheader("즐겨찾기")
    if st.session_state.favorites:
        for f in st.session_state.favorites:
            st.write(f"⭐ {f}")
    else:
        st.caption("저장된 장소가 없어요.")
