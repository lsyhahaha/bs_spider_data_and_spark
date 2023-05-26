'''
(id, username, password, gender, birthdate, signature, backgroundUrl, avatarUrl)
'''
import requests
import pymysql
import database

# 设置请求头部信息
headers = {
    'Referer': 'http://music.163.com',
    'Host': 'music.163.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

class User_crawler:
    def __init__(self, ids):
        self.ids = ids

    # 抓取用户信息
    def user_crawler(self, id):
        api = "http://localhost:3000/user/playlist?uid=" + id
        url = api
        #发送Get请求
        response = requests.get(url, headers=headers)
        print(url)

        dict_data = response.json()
        print(dict_data)

        # 用户id
        id = dict_data.get("playlist")[0].get('creator').get('userId')
        # print("id = ", id)
        #用户名
        username = dict_data.get("playlist")[0].get('creator').get('nickname')
        # print("nickname = ", username)
        #用户密码,默认为123456
        password = 123456
        #性别
        gender = dict_data.get("playlist")[0].get('creator').get('gender')
        # print("性别(男0女1)：", gender)
        #出生日期
        birthdate = dict_data.get("playlist")[0].get('creator').get('birthday')
        if birthdate == 0:
            birthdate = None
        # print("出生日期：", birthdate)
        #个人介绍
        signature = dict_data.get("playlist")[0].get('creator').get('signature')
        #背景图片
        backgroundUrl = dict_data.get("playlist")[0].get('creator').get('backgroundUrl')
        #头像
        avatarUrl = dict_data.get("playlist")[0].get('creator').get('avatarUrl')

        print(id, username, password, gender, birthdate, signature, backgroundUrl, avatarUrl)

        return (id, username, password, gender, birthdate, signature, backgroundUrl, avatarUrl)


    def intoMysql(self):
        # 连接数据库
        conn = database.conn
        ids = self.ids
        for id in ids:
            try:
                # 创建游标
                cursor = conn.cursor()
                # 定义插入语句和数据
                sql = "INSERT INTO user (id, username, password, gender, birthdate, bio, background_image, intro) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                val = self.user_crawler(id)
                # 执行插入操作
                cursor.execute(sql, val)
                # 提交更改
                conn.commit()
                # 打印插入的行数
                print(cursor.rowcount, "record inserted.")
            except Exception as e:
                # 如果发生异常，打印错误信息并回滚更改
                print("Error:", e)
                conn.rollback()
        # 关闭游标和连接
        cursor.close()
        conn.close()

#测试
ids = ['428541730', '7883295797', '97137413', '498654930', '1556672','35401017', '32993888', '1947576356', '1565909693'
       '2001242084', '3252213072', '1718782595', '1718782595']
crawler = User_crawler(ids)
crawler.intoMysql()