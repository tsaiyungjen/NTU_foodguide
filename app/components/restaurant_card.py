import streamlit as st
import pandas as pd

def render_card(row):
    st.markdown(f"### {row['name']}")
    st.write(f"⭐ {row['rating']} · 💬 {row['user_ratings_total']} 則評論")
    st.write(f"📍 {row['address']}")
    if pd.notna(row.get("map_url")):
        st.markdown(f"[🗺️ 查看地圖]({row['map_url']})")
    st.markdown("---")
