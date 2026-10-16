import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="지하철 칸별 혼잡도", layout="wide")

HTML = r'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>지하철 칸별 혼잡도 확인</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Jua&family=Gowun+Dodum&display=swap" rel="stylesheet">
<style>
  :root{
    --bg1:#e7eeff; --bg2:#f5eeff; --card:#fff; --soft:#f0f3ff; --ink:#2b3350; --muted:#6b7394;
    --accent:#5b7cfa; --accent-d:#4766e6;
    --low:#8be3b0; --mid:#ffd86b; --high:#ff8d84;
    --f-title:"Jua","Gowun Dodum","Malgun Gothic",sans-serif;
    --f-body:"Gowun Dodum","Pretendard","Noto Sans KR","Malgun Gothic",sans-serif;
  }
  *{box-sizing:border-box}
  body{margin:0;min-height:100vh;background:linear-gradient(160deg,var(--bg1),var(--bg2));color:var(--ink);font-family:var(--f-body);display:flex;justify-content:center;padding:22px 12px}
  button,select,input{font:inherit;color:inherit}
  :focus-visible{outline:3px solid var(--accent);outline-offset:2px}
  .app{width:100%;max-width:880px;background:var(--card);border-radius:36px;box-shadow:0 14px 44px rgba(91,124,250,.2);padding:26px 28px 24px}

  header{display:flex;align-items:center;gap:14px}
  .logo{width:56px;height:56px;border-radius:18px;background:var(--soft);display:grid;place-items:center;font-size:30px}
  h1{margin:0;font-family:var(--f-title);font-weight:400;font-size:1.65rem;letter-spacing:-.01em}
  header p{margin:2px 0 0;color:var(--muted);font-size:.95rem}

  .panel{margin-top:20px;padding:18px 20px;background:var(--soft);border-radius:26px;display:grid;gap:14px}
  .row{display:flex;align-items:center;gap:12px;flex-wrap:wrap}
  .lab{width:70px;flex:none;font-family:var(--f-title);font-size:1.05rem}
  .chips{display:flex;gap:7px;flex-wrap:wrap}
  .chip{width:42px;height:42px;border-radius:50%;border:0;color:#fff;font-family:var(--f-title);font-size:1.1rem;cursor:pointer;opacity:.5;transition:transform .15s,opacity .15s,box-shadow .15s}
  .chip:hover{opacity:.85}
  .chip[aria-pressed="true"]{opacity:1;transform:scale(1.14);box-shadow:0 0 0 3px #fff,0 0 0 5px var(--ink)}
  .search{position:relative;flex:1;min-width:210px}
  .search input{width:100%;padding:11px 18px;border:2px solid transparent;border-radius:999px;background:#fff;box-shadow:0 2px 8px rgba(43,51,80,.08)}
  .search input:focus{border-color:var(--accent);outline:none}
  .list{position:absolute;z-index:5;left:0;right:0;top:calc(100% + 6px);max-height:250px;overflow:auto;background:#fff;border-radius:18px;box-shadow:0 10px 30px rgba(43,51,80,.18);margin:0;padding:6px;list-style:none}
  .list[hidden]{display:none}
  .list li{display:flex;align-items:center;gap:8px;padding:9px 12px;border-radius:12px;cursor:pointer}
  .list li:hover,.list li.on{background:var(--soft)}
  .b{min-width:24px;height:24px;border-radius:12px;color:#fff;font-size:.78rem;display:inline-flex;align-items:center;justify-content:center;padding:0 7px;font-family:var(--f-title)}
  .rg{margin-left:auto;font-size:.75rem;color:var(--accent-d);background:#e3e9ff;border-radius:999px;padding:2px 9px}
  .none{color:var(--muted);cursor:default}
  select{padding:10px 16px;border:0;border-radius:999px;background:#fff;box-shadow:0 2px 8px rgba(43,51,80,.08);min-width:200px}
  .go{margin-left:auto;padding:12px 34px;border:0;border-radius:999px;background:var(--accent);color:#fff;font-family:var(--f-title);font-size:1.15rem;cursor:pointer;box-shadow:0 5px 0 var(--accent-d);transition:transform .1s,box-shadow .1s}
  .go:active{transform:translateY(4px);box-shadow:0 1px 0 var(--accent-d)}
  .msg{min-height:1.2em;font-size:.9rem;color:#d6403a;margin-top:-4px}

  [hidden]{display:none!important}
  .head{margin-top:24px;display:flex;align-items:center;gap:10px;flex-wrap:wrap}
  .head .t{font-family:var(--f-title);font-size:1.25rem}
  .lvl{margin-left:auto;padding:6px 16px;border-radius:999px;font-family:var(--f-title)}
  .lvl.low{background:var(--low)} .lvl.mid{background:var(--mid)} .lvl.high{background:var(--high)}

  .train{display:flex;align-items:flex-end;gap:3px;margin-top:18px;padding-bottom:12px;position:relative}
  .train::after{content:"";position:absolute;left:0;right:0;bottom:0;height:5px;border-radius:3px;background:repeating-linear-gradient(90deg,#c9d1ef 0 14px,transparent 14px 20px)}
  .cap{width:16px;height:58px;background:var(--ink);margin-bottom:12px}
  .cap.l{border-radius:30px 6px 6px 30px}.cap.r{border-radius:6px 30px 30px 6px}
  .cars{flex:1;display:grid;grid-template-columns:repeat(7,1fr);gap:5px}
  .car{display:flex;flex-direction:column;align-items:center;gap:6px;min-width:0;animation:pop .45s cubic-bezier(.3,1.5,.5,1) both;animation-delay:calc(var(--i)*60ms)}
  @keyframes pop{from{opacity:0;transform:translateY(16px) scale(.85)}to{opacity:1;transform:none}}
  .no{font-size:.85rem;color:var(--muted)}
  .best .no{color:var(--ink);font-family:var(--f-title)}
  .box{width:100%;height:100px;border-radius:20px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;position:relative;box-shadow:inset 0 -6px 0 rgba(43,51,80,.12)}
  .box .face{font-size:1.9rem;line-height:1}
  .box .pct{font-family:var(--f-title);font-size:1rem}
  .box.low{background:var(--low)}.box.mid{background:var(--mid)}.box.high{background:var(--high)}
  .star{position:absolute;top:-10px;right:-6px;font-size:1.2rem}
  .near{font-size:.68rem;line-height:1.2;text-align:center;color:var(--muted);min-height:2.4em}

  .lower{display:grid;grid-template-columns:230px 1fr;gap:18px;margin-top:6px;align-items:stretch}
  .legend{background:var(--soft);border-radius:24px;padding:18px 10px;display:flex;justify-content:space-around;align-items:center}
  .legend div{display:flex;flex-direction:column;align-items:center;gap:6px;font-size:.9rem}
  .dot{width:44px;height:44px;border-radius:50%;display:grid;place-items:center;font-size:1.4rem}
  .bubble{position:relative;background:var(--soft);border-radius:26px;padding:22px 28px;min-height:170px;display:flex;flex-direction:column;justify-content:center}
  .bubble::before{content:"";position:absolute;left:-10px;top:50%;margin-top:-10px;border:10px solid transparent;border-left:0;border-right-color:var(--soft)}
  .tag{align-self:flex-start;background:var(--accent);color:#fff;border-radius:999px;padding:3px 12px;font-size:.8rem;margin-bottom:8px}
  .big{margin:0;font-family:var(--f-title);font-size:2.1rem;line-height:1.3}
  .sub{margin:10px 0 0;color:var(--muted);font-size:.95rem;line-height:1.55}
  .hint{margin:24px 0 0;padding:34px 20px;border-radius:26px;background:var(--soft);text-align:center;color:var(--muted);line-height:1.7}
  .hint .e{font-size:2rem;display:block}
  .foot{margin:14px 0 0;color:var(--muted);font-size:.82rem;text-align:right}

  @media (max-width:640px){
    .app{padding:20px 14px;border-radius:26px}
    h1{font-size:1.3rem}.lab{width:100%}
    .go{width:100%;margin-left:0}select{width:100%}
    .lower{grid-template-columns:1fr}.bubble::before{display:none}
    .cars{gap:3px}.box{height:76px;border-radius:14px}.box .face{font-size:1.3rem}.box .pct{font-size:.78rem}
    .no{font-size:.7rem}.near{font-size:.58rem}.cap{width:9px;height:44px}
    .big{font-size:1.6rem}
  }
  @media (prefers-reduced-motion:reduce){.car{animation:none}.chip,.go{transition:none}}
</style>
</head>
<body>
<main class="app">
  <header>
    <div class="logo" aria-hidden="true">🚇</div>
    <div>
      <h1>지하철 칸별 혼잡도 확인</h1>
      <p>붐비는 칸 말고, 여유로운 칸으로 타요!</p>
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
      <button class="go" type="submit">확인</button>
    </div>
    <div class="msg" id="msg" role="alert"></div>
  </form>

  <section id="out" hidden>
    <div class="head">
      <span class="b" id="hLine"></span>
      <span class="t" id="hText"></span>
      <span class="lvl" id="hLvl"></span>
    </div>
    <div class="train">
      <span class="cap l"></span><div class="cars" id="cars"></div><span class="cap r"></span>
    </div>
    <div class="lower">
      <div class="legend">
        <div><span class="dot" style="background:var(--low)">😊</span>적음</div>
        <div><span class="dot" style="background:var(--mid)">😐</span>중간</div>
        <div><span class="dot" style="background:var(--high)">😫</span>많음</div>
      </div>
      <div class="bubble" aria-live="polite">
        <span class="tag">추천</span>
        <p class="big" id="rec"></p>
        <p class="sub" id="warn"></p>
      </div>
    </div>
    <p class="foot" id="time"></p>
  </section>
  <div class="hint" id="hint"><span class="e">🚉</span>노선과 역, 방향을 고르고 <b>확인</b>을 눌러 보세요.<br>다음 열차의 칸별 혼잡도를 알려드려요.</div>
</main>

<script>
/* ================= 데이터 ================= */
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
    st:"장암 도봉산 수락산 마들 노원 중계 하계 공릉 태릉입구 먹골 중화 상봉 면목 사가정 용마산 중곡 군자 어린이대공원 건대입구 뚝섬유원지 청담 강남구청 학동 논현 반포 고속터미널 내방 이수 남성 숭실대입구 상도 장승배기 신대방삼거리 보라매 신풍 대림 남구로 가산디지털단지 철산 광명사거리 천왕 온수 까치울 부천종합운동장 춘의 신중동 부천시청 상동 삼산체육관 굴포천 부평구청 산곡 석남"},
  "8":{color:"#E6186C",dir:["상행 (암사 방면)","하행 (모란 방면)"],
    st:"암사 천호 강동구청 몽촌토성 잠실 석촌 송파 가락시장 문정 장지 복정 남위례 산성 남한산성입구 단대오거리 신흥 수진 모란"},
  "9":{color:"#B8A77A",dir:["상행 (개화 방면)","하행 (중앙보훈병원 방면)"],
    st:"개화 김포공항 공항시장 신방화 마곡나루 양천향교 가양 증미 등촌 염창 신목동 선유도 당산 국회의사당 여의도 샛강 노량진 노들 흑석 동작 구반포 신반포 고속터미널 사평 신논현 언주 선정릉 삼성중앙 봉은사 종합운동장 삼전 석촌고분 석촌 송파나루 한성백제 올림픽공원 둔촌오륜 중앙보훈병원"}
};
Object.values(LINES).forEach(l => l.stations = l.st.split(" "));

/* 지역 태그 (1호선 충남·경기 남부 구간) — 지역 이름으로도 검색됩니다 */
const REGION = {};
[["천안시","두정 천안 봉명 쌍용 성환 직산"],["아산시","아산 배방 온양온천 신창"],["평택시","평택 지제 서정리 송탄 진위"]]
  .forEach(([r,s])=>s.split(" ").forEach(n=>REGION["1"+n]=r));
const regionOf=(line,st)=>REGION[line+st]||"";

/* 계단·에스컬레이터 근처 칸 (예시값 — 실제 정보는 키를 "노선+역이름"으로 추가: "1두정":[2,6]) */
const EXITS = {};

/* ================= 혼잡도 조회 =================
   지금은 (노선·역·방향·시간대)로 만든 "예시 데이터"입니다.
   실제 서비스에서는 이 함수 안을 fetch(...) 호출로 바꾸고,
   길이 7 배열 [0~100, ...] (칸별 혼잡도 %)만 돌려주면 나머지는 그대로 동작합니다. */
function rng(seed){return()=>{seed|=0;seed=seed+0x6D2B79F5|0;let t=Math.imul(seed^seed>>>15,1|seed);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
function hash(s){let h=2166136261;for(const c of s)h=Math.imul(h^c.charCodeAt(0),16777619);return h>>>0}
function exitCars(line,st){
  if(EXITS[line+st]) return EXITS[line+st];
  const r=rng(hash("exit"+line+st)), a=Math.floor(r()*CAR_COUNT)+1;
  let b=Math.floor(r()*CAR_COUNT)+1; if(b===a) b=a%CAR_COUNT+1;
  return [a,b].sort((x,y)=>x-y);
}
async function fetchCongestion(line,station,dirIdx){
  const now=new Date(), h=now.getHours()+now.getMinutes()/60, wk=now.getDay()%6!==0;
  const rush = wk ? Math.max(Math.exp(-((h-8.3)**2)/1.5), Math.exp(-((h-18.3)**2)/2)) : 0.25;
  const base = 0.25 + 0.5*rush;
  const bucket = Math.floor(now.getTime()/(5*60*1000));
  const r = rng(hash(line+station+dirIdx)+bucket);
  const near = exitCars(line,station);
  return Array.from({length:CAR_COUNT},(_,i)=>{
    const v = base + (r()-0.5)*0.55 + (near.includes(i+1)?0.22:-0.04);
    return Math.round(Math.min(1,Math.max(0.05,v))*100);
  });
}

/* ================= 유틸 ================= */
const LV = p => p<40?"low":p<70?"mid":"high";
const LVTXT = {low:"적음",mid:"중간",high:"많음"};
const FACE = {low:"😊",mid:"😐",high:"😫"};
const $ = id => document.getElementById(id);
const state = {line:"1", station:null};

/* ================= 노선 선택 ================= */
const chips=$("chips");
Object.entries(LINES).forEach(([n,l])=>{
  const b=document.createElement("button");
  b.type="button"; b.className="chip"; b.textContent=n; b.style.background=l.color;
  b.setAttribute("aria-label",n+"호선"); b.dataset.line=n;
  b.addEventListener("click",()=>setLine(n));
  chips.appendChild(b);
});
function setLine(n,keepStation){
  state.line=n;
  chips.querySelectorAll(".chip").forEach(c=>c.setAttribute("aria-pressed",c.dataset.line===n));
  $("dir").innerHTML="";
  LINES[n].dir.forEach((d,i)=>$("dir").add(new Option(d,i)));
  if(!keepStation){ state.station=null; $("q").value=""; }
  renderList();
}

/* ================= 역 검색 ================= */
const q=$("q"), list=$("list");
let items=[], active=-1;
function renderList(){
  const kw=q.value.trim().replace(/역$/,"");
  items=[];
  if(kw){
    for(const [n,l] of Object.entries(LINES))
      l.stations.forEach(s=>{ if(s.includes(kw)||regionOf(n,s).includes(kw)) items.push({line:n,st:s}); });
    items.sort((a,b)=>(a.line===state.line?0:1)-(b.line===state.line?0:1) || (a.st.startsWith(kw)?0:1)-(b.st.startsWith(kw)?0:1));
  }else{
    items=LINES[state.line].stations.map(s=>({line:state.line,st:s}));
  }
  items=items.slice(0,80); active=-1;
  list.innerHTML = items.length
    ? items.map((it,i)=>{const rg=regionOf(it.line,it.st);
        return `<li role="option" data-i="${i}"><span class="b" style="background:${LINES[it.line].color}">${it.line}</span>${it.st}역${rg?`<span class="rg">${rg}</span>`:""}</li>`}).join("")
    : `<li class="none">검색 결과가 없어요</li>`;
}
const openList=()=>{list.hidden=false;q.setAttribute("aria-expanded","true")};
const closeList=()=>{list.hidden=true;q.setAttribute("aria-expanded","false")};
function pick(i){
  const it=items[i]; if(!it) return;
  if(it.line!==state.line) setLine(it.line,true);
  state.station=it.st; q.value=it.st+"역"; $("msg").textContent=""; closeList();
}
q.addEventListener("focus",()=>{renderList();openList();});
q.addEventListener("input",()=>{state.station=null;renderList();openList();});
q.addEventListener("keydown",e=>{
  const lis=[...list.querySelectorAll("li[data-i]")];
  if(e.key==="ArrowDown"||e.key==="ArrowUp"){
    e.preventDefault(); openList();
    active=(active+(e.key==="ArrowDown"?1:-1)+lis.length)%Math.max(lis.length,1);
    lis.forEach((li,i)=>li.classList.toggle("on",i===active));
    lis[active]?.scrollIntoView({block:"nearest"});
  }else if(e.key==="Enter" && !list.hidden && active>=0){
    e.preventDefault(); pick(active);
  }else if(e.key==="Escape") closeList();
});
list.addEventListener("mousedown",e=>{const li=e.target.closest("li[data-i]"); if(li){e.preventDefault();pick(+li.dataset.i);}});
document.addEventListener("click",e=>{if(!e.target.closest(".search")) closeList();});

/* ================= 확인 ================= */
$("form").addEventListener("submit",async e=>{
  e.preventDefault();
  if(!state.station){
    const kw=q.value.trim().replace(/역$/,"");
    const hit=LINES[state.line].stations.includes(kw)?{line:state.line,st:kw}
      :Object.entries(LINES).map(([n,l])=>l.stations.includes(kw)?{line:n,st:kw}:null).find(Boolean);
    if(hit){ if(hit.line!==state.line) setLine(hit.line,true); state.station=hit.st; q.value=hit.st+"역"; }
  }
  if(!state.station){ $("msg").textContent="목록에서 역을 골라 주세요."; q.focus(); return; }
  $("msg").textContent="";
  const {line,station}=state, dirIdx=+$("dir").value;
  let data;
  try{ data=await fetchCongestion(line,station,dirIdx); }
  catch{ $("msg").textContent="혼잡도를 불러오지 못했어요. 잠시 뒤 다시 시도해 주세요."; return; }
  show(line,station,dirIdx,data);
});

function show(line,station,dirIdx,data){
  const near=exitCars(line,station), lv=data.map(LV);
  const avg=Math.round(data.reduce((a,b)=>a+b,0)/data.length);
  const min=Math.min(...data), best=data.indexOf(min)+1;

  $("hLine").textContent=line+"호선"; $("hLine").style.background=LINES[line].color;
  $("hText").textContent=`${station}역 · ${LINES[line].dir[dirIdx]}`;
  $("hLvl").textContent=`전체 ${LVTXT[LV(avg)]} (약 ${avg}%)`; $("hLvl").className="lvl "+LV(avg);

  $("cars").innerHTML=data.map((p,i)=>`
    <div class="car ${i+1===best?"best":""}" style="--i:${i}">
      <span class="no">${i+1}호차</span>
      <div class="box ${lv[i]}" role="img" aria-label="${i+1}호차 혼잡도 ${LVTXT[lv[i]]} ${p}%">
        ${i+1===best?'<span class="star">⭐</span>':""}
        <span class="face">${FACE[lv[i]]}</span><span class="pct">${p}%</span>
      </div>
      <span class="near">${near.includes(i+1)?"계단·에스컬<br>레이터 근처":""}</span>
    </div>`).join("");

  const low=lv.map((v,i)=>v==="low"?i+1:0).filter(Boolean);
  const high=lv.map((v,i)=>v==="high"?i+1:0).filter(Boolean);
  $("rec").innerHTML = low.length ? `${low.join(",")}호차<br>여유있음`
    : lv.includes("mid") ? `${best}호차가<br>제일 한산해요` : `모든 칸이 붐벼요<br>다음 열차를 추천해요`;
  const jam=near.filter(n=>lv[n-1]==="high");
  $("warn").textContent = jam.length
    ? `${jam.join(",")}호차는 계단·에스컬레이터 근처라 사람이 몰려요. 한산한 칸으로 이동해 주세요.`
    : high.length ? `${high.join(",")}호차가 붐벼요. 한산한 칸을 이용해 주세요.` : "대부분의 칸이 여유로워요.";
  $("time").textContent=`${new Date().toLocaleTimeString("ko-KR")} 기준 · 예시 데이터`;

  $("hint").hidden=true; $("out").hidden=false;
}

setLine("1");
</script>
</body>
</html>
'''

components.html(HTML, height=1050, scrolling=True)
