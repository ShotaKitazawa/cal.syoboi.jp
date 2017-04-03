# About

http://cal.syoboi.jp/ からスクレイピングします。

# Environment

- macOS 10.12.3
- Python 3.5.2
	- beautifulsoup4 (4.5.3)
	- requests (2.13.0)
	- tweepy (3.5.0)

# MEMO

- anime_db.sql 使用時は事前にデータベースの再作成を行う。(DROP DATABASE anime; CREATE DATABASE anime;) 

- 以下のコマンドで anime データベースにテーブルを自動で作成

```
mysql -uroot -p anime < anime_db.sql
```

# TODO

- 完: tweet に第何話かの情報を付ける > つけた

- 完:  今季放送開始でないアニメのイメージファイルがどこにあるかがわからない > 時期でフォルダ分けするのをやめる
	- 番組ID,番組名,番組イメージのpath のテーブルを作る。

- xx分前のアニメをリストアップするメソッドの作成
	- now_program メソッドを真似すればかんたん

- 完: insertdb.py を AniTimeTable のモジュール化 > insert_db 関数つくった

- 完: しょぼいカレンダー と あにぽた でアニメのタイトルが違うと困る。 > 全部しょぼいカレンダーで完結させる
	- 優先度高
	- しょぼいカレンダー からデータベースにinsertする情報も取ってくる
		- 画像は [title] で google 画像検索して一番上の画像とか？
			- yahoo 検索
		- insertdb の モジュール化をしちゃう
		- anime_db.sql の見直し

- 歌手名がキャラクター名であっても、その名前で DB に insert してしまう。
	- あきらめモード

- html 自動生成
	- Django?
