'''
   歌曲的详情信息：
    # 获取歌单所有歌曲 == 获取歌曲的详情信息

    待做：按照歌手id下载音乐
'''
import requests
import database

class Song_crawler:
    def __init__(self, ids):
        self.ids = ids

    # 抓取歌曲信息
    def song_crawler(self, id):
        api = "http://localhost:3000/song/detail?ids=" + str(id)
        url = api
        #发送Get请求
        response = requests.get(url, headers=headers)
        print(url)

        dict_data = response.json()
        # print(dict_data)

        #歌曲id
        id = id
        #歌曲名称
        name = dict_data.get('songs')[0].get('name')
        # print(name)
        #歌手 歌手可能有几个，所以get('ar')为列表
        artist = dict_data.get('songs')[0].get('ar')[0].get('name')
        # print(artist)
        # 专辑名称
        album = dict_data.get('songs')[0].get('al').get('name')
        # print(album)
        #时长
        duration = dict_data.get('songs')[0].get('dt')
        # print(duration)
        print(id, name, artist, album, duration)

        return (id, name, artist, album, duration)

    def intoMysql_song(self):
        ids = self.ids
        for id in ids:
            try:
                # 定义插入语句和数据
                sql = "INSERT INTO song (id, name, artist, album, duration) VALUES (%s, %s, %s, %s, %s)"
                val = self.song_crawler(id)
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


if __name__ == "__main__":
    # 设置请求头部信息
    headers = {
        'Referer': 'http://music.163.com',
        'Host': 'music.163.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # 连接数据库
    conn = database.conn
    # 创建游标
    cursor = conn.cursor()

    # 测试
    # ids = wyymusic_play_recode.song_ids
    ids = database.get_song_ids()

    crawler = Song_crawler(ids)
    # crawler.user_crawler('347230')
    crawler.intoMysql_song()

    # 关闭游标和连接
    cursor.close()
    conn.close()