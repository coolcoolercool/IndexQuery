import json

import requests
import tushare as ts

from utils.send_type_request import send_post_request

# tusharez账号的token
token = "c3746b9171b5dea22893717fde18239614a280419193f45a65ae2220"
request_content_org = {
    "api_name": "daily",
    "token": token,
    "params": {
        "ts_code": "399300",
        "exchange": "SZ",
        "start_date": "20240901",
        "end_date": "20241001",
        "is_open": "0"
    }
}

request_content = json.dumps(request_content_org)
url = "http://api.tushare.pro"


def get300():
    request_dict = {
        "url": url,
        "request_param": request_content
    }
    send_post_request(**request_dict)


if __name__ == '__main__':
    get300()
