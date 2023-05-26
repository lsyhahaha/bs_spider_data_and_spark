# -*- coding: utf-8 -*-
# @Time    : 2023/5/16 15:49
# @Author  : lsyhahaha

from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.recommendation import ALS
from pyspark.sql import SparkSession
import os

os.environ['JAVA_HOME']='/export/server/jdk1.8.0_241'

# 创建Spark会话
spark = SparkSession.builder.getOrCreate()
# 加载音乐推荐数据（用户ID、音乐ID、评分）
data = spark.read.csv("../datas/music_ratings.csv", header=True, inferSchema=True)
# 将数据拆分为训练集和测试集

train_data, test_data = data.randomSplit([0.8, 0.2])
# 创建ALS模型
als = ALS(userCol="user_id", itemCol="music_id", ratingCol="rating", coldStartStrategy="drop")
# 在训练集上拟合ALS模型
model = als.fit(train_data)

# 在测试集上进行预测
predictions = model.transform(test_data)
# 评估预测结果
evaluator = RegressionEvaluator(metricName="rmse", labelCol="rating", predictionCol="prediction")
rmse = evaluator.evaluate(predictions)
print("Root Mean Squared Error (RMSE)(模型的均方根误差) = " + str(rmse))
# 对所有用户进行音乐推荐
all_user_recs = model.recommendForAllUsers(5)
all_user_recs.show()



import matplotlib.pyplot as plt
# 将推荐结果转换为Pandas DataFrame
user_recs_pd = all_user_recs.toPandas()
# 创建一个图形
fig, ax = plt.subplots()

# 遍历每个用户的推荐结果并绘制散点图
for _, row in user_recs_pd.iterrows():
    user_id = row['user_id']
    recommendations = row['recommendations']

    # 提取音乐ID和推荐分数
    music_ids = [rec['music_id'] for rec in recommendations]
    ratings = [rec['rating'] for rec in recommendations]

    # 绘制散点图
    ax.scatter(music_ids, ratings, label=f'User {user_id}')

# 添加图例、坐标轴标签和标题
ax.legend()
ax.set_xlabel('Music ID')
ax.set_ylabel('Rating')
ax.set_title('Music Recommendations for Users')

# 显示图形
plt.show()