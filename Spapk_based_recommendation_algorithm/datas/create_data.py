# -*- coding: utf-8 -*-
# @Time    : 2023/5/16 16:12
# @Author  : lsyhahaha

import csv
import random


def music_ratings(k=100):
    print("k = ", k)
    ratings = []
    music_ids = range(1001, 1101+k)  # 音乐ID范围：1001-1100
    user_ids = range(1, 50)  # 用户ID范围：1-20

    for _ in range(k):
        user_id = random.choice(user_ids)
        music_id = random.choice(music_ids)
        rating = round(random.uniform(1.0, 5.0), 1)

        ratings.append({"user_id": user_id, "music_id": music_id, "rating": rating})

    # 保存数据到CSV文件
    with open('../faker_data/music_ratings.csv', 'w', newline='') as csvfile:
        fieldnames = ['user_id', 'music_id', 'rating']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(ratings)
    print("音乐推荐数据已保存到 music_ratings.csv 文件。")
# music_ratings(k=1000)

import random
import csv


# 生成音乐数据
def generate_music_data(num_samples):
    music_data = []
    for i in range(num_samples):
        song_id = f"song_{i}"
        genre = random.choice(["pop", "rock", "jazz", "hip-hop", "classical"])
        artist = f"artist_{random.randint(1, 10)}"
        lyrics = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        duration = random.randint(180, 600)

        music_data.append([song_id, genre, artist, lyrics, duration])

    return music_data


# 保存音乐数据到CSV文件
def save_music_data_to_csv(data, file_path):
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["song_id", "genre", "artist", "lyrics", "duration"])
        writer.writerows(data)


# 生成并保存音乐数据
num_samples = 100  # 需要生成的音乐样本数量
music_data = generate_music_data(num_samples)
save_music_data_to_csv(music_data, "music_features.csv")

