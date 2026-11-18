import requests

BASE = "https://httpbin.org"

def search(params):
    response = requests.get(BASE + "/get", params=params, timeout = 10)
    return response.json()["args"]

def search_url(params):
    response = requests.get(BASE + "/get", params=params, timeout = 10)
    return response.url


print(search({"q": "python", "page": 2}))
print(search_url({"q": "hello world & co"}))


