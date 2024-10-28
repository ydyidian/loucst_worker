import json
import requests


class CheckApi(object):
    def __init__(self):
        self.uri = "https://api-next-gateway-staging.actqa.com"
        self.bali_uri = "https://api-gateway-bali-staging.actqa.com"
        self.token = self.login(self.uri)

    @classmethod
    def login(cls, url_data):
        url = f"{url_data}/user/public/v1/login"
        headers = {
            'Content-Type': 'application/json'
        }

        data = {
            "country_code": "cn",
            "mobile": "86-13246622761",
            "method": "MOBILE",
            "code": "123456"
        }
        response = requests.request("POST", url, headers=headers, json=data)
        # print(response.text)
        # print(response.json()["data"]["token"])
        return response.json()["data"]["token"]

    def get_keys(self, data):
        if isinstance(data, dict):
            return set(data.keys())
        return set()

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

    def compare_urls(self, url1, url2, method='GET', params=None, json_data=None):
        """ 比较两个 URL 返回的数据是否相同 """
        try:
            data1 = self.fetch_data(url1, method, params, json_data)
            data2 = self.fetch_data(url2, method, params, json_data)

            print(data1)
            print(data2)

            keys1 = list(self.get_keys(data1))
            keys2 = list(self.get_keys(data2))

            if keys1 != keys2:
                with open('./file_data/check_data.txt', 'a+') as file:
                    # 写入内容为 JSON 格式
                    file.write(json.dumps({"url": url1, 'keys1': data1, "bali_url": url2, 'keys2': data2}, indent=4))
                    file.write('\n')  # 添加换行符
                return False

            return True

        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def login_api(self):
        data = "/user/public/v1/login"
        url = f"{self.uri}{data}"
        bali = f"{self.bali_uri}{data}"

        data = {
            "country_code": "cn",
            "mobile": "86-13246622761",
            "method": "MOBILE",
            "code": "123456"
        }
        are_equal_get = self.compare_urls(url, bali, method='POST', json_data=data)
        print("POST 请求的两个接口返回的参数是否相同:", are_equal_get)

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
        bali = f"{self.bali_uri}{data}"
        data = {
            "body": "5616",
            "uploaded_materials": [],
            "topics": [],
            "post_type": "NORMAL"
        }
        are_equal_get = self.compare_urls(url, bali, method='POST', json_data=data)
        print("POST 请求的两个接口返回的参数是否相同:", are_equal_get)

    # 创建评论
    def post(self):
        data = "/post/public/v1/post/MzQ5OTY1MjkwMjY2OTUxNjh8NjY5ODgyNzEzMzEwNjI4NjQ="
        url = f"{self.uri}{data}"
        bali = f"{self.bali_uri}{data}"

        are_equal_get = self.compare_urls(url, bali, method='GET', params=data)
        print("GET 请求的两个接口返回的参数是否相同:", are_equal_get)

    # 点赞
    def like(self):
        data = "/post/private/v1/like"
        url = f"{self.uri}{data}"
        bali = f"{self.bali_uri}{data}"
        data = {
            "comment_id": "NjQ3OTM3NDA5MTI3MTc4MjR8MjU2MDA0MTA3MTI2NzQzNDczNA==",
            "post_id": "",
            "action": "LIKE"
        }

        are_equal_get = self.compare_urls(url, bali, method='POST', json_data=data)
        print("POST 请求的两个接口返回的参数是否相同:", are_equal_get)

    # 推荐
    def recommended(self):
        data = "/post/public/v1/posts/recommended"
        url = f"{self.uri}{data}"
        bali = f"{self.bali_uri}{data}"
        data = {
            "limit": 15
        }

        are_equal_get = self.compare_urls(url, bali, method='GET', params=data)
        print("GET 请求的两个接口返回的参数是否相同:", are_equal_get)

    # 关注
    def followed(self):
        data = "/post/private/v1/posts/followed"
        url = f"{self.uri}{data}"
        bali = f"{self.bali_uri}{data}"
        data = {
            "limit": 15
        }

        are_equal_get = self.compare_urls(url, bali, method='GET', params=data)
        print("GET 请求的两个接口返回的参数是否相同:", are_equal_get)

    # 创建评论
    def comments(self):
        data = "/post/private/v1/comments"
        url = f"{self.uri}{data}"
        bali = f"{self.bali_uri}{data}"
        data = {
            "body": "粉尘",
            "post_id": "MzQ5OTY1MjkwMjY2OTUxNjh8NjcwMDY4MzUyMjgzMDA4Njc="
        }

        are_equal_get = self.compare_urls(url, bali, method='POST', json_data=data)
        print("POST 请求的两个接口返回的参数是否相同:", are_equal_get)


if __name__ == '__main__':
    api = CheckApi()
    api.posts()
    api.post()
    api.like()
    api.recommended()
    api.followed()
    api.comments()

