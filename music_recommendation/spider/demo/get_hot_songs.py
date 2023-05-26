from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv


def parse_html_page(html):
    # 使用双引号会出现 Unresolve reference
    # pattern = '<span class="txt"><a href="/song?id=(\d*)"><b title="(.*?)">'
    # 这里是使用lxml解析器进行解析,lxml速度快,文档容错能力强,也能使用html5lib
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all('span', 'txt')
    return items



# 将获得的歌手的热门歌曲id和名字写入csv文件
def write_to_csv(items, artist_name):
    with open("../data/music163_songs.csv", "a", encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, lineterminator='\n')
        writer.writerow(["歌手名字", artist_name])

        for item in items:
            writer.writerow([item.a['href'].replace('/song?id=', ''), item.b['title']])
        '''
            # 可视化显示
            print('歌曲id:', item.a['href'].replace('/song?id=', ''))
            song_name = item.b['title']
            print('歌曲名字:', song_name)
        '''
    csvfile.close()


# 获取歌手id和歌手姓名
def read_csv():

    with open("../data/music_163_artists_unique.csv", "r", encoding="utf-8") as csvfile:

        reader = csv.reader(csvfile)
        for row in reader:
            artist_id, artist_name = row
            if str(artist_id) == "歌手名字":
                continue
            else:
                yield artist_id, artist_name
    # 当程序的控制流程离开with语句块后, 文件将自动关闭


def main():
    driver = webdriver.Chrome()
    # 避免多次打开浏览器
    for readcsv in list(read_csv())[3467:]:
        artist_id, artist_name = readcsv
        url = "https://music.163.com/#/artist?id=" + str(artist_id)
        print("正在获取{}的热门歌曲...".format(artist_name))
        driver.get(url)
        # 切换成frame
        driver.switch_to.frame("g_iframe")
        # 休眠3秒,等待加载完成!
        time.sleep(0.5)
        html = driver.page_source
        items = parse_html_page(html)
        print("{}的热门歌曲获取完成!".format(artist_name))
        print("开始将{}的热门歌曲写入文件".format(artist_name))
        write_to_csv(items, artist_name)
        print("{}的热门歌曲写入到本地成功!".format(artist_name))


if __name__ == "__main__":
    main()