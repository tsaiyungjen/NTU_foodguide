import streamlit as st
from app.logic.filter_logic import RestaurantFilter
from app.components.restaurant_card import render_card
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="NTU Food Hunter", layout="wide")

st.title("🍽️ NTU Food Hunter 台大美食推薦系統")

# 讀取資料
data_path = "app/data/restaurants.csv"
filter_obj = RestaurantFilter(data_path)

# 側邊欄篩選選單
st.sidebar.header("🔍 篩選條件")
price_level = st.sidebar.multiselect("價位", options=["$", "$$", "$$$"])
location = st.sidebar.multiselect("地區", options=filter_obj.df["location_label"].dropna().unique())
category = st.sidebar.multiselect("餐廳類型", options=filter_obj.df["category_tag"].dropna().unique())
mood = st.sidebar.selectbox("心情推薦", ["", "吃點罪惡的", "低熱量清爽健康", "趕時間吃快點", "天氣很熱", "天氣很冷", 
                                     "半夜肚子餓", "聚餐", "讀書辦公", "異國料理探險", "下午茶時光"])

only_open = st.sidebar.checkbox("只顯示營業中")

# 套用篩選
if mood:
    df = filter_obj.filter_by_mood(mood)
else:
    df = filter_obj.df
    if price_level:
        df = filter_obj.filter_by_price(price_level)
    if location:
        df = filter_obj.filter_by_location(location)
    if category:
        df = filter_obj.filter_by_type(category)
if only_open:
    df = filter_obj.filter_by_opening_hours(df)

# 排序選項
sort_option = st.sidebar.selectbox("排序方式", ["熱門度", "評分"])
if sort_option == "熱門度":
    df = filter_obj.sort_by_popularity(df)
else:
    df = filter_obj.sort_by_rating(df)

# 顯示結果
st.subheader(f"🔎 共找到 {len(df)} 間餐廳")
for _, row in df.iterrows():
    render_card(row)
