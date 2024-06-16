# これはなに

東京都府中市内の保育園を地図上にマッピングし、市が公表している各種データと合わせて参照できるようにしたものです

[アプリはこちら](https://fuchu-hoiku-map-37wp3gnp6a-an.a.run.app/)

<img src="https://github.com/oddgai/fuchu-hoiku-map/assets/45445604/0eed4f9d-122b-4e87-9b22-7a7451051240" width="400px">

## 参照できるデータ

- 令和5,6年度の最低指数・指数分布
- 令和6年度の1次申込者数
- 令和6年度の1,2次受入人数

## 引用元

- [保育所等利用可能者最低指数・指数分布（令和6年4月1次募集）](https://www.city.fuchu.tokyo.jp/kosodate/shussan/hoikujo/hoiku_shisu.html)
- [令和6年度4月入所（1次募集）保育所等申込状況](https://www.city.fuchu.tokyo.jp/kosodate/shussan/hoikujo/R6mousikomizyoukyou.html)
- [令和6年4月入所（2次募集）保育所等受入予定人数](https://www.city.fuchu.tokyo.jp/kosodate/shussan/hoikujo/reiwa6hoikushoukeirewaku.html)


# Docker Run

### up
```
docker compose up
```

### down
```
docker compose down
```

# Local Run

### install

```
rye sync
```

### run

```
rye run streamlit run src/app.py
```
