'''
    获取曲风列表
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

class Genre_crawler:
    def __init__(self):
        self.genre = []

    def genre_crawler(self):
        api = "http://localhost:3000/playlist/catlist"
        url = api
        # 发送Get请求
        response = requests.get(url, headers=headers)
        print(url)

        dict_data = response.json()
        # print(dict_data)

        datas = dict_data.get('sub')
        each = 1
        for data in datas:
            # 曲风id
            # id = data.get("resourceCount")
            id = each
            each = each + 1
            #曲风名
            name = data.get("name")
            self.genre.append( (id, name) )

        return self.genre

    def intoMysql(self):
        #抓取数据
        self.genre_crawler()

        # 连接数据库
        conn = database.conn

        for genre in self.genre:
            # print(genre[0], end='\t')
            # print(genre[1])
            try:
                # 创建游标
                cursor = conn.cursor()
                # 定义插入语句和数据
                sql = "INSERT INTO genre (id, name) VALUES (%s, %s)"
                val = genre
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

genre_crawler = Genre_crawler()
genre_crawler.intoMysql()
