
import requests
import time

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10


response = requests.get(BASE_URL, timeout=TIMEOUT)

print("Ex. 9 - Cod HTTP:", response.status_code)
print("Raspuns bun:", response.ok)
print("URL final:", response.url)
print("Codificare:", response.encoding)

response.raise_for_status()

time.sleep(1)

try:
    lipsa = requests.get(BASE_URL + "/this-page-does-not-exist",
                         timeout=TIMEOUT)
    lipsa.raise_for_status()

    print("Ex. 10 - Codul paginii:", lipsa.status_code)

except requests.HTTPError as eroare:
    print("Ex. 10 - Eroare HTTP:", eroare)

print("\nEx. 11 - Antetele raspunsului:")

for nume, valoare in response.headers.items():
    print(nume + ":", valoare)

print("\nEx. 12 - Server:",
      response.headers.get("Server", "lipseste"))

print("Content-Type:",
      response.headers.get("Content-Type", "lipseste"))

print("content-type:",
      response.headers.get("content-type", "lipseste"))

aparitii = response.text.lower().count("cyber")

print("\nEx. 13 - Cuvantul cyber apare de", aparitii, "ori")

html = response.text

start = html.lower().find("<title>")
stop = html.lower().find("</title>")

if start != -1 and stop != -1:
    start = start + len("<title>")
    titlu = html[start:stop].strip()
else:
    titlu = "Titlu negasit"

print("Ex. 14 - Titlul paginii:", titlu)

linii = html.splitlines()

print("Ex. 15 - Numar de linii:", len(linii))

if linii:
    linia_lunga = max(linii, key=len)
    print("Cea mai lunga linie:", len(linia_lunga))
else:
    print("Pagina nu contine linii.")

if response.url.startswith("https://"):
    print("Ex. 16 - Conexiune securizata")
else:
    print("Ex. 16 - Conexiune nesecurizata")

time.sleep(1)

raspuns = requests.get("http://cybercor.org", timeout=TIMEOUT)

print("\nEx. 17 - Redirectionari:")

for pas in raspuns.history:
    print(pas.status_code, pas.url)

print("URL final:", raspuns.url)

time.sleep(1)

raspuns_head = requests.head(BASE_URL, timeout=TIMEOUT)

time.sleep(1)

raspuns_get = requests.get(BASE_URL, timeout=TIMEOUT)

print("\nEx. 18 - HEAD bytes:", len(raspuns_head.content))
print("GET bytes:", len(raspuns_get.content))

print("\nEx. 19 - Cookie-uri:")

if response.cookies:
    for cookie in response.cookies:
        print("Nume:", cookie.name)
        print("Secure:", cookie.secure)
else:
    print("Niciun cookie setat")

session = requests.Session()

session.headers.update({
    "User-Agent": "WebLab-Diacencu-Gheorghe"
})

time.sleep(1)

raspuns = session.get(ECHO_URL + "/headers", timeout=TIMEOUT)

date = raspuns.json()
antete = date.get("headers", {})

print("\nEx. 20 - User-Agent trimis:",
      antete.get("User-Agent"))

session.close()

print("\nAm terminat exercitiile 9-20.")


