import csv

import pandas as pd

from utils.readCSV import read_csv

# 数据来源 https://cn.investing.com/indices/hang-seng-tech-historical-data

# 输入当天的值
current_index_value = "4,039.58"
up_or_down_value = "-1.73%"

# 使用read_csv函数读取CSV文件
data_file_path = '../../data/沪深300指数历史数据.csv'


def huShen300Index():
    print("沪深300指数:")
    request_param = {
        "data_file_path": data_file_path,
        "current_index_value": current_index_value,
        "up_or_down_value": up_or_down_value,
        "is_plot": False
    }
    read_csv(**request_param)


if __name__ == '__main__':
    huShen300Index()
