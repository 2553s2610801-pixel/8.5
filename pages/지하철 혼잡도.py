<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>지하철 칸별 혼잡도 확인</title>
  <style>
    * {
      box-sizing: border-box;
      font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    body {
      background-color: #f5f5f7;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      margin: 0;
      padding: 20px;
    }

    /* 메인 컨테이너 (와이어프레임 외곽 레이아웃) */
    .dashboard-card {
      background: #ffffff;
      border: 3px solid #333;
      border-radius: 40px;
      padding: 25px;
      width: 100%;
      max-width: 800px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.1);
      position: relative;
    }

    /* 상단 타이틀 */
    .dashboard-title {
      text-align: center;
      font-size: 24px;
      font-weight: bold;
      margin-bottom: 20px;
      color: #222;
    }

    /* 노선 및 역 선택 바 */
    .selector-bar {
      background-color: #dbeaff;
      border: 2px solid #555;
      border-radius: 8px;
      padding: 12px 20px;
      display: flex;
      align-items: center;
      justify-content: space-around;
      margin-bottom: 25px;
    }

    .selector-group {
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 18px;
      font-weight: 600;
    }

    .selector-group select {
      padding: 6px 16px;
      font-size: 16px;
      font-weight: bold;
      border: 2px solid #333;
      border-radius: 4px;
      background-color: #fff;
      cursor: pointer;
    }

    .divider {
      width: 2px;
      height: 25px;
      background-color: #777;
    }

    /* 지하철 열차 영역 */
    .train-container {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 30px;
      position: relative;
      padding: 0 10px;
    }

    /* 열차 프론트/리어 캡 */
    .train-cap {
      width: 15px;
      height: 70px;
      border: 2px solid #333;
      background-color: #ddd;
    }
    .train-cap.left { border-radius: 12px 0 0 12px; }
    .train-cap.right { border-radius: 0 12px 12px 0; }

    .car-list {
      display: flex;
      gap: 8px;
      width: 100%;
      justify-content: space-around;
      margin: 0 10px;
    }

    .car-item {
      display: flex;
      flex-direction: column;
      align-items: center;
      flex: 1;
    }

    .car-label {
      font-size: 16px;
      font-weight: bold;
      margin-bottom: 8px;
    }

    .car-box {
      width: 100%;
      height: 70px;
      border: 2px solid #333;
      border-radius: 12px;
      transition: all 0.3s ease;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      font-size: 12px;
      font-weight: bold;
      color: #333;
      box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
    }

    /* 혼잡도 색상 규격 */
    .status-green { background-color: #00e600; }  /* 적음 */
    .status-yellow { background-color: #ffff00; } /* 중간 */
    .status-red { background-color: #ff0000; color: #fff; }    /* 많음 */

    /* 승강장 시설 아이콘 표시 */
    .facility-badge {
      margin-top: 6px;
      font-size: 12px;
      color: #555;
      height: 20px;
    }

    /* 하단 정보 섹션 */
    .bottom-section {
      display: flex;
      gap: 20px
      
