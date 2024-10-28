import requests


def del_userId():
    uri = "https://api-next-gateway-staging.actqa.com"
    url = f"{uri}/api/union/activity/task/deleteUser?userId=85031499834141647&key=owsQS221sQ"
    response = requests.request('GET', url)
    print(response.json())


if __name__ == '__main__':
    del_userId()
