'''
    获取歌单
'''
import requests
import database


class Playlist_crawler1:
    def __init__(self):
        self.datas = []

    def getUrl(self):
        genres = ["综艺", "影视原声", "ACG", "儿童", "校园", "游戏", "70后", "80后", "90后", "网络歌曲", "KTV",
                  "经典", "翻唱", "吉他", "钢琴", "器乐", "榜单", "00后 怀旧", "清新", "浪漫", "伤感", "治愈",
                  "放松", "孤独", "感动", "兴奋", "快乐", "安静", "思念", "清晨", "夜晚", "学习", "工作", "午休",
                  "下午茶", "地铁", "驾车", "运动", "旅行", "散步", "酒吧", "流行", "摇滚", "民谣", "电子", "舞曲",
                  "说唱", "轻音乐", "爵士", "乡村", "R&B/Soul", "古典", "民族", "英伦", "金属", "朋克", "蓝调", "雷鬼",
                  "世界音乐", "拉丁", "New Age", "古风", "后摇", "Bossa Nova", "华语", "欧美", "日语", "韩语", "粤语"]
        urls = []

        #最开始爬取的歌单，大概6196个歌单
        id_list = database.get_gedan_from_excel()
        for id in id_list:
            urls.append("http://localhost:3000/playlist/detail?id=" + id)

        # 其他歌单
        # id_list = database.get_id("playlist")
        # for id in id_list:
        #     urls.append("http://localhost:3000/related/playlist?id=" + id)

        # 各个genres的歌单
        # for genre in genres:
        #     cur_url = "http://localhost:3000/top/playlist/highquality?cat={}".format(urllib.parse.quote(genre))
        #     urls.append(cur_url)

        return urls

    def playlist_crawler(self):
        urls = self.getUrl()
        for url in urls:
            self.getdatas02(url)

    def getdatas01(self, url):
        # 发送Get请求
        response = requests.get(url, headers=headers)
        print(url)
        dict_data = response.json()
        playlists = dict_data.get("playlists")

        for playlist in playlists:
            # 歌单名
            name = playlist.get("name")
            # 歌单id
            id = playlist.get("id")
            # 创建者的id(userId)
            creator = playlist.get("userId")
            # 收藏数
            favorites = playlist.get("subscribedCount")
            # 播放数
            plays = playlist.get("playCount")

            data = (str(id), str(name), str(creator), str(favorites), str(plays))
            #保存数据
            self.intoMysql_playlist(data)


    def getdatas02(self, url):
        '''http://localhost:3000/playlist/detail?id=6852909267'''
        # 发送Get请求
        response = requests.get(url, headers=headers)
        print(url)
        dict_data = response.json()

        playlist = dict_data.get("playlist")
        print("歌单：", playlist)
        # 歌单名
        name = playlist.get("name")
        # 歌单id
        id = playlist.get("id")
        # 创建者的id(userId)
        creator = playlist.get("userId")
        # 收藏数
        favorites = playlist.get("subscribedCount")
        # 播放数
        plays = playlist.get("playCount")

        data = (str(id), str(name), str(creator), str(favorites), str(plays))
        # 保存数据
        self.intoMysql_playlist(data)


    def intoMysql_playlist(self, data):
        try:
            # 定义插入语句和数据
            print("插入数据: ", data)
            sql = "INSERT INTO playlist (id, name, creator, collection_count, play_count) VALUES (%s, %s, %s, %s, %s)"
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

    playlist_crawler = Playlist_crawler1()
    playlist_crawler.playlist_crawler()
    playlist_crawler.intoMysql_playlist()

    # 关闭游标和连接
    cursor.close()
    conn.close()