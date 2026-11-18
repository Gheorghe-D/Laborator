
import requests
import urllib.request
import urllib.error
import time

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10


print("Ex. 1 - Versiunea requests:", requests.__version__)

raspuns = requests.get(BASE_URL, timeout=TIMEOUT)
print("Ex. 2 - requests.get:", raspuns.status_code)

time.sleep(1)

from requests import get

raspuns = get(BASE_URL, timeout=TIMEOUT)
print("Ex. 2 - get:", raspuns.status_code)

import requests as rq

time.sleep(1)

raspuns = rq.get(BASE_URL, timeout=TIMEOUT)
print("Ex. 3 - Alias rq:", raspuns.status_code)

time.sleep(1)

try:
    with urllib.request.urlopen(BASE_URL, timeout=TIMEOUT) as raspuns_urllib:
        print("Ex. 4 - Status:", raspuns_urllib.status)

        html = raspuns_urllib.read().decode("utf-8")
        print("Primele 200 de caractere:", html[:200])

except urllib.error.HTTPError as eroare:
    print("Ex. 4 - Eroare HTTP:", eroare.code)

except urllib.error.URLError as eroare:
    print("Ex. 4 - Eroare de conexiune:", eroare.reason)

print("Ex. 5 - Continutul modulului requests:")
print(dir(requests))

print("Ex. 6 - Documentatia pentru requests.get:")
help(requests.get)

time.sleep(1)

raspuns = requests.get(BASE_URL, timeout=TIMEOUT)
print("Ex. 6 - Status:", raspuns.status_code)

time.sleep(1)

start = time.perf_counter()

raspuns = requests.get(BASE_URL, timeout=TIMEOUT)

sfarsit = time.perf_counter()
durata = sfarsit - start

print("Ex. 7 - Timp masurat:", round(durata, 3), "secunde")
print("Ex. 7 - response.elapsed:", raspuns.elapsed.total_seconds(), "secunde")

try:
    import bs4
    print("Ex. 8 - Modulul bs4 este instalat")

except ImportError:
    print("Instalati modulul cu: pip install beautifulsoup4")

print("\nAm terminat exercitiile 1-8.")



