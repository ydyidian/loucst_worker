import json
import random

import requests


class InviteFriends(object):
    def __init__(self, phone):
        self.uri = "https://api-next-gateway-staging.actqa.com"
        self.phone = phone
        self.token = self.login(self.uri, self.phone)
        self.code = self.user_codes(self.uri, self.token)
        self.friends_token = None

    @classmethod
    def login(cls, uri, phone):
        url = f"{uri}/user/public/v1/login"
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
        print(f'用户登陆号码为：{phone}')
        return response.json()["data"]["token"]

    # 获取用户邀请码
    @classmethod
    def user_codes(cls, uri, token):
        url = f"{uri}/user/private/v1/user_codes"
        headers = {
            'Content-Type': 'application/json',
            "Authorization": "Bearer " + token
        }
        data = {}
        response = requests.request("POST", url, json=data, headers=headers)
        print(f'获取用户邀请码为：{response.json()["data"].get("code")}')
        return response.json()["data"].get("code")

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
        url = f"{self.uri}/user/public/v1/login"
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            "country_code": "cn",
            "mobile": f"86-{self.generate_phone_number()}",
            "method": "MOBILE",
            "code": "123456"
        }
        response = requests.request('POST', url, json=data, headers=headers)
        self.friends_token = response.json()["data"]["token"]
        # print(self.friends_token)

    # 登陆和输入邀请码
    def login_use_code(self):

        url = f"{self.uri}/user/private/v1/login_use_code"
        headers = {
            'Content-Type': 'application/json',
            "Authorization": "Bearer " + self.friends_token
        }
        data = {
            "code": self.code
        }

        response = requests.request('POST', url, json=data, headers=headers)
        print("邀请状态码：", response.json().get("code"))
        # print(response.json())

    def generate_phone_number(self):
        # 中国手机号码格式：11位数字，第一位是1
        number = '1'
        for _ in range(10):
            number += random.choice('0123456789')
        self.write_phone(number)
        print(f"被邀请手机号码为：{number}")
        return number

    def my_info(self):
        url = f"{self.uri}/user/private/v1/my_info"
        headers = {
            'Content-Type': 'application/json',
            "Authorization": "Bearer " + self.friends_token
        }
        data = {}

        response = requests.request('GET', url, params=data, headers=headers)
        # print(response.json())
    def hist_detail(self):
        url = f"{self.uri}/api/union/activity/home/histDetail?activityId=1031"
        headers = {
            'Content-Type': 'application/json',
            "Authorization": "Bearer " + self.friends_token
        }
        data = {}

        response = requests.request('GET', url, params=data, headers=headers)
        print(response.json().get("myPoints"))
        print(response.json().get("rewardAmount"))
    # 发布帖子
    def posts(self):
        url = f"{self.uri}/post/private/v1/posts"
        data = {
            "body": self.generate_random_title(),
            "uploaded_materials": [],
            "topics": [],
            "post_type": "NORMAL"
        }
        response = self.fetch_data(url, method='POST', json_data=data)
        print(f'发布帖子状态为：{response.get("msg")}')

    # 写入随机生成的手机号码
    def write_phone(self, phone):
        with open('./file_data/phone_data.txt', 'a+') as file:
            # 写入内容为 JSON 格式
            file.write(json.dumps(phone))
            file.write('\n')  # 添加换行符

    # 随机生成帖子标题
    def generate_random_title(self):
        # 定义一些主题词和修饰词
        subjects = ["生活", "爱情", "旅行", "科技", "教育", "健康", "美食", "艺术"]
        adjectives = ["奇妙的", "幸福的", "美丽的", "神秘的", "有趣的", "重要的", "创新的"]

        # 随机选择一个主题词和一个修饰词
        subject = random.choice(subjects)
        adjective = random.choice(adjectives)

        # 组合成标题
        title = f"{adjective}{subject}故事"
        print(f"生成帖子标题为：{title}")
        return title


if __name__ == '__main__':
    # invite = InviteFriends("13246622761")
    # invite = InviteFriends("12345678998")
    invite = InviteFriends("17693747630")
    # invite = InviteFriends("13581500991")
    # invite.posts()
    for i in range(14):
        invite.login_api()
        invite.login_use_code()
        invite.my_info()
        print("邀请用户总数为：", i + 1)
