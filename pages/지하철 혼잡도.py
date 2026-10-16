<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>지하철 칸별 혼잡도 확인</title>
<style>
  :root{
    --bg:#eef1f4; --panel:#fff; --ink:#1d2430; --muted:#5d6775; --bar:#cfe2f3;
    --low:#2fd24a; --mid:#ffe83a; --high:#f5271f; --accent:#1a5fd0;
  }
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);font-family:"Pretendard","Noto Sans KR","Malgun Gothic",sans-serif;display:flex;justify-content:center;padding:24px 12px}
  .app{width:100%;max-width:860px;background:var(--panel);border:1px solid var(--ink);border-radius:44px;padding-bottom:28px}
  h1{margin:0;padding:22px 0 14px;text-align:center;font-size:1.15rem;font-weight:500;border-bottom:1px solid var(--ink)}
  .wrap{padding:0 28px}
  button,select,input{font:inherit}
  button:focus-visible,select:focus-visible,input:focus-visible{outline:3px solid var(--accent);outline-offset:2px}

  .panel{margin-top:18px;padding:16px 20px;background:var(--bar);border:1px solid var(--ink);display:grid;gap:14px}
  .row{display:flex;align-items:center;gap:12px;flex-wrap:wrap}
  .row > .lab{width:72px;flex:none;font-size:1rem}
  .chips{display:flex;gap:6px;flex-wrap:wrap}
  .chip{width:40px;height:40px;border-radius:50%;border:2px solid transparent;color:#fff;font-weight:700;cursor:pointer;opacity:.55}
  .chip[aria-pressed="true"]{opacity:1;border-color:var(--ink);box-shadow:0 0 0 2px #fff inset}
  .search{position:relative;flex:1;min-width:200px}
  .search input{width:100%;padding:9px 12px;border:1px solid var(--ink);background:#fff}
  .list{position:absolute;z-index:5;left:0;right:0;top:100%;max-height:240px;overflow:auto;background:#fff;border:1px solid var(--ink);border-top:0;margin:0;padding:0;list-style:none}
  .list[hidden]{display:none}
  .list li{display:flex;align-items:center;gap:8px;padding:8px 12px;cursor:pointer}
  .list li:hover,.list li.on{background:#e6eefb}
  .list .b{min-width:22px;height:22px;border-radius:11px;color:#fff;font-size:.72rem;font-weight:700;display:inline-flex;align-items:center;justify-content:center;padding:0 6px}
  .list .none{cursor:default;color:var(--muted)}
  select{padding:8px 10px;border:1px solid var(--ink);background:#fff;min-width:140px}
  .go{padding:10px 26px;border:1px solid var(--ink);background:var(--ink);color:#fff;font-weight:700;cursor:pointer;margin-left:auto}
  .go:hover{background:#2f3a4a}
  .msg{min-height:1.3em;font-size:.88rem;color:#b3261e}

  #out[hidden]{display:none}
  .head{margin-top:22px;display:flex;align-items:center;gap:10px;flex-wrap:wrap}
  .head .b{height:26px;min-width:26px;border-radius:13px;color:#fff;font-weight:700;display:inline-flex;align-items:center;justify-content:center;padding:0 8px}
  .head .t{font-size:1.05rem}
  .head .lvl{margin-left:auto;padding:4px 12px;border:1px solid var(--ink);border-radius:16px;font-weight:700;font-size:.9rem}
  .lvl.low{background:var(--low)} .lvl.mid{background:var(--mid)} .lvl.high{background:var(--high);color:#fff}

  .train{display:flex;align-items:flex-end;gap:2px;margin-top:14px}
  .cap{width:14px;height:44px;border:1px solid var(--ink)}
  .cap.l{border-right:0;border-radius:10px 0 0 10px}
  .cap.r{border-left:0;border-radius:0 10px 10px 0}
  .cars{flex:1;display:grid;grid-template-columns:repeat(7,1fr);gap:4px}
  .car{display:flex;flex-direction:column;gap:6px;min-width:0}
  .car .no{text-align:center;font-size:.95rem}
  .car .box{height:68px;border:1px solid var(--ink);border-radius:8px;display:flex;flex-direction:column;align-items:center;justify-content:center;font-weight:700;font-size:.8rem;color:#111}
  .car .box small{font-weight:400;font-size:.72rem}
  .box.low{background:var(--low)} .box.mid{background:var(--mid)} .box.high{background:var(--high);color:#fff}
  .car .near{text-align:center;font-size:.68rem;color:var(--muted);min-height:2.2em;line-height:1.1}
  .car.best .no{font-weight:700}

  .lower{display:grid;grid-template-columns:240px 1fr;gap:20px;margin-top:12px}
  .legend{border:1px solid var(--ink);padding:16px 12px;display:flex;justify-content:space-around;height:fit-content}
  .legend div{display:flex;flex-direction:column;align-items:center;gap:6px;font-size:.9rem}
  .dot{width:42px;height:42px;border-radius:50%;border:1px solid var(--ink)}
  .result{border:1px solid var(--ink);padding:22px 26px;min-height:180px;display:flex;flex-direction:column;justify-content:center}
  .result .big{font-size:1.9rem;line-height:1.35;font-weight:500;margin:0}
  .result .sub{margin:12px 0 0;color:var(--muted);font-size:.92rem;line-height:1.5}
  .hint{margin:26px 0 0;padding:30px;border:1px dashed var(--ink);text-align:center;color:var(--muted)}
  .foot{margin-top:14px;color:var(--muted);font-size:.85rem}

  @media (max-width:640px){
    .app{border-radius:26px}.wrap{padding:0 14px}
    .row > .lab{width:100%}
    .go{width:100%;margin-left:0}
    .lower{grid-template-columns:1fr}
    .cap{width:8px}.cars{gap:3px}
    .car .box{height:56px;font-size:.7rem}.car .no{font-size:.75rem}.car .near{font-size:.6rem}
    .result .big{font-size:1.5rem}
  }
</style>
</head>
<body>
<main class="app">
  <h1>지하철 칸별 혼잡도 확인</h1>
  <div class="wrap">
    <form class="panel" id="form" autocomplete="off">
      <div class="row"><span class="lab">노선선택</span><div class="chips" id="chips"></div></div>
      <div class="row">
        <span class="lab">역 선택</span>
        <div class="search">
          <input id="q" type="text" placeholder="역 이름을 검색하세요 (예: 강남)" role="combobox" aria-expanded="false" aria-controls="list">
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
          <div><span class="dot" style="background:var(--low)"></span>적음</div>
          <div><span class="dot" style="background:var(--mid)"></span>중간</div>
          <div><span class="dot" style="background:var(--high)"></span>많음</div>
        </div>
        <div class="result" aria-live="polite">
          <p class="big" id="rec"></p>
          <p class="sub" id="warn"></p>
        </div>
      </div>
      <p class="foot" id="time"></p>
    </section>
    <p class="hint" id="hint">노선과 역, 방향을 선택하고 <b>확인</b>을 누르면 다음 열차의 칸별 혼잡도가 표시됩니다.</p>
  </div>
</main>

<script>
/* ================= 데이터 ================= */
const CAR_COUNT = 7;

const LINES = {
  "1":{color:"#0052A4",dir:["상행 (소요산 방면)","하행 (인천·신창 방면)"],
       st:"소요산 동두천 보산 의정부 회룡 도봉산 창동 광운대 석계 신이문 외대앞 회기 청량리 제기동 신설동 동묘앞 동대문 종로5가 종로3가 종각 시청 서울역 남영 용산 노량진 대방 신길 영등포 신도림 구로 가산디지털단지 금천구청 안양 군포 수원 병점 오산 평택 천안 인천"},
  "2":{color:"#00A84D",dir:["내선순환","외선순환"],
       st:"시청 을지로입구 을지로3가 을지로4가 동대문역사문화공원 신당 상왕십리 왕십리 한양대 뚝섬 성수 건대입구 구의 강변 잠실나루 잠실 잠실새내 종합운동장 삼성 선릉 역삼 강남 교대 서초 방배 사당 낙성대 서울대입구 봉천 신림 신대방 구로디지털단지 대림 신도림 문래 영등포구청 당산 합정 홍대입구 신촌 이대 아현 충정로"},
  "3":{color:"#EF7C1C",dir:["상행 (대화 방면)","하행 (오금 방면)"],
       st:"대화 주엽 정발산 마두 백석 대곡 연신내 불광 녹번 홍제 무악재 독립문 경복궁 안국 종로3가 을지로3가 충무로 동대입구 약수 금호 옥수 압구정 신사 잠원 고속터미널 교대 남부터미널 양재 매봉 도곡 대치 학여울 대청 일원 수서 가락시장 경찰병원 오금"},
  "4":{color:"#00A5DE",dir:["상행 (당고개 방면)","하행 (오이도 방면)"],
       st:"당고개 상계 노원 창동 쌍문 수유 미아 길음 성신여대입구 한성대입구 혜화 동대문 동대문역사문화공원 충무로 명동 회현 서울역 숙대입구 삼각지 신용산 이촌 동작 총신대입구 사당 남태령 선바위 경마공원 대공원 과천 정부과천청사 인덕원 평촌 범계 금정 산본 오이도"},
  "5":{color:"#996CAC",dir:["상행 (방화 방면)","하행 (상일동·마천 방면)"],
       st:"방화 개화산 김포공항 송정 마곡 발산 우장산 화곡 까치산 신정 목동 오목교 양평 영등포구청 영등포시장 신길 여의도 여의나루 마포 공덕 애오개 충정로 서대문 광화문 종로3가 을지로4가 동대문역사문화공원 청구 신금호 행당 왕십리 마장 답십리 장한평 군자 아차산 광나루 천호 강동 길동 둔촌동 올림픽공원 방이 오금 개롱 거여 마천 상일동"},
  "6":{color:"#CD7C2F",dir:["상행 (응암 방면)","하행 (봉화산 방면)"],
       st:"응암 역촌 불광 독바위 연신내 구산 새절 증산 디지털미디어시티 월드컵경기장 마포구청 망원 합정 상수 광흥창 대흥 공덕 효창공원앞 삼각지 녹사평 이태원 한강진 버티고개 약수 청구 신당 동묘앞 창신 보문 안암 고려대 월곡 상월곡 돌곶이 석계 태릉입구 화랑대 봉화산"},
  "7":{color:"#747F00",dir:["상행 (장암 방면)","하행 (부평구청 방면)"],
       st:"장암 도봉산 수락산 마들 노원 중계 하계 공릉 태릉입구 먹골 중화 상봉 면목 사가정 용마산 중곡 군자 어린이대공원 건대입구 뚝섬유원지 청담 강남구청 학동 논현 반포 고속터미널 내방 이수 남성 숭실대입구 상도 장승배기 신대방삼거리 보라매 신풍 대림 남구로 가산디지털단지 철산 광명사거리 천왕 온수"},
  "8":{color:"#E6186C",dir:["상행 (암사 방면)","하행 (모란 방면)"],
       st:"암사 천호 강동구청 몽촌토성 잠실 석촌 송파 가락시장 문정 장지 복정 남위례 산성 남한산성입구 단대오거리 신흥 수진 모란"},
  "9":{color:"#BDB092",dir:["상행 (개화 방면)","하행 (중앙보훈병원 방면)"],
       st:"개화 김포공항 공항시장 신방화 마곡나루 양천향교 가양 증미 등촌 염창 신목동 선유도 당산 국회의사당 여의도 샛강 노량진 노들 흑석 동작 구반포 신반포 고속터미널 사평 신논현 언주 선정릉 삼성중앙 봉은사 종합운동장"}
};
Object.values(LINES).forEach(l => l.stations = l.st.split(" "));

/* 계단·에스컬레이터 근처 칸 (예시값 — 실제 승강장 정보로 교체) */
const EXITS = {};

/* ================= 혼잡도 조회 =================
   지금은 (노선·역·방향·시간대)로 만든 "예시 데이터"입니다.
   실제 서비스에서는 이 함수 안을 fetch(...) 호출로 바꾸고,
   길이 7 배열 [0~100, ...] (칸별 혼잡도 %) 만 돌려주면 나머지는 그대로 동작합니다. */
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
  const bucket = Math.floor(now.getTime()/(5*60*1000));          // 5분마다 값이 바뀜
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
const $ = id => document.getElementById(id);
const state = {line:"2", station:null};

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
      l.stations.forEach(s=>{ if(s.includes(kw)) items.push({line:n,st:s}); });
    items.sort((a,b)=>(a.line===state.line?0:1)-(b.line===state.line?0:1) || (a.st.startsWith(kw)?0:1)-(b.st.startsWith(kw)?0:1));
  }else{
    items=LINES[state.line].stations.map(s=>({line:state.line,st:s}));
  }
  items=items.slice(0,60); active=-1;
  list.innerHTML = items.length
    ? items.map((it,i)=>`<li role="option" data-i="${i}"><span class="b" style="background:${LINES[it.line].color}">${it.line}</span>${it.st}역</li>`).join("")
    : `<li class="none">검색 결과가 없습니다</li>`;
}
function open(){ list.hidden=false; q.setAttribute("aria-expanded","true"); }
function close(){ list.hidden=true; q.setAttribute("aria-expanded","false"); }
function pick(i){
  const it=items[i]; if(!it) return;
  if(it.line!==state.line) setLine(it.line,true);
  state.station=it.st; q.value=it.st+"역"; $("msg").textContent=""; close();
}
q.addEventListener("focus",()=>{renderList();open();});
q.addEventListener("input",()=>{state.station=null;renderList();open();});
q.addEventListener("keydown",e=>{
  const lis=[...list.querySelectorAll("li[data-i]")];
  if(e.key==="ArrowDown"||e.key==="ArrowUp"){
    e.preventDefault(); open();
    active=(active+(e.key==="ArrowDown"?1:-1)+lis.length)%Math.max(lis.length,1);
    lis.forEach((li,i)=>li.classList.toggle("on",i===active));
    lis[active]?.scrollIntoView({block:"nearest"});
  }else if(e.key==="Enter" && !list.hidden && active>=0){
    e.preventDefault(); pick(active);
  }else if(e.key==="Escape") close();
});
list.addEventListener("mousedown",e=>{ const li=e.target.closest("li[data-i]"); if(li){e.preventDefault();pick(+li.dataset.i);} });
document.addEventListener("click",e=>{ if(!e.target.closest(".search")) close(); });

/* ================= 확인 ================= */
$("form").addEventListener("submit",async e=>{
  e.preventDefault();
  /* 입력창에 이름만 치고 확인을 눌러도, 정확히 일치하는 역이 있으면 선택 처리 */
  if(!state.station){
    const kw=q.value.trim().replace(/역$/,"");
    const hit=LINES[state.line].stations.includes(kw)?{line:state.line,st:kw}
             :Object.entries(LINES).map(([n,l])=>l.stations.includes(kw)?{line:n,st:kw}:null).find(Boolean);
    if(hit){ if(hit.line!==state.line) setLine(hit.line,true); state.station=hit.st; q.value=hit.st+"역"; }
  }
  if(!state.station){ $("msg").textContent="목록에서 역을 선택해 주세요."; q.focus(); return; }
  $("msg").textContent="";
  const {line,station}=state, dirIdx=+$("dir").value;
  let data;
  try{ data=await fetchCongestion(line,station,dirIdx); }
  catch{ $("msg").textContent="혼잡도를 불러오지 못했습니다. 잠시 후 다시 시도해 주세요."; return; }
  show(line,station,dirIdx,data);
});

function show(line,station,dirIdx,data){
  const near=exitCars(line,station), lv=data.map(LV);
  const avg=Math.round(data.reduce((a,b)=>a+b,0)/data.length);

  $("hLine").textContent=line+"호선"; $("hLine").style.background=LINES[line].color;
  $("hText").textContent=`${station}역 · ${LINES[line].dir[dirIdx]}`;
  $("hLvl").textContent=`전체 ${LVTXT[LV(avg)]} (약 ${avg}%)`; $("hLvl").className="lvl "+LV(avg);

  const min=Math.min(...data);
  $("cars").innerHTML=data.map((p,i)=>`
    <div class="car ${p===min?"best":""}">
      <span class="no">${i+1}호차</span>
      <div class="box ${lv[i]}" role="img" aria-label="${i+1}호차 혼잡도 ${LVTXT[lv[i]]} ${p}%">${LVTXT[lv[i]]}<small>${p}%</small></div>
      <span class="near">${near.includes(i+1)?"계단·에스컬레이터<br>근처":""}</span>
    </div>`).join("");

  const low=lv.map((v,i)=>v==="low"?i+1:0).filter(Boolean);
  const mid=lv.map((v,i)=>v==="mid"?i+1:0).filter(Boolean);
  const high=lv.map((v,i)=>v==="high"?i+1:0).filter(Boolean);
  $("rec").innerHTML = low.length ? `${low.join(",")}호차<br>여유있음`
    : mid.length ? `${data.indexOf(min)+1}호차가<br>가장 한산함` : `전 칸 혼잡<br>다음 열차 권장`;
  const jam=near.filter(n=>lv[n-1]==="high");
  $("warn").textContent = jam.length
    ? `${jam.join(",")}호차는 계단·에스컬레이터 근처라 승객이 몰립니다. 한산한 칸으로 이동해 주세요.`
    : high.length ? `${high.join(",")}호차가 혼잡합니다. 한산한 칸을 이용해 주세요.` : "대부분의 칸이 여유롭습니다.";
  $("time").textContent=`${new Date().toLocaleTimeString("ko-KR")} 기준 · 예시 데이터`;

  $("hint").hidden=true; $("out").hidden=false;
}

setLine("2");
</script>
</body>
</html>
