import pandas as pd

# データ読み込み・整形
## 読み込み
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
df_merged = pd.concat([df_index_merged, df_apply_merged, df_r6_1st_accept_melted, df_r6_2nd_accept_melted], axis=0).reset_index()
df_merged.to_csv("./src/data/processed_data.tsv", sep="\t", index=False)
