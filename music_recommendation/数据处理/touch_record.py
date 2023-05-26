# -*- coding: utf-8 -*-
# @Time    : 2023/5/22 1:45
# @Author  : lsyhahaha

import csv
import requests

headers = {'User-Agent':
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
           }

csv.field_size_limit(100000000)

# 获取听歌记录
def read_csv():
    with open("../spider/data/record_unique.csv", "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            user_id, records = row
            if "用户" in str(user_id) or user_id=='' or records=='':
                continue
            else:
                yield user_id, records
    # 当程序的控制流程离开with语句块后, 文件将自动关闭

# for row in list(read_csv())[:1]:
#     print(row)

def touch_collecton():
    alist = list(read_csv())
    for row in alist:
        try:
            user_id, records = row
            print("user_id:", user_id)

            url = r"http://localhost:4000/user/record?uid={}&type=1".format(user_id)
            print(url)
            # 发送HTTP请求
            response = requests.get(url, headers=headers)
            # 获取听歌记录
            weekdata = response.json().get('weekData')

            for data in weekdata:
                playCount = data.get('playCount')
                name = data.get('song').get('name')
                song_id = data.get('song').get('id')
                publishTime = data.get('song').get('publishTime')
                isDelete = "1"
                writer.writerow((user_id, song_id, publishTime, isDelete))
                print((user_id, song_id, publishTime, isDelete))
        except Exception as e:
            print(e)
            continue

if __name__ == '__main__':
    fieldnames = ["uid", "iid", "timestamp", "isDelete"]
    with open("../dataset/new_data/record.csv", "a+", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, lineterminator='\n')
        writer.writerow(fieldnames)
        touch_collecton()