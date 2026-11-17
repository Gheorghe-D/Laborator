
# Laborator: functii, metode si importuri pe web
# Student: Diacencu Gheorghe
# Grupa: SI-262
# Anul: I

import requests
import time

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10


# Exercitiul 9 - Atributele raspunsului
response = requests.get(BASE_URL, timeout=TIMEOUT)

print("Ex. 9 - Cod HTTP:", response.status_code)  # atribut
print("Raspuns bun:", response.ok)  # atribut
print("URL final:", response.url)  # atribut
print("Codificare:", response.encoding)  # atribut


# Exercitiul 10 - Tratarea erorilor
response.raise_for_status()

time.sleep(1)

try:
    lipsa = requests.get(BASE_URL + "/this-page-does-not-exist",
                         timeout=TIMEOUT)
    lipsa.raise_for_status()

    print("Ex. 10 - Codul paginii:", lipsa.status_code)

except requests.HTTPError as eroare:
    print("Ex. 10 - Eroare HTTP:", eroare)

# raise_for_status() produce o eroare pentru codurile 4xx si 5xx.
# La testarea mea, site-ul a raspuns cu 200 si pentru aceasta cale.


# Exercitiul 11 - Afisarea antetelor
print("\nEx. 11 - Antetele raspunsului:")

for nume, valoare in response.headers.items():
    print(nume + ":", valoare)


# Exercitiul 12 - Cautarea unui antet
print("\nEx. 12 - Server:",
      response.headers.get("Server", "lipseste"))

print("Content-Type:",
      response.headers.get("Content-Type", "lipseste"))

print("content-type:",
      response.headers.get("content-type", "lipseste"))

# Numele antetelor nu depind de litere mari sau mici.


# Exercitiul 13 - Metode pentru text
aparitii = response.text.lower().count("cyber")

print("\nEx. 13 - Cuvantul cyber apare de", aparitii, "ori")

# lower() transforma textul in litere mici.
# count() numara aparitiile cuvantului cautat.


# Exercitiul 14 - Titlul paginii
html = response.text

start = html.lower().find("<title>")
stop = html.lower().find("</title>")

if start != -1 and stop != -1:
    start = start + len("<title>")
    titlu = html[start:stop].strip()
else:
    titlu = "Titlu negasit"

print("Ex. 14 - Titlul paginii:", titlu)

# find() cauta pozitia unui text.
# [start:stop] extrage o parte din text.
# strip() elimina spatiile de la inceput si sfarsit.


# Exercitiul 15 - Numararea liniilor
linii = html.splitlines()

print("Ex. 15 - Numar de linii:", len(linii))

if linii:
    linia_lunga = max(linii, key=len)
    print("Cea mai lunga linie:", len(linia_lunga))
else:
    print("Pagina nu contine linii.")

# splitlines() imparte textul in linii.
# max() gaseste linia cu cele mai multe caractere.


# Exercitiul 16 - Verificarea HTTPS
if response.url.startswith("https://"):
    print("Ex. 16 - Conexiune securizata")
else:
    print("Ex. 16 - Conexiune nesecurizata")

# startswith() verifica inceputul unui sir de caractere.


# Exercitiul 17 - Redirectionari
time.sleep(1)

raspuns = requests.get("http://cybercor.org", timeout=TIMEOUT)

print("\nEx. 17 - Redirectionari:")

for pas in raspuns.history:
    print(pas.status_code, pas.url)

print("URL final:", raspuns.url)

# history pastreaza raspunsurile de redirectionare.
# Site-ul poate redirectiona de la HTTP la HTTPS.


# Exercitiul 18 - HEAD si GET
time.sleep(1)

raspuns_head = requests.head(BASE_URL, timeout=TIMEOUT)

time.sleep(1)

raspuns_get = requests.get(BASE_URL, timeout=TIMEOUT)

print("\nEx. 18 - HEAD bytes:", len(raspuns_head.content))
print("GET bytes:", len(raspuns_get.content))

# HEAD primeste antetele, fara corpul paginii.
# GET primeste si continutul paginii.


# Exercitiul 19 - Cookie-uri
print("\nEx. 19 - Cookie-uri:")

if response.cookies:
    for cookie in response.cookies:
        print("Nume:", cookie.name)
        print("Secure:", cookie.secure)
else:
    print("Niciun cookie setat")

# Cookie-urile pot pastra informatii despre o sesiune.


# Exercitiul 20 - Sesiuni
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

# Session pastreaza setarile intre cereri.
# Antetul personalizat este trimis doar catre httpbin.org.
# response.text este atribut, iar response.json() este metoda.


print("\nAm terminat exercitiile 9-20.")

