# -*- coding: utf-8 -*-
# @Time    : 2023/5/21 16:14
# @Author  : lsyhahaha

''' 读取user_data.csv文件，通过http://localhost:4000/user/detail?uid=32953014，获取每个用户的详情信息'''
import csv
import requests

headers = {'User-Agent':
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
           }

# 读取CSV文件
with open('../data/user_data.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in list(reader):
        print(row)
        print("正在获取{}的详情信息".format(row.get('昵称')))
        user_id = row.get('用户ID')
        # 构建请求URL
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

        # 将用户信息保存到CSV文件
        filename = '../data/user_details.csv'
        fieldnames = ['用户ID', '昵称', '性别', '年龄', '地区', '注册时间', '简介']
        with open(filename, 'a+', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({
                '用户ID': user_id,
                '昵称': nickname,
                '性别': gender,
                '年龄': age,
                '地区': area,
                '注册时间': register_time,
                '简介': description
            })
        print(f"用户信息已保存到{filename}")

        # 听歌记录
        # http://localhost:4000/user/record?uid=8542367555&type=1
        print(url)
        url = r"http://localhost:4000/user/record?uid={}&type=1".format(user_id)
        # 发送HTTP请求
        response = requests.get(url, headers=headers)
        #获取听歌记录
        weekdata = response.json().get('weekData')
        print(weekdata)
        filename='../data/record.csv'
        fieldnames=['用户ID',"听歌记录"]
        with open(filename, 'a+', newline='',encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({
                '用户ID': user_id,
                '听歌记录': weekdata
            })
        print(f"用户信息已保存到{filename}")
