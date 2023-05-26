import json
import csv

# 读取fensi.json文件
with open("../data/fensi.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# 创建CSV文件并写入数据
with open("../data/user_data.csv", "w", encoding="utf-8", newline="") as csvfile:
    writer = csv.writer(csvfile, lineterminator='\n')
    writer.writerow(["昵称", "用户ID"])  # 写入CSV文件的标题行

    # 遍历每个用户的数据
    for user_data in data:
        # 提取昵称和用户ID
        nickname = user_data["nickname"]
        user_id = user_data["userId"]

        # 写入CSV文件的数据行
        print([nickname, user_id, "https://music.163.com/#/user/home?id={}".format(user_id)])
        writer.writerow([nickname, user_id])

print("用户数据已保存到 user_data.csv 文件中。")
