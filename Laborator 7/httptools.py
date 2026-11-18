import requests

BASE = "https://httpbin.org"

def search(params):
    response = requests.get(BASE + "/get", params=params, timeout = 10)
    return response.json()["args"]

def search_url(params):
    response = requests.get(BASE + "/get", params=params, timeout = 10)
    return response.url

def fetch_with_agent(agent):
    response = requests.get(
        BASE + "/headers",
        headers={"User-Agent": agent},
        timeout = 10
    )
    return response.json()["headers"]["User-Agent"]

def default_agent():
    response = requests.get(BASE + "/headers", timeout = 10)
    return response.json()["headers"]["User-Agent"]

def post_json(data):
    response = requests.post(BASE + "/post", json=data, timeout=10)
    return response.json()["json"]

def post_from(data):
    response = requests.post(BASE +  "/post", data=data, timeout=10)
    return response.json()["form"]

print(search({"q": "python", "page": 2}))
print(search_url({"q": "hello world & co"}))
print(fetch_with_agent("MyBot/1.0"))
print(default_agent())
print(post_json({"name": "Ana", "age": 19}))
print((post_from({"user": "ana", "city": "Balti"})))




