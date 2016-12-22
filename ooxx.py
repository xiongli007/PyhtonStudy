#!/usr/bin/env python3
import requests, re, json, html2text, sys, time
from bs4 import BeautifulSoup
import time
from urllib.request import urlretrieve

url ="https://www.douban.com/group/haixiuzu/\"


def getTopicList():
    # 循环分页抓取 括号里的换成需要抓取的页数区间，从0开始，间隔越大，时间越长
    for x in range(16, 20):
        page = x * 25
        get_url = requests.get(url +\"discussion?start=\"+str(page))

        soup = BeautifulSoup(get_url.text,\"html.parser\")
        tdList = soup.find_all(\"td\",class_='title')
        for i in tdList:
            title = i.a.get(\"title\")
        if len(i.contents) > 1:
        # 因为大家晒照片都喜欢在前面加一个【晒】
            if
        '晒' in title:
        i_href = i.a.get('href')
        getTopicContext(i_href)
        time.sleep(1)
        # 获取帖子里的内容


def getTopicContext(topicUrl):
    url = requests.get(topicUrl)
    soup = BeautifulSoup(url.text,\"html.parser\")
    topicDiv = soup.find_all(\"div\",class_='topic-figure cc')
    for div in topicDiv:
        if
    len(div.contents) > 1:
    img = div.img
    saveImage(img.get(\"src\"))

    # 下载图片到本地


def saveImage(imgUrl):
    fileName = imgUrl[imgUrl.rfind(\"/\")+1:]
    path = r\"你的路径\"+fileName
    urlretrieve(imgUrl, path)

    if __name__ ==\"__main__\":
    getTopicList()