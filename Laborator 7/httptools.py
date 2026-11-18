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


print(search({"q": "python", "page": 2}))
print(search_url({"q": "hello world & co"}))
print(fetch_with_agent("MyBot/1.0"))
print(default_agent())




