import json
import random

import requests
import json
import base64
import urllib3

urllib3.disable_warnings()
hear = None
# url = "https://api-gateway.socrates.com/user/public/v1/login"
uri = "https://api-next-gateway-staging.actqa.com"

def base_64(data):
    # 假设这是你的Base64编码过的字符串
    encoded_string = data

    # 解码Base64字符串
    decoded_string = base64.b64decode(encoded_string).decode("utf-8")

    split_result = decoded_string.split('|')

    # 输出解码后的字符串
    return split_result

class CheckApi(object):
    def __init__(self, phone):
        self.uri = "https://api-next-gateway-staging.actqa.com"
        self.token = self.login(self.uri, phone)

    @classmethod
    def login(cls, url, phone):
        url = f"{url}/user/public/v1/login"
        headers = {
            'Content-Type': 'application/json'
        }

        data = {
            "country_code": "cn",
            "mobile": f"86-{phone}",
            "method": "MOBILE",
            "code": "123456"
        }
        response = requests.request("POST", url, headers=headers, json=data)
        # print(response.text)
        # print(response.json()["data"]["token"])
        return response.json()["data"]["token"]

    def fetch_data(self, url, method='GET', params=None, json_data=None):
        """ 根据请求方法获取数据 """
        headers = {
            'Content-Type': 'application/json',
            "Authorization": "Bearer " + self.token
        }
        if method == 'POST':
            response = requests.post(url, json=json_data, headers=headers)
        else:  # 默认为 GET 请求
            response = requests.get(url, params=params)

        response.raise_for_status()  # 确保请求成功
        return response.json()  # 假设返回的数据是 JSON 格式

    def login_api(self):
        data = "/user/public/v1/login"
        url = f"{self.uri}{data}"

        data = {
            "country_code": "cn",
            "mobile": f"86-{self.generate_phone_number()}",
            "method": "MOBILE",
            "code": "123456"
        }
        response = self.fetch_data(url, method='POST', json_data=data)
        print(response.json())

    # def comments(self):
    #     data = "/post/public/v1/posts/comments"
    #     url = f"{self.uri}{data}"
    #     bali = f"{self.bali_uri}{data}"
    #
    #     data = {
    #         "post_id": "NDIzNTExOTA0ODcxMzgzMDR8NjYyNjg2MjgxMDIwMjUyMTY=",
    #         "option": "",
    #         "parent_comment_id": "",
    #         "sorted_by": "POPULARITY",
    #         "limit": 15
    #     }
    #     are_equal_get = self.compare_urls(url, bali, method='GET', params=data)
    #     print("GET 请求的两个接口返回的参数是否相同:", are_equal_get)

    # 创建帖子
    def posts(self):
        data = "/post/private/v1/posts"
        url = f"{self.uri}{data}"
        data = {
            "body": "5616",
            "uploaded_materials": [],
            "topics": [],
            "post_type": "NORMAL"
        }
        response = self.fetch_data(url, method='POST', json_data=data)
        print(response.json())

    # 创建评论
    def post(self):
        data = "/post/public/v1/post/MzQ5OTY1MjkwMjY2OTUxNjh8NjY5ODgyNzEzMzEwNjI4NjQ="
        url = f"{self.uri}{data}"

        response = self.fetch_data(url, method='GET', params=data)
        print(response.json())

    # 点赞
    def like(self):
        url = f"{self.uri}/post/private/v1/like"
        data = {
            "comment_id": "NjQ3OTM3NDA5MTI3MTc4MjR8MjU2MDA0MTA3MTI2NzQzNDczNA==",
            "post_id": "",
            "action": "LIKE"
        }

        response = self.fetch_data(url, method='POST', json_data=data)
        print(response.json())

    # 推荐
    def recommended(self):
        url = f"{self.uri}/post/public/v1/posts/recommended"
        data = {
            "limit": 15
        }

        response = self.fetch_data(url, method='GET', params=data)
        print(response.json())

    # 关注
    def followed(self):
        url = f"{self.uri}/post/private/v1/posts/followed"
        data = {
            "limit": 15
        }

        response = self.fetch_data(url, method='GET', params=data)
        print(response.json())

    # 创建评论
    def comments(self):
        url = f"{self.uri}/post/private/v1/comments"
        data = {
            "body": "粉尘",
            "post_id": "MzQ5OTY1MjkwMjY2OTUxNjh8NjcwMDY4MzUyMjgzMDA4Njc="
        }

        response = self.fetch_data(url, method='POST', json_data=data)
        print(response.json())

    # 获取用户邀请码
    def user_codes(self):
        url = f"{self.uri}/user/private/v1/user_codes"
        data = {}
        response = self.fetch_data(url, "POST", json_data=data)
        print(response["data"].get("code"))

    # 登陆和输入邀请码
    def login_use_code(self):
        url = f"{self.uri}/user/private/v1/login_use_code"
        data = {
            "code": self.user_codes()
        }

        response = self.fetch_data(url, method='POST', json_data=data)
        print(response.json())

    def generate_phone_number(self):
        # 中国手机号码格式：11位数字，第一位是1
        number = '1'
        for _ in range(10):
            number += random.choice('0123456789')
        self.write_phone(number)
        return number

    def write_phone(self, phone):
        with open('phone_data.txt', 'a+') as file:
            # 写入内容为 JSON 格式
            file.write(json.dumps(phone))
            file.write('\n')  # 添加换行符


if __name__ == '__main__':
    api = CheckApi("13246622761")
    api.user_codes()
    for i in range(5):
        api.login_api()
        api.login_use_code()
    # api.generate_phone_number()
