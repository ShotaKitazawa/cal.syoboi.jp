#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: http://qiita.com/takumi_TKHS/items/18431740699f04f38642

import sys
import os
import re
import subprocess as cmd


# クエリ検索したHTMLの取得
def get_HTML(query):

    html = cmd.check_output(["wget", "-O", "-", "https://www.bing.com/images/search?q={}".format(query)])

    return html



# jpg画像のURLを抽出
## TODO: url 配列に値が何も入らない
def extract_URL(html):

    url = []
    sentences = html[1].split('\n')
    ptn = re.compile('<a href="(.+\.jpg)" class="thumb"')

    for sent in sentences:
        if sent.find('<div class="item">') >= 0:
            element = sent.split('<div class="item">')

            for j in range(len(element)):
                mtch = re.match(ptn, element[j])
                if mtch >= 0:
                    url.append(mtch.group(1))
    return url



# ローカルに画像を保存
def get_IMG(directory, url):

    for u in url:
        try:
            cmd.check_output(["wget", "-P", directory, u])
        except:
            print("error")
            continue


# 外部プログラムからの参照用
def ext_ref(image, directory):
    html = get_THML(image)
    url = extract_URL(html)
    for u in url:
        print(u)
    get_IMG(directory, url)


if __name__ == "__main__":

    argvs = sys.argv  # argvs[1]: 画像検索のクエリ, argvs[2]: 保存先のディレクトリ(保存したい時のみ)
    query = argvs[1]  # some images  e.g. leopard

    html = str(get_HTML(query))

    url = extract_URL(html)

    for u in url:
        print(u)

    # 画像をローカルに保存したいときに有効にする
    get_IMG(argvs[2], url)
