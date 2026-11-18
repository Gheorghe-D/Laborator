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

def describe_status(code):
    response = requests.get(BASE + "/status/" + str(code), timeout=10)

    if 200 <= response.status_code < 300:
        return "Success"
    elif 400 <= response.status_code < 500:
        return "eroare Client"
    elif 500 <= response.status_code < 600:
        return "eroare Server"

def is_ok(code):
    try:
        response = requests.get(BASE + "/status/" + str(code), timeout=10)
        response.raise_for_status()
        return True
    except requests.RequestException:
        return False
    

print(search({"q": "python", "page": 2}))
print(search_url({"q": "hello world & co"}))
print(fetch_with_agent("MyBot/1.0"))
print(default_agent())
print(post_json({"name": "Ana", "age": 19}))
print((post_from({"user": "ana", "city": "Balti"})))
print(describe_status(200))
print(describe_status(404))
print(describe_status(503))
print(is_ok(200))
print(is_ok(500))



