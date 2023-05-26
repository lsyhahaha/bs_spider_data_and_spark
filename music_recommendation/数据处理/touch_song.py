# -*- coding: utf-8 -*-
# @Time    : 2023/5/22 13:08
# @Author  : lsyhahaha

import csv
import random

import requests
from selenium import webdriver
from lxml import etree

headers = {'User-Agent':
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
           }
# webdriver实例化，因为需要进入到iframe中获取数据，所以需要使用selenium
option = webdriver.ChromeOptions()
# 设置option，不弹出显示框
# option.add_argument('headless')
# 调用带参数的谷歌浏览器
driver = webdriver.Chrome(options=option)



def get_song_id():
    song_id_set = set()
    with open("../dataset/new_data/collection.csv", 'r' ,encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if "uid" in row:
                continue
            else:
                song_id = row[1]
                song_id_set.add(song_id)
    return song_id_set

# print(get_song_id())
# print(len(get_song_id()))

def get_song(song_id):
    url = "https://music.163.com/#/song?id=" + str(song_id)
    driver.get(url)
    # 切换成frame
    driver.switch_to.frame("g_iframe")
    html = driver.page_source
    # print(html)
    tree = etree.HTML(html)

    song_url = "https://music.163.com/#/song?id={}".format(song_id)
    suid = tree.xpath("//p[@class='des s-fc4']/span/a/@href")[0]
    suid = suid.split("=")[1]

    # 提取歌曲名
    song_name = tree.xpath("//em[@class='f-ff2']/text()")[0]
    # 提取艺术家
    artist = tree.xpath("//p[@class='des s-fc4']/span/@title")[0]
    # 提取专辑
    album = tree.xpath('//div[@class="cnt"]/p[2]/a/text()')[0]
    # 下载链接
    down_url = "http://music.163.com/song/media/outer/url?id={}.mp3".format(song_id)
    # 歌曲时长
    song_time = 0
    # 歌曲图片
    picUrl = tree.xpath('//div[@class="u-cover u-cover-6 f-fl"]/img/@data-src')[0]

    return (song_name,song_url,suid, random.randint(1,100),album,down_url,song_time,picUrl,"publishTime","1")

# print(get_song(448317748))

def touch_song():
    song_ids = get_song_id()

    filenames = ["iid","song_name","song_url","suid","playcnt","album","down_url","song_time","picUrl","publishTime","isDelete"]
    with open("../dataset/new_data/song.csv", "a+", encoding="utf-8") as filecsv:
        writer = csv.writer(filecsv,lineterminator='\n')
        writer.writerow(filenames)

        for song_id in song_ids:
            try:
                # "iid","song_name","song_url","suid","playcnt","album","down_url","song_time","picUrl","publishTime","isDelete"
                detail = get_song(song_id)
                print(detail)
                writer.writerow(detail)
            except:
                continue

if __name__ == '__main__':
    touch_song()
