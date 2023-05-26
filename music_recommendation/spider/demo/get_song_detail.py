'''
 获取歌曲详情，判断是否需要VIP
'''
import csv

from selenium import webdriver
from lxml import etree


# 获取歌曲id
def read_csv():
    with open("../data/music163_songs.csv", "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            song_id,song_name = row
            if str(song_id) == "歌手名字":
                continue
            else:
                yield song_id, song_name
    # 当程序的控制流程离开with语句块后, 文件将自动关闭

def main(song_id):
    url = "https://music.163.com/#/song?id=" + str(song_id)
    driver.get(url)
    # 切换成frame
    driver.switch_to.frame("g_iframe")
    html = driver.page_source
    # print(html)
    tree = etree.HTML(html)


    # 提取歌曲名
    song_name = tree.xpath("//em[@class='f-ff2']/text()")[0]
    # 提取艺术家
    artist = tree.xpath("//p[@class='des s-fc4']/span/@title")[0]
    # 提取专辑
    album = tree.xpath('//div[@class="cnt"]/p[2]/a/text()')[0]
    #是否需要VIP
    vip = False
    res = tree.xpath('/html/body/div[3]/div[1]/div/div/div[1]/div[1]/div[2]/div[1]/i/text()')
    if len(res) != 0:
        print("VIP res = ", res)
        vip = True
    # 下载链接
    down_url = "http://music.163.com/song/media/outer/url?id={}.mp3".format(song_id)
    #歌曲时长
    song_time=0
    #歌曲图片
    picUrl=tree.xpath('//div[@class="u-cover u-cover-6 f-fl"]/img/@data-src')[0]


    # 打印提取的信息
    print("歌曲id:", song_id)
    print("歌曲url", url)
    print('歌曲名:', song_name)
    print('艺术家:', artist)
    print('专辑:', album)
    print("VIP:", vip)
    print("下载链接", down_url)
    print("歌曲时长", song_time)
    print("歌曲图片", picUrl)

    with open("../data/music163_songs_detail.csv", "a", encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, lineterminator='\n')
        writer.writerow([song_id, url,song_name, artist, album, vip, down_url, song_time, picUrl])
    csvfile.close()

if __name__ == '__main__':
    # webdriver实例化，因为需要进入到iframe中获取数据，所以需要使用selenium
    option = webdriver.ChromeOptions()
    # 设置option，不弹出显示框
    # option.add_argument('headless')
    # 调用带参数的谷歌浏览器
    driver = webdriver.Chrome(options=option)

    for readcsv in list(read_csv())[685:]:
        try:
            song_id, song_name = readcsv
            print("正在获取歌曲: {}...".format(song_name))
            main(song_id)
            print("歌{}曲获取完成!\n".format(song_name))
        except:
            continue