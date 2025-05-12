# 🍽️ NTU Food Guide / NTU Food Hunter

本專案旨在打造一個專屬台大學生的美食搜尋與推薦平台，結合餐廳篩選、評分排序、地圖標示與互動式推薦，幫助使用者快速找到「當下最適合」的餐廳。

---

## 📦 專案架構比較

### 方案一: 原始架構（Flask + 前後端分離）

- 適合正式部署、多頁應用、自訂 UI 複雜流程

ntu-foodmap/
├── backend/ # Python 後端
│ ├── app.py # 入口點
│ ├── models/ # ORM 資料模型
│ ├── routes/ # API 路由
│ ├── services/ # 業務邏輯 / API 整合
│ ├── database/ # 資料庫連線與初始資料
│ └── requirements.txt # Python 套件清單
├── frontend/ # 前端靜態頁面
│ ├── index.html # 首頁入口
│ ├── js/ # 地圖與互動功能 JS
│ ├── css/ # 客製樣式（可用 Tailwind）
│ └── assets/ # 圖片、icon 等
├── data/ # 餐廳種子資料
│ └── restaurants.json
├── .env # API 金鑰（勿上傳）
├── .gitignore # 忽略的檔案類型
├── README.md
└── run.sh / start.sh # 本地啟動腳本


---


### 方案二: 精簡架構（Streamlit 快速部署版）

- 適合期末專案快速開發、部署與展示 
- 全 Python 編寫  
- 可用 [Streamlit Cloud](https://streamlit.io/cloud) 一鍵部署

ntu-food-hunter/
├── app/
│ ├── main.py # 主介面（首頁、搜尋、顯示結果）
│ ├── components/ # 拆出模組：卡片、元件
│ ├── logic/ # 選單邏輯、距離計算等函式
│ └── data/ # 餐廳清單（CSV）
├── .streamlit/
│ └── config.toml # 頁面寬度與標題設定
├── requirements.txt # pip 套件安裝清單
├── .gitignore # 忽略 pycache、env 等
└── README.md

---

## 功能規劃（核心）

- 餐廳條件篩選（價位、類型、地區、營業中）
- 心情推薦：「我現在想…」 → 自動篩選邏輯
- 綜合排序：評分 × 距離 × 偏好加權
- 一鍵抽餐廳（懶人模式）
- 熱門排行榜（以評分與評論數排序）
- 地圖標記餐廳位置（使用 Streamlit Folium）
- 使用者互動（收藏、喜好、打星）＊限本地端記憶

---

## 🛠 安裝與執行

```bash
# 安裝依賴套件
pip install -r requirements.txt

# 執行主程式（Streamlit 版本）
streamlit run app/main.py
```