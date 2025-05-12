# NTU_foodguide


ntu-foodmap/
├── backend/                     # Python (Flask or FastAPI)
│   ├── app.py                   # Main app entry
│   ├── models/                  # DB models (if using ORM like SQLAlchemy)
│   │   └── restaurant.py
│   ├── routes/                  # API routes
│   │   ├── __init__.py
│   │   └── restaurants.py
│   ├── services/                # Business logic or external API calls
│   │   └── google_maps.py
│   ├── database/                # DB connection & seed data
│   │   └── db.py
│   └── requirements.txt         # Python dependencies

├── frontend/                    # Static frontend
│   ├── index.html               # Entry point
│   ├── js/
│   │   └── main.js              # Handles fetch(), map rendering, etc.
│   ├── css/
│   │   └── styles.css           # Tailwind or custom styles
│   └── assets/                  # Images, icons, etc.

├── data/                        # Optional: seed data or scraped results
│   └── restaurants.json

├── .env                         # API keys (NEVER commit this!)
├── .gitignore                   # Ignore virtualenv, .env, etc.
├── README.md
└── run.sh / start.sh            # Run scripts for dev

//new ver.
ntu-food-hunter/
├── app/
│   ├── main.py                  ← Streamlit 主程式（首頁 + 篩選 + 顯示）
│   ├── components/              ← 子區塊：卡片、篩選器等（可拆開寫）
│   │   └── restaurant_card.py
│   ├── logic/
│   │   ├── filter_logic.py      ← 篩選與排序邏輯
│   │   └── distance_utils.py    ← geopy 計算距離
│   └── data/
│       └── restaurants.csv      ← 你們已清理好的餐廳資料
│
├── .streamlit/
│   └── config.toml              ← 設定標題、頁面寬度（部署用）
│
├── requirements.txt             ← pip 套件清單
├── .gitignore                   ← 忽略 .env、__pycache__、pkl 等
└── README.md
