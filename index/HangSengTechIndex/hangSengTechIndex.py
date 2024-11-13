import csv

import pandas as pd

# 数据来源 https://cn.investing.com/indices/hang-seng-tech-historical-data

# 输入当天的值
currentIndexValue = "4,458.11"

# 使用read_csv函数读取CSV文件
data_file_path = '../../data/恒生科技指数历史数据daily.csv'
# 读取CSV文件
df = pd.read_csv(data_file_path, thousands=',')
# 计算最大值、最小值和平均值
max_value = df['收盘'].max()
min_value = df['收盘'].min()
mean_value = round(df['收盘'].mean(), 2)
total_value = df['收盘'].count()

print("最大值:", max_value)
print("最小值:", min_value)
print("平均值:", mean_value)
print("总条数:", total_value)


def hangSengTechIndex():
    num = float(currentIndexValue.replace(",", ""))
    # 计算排名（使用 argsort 方法获取排序后的索引，然后找到输入值的索引位置加1得到排名）
    sorted_indices = df['收盘'].argsort()[::-1]
    rank = (df['收盘'].iloc[sorted_indices] == currentIndexValue).idxmax() + 1

    # 计算排名百分比
    rank_percentage = (1 - (rank - 1) / total_value) * 100
    print(f"输入值 {currentIndexValue} 在收盘数据中的排名是: {rank}_{total_value} 百分比为: {rank_percentage:.2f}%")


if __name__ == '__main__':
    hangSengTechIndex()
