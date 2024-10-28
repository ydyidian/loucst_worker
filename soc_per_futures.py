import concurrent.futures
import random
import requests
import csv
import time
from datetime import datetime
import numpy as np


def generate_phone_number():
    # 中国手机号码格式：11位数字，第一位是1
    number = '1'
    for _ in range(10):
        number += random.choice('0123456789')
    return number


# 定义接口地址和测试参数
API_BASE_URL = 'https://api-gateway.socrates.com'
# post访问
# API_BASE_URL = 'https://172.31.5.242:5333'
# gateway
# API_BASE_URL = 'https://172.31.47.179:28081'

INTERFACES = [
    {
        'name': 'recommended',
        'endpoint': '/post/public/v1/posts/recommended',
        'method': 'GET',
        'params': {
            "limit": 10,
            "time": int(time.time()),
            "sign": "dafba112cca7d66819c76343bd45e778"
        }
    },
    {
        'name': 'posts',
        'endpoint': '/post/public/v1/posts',
        'method': 'GET',
        'params': {
            "sorted_by": "LATEST",
            "limit": 10,
            "time": int(time.time()),
            "sign": "dafba112cca7d66819c76343bd45e778"
        }
    },
    {
        'name': 'post',
        'endpoint': '/post/public/v1/post/NDI0MDI1MjAyMjM1MTQ2MjR8NDQ1NDI1ODA5MDU4ODU2OTY=',
        'method': 'GET',
        'params': {}
    },
    {
        'name': 'private_comments',
        'endpoint': '/post/private/v1/comments',
        'method': 'POST',
        'data': {
            "post_id": "NDQ0Mzc3NTIzNTk1Mzg2ODh8NDQ4ODk3OTc5NTcyMTAxMTI=",
            "body": "让世界听到不一样的声音，从你我开始",
            "action": "AGAINST",
            "source": "MOBILE",
            "reply_to_comment_id": ""
        }
    }
]
TOTAL_REQUESTS = 5000  # 总请求次数
TIMEOUT = 5  # 超时时间（秒）


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


headers = {"User-Agent": "socrates/v1.0.0 (Android 29;Redmi M2010J19SC)",
           "Authorization": f"Bearer {login()}"}


def run_performance_test(interface):
    url = API_BASE_URL + interface['endpoint']
    method = interface['method']
    data = interface.get('data')
    params = interface.get('params')

    success_count = 0
    fail_count = 0
    timeout_count = 0
    response_times = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = []
        for _ in range(TOTAL_REQUESTS):
            print(f"运行次数为：{_ + 1}")
            # start_time = time.time()
            if method == 'POST':
                futures.append(executor.submit(requests.post, url, json=data, headers=headers, timeout=TIMEOUT))
            elif method == 'GET':
                futures.append(executor.submit(requests.get, url, params=params, timeout=TIMEOUT))
        # print(futures)
        for future in concurrent.futures.as_completed(futures):
            try:
                start_time = time.time()
                response = future.result()
                # print(response.json())
                end_time = time.time()
                if response.status_code == 200 and response.json()["code"] == 200 and response.json()[
                    "msg"] == "success":
                    success_count += 1
                    response_times.append(end_time - start_time)
                else:
                    fail_count += 1
            except requests.exceptions.Timeout:
                timeout_count += 1
            except requests.exceptions.RequestException as e:
                fail_count += 1
                print(f"Request failed: {e}")

    # 计算各项指标
    total_time = sum(response_times)
    if response_times:
        max_time = max(response_times)
        min_time = min(response_times)
        avg_time = total_time / len(response_times)
    else:
        max_time = 0
        min_time = 0
        avg_time = 0

    qps = TOTAL_REQUESTS / total_time if total_time > 0 else 0
    tps = success_count / total_time if total_time > 0 else 0
    percentiles = np.percentile(response_times, [50, 60, 70, 80, 90, 99])

    return {
        'name': interface['name'],
        'total_requests': TOTAL_REQUESTS,
        "success": success_count,
        'failures': fail_count,
        'timeouts': timeout_count,
        'qps': qps,
        'tps': tps,
        'max_response_time': max_time,
        'min_response_time': min_time,
        'avg_response_time': avg_time,
        "50%": percentiles[0],
        "60%": percentiles[1],
        "70%": percentiles[2],
        "80%": percentiles[3],
        "90%": percentiles[4],
        "99%": percentiles[5]
    }


# 执行测试并写入 CSV 文件
def main():
    print("测试开始")
    results = []
    for interface in INTERFACES:
        result = run_performance_test(interface)
        # print(result)
        results.append(result)
    print(results)
    # 写入 CSV 文件
    csv_filename = f'./file_data/performance{get_date()}.csv'
    with open(csv_filename, 'w', newline='') as csvfile:
        fieldnames = ['name', 'total_requests', 'success', 'failures', 'timeouts', 'qps', 'tps', 'max_response_time',
                      'min_response_time', 'avg_response_time', '50%', '60%', '70%', '80%', '90%', '99%']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(result)

    print(f"Performance test results written to {csv_filename}")


def get_date():
    current_time = datetime.now()
    time_name = current_time.strftime("%Y-%m-%d-%H-%M-%S")
    return time_name


if __name__ == "__main__":
    main()
