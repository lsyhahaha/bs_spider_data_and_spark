# -*- coding: utf-8 -*-
# @Time    : 2023/5/22 13:34
# @Author  : lsyhahaha

'''
"id","suid","singer_name","singer_url"
"0000001","896894","贰佰","https://music.163.com/#/artist?id=896894"
'''
import csv
import requests

headers = {'User-Agent':
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
           }

def get_suid():
    suid_set = set()
    with open("../spider/data/music_163_artists_unique.csv", "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            if "artist_id" in row:
                continue
            suid = row[0]
            suid_set.add(suid)
    return suid_set

# print(get_suid())
# print(len(get_suid()))

def get_suid_detail(suid):
    '''
    获取歌手详情信息
    :param suid:
    :return:
    '''
    url = r"http://localhost:4000/artist/detail?id={}".format(suid)
    print(url)
    # 发送HTTP请求
    response = requests.get(url, headers=headers)
    # 获取听歌记录
    artist = response.json().get('data').get("artist")
    singer_name =artist.get('name')
    sing_url = "https://music.163.com/#/artist?id={}".format(suid)
    return (suid, singer_name, sing_url)
# print(get_suid_detail(11972054))

def touch_songer():
    filenames = ["suid","singer_name","singer_url"]
    with open("../dataset/new_data/songer.csv", "a+", encoding="utf-8") as filecsv:
        writer = csv.writer(filecsv, lineterminator='\n')
        writer.writerow(filenames)

        for suid in list(get_suid()):
            try:
                detail = get_suid_detail(suid)
                print(detail)
                writer.writerow(detail)
            except:
                continue

if __name__ == '__main__':
    touch_songer()