import folium
import streamlit as st
from folium.features import Marker, Popup, Circle, Icon
import pandas as pd
from streamlit_folium import st_folium

st.set_page_config(layout="wide")

facility_df = pd.read_table("./data/facility_data.tsv")
facility_df.set_index("施設名", drop=False, inplace=True)

m = folium.Map(location=[35.672206, 139.480196], zoom_start=15,
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}",
    attr="Tiles &copy; Esri &mdash; Source: Esri, DeLorme, NAVTEQ, USGS, Intermap, iPC, NRCAN, Esri Japan, METI, Esri China (Hong Kong), Esri (Thailand), TomTom, 2012")

color_map = {
    "市立": "blue",
    "私立": "green",
    "認可外": "red"
}

for row in facility_df.itertuples():
    Marker(
        location=[row.lat, row.lon],
        radius=50,
        icon=Icon(color=color_map[row.区分], icon="home"),
        popup=Popup(f"<h5>{row.施設名}</h5>", parse_html=False, max_width=10000),
    ).add_to(m)

st.subheader("府中市保育園マップ")
st.caption("府中市内の保育園をマッピングし、[府中市が公開している保育園の指数分布](https://www.city.fuchu.tokyo.jp/kosodate/shussan/hoikujo/hoiku_shisu.html)と合わせて参照できるようにしたものです")

st.markdown("**Step 1. ↖️から知りたい項目を選んでね**")
st.caption("令和5,6年の0～3歳の指数分布・最低指数が選べます")

df_columns = [c for c in facility_df.columns if "歳" in c]

# layout_columns = st.columns(5)
# for i, col in enumerate(layout_columns):
#     with col:
#         st.checkbox(df_columns[i*5])
#         st.checkbox(df_columns[i*5+1])
#         st.checkbox(df_columns[i*5+2])
#         st.checkbox(df_columns[i*5+3])
#         st.checkbox(df_columns[i*5+4])
with st.sidebar:
    options = st.multiselect(
        label="",
        options=[c for c in facility_df.columns if "歳" in c],
        placeholder="知りたい項目を選んでね"
    )

st.markdown(f"**Step 2. 見たい保育園を選んでね※:blue[市立] / :green[私立] / :red[認可外]**")
output = st_folium(m, height=400, use_container_width=True)

st.markdown("**Step 3. 選んだデータがここに出るよ**")
if isinstance(output["last_object_clicked_popup"], str):
    st.write(output["last_object_clicked_popup"])
    if options:
        st.dataframe(facility_df.query(f"施設名 == '{output['last_object_clicked_popup']}'")[options].T)
    else:
        st.dataframe(facility_df.query(f"施設名 == '{output['last_object_clicked_popup']}'").T)
