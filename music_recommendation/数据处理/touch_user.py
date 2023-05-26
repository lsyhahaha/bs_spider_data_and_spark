# -*- coding: utf-8 -*-
# @Time    : 2023/5/22 12:51
# @Author  : lsyhahaha

'''
"id","uid","name","password","gender","age","area","registerTime","des"
"000001","338663754","lsyhahaha","123","男","21","浙江省-杭州市","1621148677573","永无BUG，永不宕机"
'''
import csv
import requests

headers = {'User-Agent':
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
           }



def get_uid():
    uid_set = set()
    with open("../dataset/new_data/collection.csv", 'r' ,encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if "uid" in row:
                continue
            else:
                uid = row[0]
                uid_set.add(uid)
    return uid_set

# uids = get_uid()
# print(uids)

def get_user(user_id):
    url = f"http://localhost:4000/user/detail?uid={user_id}"
    # 发送HTTP请求
    print(url)
    response = requests.get(url, headers=headers)
    # 处理响应数据
    user_detail = response.json()
    # 打印用户详情信息
    print(user_detail)
    # 提取用户信息
    user_id = user_detail['profile']['userId']
    nickname = user_detail['profile']['nickname']
    gender = "男" if user_detail['profile']['gender'] < 0 else "nv"
    age = user_detail['profile']['birthday']
    area = user_detail['profile']['province']
    register_time = user_detail['profile']['createTime']
    description = "这个人很懒，什么也没有写	" if user_detail['profile']['description'] == None else user_detail['profile']['description']

    return (user_id, nickname, "123", gender, age, area, register_time, "这个人很懒，什么也没有写	")

print(get_user(8561321139))

def touch_user():
    uids = get_uid()
    # print(uids)

    filenames = ["uid", "name", "password", "gender", "age", "area", "registerTime", "des"]
    with open("../dataset/new_data/user.csv", "a+", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile,lineterminator='\n')
        writer.writerow(filenames)

        for uid in uids:
            detail = get_user(uid)
            writer.writerow(detail)

if __name__ == '__main__':
    touch_user()