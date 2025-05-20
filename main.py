
import streamlit as st
import pandas as pd
from app.logic.filter_logic import RestaurantFilter
from app.components.restaurant_card import render_card
from datetime import datetime

st.set_page_config(page_title="NTU Food Hunter", layout="wide")

# 主視覺區塊
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

# 讀資料
data_path = "app/data/restaurants.csv"
filter_obj = RestaurantFilter(data_path)
df = filter_obj.df.copy()

st.sidebar.title("篩選器")

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

price_map = {"1.0": "平價", "2.0": "中等", "3.0": "奢華"}
df["price_level"] = df["price_level"].astype(str).str.strip()
available_prices = sorted(set(p for p in df["price_level"] if p in price_map))
price_display = [price_map[p] for p in available_prices]
price_lookup = {price_map[k]: k for k in price_map if k in available_prices}
price_level = st.sidebar.multiselect("價位", options=price_display)

location_tags = extract_tags(df["location_label"])
location = st.sidebar.multiselect("地區", options=location_tags)

category_tags = extract_tags(df["predicted_tags"])
category = st.sidebar.multiselect("餐廳類型", options=category_tags)

mood = st.sidebar.selectbox("心情推薦", ["", "吃點罪惡的", "低熱量清爽健康", "趕時間吃快點", "天氣很熱", "天氣很冷",
                                     "半夜肚子餓", "聚餐", "讀書辦公", "異國料理探險", "下午茶時光"])
only_open = st.sidebar.checkbox("只顯示營業中")

sort_option = st.sidebar.selectbox("排序方式", ["熱門度", "評分"])
search = st.sidebar.button("🔎搜尋")

if search:
    if mood:
        df = filter_obj.filter_by_mood(mood)
    else:
        if price_level:
            df = df[df["price_level"].isin([price_lookup[p] for p in price_level])]
        if location:
            df = filter_contains(df, "location_label", location)
        if category:
            df = filter_contains(df, "predicted_tags", category)

    if only_open:
        df = filter_obj.filter_by_opening_hours(df)

    df = filter_obj.sort_by_popularity(df) if sort_option == "熱門度" else filter_obj.sort_by_rating(df)

    st.markdown(f"<h5 style='color:#444;'>🔍 共找到 <span style='color:#FBA81A;'>{len(df)}</span> 間餐廳</h5>", unsafe_allow_html=True)

    for _, row in df.iterrows():
        render_card(row)
else:
    st.markdown("<p style='color:#888;'>📂 點選左上角「＞」挑選餐廳</p>", unsafe_allow_html=True)
