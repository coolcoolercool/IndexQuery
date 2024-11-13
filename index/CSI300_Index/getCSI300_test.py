import json
from datetime import datetime
import akshare as ak

import pandas as pd
import tushare as ts

# tusharez账号的token
token = "c3746b9171b5dea22893717fde18239614a280419193f45a65ae2220"
url = f"https://api.tushare.pro/index_daily.pro?ts_code=399300.SZ&token={token}"

pro = ts.pro_api()
# 获取沪深300指数历史数据，例如获取最近一年的数据

# 获取常见股票指数行情
indexs = {'上证综指': 'sh',
          '深证成指': 'sz',
          '沪深300': 'hs300', '创业板指': 'cyb',
          '上证50': 'sz50', '中小板指': 'zxb'}


def get300():
    pa=pro.daily(ts_code='000001.SZ', start_date='20240101',
                 end_date='20241113')
    ## 可以安排日期排序
    pa.index = pd.to_datetime(pa.trade_date)
    pa.sort_index(inplace=True)
    pa.drop(axis=1, columns='trade_date', inplace=True)
    print(pa.head())

def get300_v1():
    stock_individual_spot_xq_df = ak.stock_individual_spot_xq(symbol="000001")
    print(stock_individual_spot_xq_df.dtypes)


if __name__ == '__main__':
    get300_v1()
