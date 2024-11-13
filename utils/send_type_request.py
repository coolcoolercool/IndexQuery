import requests

from utils.print_utils import print_request_content, print_response_content


def send_post_request(**kwargs):
    print("request url:" + format(kwargs['url']))

    headers = {}
    if 'headers' in kwargs:
        headers = kwargs['headers']

    response = None
    if "request_param" in kwargs:
        print_request_content(kwargs['request_param'])
        response = requests.post(kwargs['url'], headers=headers, data=kwargs['request_param'])
    else:
        response = requests.get(kwargs['url'], headers=headers)
    print_response_content(response)


def send_get_request(**kwargs):
    print("request url:" + format(kwargs['url']))

    headers = None
    if 'headers' in kwargs:
        headers = kwargs['headers']

    response = None
    if "request_param" in kwargs:
        print_request_content(kwargs['request_param'])
        response = requests.get(kwargs['url'], headers=headers, data=kwargs['request_param'])
    else:
        response = requests.get(kwargs['url'], headers=headers)
    print_response_content(response)