
# Laborator: functii, metode si importuri pe web
# Student: Diacencu Gheorghe
# Grupa: SI-262
# Anul: I

import requests
import urllib.request
import urllib.error
import time

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10


# Exercitiul 1 - Importuri
print("Ex. 1 - Versiunea requests:", requests.__version__)

# requests se instaleaza separat cu pip.
# urllib este inclus in Python.


# Exercitiul 2 - Doua stiluri de import
raspuns = requests.get(BASE_URL, timeout=TIMEOUT)
print("Ex. 2 - requests.get:", raspuns.status_code)

# Cu requests.get vad clar din ce biblioteca vine functia.

time.sleep(1)

from requests import get

raspuns = get(BASE_URL, timeout=TIMEOUT)
print("Ex. 2 - get:", raspuns.status_code)

# Cu from import pot apela functia direct.


# Exercitiul 3 - Alias
import requests as rq

time.sleep(1)

raspuns = rq.get(BASE_URL, timeout=TIMEOUT)
print("Ex. 3 - Alias rq:", raspuns.status_code)

# Aliasul poate scurta un nume lung.
# Daca aleg un nume neclar, codul este mai greu de inteles.


# Exercitiul 4 - Biblioteca standard
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

# read() citeste octeti, iar decode() ii transforma in text.
# Daca serverul raspunde cu 403, afisez eroarea.


# Exercitiul 5 - Continutul unui modul
print("Ex. 5 - Continutul modulului requests:")
print(dir(requests))

# requests.get este o functie.
# requests.Session este o clasa.
# requests.exceptions este un modul.


# Exercitiul 6 - Documentatia
print("Ex. 6 - Documentatia pentru requests.get:")
help(requests.get)

# timeout stabileste timpul maxim de asteptare.

time.sleep(1)

raspuns = requests.get(BASE_URL, timeout=TIMEOUT)
print("Ex. 6 - Status:", raspuns.status_code)


# Exercitiul 7 - Masurarea timpului
time.sleep(1)

start = time.perf_counter()

raspuns = requests.get(BASE_URL, timeout=TIMEOUT)

sfarsit = time.perf_counter()
durata = sfarsit - start

print("Ex. 7 - Timp masurat:", round(durata, 3), "secunde")
print("Ex. 7 - response.elapsed:", raspuns.elapsed.total_seconds(), "secunde")

# perf_counter masoara durata apelului.
# response.elapsed masoara timpul pana la primirea antetelor.


# Exercitiul 8 - Eroare la import
try:
    import bs4
    print("Ex. 8 - Modulul bs4 este instalat")

except ImportError:
    print("Instalati modulul cu: pip install beautifulsoup4")

# Un modul este un fisier cu cod Python.
# Un pachet grupeaza mai multe module.
# O biblioteca contine cod care poate fi reutilizat.


print("\nAm terminat exercitiile 1-8.")


