<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>지하철 칸별 혼잡도 확인</title>
  <style>
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }

    body {
      background-color: #f0f2f5;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      padding: 20px;
    }

    /* 메인 대시보드 카드 */
    .dashboard-card {
      background: #ffffff;
      border: 3px solid #222222;
      border-radius: 30px;
      padding: 30px;
      width: 100%;
      max-width: 820px;
      box-shadow: 0 12px 28px rgba(0, 0, 0, 0.12);
    }

    /* 상단 타이틀 */
    .dashboard-title {
      text-align: center;
      font-size: 26px;
      font-weight: 800;
      margin-bottom: 22px;
      color: #111111;
      letter-spacing: -0.5px;
    }

    /* 선택 바 */
    .selector-bar {
      background-color: #d8e8ff;
      border: 2px solid #333333;
      border-radius: 12px;
      padding: 14px 24px;
      display: flex;
      align-items: center;
      justify-content: space-around;
      margin-bottom: 28px;
    }

    .selector-group {
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 18px;
      font-weight: 700;
      color: #222222;
    }

    .selector-group select {
      padding: 8px 16px;
      font-size: 16px;
      font-weight: 700;
      border: 2px solid #333333;
      border-radius: 6px;
      background-color: #ffffff;
      cursor: pointer;
      outline: none;
    }

    .selector-group select:focus {
      border-color: #0056b3;
    }

    .divider {
      width: 2px;
      height: 28px;
      background-color: #666666;
    }

    /* 지하철 표현 구역 */
    .train-container {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      margin-bottom: 30px;
      padding: 10px 0;
    }

    .train-cap {
      width: 16px;
      height: 76px;
      border: 2px solid #333333;
      background-color: #cccccc;
      margin-top: 31px;
    }
    .train-cap.left { border-radius: 10px 0 0 10px; }
    .train-cap.right { border-radius: 0 10px 10px 0; }

    .car-list {
      display: flex;
      gap: 10px;
      width: 100%;
      justify-content: space-between;
      margin: 0 8px;
    }

    .car-item {
      display: flex;
      flex-direction: column;
      align-items: center;
      flex: 1;
    }

    .car-label {
      font-size: 16px;
      font-weight: 700;
      margin-bottom: 8px;
      color: #333333;
    }

    .car-box {
      width: 100%;
      height: 76px;
      border: 2px solid #333333;
      border-radius: 14px;
      transition: background-color 0.3s ease;
      box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.08);
    }

    /* 혼잡도 색상 상태 */
    .status-green { background-color: #00e600; }  /* 적음 */
    .status-yellow { background-color: #ffea00; } /* 중간 */
    .status-red { background-color: #ff2222; }    /* 많음 */

    /* 승강장 시설 아이콘 */
    .facility-badge {
      margin-top: 8px;
      font-size: 12px;
      font-weight: 700;
      color: #444444;
      height: 24px;
      text-align: center;
      line-height: 1.2;
    }

    /* 하단 레이아웃 */
    .bottom-section {
      display: flex;
      gap: 20px;
      align-items: stretch;
    }

    .left-panel {
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      width: 220px;
      gap: 14px;
    }

    /* 범례 박스 */
    .legend-box {
      border: 2px solid #333333;
      padding: 16px;
      border-radius: 8px;
      display: flex;
      justify-content: space-around;
      align-items: center;
      background: #fafafa;
    }

    .legend-item {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 6px;
      font-size: 14px;
      font-weight: 700;
      color: #333333;
    }

    .circle {
      width: 38px;
      height: 38px;
      border-radius: 50%;
      border: 2px solid #333333;
    }

    /* 새로고침 버튼 */
    .btn-refresh {
      padding: 12px;
      font-size: 16px;
      font-weight: 800;
      border: 2px solid #333333;
      background-color: #ffffff;
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.2s ease;
      color: #222222;
    }

    .btn-refresh:hover {
      background-color: #e2e2e2;
    }

    .btn-refresh:active {
      transform: scale(0.98);
    }

    /* 안내 메시지 전용 패널 */
    .recommendation-panel {
      flex: 1;
      border: 2px solid #333333;
      border-radius: 8px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      text-align: center;
      background-color: #fafafa;
      min-height: 130px;
    }

    .recommendation-text {
      font-size: 36px;
      font-weight: 900;
      line-height: 1.25;
      color: #111111;
      word-break: keep-all;
    }

    .recommendation-subtext {
      font-size: 13px;
      color: #666666;
      margin-top: 10px;
      font-weight: 600;
    }

    /* 반응형 레이아웃 대응 */
    @media (max-width: 640px) {
      .selector-bar {
        flex-direction: column;
        gap: 10px;
      }
      .divider {
        display: none;
      }
      .bottom-section {
        flex-direction: column;
      }
      .left-panel {
        width: 100%;
      }
      .recommendation-text {
        font-size: 28px;
      }
    }
  </style>
</head>
<body>

  <div class="dashboard-card">
    <div class="dashboard-title">지하철 칸별 혼잡도 확인</div>

    <!-- 노선 및 역 선택 구역 -->
    <div class="selector-bar">
      <div class="selector-group">
        <label for="lineSelect">노선선택</label>
        <select id="lineSelect">
          <option value="1호선">1호선</option>
          <option value="2호선" selected>2호선</option>
          <option value="3호선">3호선</option>
        </select>
      </div>
      <div class="divider"></div>
      <div class="selector-group">
        <label for="stationSelect">역 선택</label>
        <select id="stationSelect">
          <!-- 스크립트에서 동적 로드됩니다 -->
        </select>
      </div>
    </div>

    <!-- 열차 칸 및 승강장 시설 표시 구역 -->
    <div class="train-container">
      <div class="train-cap left"></div>
      <div class="car-list" id="carList">
        <!-- 스크립트에서 동적 생성됩니다 -->
      </div>
      <div class="train-cap right"></div>
    </div>

    <!-- 하단 상태 범례 및 추천 메시지 -->
    <div class="bottom-section">
      <div class="left-panel">
        <div class="legend-box">
          <div class="legend-item">
            <div class="circle status-green"></div>
            <span>적음</span>
          </div>
          <div class="legend-item">
            <div class="circle status-yellow"></div>
            <span>중간</span>
          </div>
          <div class="legend-item">
            <div class="circle status-red"></div>
            <span>많음</span>
          </div>
        </div>
        <button id="refreshBtn" class="btn-refresh" type="button">새로고침</button>
      </div>

      <div class="recommendation-panel">
        <div class="
      
