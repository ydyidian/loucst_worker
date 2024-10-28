import requests
import time
import csv

# 定义接口的URL和测试参数
base_url = 'http://example.com/api'
login_url = f'{base_url}/login'
like_url = f'{base_url}/like'
list_url = f'{base_url}/list'

username = 'test_user'
password = 'test_pass'

# 测试配置
num_requests = 100  # 总请求数
timeout_limit = 2   # 超时时间限制

# 存储性能数据
performance_data = {
    'interface': ['login', 'like', 'list'],
    'total_requests': [0, 0, 0],
    'failed_requests': [0, 0, 0],
    'timeout_requests': [0, 0, 0],
    'response_times': {'login': [], 'like': [], 'list': []}
}

# 登陆函数
def login():
    start_time = time.time()
    try:
        response = requests.post(login_url, data={'username': username, 'password': password}, timeout=timeout_limit)
        elapsed_time = time.time() - start_time
        performance_data['response_times']['login'].append(elapsed_time)
        performance_data['total_requests'][0] += 1
        if response.status_code != 200:
            performance_data['failed_requests'][0] += 1
    except requests.exceptions.Timeout:
        performance_data['timeout_requests'][0] += 1
        performance_data['total_requests'][0] += 1
    except requests.exceptions.RequestException:
        performance_data['failed_requests'][0] += 1
        performance_data['total_requests'][0] += 1

# 点赞函数
def like():
    start_time = time.time()
    try:
        response = requests.post(like_url, timeout=timeout_limit)
        elapsed_time = time.time() - start_time
        performance_data['response_times']['like'].append(elapsed_time)
        performance_data['total_requests'][1] += 1
        if response.status_code != 200:
            performance_data['failed_requests'][1] += 1
    except requests.exceptions.Timeout:
        performance_data['timeout_requests'][1] += 1
        performance_data['total_requests'][1] += 1
    except requests.exceptions.RequestException:
        performance_data['failed_requests'][1] += 1
        performance_data['total_requests'][1] += 1

# 获取列表函数
def get_list():
    start_time = time.time()
    try:
        response = requests.get(list_url, timeout=timeout_limit)
        elapsed_time = time.time() - start_time
        performance_data['response_times']['list'].append(elapsed_time)
        performance_data['total_requests'][2] += 1
        if response.status_code != 200:
            performance_data['failed_requests'][2] += 1
    except requests.exceptions.Timeout:
        performance_data['timeout_requests'][2] += 1
        performance_data['total_requests'][2] += 1
    except requests.exceptions.RequestException:
        performance_data['failed_requests'][2] += 1
        performance_data['total_requests'][2] += 1

# 执行测试
for _ in range(num_requests):
    login()
    like()
    get_list()

# 计算QPS、TPS、最大值、最小值、平均值
results = []
for interface in performance_data['interface']:
    times = performance_data['response_times'][interface]
    total_requests = performance_data['total_requests'][performance_data['interface'].index(interface)]
    failed_requests = performance_data['failed_requests'][performance_data['interface'].index(interface)]
    timeout_requests = performance_data['timeout_requests'][performance_data['interface'].index(interface)]

    if times:
        max_time = max(times)
        min_time = min(times)
        avg_time = sum(times) / len(times)
        qps = total_requests / (sum(times) if sum(times) > 0 else 1)
        tps = (total_requests - failed_requests - timeout_requests) / (sum(times) if sum(times) > 0 else 1)
    else:
        max_time = min_time = avg_time = qps = tps = 0

    results.append({
        'interface': interface,
        'total_requests': total_requests,
        'failed_requests': failed_requests,
        'timeout_requests': timeout_requests,
        'qps': qps,
        'tps': tps,
        'max_time': max_time,
        'min_time': min_time,
        'avg_time': avg_time
    })

# 输出到CSV文件
with open('performance_results.csv', mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['interface', 'total_requests', 'failed_requests', 'timeout_requests', 'qps', 'tps', 'max_time', 'min_time', 'avg_time'])
    writer.writeheader()
    for result in results:
        writer.writerow(result)

print("Performance test results have been written to performance_results.csv")
