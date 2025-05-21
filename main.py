import streamlit as st
import pandas as pd
from app.logic.filter_logic import RestaurantFilter
from app.components.restaurant_card import render_card
from datetime import datetime

# 網站基本設定
st.set_page_config(page_title="NTU Food Hunter", layout="wide")

# 🔺 頁面標題區塊（包含主標、副標與說明）
st.markdown(
    """
    <div style="text-align: left; line-height: 1.6; margin-bottom: 1.2rem;">
        <div style="font-size: 2rem; font-weight: bold; color: #9D3327; margin-bottom: 0.3rem;">
            NTU Food Hunter
        </div>
        <div style="font-size: 1.3rem; font-weight: bold; color: #676B18; margin-bottom: 0.3rem;">
            最懂你的台大美食導航🍜
        </div>
        <div style="font-size: 1rem; color: #444; margin-top: 0.2rem;">
            根據地區、類型和心情推薦餐廳！
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# 📂 載入餐廳資料與初始化篩選器物件
data_path = "app/data/restaurants.csv"
filter_obj = RestaurantFilter(data_path)
df = filter_obj.df.copy()

# 📋 Sidebar 區塊
st.sidebar.title("一般篩選器")

# 工具函式
def extract_tags(series, delimiter=","):
    return sorted(set(
        tag.strip()
        for items in series.dropna().astype(str)
        for tag in items.split(delimiter)
        if tag.strip() and tag.strip().lower() != "none"
    ))

def filter_contains(df, column, selected, delimiter=","):
    return df[df[column].dropna().astype(str).apply(
        lambda x: any(sel in [tag.strip() for tag in x.split(delimiter)] for sel in selected)
    )]

# 資料欄位預處理
df["price_level"] = df["price_level"].astype(str).str.strip()
price_map = {"1.0": "平價", "2.0": "中等", "3.0": "奢華"}
available_prices = sorted(set(p for p in df["price_level"] if p in price_map))
price_display = [price_map[p] for p in available_prices]
price_lookup = {price_map[k]: k for k in price_map if k in available_prices}

# 下拉選單樣式
dropdown_style = "style='background-color:white; border:1px solid #ccc; border-radius:4px;'"

# 一般條件
st.markdown("<div style='margin-bottom:0.2rem;'>價位</div>", unsafe_allow_html=True)
price_level = st.sidebar.multiselect("", options=price_display, label_visibility="collapsed")
st.markdown("<div style='margin-bottom:0.2rem;'>地區</div>", unsafe_allow_html=True)
location_tags = extract_tags(df["location_label"])
location = st.sidebar.multiselect("", options=location_tags, label_visibility="collapsed")
st.markdown("<div style='margin-bottom:0.2rem;'>餐廳類型</div>", unsafe_allow_html=True)
category_tags = extract_tags(df["predicted_tags"])
category = st.sidebar.multiselect("", options=category_tags, label_visibility="collapsed")
only_open_general = st.sidebar.checkbox("只顯示營業中", key="open_general")
sort_general = st.sidebar.selectbox("排序方式", ["熱門度", "評分"], key="sort_general")
search_general = st.sidebar.button("🔍 搜尋一般條件", type="primary")

# 心情條件區塊
st.sidebar.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.title("心情篩選器")
moods = [
    ("🍔吃點罪惡的"),
    ("🥗低熱量清爽健康"),
    ("⏱️趕時間吃快點"),
    ("🌞天氣很熱"),
    ("❄️天氣很冷"),
    ("🌙半夜肚子餓"),
    ("👥聚餐"),
    ("💻讀書辦公"),
    ("🌍異國料理探險"),
    ("🧁下午茶時光")
]
if "selected_mood" not in st.session_state:
    st.session_state.selected_mood = ""

for mood_option in moods:
    if st.sidebar.button(mood_option):
        st.session_state.selected_mood = mood_option

only_open_mood = st.sidebar.checkbox("只顯示營業中", key="open_mood")
sort_mood = st.sidebar.selectbox("排序方式", ["熱門度", "評分"], key="sort_mood")
search_mood = st.sidebar.button("🔍 搜尋心情推薦", type="primary")

# 資料處理邏輯
if search_general:
    df_filtered = df.copy()
    if price_level:
        df_filtered = df_filtered[df_filtered["price_level"].isin([price_lookup[p] for p in price_level])]
    if location:
        df_filtered = filter_contains(df_filtered, "location_label", location)
    if category:
        df_filtered = filter_contains(df_filtered, "predicted_tags", category)
    if only_open_general:
        df_filtered = filter_obj.filter_by_opening_hours(df_filtered)
    df_filtered = filter_obj.sort_by_popularity(df_filtered) if sort_general == "熱門度" else filter_obj.sort_by_rating(df_filtered)
    st.markdown(f"<h5 style='color:#444;'>🔍 共找到 <span style='color:#FBA81A;'>{len(df_filtered)}</span> 間餐廳</h5>", unsafe_allow_html=True)
    for _, row in df_filtered.iterrows():
        render_card(row)

elif search_mood and st.session_state.selected_mood:
    df_filtered = filter_obj.filter_by_mood(st.session_state.selected_mood)
    if only_open_mood:
        df_filtered = filter_obj.filter_by_opening_hours(df_filtered)
    df_filtered = filter_obj.sort_by_popularity(df_filtered) if sort_mood == "熱門度" else filter_obj.sort_by_rating(df_filtered)
    st.markdown(f"<h5 style='color:#444;'>🔍 共找到 <span style='color:#FBA81A;'>{len(df_filtered)}</span> 間餐廳</h5>", unsafe_allow_html=True)
    for _, row in df_filtered.iterrows():
        render_card(row)

else:
    st.markdown("""
    <div style='color:#888;'>📂 點選左上角「＞」挑選餐廳</div>
    <div style='color:#888;'>可以選擇使用「一般篩選器」或「心情篩選器」🔍</div>
    """, unsafe_allow_html=True)