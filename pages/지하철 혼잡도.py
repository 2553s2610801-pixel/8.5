import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="지하철 칸별 혼잡도", layout="wide")

HTML_CONTENT = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>지하철 칸별 혼잡도 확인</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Jua&family=Gowun+Dodum&display=swap" rel="stylesheet">
<style>
  :root {
    --bg1: #fff0f5; --bg2: #f0f7ff; --card: #ffffff; --soft: #fff5f8; --ink: #3a3238; --muted: #8c7d87;
    --accent: #ff9ebb; --accent-d: #ff7399;
    --low: #b2f2bb; --mid: #ffec99; --high: #ffc9c9;
    --f-title: "Jua", "Gowun Dodum", sans-serif;
    --f-body: "Gowun Dodum", "Pretendard", sans-serif;
  }
  * { box-sizing: border-box; }
  body { margin: 0; min-height: 100vh; background: linear-gradient(135deg, var(--bg1), var(--bg2)); color: var(--ink); font-family: var(--f-body); display: flex; justify-content: center; padding: 22px 12px; }
  button, select, input { font: inherit; color: inherit; }
  :focus-visible { outline: 3px solid var(--accent); outline-offset: 2px; }
  
  .app { width: 100%; max-width: 880px; background: var(--card); border-radius: 42px; border: 4px solid #f2d6e3; box-shadow: 0 16px 36px rgba(255, 182, 193, .35); padding: 28px 30px 24px; }

  header { display: flex; align-items: center; gap: 16px; }
  .logo { width: 62px; height: 62px; border-radius: 50%; background: #ffe3ec; border: 3px solid #ffc2d4; display: grid; place-items: center; font-size: 34px; box-shadow: inset 0 -4px 0 #ffa8c0; }
  h1 { margin: 0; font-family: var(--f-title); font-size: 1.8rem; color: #5a434d; }
  header p { margin: 2px 0 0; color: var(--muted); font-size: .95rem; font-weight: bold; }

  .panel { margin-top: 20px; padding: 20px 24px; background: var(--soft); border-radius: 30px; border: 2px dashed #fcd5e4; display: grid; gap: 14px; }
  .row { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
  .lab { width: 75px; flex: none; font-family: var(--f-title); font-size: 1.1rem; color: #6b4d5a; }
  .chips { display: flex; gap: 8px; flex-wrap: wrap; }
  .chip { width: 40px; height: 40px; border-radius: 50%; border: 2px solid rgba(0,0,0,.08); color: #fff; font-family: var(--f-title); font-size: 1.05rem; cursor: pointer; opacity: .6; transition: transform .2s, opacity .2s, box-shadow .2s; }
  .chip:hover { opacity: .9; transform: scale(1.08); }
  .chip[aria-pressed="true"] { opacity: 1; transform: scale(1.18); box-shadow: 0 0 0 3px #fff, 0 0 0 5px var(--accent-d); }
  
  .search { position: relative; flex: 1; min-width: 210px; }
  .search input { width: 100%; padding: 12px 20px; border: 2px solid #ffd0e0; border-radius: 999px; background: #fff; box-shadow: 0 3px 10px rgba(255, 182, 193, .15); }
  .search input:focus { border-color: var(--accent-d); outline: none; }
  .list { position: absolute; z-index: 5; left: 0; right: 0; top: calc(100% + 6px); max-height: 250px; overflow: auto; background: #fff; border-radius: 22px; border: 2px solid #fcd5e4; box-shadow: 0 10px 30px rgba(255, 182, 193, .25); margin: 0; padding: 8px; list-style: none; }
  .list[hidden] { display: none; }
  .list li { display: flex; align-items: center; gap: 8px; padding: 10px 14px; border-radius: 14px; cursor: pointer; }
  .list li:hover, .list li.on { background: var(--soft); }
  .b { min-width: 24px; height: 24px; border-radius: 12px; color: #fff; font-size: .78rem; display: inline-flex; align-items: center; justify-content: center; padding: 0 7px; font-family: var(--f-title); }
  .rg { margin-left: auto; font-size: .75rem; color: var(--accent-d); background: #ffeaf1; border-radius: 999px; padding: 2px 10px; font-weight: bold; }
  .none { color: var(--muted); cursor: default; }
  select { padding: 11px 18px; border: 2px solid #ffd0e0; border-radius: 999px; background: #fff; box-shadow: 0 3px 10px rgba(255, 182, 193, .15); min-width: 200px; }
  
  .go { margin-left: auto; padding: 12px 36px; border: 0; border-radius: 999px; background: var(--accent); color: #fff; font-family: var(--f-title); font-size: 1.2rem; cursor: pointer; box-shadow: 0 6px 0 var(--accent-d); transition: transform .1s, box-shadow .1s; }
  .go:hover { background: #ff8daf; }
  .go:active { transform: translateY(4px); box-shadow: 0 2px 0 var(--accent-d); }
  .msg { min-height: 1.2em; font-size: .92rem; color: #ff4d4d; margin-top: -4px; font-weight: bold; }

  [hidden] { display: none !important; }
  
  .head { margin-top: 24px; display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
  .head .t { font-family: var(--f-title); font-size: 1.35rem; color: #4a3842; }
  .lvl { margin-left: auto; padding: 6px 18px; border-radius: 999px; font-family: var(--f-title); border: 2px solid rgba(0,0,0,.05); }
  .lvl.low { background: var(--low); color: #2b6e3b; } 
  .lvl.mid { background: var(--mid); color: #856404; } 
  .lvl.high { background: var(--high); color: #9c2b2b; }

  .btn-refresh { padding: 8px 18px; border: 2px solid #ffc2d4; border-radius: 999px; background: #fff; color: #5a434d; font-family: var(--f-title); font-size: .95rem; cursor: pointer; display: inline-flex; align-items: center; gap: 6px; box-shadow: 0 3px 8px rgba(0,0,0,.05); transition: all .2s; }
  .btn-refresh:hover { background: #ffeef4; transform: rotate(10deg); }
  .btn-refresh:active { transform: scale(.95); }
  .btn-refresh.spinning .icon { animation: spin .6s ease-in-out; }
  @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

  .train { display: flex; align-items: flex-end; gap: 4px; margin-top: 20px; padding-bottom: 14px; position: relative; }
  .train::after { content: ""; position: absolute; left: 0; right: 0; bottom: 0; height: 6px; border-radius: 3px; background: repeating-linear-gradient(90deg, #ffd0e0 0 16px, transparent 16px 24px); }
  .cap { width: 18px; height: 62px; background: #6c5b65; margin-bottom: 12px; border-radius: 6px; }
  .cap.l { border-radius: 30px 6px 6px 30px; } .cap.r { border-radius: 6px 30px 30px 6px; }
  .cars { flex: 1; display: grid; grid-template-columns: repeat(7, 1fr); gap: 6px; }
  
  .car { display: flex; flex-direction: column; align-items: center; gap: 6px; min-width: 0; animation: pop .45s cubic-bezier(.3,1.5,.5,1) both; animation-delay: calc(var(--i) * 60ms); }
  @keyframes pop { from { opacity: 0; transform: translateY(16px) scale(.85); } to { opacity: 1; transform: none; } }
  .no { font-size: .85rem; color: var(--muted); font-weight: bold; }
  .best .no { color: #ff5285; font-family: var(--f-title); font-size: .95rem; }
  
  .box { width: 100%; height: 105px; border-radius: 24px; border: 3px solid rgba(0,0,0,.06); display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 2px; position: relative; box-shadow: inset 0 -6px 0 rgba(0,0,0,.08); }
  .box .face { font-size: 2.2rem; line-height: 1; filter: drop-shadow(0 2px 4px rgba(0,0,0,.1)); }
  .box .pct { font-family: var(--f-title); font-size: 1.05rem; color: #333; }
  .box.low { background: var(--low); } .box.mid { background: var(--mid); } .box.high { background: var(--high); }
  .star { position: absolute; top: -12px; right: -4px; font-size: 1.4rem; animation: bounce 1s infinite alternate; }
  @keyframes bounce { from { transform: translateY(0); } to { transform: translateY(-4px); } }
  .near { font-size: .72rem; line-height: 1.2; text-align: center; color: #8a707c; font-weight: bold; min-height: 2.4em; }

  .lower { display: grid; grid-template-columns: 230px 1fr; gap: 18px; margin-top: 10px; align-items: stretch; }
  .legend { background: var(--soft); border-radius: 28px; border: 2px solid #fcd5e4; padding: 18px 10px; display: flex; justify-content: space-around; align-items: center; }
  .legend div { display: flex; flex-direction: column; align-items: center; gap: 6px; font-size: .9rem; font-weight: bold; }
  .dot { width: 46px; height: 46px; border-radius: 50%; display: grid; place-items: center; font-size: 1.6rem; box-shadow: 0 3px 8px rgba(0,0,0,.08); }
  
  .bubble { position: relative; background: var(--soft); border-radius: 30px; border: 3px solid #ffcadb; padding: 22px 28px; min-height: 170px; display: flex; flex-direction: column; justify-content: center; }
  .bubble::before { content: ""; position: absolute; left: -12px; top: 50%; margin-top: -10px; border: 10px solid transparent; border-left: 0; border-right-color: #ffcadb; }
  .tag { align-self: flex-start; background: var(--accent-d); color: #fff; border-radius: 999px; padding: 4px 14px; font-family: var(--f-title); font-size: .85rem; margin-bottom: 8px; box-shadow: 0 2px 6px rgba(255,115,153,.3); }
  .big { margin: 0; font-family: var(--f-title); font-size: 2.1rem; line-height: 1.3; color: #4a323d; }
  .sub { margin: 10px 0 0; color: #7a626f; font-size: .98rem; line-height: 1.55; font-weight: bold; }
  
  .hint { margin: 24px 0 0; padding: 36px 20px; border-radius: 30px; background: var(--soft); border: 2px dashed #fcd5e4; text-align: center; color: #7a626f; line-height: 1.7; font-weight: bold; }
  .hint .e { font-size: 2.2rem; display: block; margin-bottom: 6px; }
  .foot { margin: 14px 0 0; color: var(--muted); font-size: .85rem; text-align: right; font-weight: bold; }

  @media (max-width: 640px) {
    .app { padding: 20px 16px; border-radius: 30px; }
    h1 { font-size: 1.4rem; } .lab { width: 100%; }
    .go { width: 100%; margin-left: 0; } select { width: 100%; }
    .lower { grid-template-columns: 1fr; } .bubble::before { display: none; }
    .cars { gap: 3px; } .box { height: 82px; border-radius: 18px; } .box .face { font-size: 1.5rem; } .box .pct { font-size: .82rem; }
    .no { font-size: .72rem; } .near { font-size: .6rem; } .cap { width: 10px; height: 48px; }
    .big { font-size: 1.65rem; }
  }
</style>
</head>
<body>
<main class="app">
  <header>
    <div class="logo" aria-hidden="true">🐰</div>
    <div>
      <h1>지하철 칸별 혼잡도 확인</h1>
      <p>복잡복잡 싫어! 쾌적하고 여유로운 칸으로 타요 ( •̀ω•́ )✨</p>
    </div>
  </header>

  <form class="panel" id="form" autocomplete="off">
    <div class="row"><span class="lab">노선선택</span><div class="chips" id="chips"></div></div>
    <div class="row">
      <span class="lab">역 선택</span>
      <div class="search">
        <input id="q" type="text" placeholder="역 이름 검색 (예: 두정, 천안, 강남)" role="combobox" aria-expanded="false" aria-controls="list">
        <ul class="list" id="list" role="listbox" hidden></ul>
      </div>
    </div>
    <div class="row">
      <span class="lab">방향</span>
      <select id="dir" aria-label="방향 선택"></select>
      <button class="go" type="submit">확인 💖</button>
    </div>
    <div class="msg" id="msg" role="alert"></div>
  </form>

  <section id="out" hidden>
    <div class="head">
      <span class="b" id="hLine"></span>
      <span class="t" id="hText"></span>
      <span class="lvl" id="hLvl"></span>
      <button class="btn-refresh" id="refreshBtn" type="button"><span class="icon">🔄</span>실시간 새로고침</button>
    </div>
    <div class="train">
      <span class="cap l"></span><div class="cars" id="cars"></div><span class="cap r"></span>
    </div>
    <div class="lower">
      <div class="legend">
        <div><span class="dot" style="background:var(--low)">( ˶ˆ⤙ˆ˵ )</span>여유</div>
        <div><span class="dot" style="background:var(--mid)">( • ̀ω•́ )</span>보통</div>
        <div><span class="dot" style="background:var(--high)">( 😭 )</span>복잡</div>
      </div>
      <div class="bubble" aria-live="polite">
        <span class="tag">치이카와 추천!</span>
        <p class="big" id="rec"></p>
        <p class="sub" id="warn"></p>
      </div>
    </div>
    <p class="foot" id="time"></p>
  </section>
  <div class="hint" id="hint"><span class="e">🌸 🚇 🌸</span>노선과 역, 방향을 고르고 <b>확인</b>을 눌러 보세요!<br>다음 열차의 칸별 혼잡도를 귀엽게 알려드려요.</div>
</main>

<script>
const CAR_COUNT = 7;

const LINES = {
  "1":{color:"#0052A4",dir:["상행 (소요산·청량리 방면)","하행 (인천·신창 방면)"],
    st:"소요산 동두천 보산 동두천중앙 지행 덕정 덕계 양주 녹양 가능 의정부 회룡 망월사 도봉산 방학 창동 녹천 월계 광운대 석계 신이문 외대앞 회기 청량리 제기동 신설동 동묘앞 동대문 종로5가 종로3가 종각 시청 서울역 남영 용산 노량진 대방 신길 영등포 신도림 구로 가산디지털단지 독산 금천구청 석수 관악 안양 명학 금정 군포 당정 의왕 성균관대 화서 수원 세류 병점 세마 오산대 오산 진위 송탄 서정리 지제 평택 성환 직산 두정 천안 봉명 쌍용 아산 배방 온양온천 신창 구일 개봉 오류동 온수 역곡 소사 부천 중동 송내 부개 부평 백운 동암 간석 주안 도화 제물포 도원 동인천 인천"},
  "2":{color:"#00A84D",dir:["내선순환","외선순환"],
    st:"시청 을지로입구 을지로3가 을지로4가 동대문역사문화공원 신당 상왕십리 왕십리 한양대 뚝섬 성수 건대입구 구의 강변 잠실나루 잠실 잠실새내 종합운동장 삼성 선릉 역삼 강남 교대 서초 방배 사당 낙성대 서울대입구 봉천 신림 신대방 구로디지털단지 대림 신도림 문래 영등포구청 당산 합정 홍대입구 신촌 이대 아현 충정로 용답 신답 용두 도림천 양천구청 신정네거리 까치산"},
  "3":{color:"#EF7C1C",dir:["상행 (대화 방면)","하행 (오금 방면)"],
    st:"대화 주엽 정발산 마두 백석 대곡 화정 원당 원흥 삼송 지축 구파발 연신내 불광 녹번 홍제 무악재 독립문 경복궁 안국 종로3가 을지로3가 충무로 동대입구 약수 금호 옥수 압구정 신사 잠원 고속터미널 교대 남부터미널 양재 매봉 도곡 대치 학여울 대청 일원 수서 가락시장 경찰병원 오금"},
  "4":{color:"#00A5DE",dir:["상행 (진접·당고개 방면)","하행 (오이도 방면)"],
    st:"진접 오남 별내별가람 당고개 상계 노원 창동 쌍문 수유 미아 미아사거리 길음 성신여대입구 한성대입구 혜화 동대문 동대문역사문화공원 충무로 명동 회현 서울역 숙대입구 삼각지 신용산 이촌 동작 총신대입구 사당 남태령 선바위 경마공원 대공원 과천 정부과천청사 인덕원 평촌 범계 금정 산본 수리산 대야미 반월 상록수 한대앞 중앙 고잔 초지 안산 신길온천 정왕 오이도"},
  "5":{color:"#996CAC",dir:["상행 (방화 방면)","하행 (상일동·마천 방면)"],
    st:"방화 개화산 김포공항 송정 마곡 발산 우장산 화곡 까치산 신정 목동 오목교 양평 영등포구청 영등포시장 신길 여의도 여의나루 마포 공덕 애오개 충정로 서대문 광화문 종로3가 을지로4가 동대문역사문화공원 청구 신금호 행당 왕십리 마장 답십리 장한평 군자 아차산 광나루 천호 강동 길동 굽은다리 명일 고덕 상일동 강일 미사 하남풍산 하남시청 하남검단산 둔촌동 올림픽공원 방이 오금 개롱 거여 마천"},
  "6":{color:"#CD7C2F",dir:["상행 (응암 방면)","하행 (봉화산 방면)"],
    st:"응암 역촌 불광 독바위 연신내 구산 새절 증산 디지털미디어시티 월드컵경기장 마포구청 망원 합정 상수 광흥창 대흥 공덕 효창공원앞 삼각지 녹사평 이태원 한강진 버티고개 약수 청구 신당 동묘앞 창신 보문 안암 고려대 월곡 상월곡 돌곶이 석계 태릉입구 화랑대 봉화산"},
  "7":{color:"#747F00",dir:["상행 (장암 방면)","하행 (석남 방면)"],
    st:"장암 도봉산 수락산 마들 노원 중계 하계 공릉 태릉입구 먹골 중화 상봉 면목 사가정
