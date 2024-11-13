# -*- coding: utf-8 -*
import json
import textwrap


def print_json_with_name(data, name):
    print(name, ":", json.dumps(data, indent=4))


def print_json(data):
    print(json.dumps(data, indent=4))


def print_request_content(request_data):
    print("request_data", ":", json.dumps(request_data, indent=4))


# 打印响应中的body
def print_response_content(response):
    print("response data:")
    print_json(response.json())

    # resp = response.json()
    # token = resp["data"]["token1"]
    # print(token )


# 打印请求和响应信息
def print_request_and_response(response, *args, **kwargs):
    format_headers = lambda d: '\n'.join(f'{k}: {v}' for k, v in d.items())
    print(textwrap.dedent('''
        ---------------- request ----------------
        {req.method} {req.url}
        {reqhdrs}

        {req.body}
        ---------------- response ----------------
        {res.status_code} {res.reason} {res.url}
        {reshdrs}

        {res_content_print}
    ''').format(
        req=response.request,
        res=response,
        reqhdrs=format_headers(response.request.headers),
        reshdrs=format_headers(response.headers),
        res_content_print=response.text
    ))


