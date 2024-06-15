import folium
import streamlit as st
from folium.features import Marker, Popup, Circle, Icon
import pandas as pd
from streamlit_folium import st_folium

st.set_page_config(layout="wide")

# データ読み込み・整形
## 読み込み
facility_df = pd.read_table("./src/data/facility_data.tsv")
df_facility_master = pd.read_table("./src/data/保育園マスタ.tsv")
df_r5_index = pd.read_table("./src/data/R5_認可保育園_指数分布.tsv")
df_r6_index = pd.read_table("./src/data/R6_認可保育園_指数分布.tsv")
df_r5_1st_apply = pd.read_table("./src/data/R5_1次申込者数.tsv")
df_r6_1st_apply = pd.read_table("./src/data/R6_1次申込者数.tsv")
df_r6_1st_accept = pd.read_table("./src/data/R6_1次受入予定人数.tsv")
df_r6_2nd_accept = pd.read_table("./src/data/R6_2次受入予定人数.tsv")

## 表示用にデータを整形
### 指数データをマージ
df_r5_index_melted = df_r5_index.melt(id_vars=["id", "施設名"],
                      value_vars=["0歳_199以下", "0歳_200", "0歳_201以上", "0歳_最低指数", "1歳_199以下", "1歳_200", "1歳_201以上", "1歳_最低指数", "2歳_199以下", "2歳_200", "2歳_201以上", "2歳_最低指数", "3歳_199以下", "3歳_200", "3歳_201以上", "3歳_最低指数"],
                      var_name="項目名", value_name="令和5年")
df_r6_index_melted = df_r6_index.melt(id_vars=["id", "施設名"],
                      value_vars=["0歳_199以下", "0歳_200", "0歳_201以上", "0歳_最低指数", "1歳_199以下", "1歳_200", "1歳_201以上", "1歳_最低指数", "2歳_199以下", "2歳_200", "2歳_201以上", "2歳_最低指数", "3歳_199以下", "3歳_200", "3歳_201以上", "3歳_最低指数"],
                      var_name="項目名", value_name="令和6年")
df_index_merged = pd.merge(df_r5_index_melted, df_r6_index_melted, on=["id", "施設名", "項目名"])
df_index_merged = df_index_merged[["項目名", "id", "施設名", "令和5年", "令和6年"]]

### 申込者数をマージ
df_r5_1st_apply_melted = df_r5_1st_apply.melt(id_vars=["id", "施設名"],
                      value_vars=["0歳", "1歳", "2歳", "3歳", "4歳", "5歳"],
                      var_name="項目名", value_name="令和5年")
df_r6_1st_apply_melted = df_r6_1st_apply.melt(id_vars=["id", "施設名"],
                      value_vars=["0歳", "1歳", "2歳", "3歳", "4歳", "5歳"],
                      var_name="項目名", value_name="令和6年")
df_apply_merged = pd.merge(df_r5_1st_apply_melted, df_r6_1st_apply_melted, on=["id", "施設名", "項目名"])
df_apply_merged = df_apply_merged[["項目名", "id", "施設名", "令和5年", "令和6年"]]
df_apply_merged["項目名"] = df_apply_merged["項目名"] + "_のべ申込者数"

### 受入予定人数を整形
df_r6_1st_accept_melted = df_r6_1st_accept.melt(id_vars=["id", "施設名"],
                      value_vars=["0歳", "1歳", "2歳", "3歳", "4歳", "5歳"],
                      var_name="項目名", value_name="令和6年")
df_r6_1st_accept_melted["令和5年"] = pd.Series()
df_r6_1st_accept_melted["項目名"] = df_r6_1st_accept_melted["項目名"] + "_1次受入人数"
df_r6_2nd_accept_melted = df_r6_2nd_accept.melt(id_vars=["id", "施設名"],
                        value_vars=["0歳", "1歳", "2歳", "3歳", "4歳", "5歳"],
                        var_name="項目名", value_name="令和6年")
df_r6_2nd_accept_melted["令和5年"] = pd.Series()
df_r6_2nd_accept_melted["項目名"] = df_r6_2nd_accept_melted["項目名"] + "_2次受入人数"

### 全データを縦に結合
df_merged = pd.concat([df_index_merged, df_apply_merged, df_r6_1st_accept_melted, df_r6_2nd_accept_melted], axis=0)

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

for row in facility_df.itertuples():
    Marker(
        location=[row.lat, row.lon],
        radius=50,
        icon=Icon(color=color_map[row.区分], icon="home"),
        popup=Popup(f"<h5>{row.施設名}</h5>", parse_html=False, max_width=10000),
    ).add_to(m)

# UI
st.subheader("府中市保育園マップ")
st.caption("府中市内の保育園をマッピングし、市が公表している各種データと合わせて参照できるようにしたものです")

st.markdown("**Step 1. 知りたい年齢を選んでね**")
target_age = st.radio(label="", options=["0歳", "1歳", "2歳", "3歳"], horizontal=True,  label_visibility="collapsed")

st.markdown(f"**Step 2. 見たい保育園を選んでね** ※:blue[市立] / :green[私立] / :orange[地域型] / :red[認可外]")
output = st_folium(m, height=400, use_container_width=True)

st.markdown("**Step 3. 選んだデータがここに出るよ**")
if isinstance(output["last_object_clicked_popup"], str):
    st.write(output["last_object_clicked_popup"])
    columns = [c for c in facility_df.columns if target_age in c]
    # st.dataframe(facility_df.query(f"施設名 == '{output['last_object_clicked_popup']}'")[columns].T)
    st.dataframe(
        df_merged.query(f"施設名 == '{output['last_object_clicked_popup']}' & 項目名.str.contains('{target_age}')").set_index("項目名")[["令和5年", "令和6年"]].style.highlight_null(props="color: transparent;")
        )

# footer
st.divider()
st.markdown('''データ引用元
- [保育所・保育園 | 東京都府中市](https://www.city.fuchu.tokyo.jp/kosodate/shussan/hoikujo/index.html)
- [保育所等利用可能者最低指数・指数分布（令和6年4月1次募集） | 東京都府中市](https://www.city.fuchu.tokyo.jp/kosodate/shussan/hoikujo/hoiku_shisu.html)
- [令和6年度4月入所（1次募集）保育所等申込状況 | 東京都府中市](https://www.city.fuchu.tokyo.jp/kosodate/shussan/hoikujo/R6mousikomizyoukyou.html)
- [令和6年4月入所（2次募集）保育所等受入予定人数 | 東京都府中市](https://www.city.fuchu.tokyo.jp/kosodate/shussan/hoikujo/reiwa6hoikushoukeirewaku.html)''')
st.caption("本アプリで表示してるデータは市が公表しているデータを開発者が手入力して作成したものです。そのため、誤りがある可能性もありますので正確な数字は市のHPを参照ください。")
