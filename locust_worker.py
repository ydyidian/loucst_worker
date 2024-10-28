import json
import os
import random
import time
import logging
from datetime import datetime
import gevent.monkey

gevent.monkey.patch_all()
import ssl
import requests
from locust import FastHttpUser, task, between

time_date = time.time()


def get_date():
    current_time = datetime.now()
    time_name = current_time.strftime("%Y-%m-%d-%H-%M-%S")
    return time_name


def generate_phone_number():
    # 中国手机号码格式：11位数字，第一位是1
    number = '1'
    for _ in range(10):
        number += random.choice('0123456789')
    return number


def login():
    url = "https://api-gateway.socrates.com/user/public/v1/login"
    headers = {
        'Content-Type': 'application/json'
    }

    data = {
        "country_code": "cn",
        "mobile": f"86-20000000010",
        "method": "MOBILE",
        "code": "223311"
    }
    response = requests.request("POST", url, headers=headers, json=data)
    return response.json()["data"]["token"]


class ApiUser(FastHttpUser):
    # wait_time = between(1, 5)  # 设置用户执行任务之间的等待时间
    host = "https://api-gateway.socrates.com"

    def on_start(self):
        # 设置日志记录器
        self.logger = logging.getLogger(__name__)
        handler = logging.FileHandler(f'{get_date()}-request.log')
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        # self.token = login()

    # @task
    # def recommended(self):
    #     params = {
    #         "limit": 10,
    #         "time": time_date,
    #         "sign": "dafba112cca7d66819c76343bd45e778"
    #     }
    #     with self.client.get("/post/public/v1/posts/recommended", params=params, catch_response=True) as resp:
    #         # print(response.text)
    #         try:
    #             response = resp.json()
    #             if resp.status_code == 200 and response.get("msg") == "success" and response.get("code") == 200:
    #                 resp.success()
    #             else:
    #                 print(resp.text, resp.status_code)
    #                 resp.failure("recommended failure")
    #                 self.logger.error(f"recommended failure status_code:{resp.status_code}\n,response:{resp.text}\n")
    #         except Exception as e:
    #             print(resp.text, resp.status_code)
    #             resp.failure(f"recommended failure:{str(e)}")
    #             self.logger.error(
    #                 f"recommended failure status_code:{resp.status_code}\n,response:{resp.text}\n,error:{str(e)}\n")

    @task
    def posts(self):
        params = {
            "sorted_by": "LATEST",
            "limit": 10,
            "time": time_date,
            "sign": "dafba112cca7d66819c76343bd45e778"
        }
        with self.client.get("/post/public/v1/posts", params=params, catch_response=True) as resp:
            try:
                response = resp.json()
                if resp.status_code == 200 and response.get("msg") == "success" and response.get("code") == 200:
                    resp.success()
                else:
                    print(resp.text, resp.status_code)
                    resp.failure("posts failure")
                    self.logger.error(f"posts failure status_code:{resp.status_code}\n,response:{resp.text}\n")

            except Exception as e:
                print(resp.text)
                resp.failure(f"posts failure:{str(e)}")
                self.logger.error(
                    f"posts failure status_code:{resp.status_code}\n,response:{resp.text}\n,error:{str(e)}\n")

    # @task
    # def post(self):
    #     headers = {
    #         'Content-Type': 'application/json'
    #     }
    #     with self.client.get("/post/public/v1/post/NDM0MjkxODcwMzc1NTI2NDB8NDU4NzMyMjMyMTI0NDk3OTI=",
    #                          headers=headers, catch_response=True) as resp:
    #         try:
    #             response = resp.json()
    #             # print(response)
    #             if resp.status_code == 200 and response.get("msg") == "success" and response.get("code") == 200:
    #                 resp.success()
    #             else:
    #                 print(resp.text, resp.status_code)
    #                 resp.failure("post failure")
    #                 self.logger.error(f"post failure status_code:{resp.status_code}\n,response:{resp.text}\n")
    #         except Exception as e:
    #             print(resp.text)
    #             resp.failure(f"post failure:{str(e)}")
    #             self.logger.error(
    #                 f"post failure status_code:{resp.status_code}\n,response:{resp.text}\n,exception:{str(e)}\n")

    # @task
    # def private_comments(self):
    #     data = {
    #         "action": "AGAINST",
    #         "body": "我是个简简单单的人，",
    #         "post_id": "NDQ3NDI0Mzc1NzAyMDM2NDh8NDU2MTY1NTA2NjUyMjAwOTY=",
    #         "reply_to_comment_id": "",
    #         "source": "MOBILE"
    #     }
    #     headers = {"User-Agent": "socrates/v1.0.0 (Android 29;Redmi M2010J19SC)",
    #                "Authorization": "Bearer 6lT41daQ9xxxvhRB4m6ONpuShHH7tm7AzVVHxVXV1eH9LFRMY-P5svroy0XgxtQr1Y2avDCP7tiB9Nh87HTqG8oaF8XRycEpk5FeJP1YoBs="}
    #     with self.client.post("/post/private/v1/comments", headers=headers, json=data, catch_response=True) as resp:
    #         # print(headers)
    #         try:
    #             response = resp.json()
    #             if resp.status_code == 200 and response.get("msg") == "success" and response.get("code") == 200:
    #                 resp.success()
    #             else:
    #                 print(resp.text, resp.status_code)
    #                 resp.failure("comments failure")
    #                 self.logger.error(f"comments failure status_code:{resp.status_code}\n,response:{resp.text}\n")
    #         except Exception as e:
    #             print(resp.text)
    #             resp.failure(f"comments failure:{str(e)}")
    #             self.logger.error(
    #                 f"comments failure status_code:{resp.status_code}\n,response:{resp.text}\n,exception:{str(e)}\n")


if __name__ == '__main__':
    os.system(
        f"locust -f locust_worker.py --headless -u 1 -r 1 --host https://dev-api-gateway.actqa.com --run-time 5s --csv=./file_data/{get_date()}")
