import requests
import database


# 设置请求头部信息
headers = {
    'Referer': 'http://music.163.com',
    'Host': 'music.163.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# 连接数据库
conn = database.conn
# 创建游标对象
cursor = conn.cursor()

# 查询id列
query = "SELECT id FROM playlist"

# 执行查询
cursor.execute(query)
# 读取所有结果并存放在列表中
playlists = [row.get("id") for row in cursor.fetchall()]

# print("playlists = ", playlists)

def songId_crawler():
    items = []
    for playlist in playlists:
        api = "http://localhost:3000/playlist/detail?id=" + playlist
        print(api)
        url = api
        # 发送Get请求
        response = requests.get(url, headers=headers)
        # print(url)
        dict_data = response.json()

        privileges = dict_data.get('privileges')
        for privilege in privileges:
            id = privilege.get("id")
            print((playlist ,str(id)))
            items.append((playlist, id))
    return items

def intomysql(item):
    for data in item:
        try:
            # 创建游标
            cursor = conn.cursor()
            # 定义插入语句和数据
            sql = "INSERT INTO playlist_song (playlist_id, song_id) VALUES (%s, %s)"
            val = data
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
        finally:
            continue
    # 关闭游标和连接

item = songId_crawler()
print("item完成", item)
intomysql(item)

# 关闭游标和数据库连接
cursor.close()
conn.close()