
from datetime import datetime
from dateutil.relativedelta import relativedelta

# 获取当前时间
current_time = datetime.now()

# 获取一个月前的时间
one_month_ago = current_time - relativedelta(months=1)

# 格式化输出
current_time_str = current_time.strftime("%Y-%m-%d")
one_month_ago_str = one_month_ago.strftime("%Y-%m-%d")

# 打印结果
print(f"当前时间: {current_time_str}")
print(f"一个月前的时间: {one_month_ago_str}")