from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import pandas as pd


def read_csv(**kwargs):
    current_index_value = kwargs["current_index_value"]
    data_file_path = kwargs["data_file_path"]
    up_or_down_value = kwargs["up_or_down_value"]
    num = float(current_index_value.replace(",", ""))
    is_plot = kwargs["is_plot"]

    df = pd.read_csv(data_file_path, thousands=',')
    # 获取“收盘”列的数据
    closing_prices = df['收盘']

    # 计算最大值、最小值和平均值
    max_value = closing_prices.max()
    min_value = closing_prices.min()
    mean_value = round(closing_prices.mean(), 2)
    total_value = closing_prices.count()
    # 排名的计算
    rank = 0
    for _, value in enumerate(closing_prices):
        if value > num:
            rank = rank + 1

    # 计算排名百分比
    rank_percentage = (1 - (rank - 1) / total_value) * 100

    # 画图
    if is_plot:
        plot_volatility_chart(df, num, rank, rank_percentage)

    print(f"数据日期范围: {df['日期'][total_value-1]} ~ {df['日期'][0]}\n")
    print("最大值:", max_value)
    print("最小值:", min_value)
    print("平均值:", mean_value)
    print("总条数:", total_value)
    print(f"输入值 {num} 在收盘数据中的排名是: 排名:{rank}_总数:{total_value} 超越历史百分比为: {rank_percentage:.2f}%\n")

    # 打印最近时间段的数据
    print_period_data(data_file_path, num)

    # 打印基于全部数据涨跌数据
    # print_fall_raise(df, up_or_down_value, total_value)


# 画图函数
def plot_volatility_chart(df, num, rank_value, rank_percentage_value):
    # 将日期列转换为日期时间格式
    df['日期'] = pd.to_datetime(df['日期'])
    # 设置图形大小
    plt.figure(figsize=(15, 6))
    # 绘制指数波动图
    plt.plot(df['日期'], df['收盘'])
    # 获取当前日期
    today = datetime.now().date()
    # 在图中标注当前日期和输入的收盘值以及排名百分比
    plt.annotate(f"Today: {today}\nValue: {num}\nRank: {rank_value} ({rank_percentage_value:.2f}%)",
                 xy=(today, num), xytext=(today, num + 100),
                 arrowprops=dict(facecolor='red', arrowstyle='->'))
    # 设置图形的标签和标题
    plt.xlabel('日期')
    plt.ylabel('收盘')
    # 自动旋转日期标签，使其更清晰可读
    plt.xticks(rotation=45)
    # 显示网格线
    plt.grid(True)
    # 紧凑布局
    plt.tight_layout()
    # 显示图形
    plt.show()


def print_fall_raise(df, up_or_down_value,total_value):
    # 去除%符号并转换为浮点数
    fall_value = float(up_or_down_value.replace('%', ''))

    # 计算跌幅最大值及其对应日期
    df['涨跌幅_float'] = df['涨跌幅'].str.replace('%', '').astype(float)
    df_fall = df[df['涨跌幅_float'] < 0]
    max_fall = df_fall['涨跌幅_float'].min()
    max_fall_date = df_fall.loc[df_fall['涨跌幅_float'] == max_fall, '日期'].iloc[0]

    # 计算涨幅最大值及其对应日期
    df_rise = df[df['涨跌幅_float'] > 0]
    max_rise = df_rise['涨跌幅_float'].max()
    max_rise_date = df_rise.loc[df_rise['涨跌幅_float'] == max_rise, '日期'].iloc[0]

    print(f"涨幅最大值:{max_rise}%, 对应日期:{max_rise_date}, 跌幅最大值:{max_fall}%, 对应日期:{max_fall_date}")

    # 判断跌幅正负，分别计算排名
    if fall_value >= 0:
        # 计算涨幅排名（正数情况） 这里逻辑不对，需要重新写
        sorted_indices_up = df['涨跌幅'].str.replace('%', '').astype(float).argsort()[::-1]
        rank_up = (df['涨跌幅'].str.replace('%', '').astype(float).iloc[sorted_indices_up] == fall_value).idxmax() + 1
        total_count = len(df)
        rank_percentage_up = (1 - (rank_up - 1) / total_count) * 100
        print(f"输入的涨幅值 {fall_value} 在涨跌幅数据中的排名是: {rank_up}_总数:{total_value}，百分比为: {rank_percentage_up:.2f}%")
    else:
        # 计算跌幅排名（负数情况）
        sorted_indices_down = df['涨跌幅'].str.replace('%', '').astype(float).abs().argsort()[::-1]
        rank_down = (df['涨跌幅'].str.replace('%', '').astype(float).iloc[sorted_indices_down] == fall_value).idxmax() + 1
        total_count = len(df)
        rank_percentage_down = (1 - (rank_down - 1) / total_count) * 100
        print(f"输入的跌幅值 {fall_value} 在涨跌幅数据中的排名是: {rank_down}_总数:{total_value}，百分比为: {rank_percentage_down:.2f}%")


def print_period_data(data_file_path, input_value):
    # 读取CSV文件，设置 thousands=',' 处理数据中的逗号分隔符，并确保日期列被正确解析为日期时间类型
    df = pd.read_csv(data_file_path, thousands=',')

    # 处理“收盘”列中的逗号，将其转换为数字
    df['收盘'] = df['收盘'].replace({',': ''}, regex=True).astype(float)

    # 确保“日期”列是日期格式
    df['日期'] = pd.to_datetime(df['日期'])  # 默认会处理 yyyy-mm-dd 格式

    # 处理“涨跌幅”列，去掉百分号并转换为浮动数值
    df['涨跌幅'] = df['涨跌幅'].replace({',': '', '%': ''}, regex=True).astype(float)

    # 获取当前日期
    current_date = datetime.now() - timedelta(days=1)
    # 计算最近一周的时间范围
    one_week_ago = current_date - timedelta(weeks=1)
    # 计算最近一月的时间范围
    one_month_ago = current_date - timedelta(days=30)
    # 计算最近三个月的时间范围
    three_month_ago = current_date - timedelta(days=30 * 3)
    # 计算最近六个月的时间范围
    six_month_ago = current_date - timedelta(days=30 * 6)
    # 计算最近一年的时间范围
    one_year_ago = current_date - timedelta(days=365)
    # 计算最近两年年的时间范围
    one_year_ago = current_date - timedelta(days=365)
    # 计算最近三年的时间范围
    three_years_ago = current_date - timedelta(days=365 * 3)
    # 计算最近五年的时间范围
    five_years_ago = current_date - timedelta(days=365 * 5)
    # 计算最近七年的时间范围
    seven_years_ago = current_date - timedelta(days=365 * 7)
    # 计算最近十年的时间范围
    ten_years_ago = current_date - timedelta(days=365 * 10)

    # 筛选出最近一周的数据
    recent_week_data = df[(df['日期'] >= one_week_ago) & (df['日期'] <= current_date)]
    # 获取最近一周的起始和结束日期
    start_date = recent_week_data['日期'].min().strftime('%Y-%m-%d')
    end_date = recent_week_data['日期'].max().strftime('%Y-%m-%d')

    # 通过累计涨跌幅列来计算这一段时间的总涨跌幅
    cumulative_change = (1 + recent_week_data['涨跌幅'] / 100).prod() - 1
    cumulative_change_percentage = cumulative_change * 100

    # 计算输入值在最近一周中的排名
    rank = (recent_week_data['收盘'] <= input_value).sum()  # 大于等于该值的个数
    total = len(recent_week_data)
    percentage = (rank / total) * 100

    # 输出结果
    print(f"最近一周的日期范围是: {start_date} 到 {end_date}")
    print(f"输入值 {input_value} 的排名为: {rank}_{total} (超过了百分比: {percentage:.2f}%)")
    print(f"最近一周的涨跌幅度: {cumulative_change_percentage:.2f}%\n")

    # 筛选最近一月的数据
    recent_month_data = df[(df['日期'] >= one_month_ago) & (df['日期'] <= current_date)]
    # 获取最近一周的起始和结束日期
    start_date = recent_month_data['日期'].min().strftime('%Y-%m-%d')
    end_date = recent_month_data['日期'].max().strftime('%Y-%m-%d')
    # 通过累计涨跌幅列来计算这一段时间的总涨跌幅
    cumulative_change = (1 + recent_month_data['涨跌幅'] / 100).prod() - 1
    cumulative_change_percentage = cumulative_change * 100
    # 计算输入值在最近一月中的排名
    rank = (recent_month_data['收盘'] <= input_value).sum()  # 大于等于该值的个数
    total = len(recent_month_data)
    percentage = (rank / total) * 100
    # 输出结果
    print(f"最近一月的日期范围是: {start_date} 到 {end_date}")
    print(f"输入值 {input_value} 的排名为: {rank}_{total} (超过了百分比: {percentage:.2f}%)")
    print(f"最近一月的涨跌幅度: {cumulative_change_percentage:.2f}%\n")

    # 筛选最近三个月的数据
    recent_three_month_data = df[(df['日期'] >= three_month_ago) & (df['日期'] <= current_date)]
    # 获取最近一周的起始和结束日期
    start_date = recent_three_month_data['日期'].min().strftime('%Y-%m-%d')
    end_date = recent_three_month_data['日期'].max().strftime('%Y-%m-%d')
    # 通过累计涨跌幅列来计算这一段时间的总涨跌幅
    cumulative_change = (1 + recent_three_month_data['涨跌幅'] / 100).prod() - 1
    cumulative_change_percentage = cumulative_change * 100
    # 计算输入值在最近一周中的排名
    rank = (recent_three_month_data['收盘'] <= input_value).sum()  # 大于等于该值的个数
    total = len(recent_three_month_data)
    percentage = (rank / total) * 100
    # 输出结果
    print(f"最近三个月的日期范围是: {start_date} 到 {end_date}")
    print(f"输入值 {input_value} 的排名为: {rank}_{total} (超过了百分比: {percentage:.2f}%)")
    print(f"最近三个月的涨跌幅度: {cumulative_change_percentage:.2f}%\n")

    # 筛选最近六个月的数据
    recent_six_month_data = df[(df['日期'] >= six_month_ago) & (df['日期'] <= current_date)]
    # 获取最近六个月的起始和结束日期
    start_date = recent_six_month_data['日期'].min().strftime('%Y-%m-%d')
    end_date = recent_six_month_data['日期'].max().strftime('%Y-%m-%d')
    # 通过累计涨跌幅列来计算这一段时间的总涨跌幅
    cumulative_change = (1 + recent_six_month_data['涨跌幅'] / 100).prod() - 1
    cumulative_change_percentage = cumulative_change * 100

    # 计算输入值在最近六个月中的排名
    rank = (recent_six_month_data['收盘'] <= input_value).sum()  # 大于等于该值的个数
    total = len(recent_six_month_data)
    percentage = (rank / total) * 100
    # 输出结果
    print(f"最近六个月的日期范围是: {start_date} 到 {end_date}")
    print(f"输入值 {input_value} 的排名为: {rank}_{total} (超过了百分比: {percentage:.2f}%)")
    print(f"最近六个月的涨跌幅度: {cumulative_change_percentage:.2f}%\n")

    # 筛选最近一年的数据
    recent_year_data = df[(df['日期'] >= one_year_ago) & (df['日期'] <= current_date)]
    # 获取最近一年的起始和结束日期
    start_date = recent_year_data['日期'].min().strftime('%Y-%m-%d')
    end_date = recent_year_data['日期'].max().strftime('%Y-%m-%d')
    # 通过累计涨跌幅列来计算这一段时间的总涨跌幅
    cumulative_change = (1 + recent_year_data['涨跌幅'] / 100).prod() - 1
    cumulative_change_percentage = cumulative_change * 100
    # 计算输入值在最近一年中的排名
    rank = (recent_year_data['收盘'] <= input_value).sum()  # 大于等于该值的个数
    total = len(recent_year_data)
    percentage = (rank / total) * 100
    # 输出结果
    print(f"最近一年的日期范围是: {start_date} 到 {end_date}")
    print(f"输入值 {input_value} 的排名为: {rank}_{total} (超过了百分比: {percentage:.2f}%)")
    print(f"最近一年的涨跌幅度: {cumulative_change_percentage:.2f}%\n")

    # 筛选最近三年的数据
    recent_three_year_data = df[(df['日期'] >= three_years_ago) & (df['日期'] <= current_date)]
    # 获取最近三年的起始和结束日期
    start_date = recent_three_year_data['日期'].min().strftime('%Y-%m-%d')
    end_date = recent_three_year_data['日期'].max().strftime('%Y-%m-%d')
    # 通过累计涨跌幅列来计算这一段时间的总涨跌幅
    cumulative_change = (1 + recent_three_year_data['涨跌幅'] / 100).prod() - 1
    cumulative_change_percentage = cumulative_change * 100
    # 计算输入值在最近三年中的排名
    rank = (recent_three_year_data['收盘'] <= input_value).sum()  # 大于等于该值的个数
    total = len(recent_three_year_data)
    percentage = (rank / total) * 100
    # 输出结果
    print(f"最近三年的日期范围是: {start_date} 到 {end_date}")
    print(f"输入值 {input_value} 的排名为: {rank}_{total} (超过了百分比: {percentage:.2f}%)")
    print(f"最近三年的涨跌幅度: {cumulative_change_percentage:.2f}%\n")

    # 筛选最近五年的数据
    recent_five_year_data = df[(df['日期'] >= five_years_ago) & (df['日期'] <= current_date)]
    # 获取最近五年的起始和结束日期
    start_date = recent_five_year_data['日期'].min().strftime('%Y-%m-%d')
    end_date = recent_five_year_data['日期'].max().strftime('%Y-%m-%d')
    # 通过累计涨跌幅列来计算这一段时间的总涨跌幅
    cumulative_change = (1 + recent_five_year_data['涨跌幅'] / 100).prod() - 1
    cumulative_change_percentage = cumulative_change * 100
    # 计算输入值在最近五年中的排名
    rank = (recent_five_year_data['收盘'] <= input_value).sum()  # 大于等于该值的个数
    total = len(recent_five_year_data)
    percentage = (rank / total) * 100
    # 输出结果
    print(f"最近五年的日期范围是: {start_date} 到 {end_date}")
    print(f"输入值 {input_value} 的排名为: {rank}_{total} (超过了百分比: {percentage:.2f}%)")
    print(f"最近五年的涨跌幅度: {cumulative_change_percentage:.2f}%\n")

    # 筛选最近七年的数据
    recent_seven_year_data = df[(df['日期'] >= seven_years_ago) & (df['日期'] <= current_date)]
    # 获取最近七年的起始和结束日期
    start_date = recent_seven_year_data['日期'].min().strftime('%Y-%m-%d')
    end_date = recent_seven_year_data['日期'].max().strftime('%Y-%m-%d')
    # 通过累计涨跌幅列来计算这一段时间的总涨跌幅
    cumulative_change = (1 + recent_seven_year_data['涨跌幅'] / 100).prod() - 1
    cumulative_change_percentage = cumulative_change * 100
    # 计算输入值在最近七年中的排名
    rank = (recent_seven_year_data['收盘'] <= input_value).sum()  # 大于等于该值的个数
    total = len(recent_seven_year_data)
    percentage = (rank / total) * 100
    # 输出结果
    print(f"最近七年的日期范围是: {start_date} 到 {end_date}")
    print(f"输入值 {input_value} 的排名为: {rank}_{total} (超过了百分比: {percentage:.2f}%)")
    print(f"最近七年的涨跌幅度: {cumulative_change_percentage:.2f}%\n")

    # 筛选最近十年的数据
    recent_ten_year_data = df[(df['日期'] >= ten_years_ago) & (df['日期'] <= current_date)]
    # 获取最近十年的起始和结束日期
    start_date = recent_ten_year_data['日期'].min().strftime('%Y-%m-%d')
    end_date = recent_ten_year_data['日期'].max().strftime('%Y-%m-%d')
    # 通过累计涨跌幅列来计算这一段时间的总涨跌幅
    cumulative_change = (1 + recent_ten_year_data['涨跌幅'] / 100).prod() - 1
    cumulative_change_percentage = cumulative_change * 100
    # 计算输入值在最近十年中的排名
    rank = (recent_ten_year_data['收盘'] <= input_value).sum()  # 大于等于该值的个数
    total = len(recent_ten_year_data)
    percentage = (rank / total) * 100
    # 输出结果
    print(f"最近十年的日期范围是: {start_date} 到 {end_date}")
    print(f"输入值 {input_value} 的排名为: {rank}_{total} (超过了百分比: {percentage:.2f}%)")
    print(f"最近十年的涨跌幅度: {cumulative_change_percentage:.2f}%\n")