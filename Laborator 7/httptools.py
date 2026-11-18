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

def count_redirects(n):
    response = requests.get(BASE + "/redirect/" + str(n), timeout=10)
    return len(response.history)

def final_url(n):
    response = requests.get(BASE + "/redirect/" + str(n), timeout=10)
    return response.url

def first_hop(n):
    response = requests.get(
        BASE + "/redirect/" + str(n),
        allow_redirects=False,
        timeout=10

    )    
    return response.headers["Location"]


    

def cookie_demo(name, value):
    session = requests.Session()
    session.get(BASE + "/cookies/set", params={name: value}, timeout=10)
    response = session.get(BASE + "/cookies", timeout=10)
    return response.json()["cookies"]


def no_session_demo(name, value):
    requests.get(BASE + "/cookies/set", params={name: value}, timeout=10)
    response = requests.get(BASE + "/cookies", timeout=10)
    return response.json()["cookies"]
 

PATHS = ["/get", "/redirect/2", "/delay/1", "/status/404", "/delay/5"]


def report(path):
    try:
        response = requests.get(BASE + path, timeout=3)

        return {
            "status": response.status_code,
            "final_url": response.url,
            "redirects": len(response.history),
            "seconds": response.elapsed.total_seconds(),
            "content_type": response.headers.get("Content-Type")
        }

    except requests.RequestException as error:
        return {"status": None, "error": str(error)}





def check_login(user, password):
    try:
        response = requests.get(
            BASE + "/basic-auth/admin/secret",
            auth=(user, password),
            timeout=10
        )
        return response.status_code == 200
    except requests.RequestException:
        return False




# print(check_login("admin", "secret"))
# print(check_login("admin", "gresit"))

# print(search({"q": "python", "page": 2}))
# print(search_url({"q": "hello world & co"}))
print(fetch_with_agent("MyBot/1.0"))
print(default_agent())
print(post_json({"name": "Ana", "age": 19}))
print((post_from({"user": "ana", "city": "Balti"})))
print(describe_status(200))
print(describe_status(404))
print(describe_status(503))
print(is_ok(200))
print(is_ok(500))
print(count_redirects(3))
print(final_url(3))
print(first_hop(3))
# print(cookie_demo("theme", "dark"))
# print(no_session_demo("theme", "dark"))




