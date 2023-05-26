import pymysql
import pandas as pd
import re

# 创建数据库连接
import requests

# 设置请求头部信息
headers = {
    'Referer': 'http://music.163.com',
    'Host': 'music.163.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='123456',  # 修改为自己的密码
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor,
    db='music_re'
)

# 创建表格
def creat():
    with conn.cursor() as cursor:
        # 创建用户表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user (
                id VARCHAR(255) PRIMARY KEY,
                username VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL,
                gender VARCHAR(255),
                birthdate VARCHAR(255),
                bio TEXT,
                background_image VARCHAR(255),
                intro TEXT
            );
        ''')

        #创建genre表
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS genre (
                    id VARCHAR(255) PRIMARY KEY,
                    name VARCHAR (255)
                );
            ''')


        # 创建歌曲表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS song (
                id VARCHAR(255) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                artist VARCHAR(255),
                album VARCHAR(255),
                duration VARCHAR(255)
            );
        ''')

        # 创建歌单表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS playlist (
                id VARCHAR(255) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                creator VARCHAR(255),
                collection_count VARCHAR(255),
                play_count VARCHAR(255)
            );
        ''')

        # 创建歌单与歌曲关系表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS playlist_song (
                playlist_id VARCHAR(255),
                song_id VARCHAR(255),
                PRIMARY KEY (playlist_id, song_id)
            );
        ''')

        # 创建歌曲与风格关系表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS song_genre (
                song_id VARCHAR(255),
                genre_id VARCHAR(255),
                PRIMARY KEY (song_id, genre_id)
            );
        ''')

        # 创建用户喜好标签表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_tag (
                user_id VARCHAR(255),
                tag_id VARCHAR(255),
                PRIMARY KEY (user_id, tag_id)
            );
        ''')

        # 创建用户播放历史表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_play_history (
                user_id VARCHAR(255),
                song_id VARCHAR(255),
                play_time DATETIME,
                PRIMARY KEY (user_id, song_id, play_time)
            );
        ''')

        # 创建用户收藏表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_favorite (
                user_id VARCHAR(255),
                favorite_id VARCHAR(255),
                favorite_type ENUM('song', 'playlist'),
                favorite_time DATETIME,
                PRIMARY KEY (user_id, favorite_id, favorite_type)
            );
        ''')

        # 创建歌曲评分表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS song_rating (
                user_id VARCHAR(255),
                song_id VARCHAR(255),
                rating INT,
                rating_time DATETIME,
                PRIMARY KEY (user_id, song_id)
            );
        ''')

        # 创建歌单评分表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS playlist_rating (
                user_id VARCHAR(255),
                playlist_id VARCHAR(255),
                rating INT,
                rating_time DATETIME,
                PRIMARY KEY (user_id, playlist_id)
            );
        ''')

        # 提交更改
        conn.commit()


# 查看某个表格的数据长度
def show_length(table_name):
    # 创建游标对象
    cursor = conn.cursor()

    # 执行查询语句获取表格的行数
    cursor.execute("SELECT COUNT(*) FROM {}".format(table_name))

    # 获取查询结果
    row_count = cursor.fetchone()
    # 打印行数
    print("行数：", row_count)
    # 创建游标对象
    cursor = conn.cursor()

def get_id(table_name):
    # 创建游标对象
    cursor = conn.cursor()
    # 执行查询语句获取id值
    cursor.execute("SELECT id FROM {}".format(table_name))
    # 获取查询结果
    id_list = [row.get("id") for row in cursor.fetchall()]
    # 打印id列表
    print("id列表：", id_list)
    # 创建游标对象
    cursor = conn.cursor()

    return id_list

def get_gedan_from_excel():
    # 读取Excel文件中的第一列
    df = pd.read_excel(r'G:\GraduationDesign\000DEMO\getdatas\Test_demo\gedan.xlsx', usecols=[0], header=None)
    # 将第一列中的每个元素转换为字符串，并合并成一个字符串
    text = ' '.join(df[0].astype(str).tolist())
    # 使用正则表达式提取id值
    id_list = re.findall(r'id=([^\s]+)', text)
    # 打印id列表
    print("id列表：", id_list)

    return id_list

def get_song_ids():
    ids = []

    playlists_id = get_id("playlist")

    for playlist_id in playlists_id:
        print("正在查找歌单id为{}中的音乐id".format(playlist_id))
        url = "http://localhost:3000/playlist/detail?id={}".format(playlist_id)
        print("歌单url:{}".format(url))

        #获取音乐id
        # 发送Get请求
        response = requests.get(url, headers=headers)
        print(url)
        dict_data = response.json()

        privileges = dict_data.get("privileges")
        for song in privileges:
            id = song.get("id")
            print("http://localhost:3000/song/detail?ids=" + str(id))
            ids.append(id)

    return ids

if __name__ =="__main__":
    # creat()

    # get_id("playlist")
    show_length("song")
    # get_gedan_from_excel()

    # 关闭连接
    conn.close