# -*- coding: utf-8 -*-
# @Time    : 2023/5/19 2:17
# @Author  : lsyhahaha

# 给  ../data/music_163_artists.csv 文件去重
def quchong(filename = 'music_163_artists'):
    import pandas as pd
    # 读取CSV文件
    df = pd.read_csv('../data/{}.csv'.format(filename))
    # 去重
    df.drop_duplicates(inplace=True)
    # 保存去重后的文件
    df.to_csv('../data/{}_unique.csv'.format(filename), index=False)

# quchong("user_details")
quchong('record')
quchong('music163_songs')
quchong('music163_songs_detail')