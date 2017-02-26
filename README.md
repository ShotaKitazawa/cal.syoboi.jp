# About

http://cal.syoboi.jp/ からスクレイピングします。

# Environment

- macOS 10.12.3
- Python 3.5.2
	- beautifulsoup4 (4.5.3)
	- requests (2.13.0)
	- tweepy (3.5.0)

# TODO

- tweet に第何話かの情報を付ける

- 今季放送開始でないアニメのイメージファイルがどこにあるかがわからない
	- 番組ID,番組名,番組イメージのpath のテーブルを作る。

- xx分前のアニメをリストアップするメソッドの作成
	- now_program メソッドを真似すればかんたん

- insertdb.py を AniTimeTable のモジュール化

- しょぼいカレンダー と あにぽた でアニメのタイトルが違うと困る。
	- 優先度高
