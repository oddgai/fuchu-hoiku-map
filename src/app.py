import folium
import streamlit as st
from folium.features import Marker, Popup, Circle, Icon
import pandas as pd
from streamlit_folium import st_folium

st.set_page_config(layout="wide")

# データ読み込み
df_facility_master = pd.read_table("./src/data/保育園マスタ.tsv")
df_merged = pd.read_table("./src/data/processed_data.tsv")

# マップの作成
m = folium.Map(location=[35.672206, 139.480196], zoom_start=15,
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}",
    attr="Tiles &copy; Esri &mdash; Source: Esri, DeLorme, NAVTEQ, USGS, Intermap, iPC, NRCAN, Esri Japan, METI, Esri China (Hong Kong), Esri (Thailand), TomTom, 2012")

color_map = {
    "市立": "blue",
    "私立": "green",
    "地域型": "orange",
    "認可外": "red"
}

for row in df_facility_master.itertuples():
    Marker(
        location=[row.lat, row.lon],
        radius=50,
        icon=Icon(color=color_map[row.区分], icon="home"),
        popup=Popup(f"<h5>{row.施設名}</h5>", parse_html=False, max_width=10000),
    ).add_to(m)

# UI
st.subheader("府中市保育園マップ")
st.caption("府中市内の保育園をマッピングし、市が公表している各種データと合わせて参照できるようにしたものです")

st.markdown("**1. 知りたい年齢を選んでね**")
target_age = st.radio(label="", options=["0歳", "1歳", "2歳", "3歳"], horizontal=True,  label_visibility="collapsed")

st.markdown("**2. 見たい保育園を選んでね**")
st.caption(f"※:blue[市立] / :green[私立] / :orange[地域型] / :red[認可外]  \n※認可外のデータは非公表のため地図のみ表示")
output = st_folium(m, height=400, use_container_width=True)

st.markdown("**3. 選んだデータがここに出るよ**")
if isinstance(output["last_object_clicked_popup"], str):
    clicked_facility_name = output["last_object_clicked_popup"]
    st.write(clicked_facility_name)
    st.dataframe(
        df_merged.query("施設名 == @clicked_facility_name & 項目名.str.contains(@target_age)").set_index("項目名")[["令和5年", "令和6年"]]
        )

# footer
st.divider()
st.caption('''データ引用元
- [保育所・保育園 | 東京都府中市](https://www.city.fuchu.tokyo.jp/kosodate/shussan/hoikujo/index.html)
- [保育所等利用可能者最低指数・指数分布（令和6年4月1次募集） | 東京都府中市](https://www.city.fuchu.tokyo.jp/kosodate/shussan/hoikujo/hoiku_shisu.html)
- [令和6年度4月入所（1次募集）保育所等申込状況 | 東京都府中市](https://www.city.fuchu.tokyo.jp/kosodate/shussan/hoikujo/R6mousikomizyoukyou.html)
- [令和6年4月入所（2次募集）保育所等受入予定人数 | 東京都府中市](https://www.city.fuchu.tokyo.jp/kosodate/shussan/hoikujo/reiwa6hoikushoukeirewaku.html)''')
st.caption("本アプリで表示しているデータは市が公表しているデータを開発者が手入力して作成したものです。そのため、誤りがある可能性もありますので正確な数字は市のHPを参照ください。")
