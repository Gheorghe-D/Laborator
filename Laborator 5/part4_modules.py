
# Laborator: functii, metode si importuri pe web
# Student: Diacencu Gheorghe
# Grupa: SI-262
# Anul: I

import requests
import time
import re
import hashlib
import json
import socket
import ssl

from datetime import datetime, timezone
from urllib.parse import urlparse, urljoin
from html.parser import HTMLParser

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10


# Exercitiul 35 - Componentele unui URL
def url_parts(url: str) -> None:
    """Afiseaza componentele unei adrese URL."""
    parti = urlparse(url)

    print("Schema:", parti.scheme)
    print("Domeniu:", parti.netloc)
    print("Cale:", parti.path)
    print("Parametri:", parti.query)
    print("Fragment:", parti.fragment)


# Exercitiul 36 - Unirea adreselor
def make_urls(base: str, links: list) -> list:
    """Transforma linkurile relative in adrese complete."""
    rezultat = []

    for link in links:
        rezultat.append(urljoin(base, link))

    return rezultat


# Exercitiul 37 - Extragerea linkurilor
def extract_links(html: str) -> list:
    """Extrage linkurile href si elimina duplicatele."""
    gasite = re.findall(r'href="([^"]+)"', html)
    linkuri = []

    for link in gasite:
        if link not in linkuri:
            linkuri.append(link)

    return linkuri


# Exercitiul 38 - Linkuri interne si externe
def split_links(links: list, domain: str):
    """Imparte linkurile in interne si externe."""
    interne = []
    externe = []

    baza = "https://" + domain

    for link in links:
        adresa = urljoin(baza, link)
        parti = urlparse(adresa)

        if parti.scheme not in ("http", "https"):
            continue

        if parti.netloc.lower() == domain.lower():
            interne.append(adresa)
        else:
            externe.append(adresa)

    return interne, externe


# Exercitiul 39 - Extragerea imaginilor
class ImageFinder(HTMLParser):
    """Gaseste imaginile din codul HTML."""

    def __init__(self):
        """Creeaza o lista pentru imagini."""
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        """Cauta atributul src al imaginilor."""
        if tag == "img":
            src = dict(attrs).get("src")

            if src:
                self.images.append(src)


# Exercitiul 40 - Calcularea unui hash
def page_fingerprint(url: str) -> str:
    """Calculeaza hash-ul SHA-256 al paginii."""
    time.sleep(1)

    raspuns = requests.get(url, timeout=TIMEOUT)
    hash_pagina = hashlib.sha256(raspuns.content).hexdigest()

    return hash_pagina


# Exercitiul 41 - Salvarea antetelor in JSON
def save_headers(url: str) -> None:
    """Salveaza antetele HTTP intr-un fisier JSON."""
    time.sleep(1)

    raspuns = requests.get(url, timeout=TIMEOUT)

    with open("headers.json", "w", encoding="utf-8") as fisier:
        json.dump(dict(raspuns.headers), fisier, indent=2)

    with open("headers.json", "r", encoding="utf-8") as fisier:
        date = json.load(fisier)

    print("Content-Type din JSON:",
          date.get("Content-Type", "lipseste"))


# Exercitiul 42 - Obtinerea adresei IP
def resolve(hostname: str) -> str:
    """Obtine adresa IPv4 a unui domeniu."""
    return socket.gethostbyname(hostname)


# Exercitiul 43 - Verificarea certificatului
def cert_days_left(hostname: str) -> int:
    """Calculeaza cate zile mai este valabil certificatul TLS."""
    context = ssl.create_default_context()

    with socket.create_connection((hostname, 443), timeout=TIMEOUT) as conexiune:
        with context.wrap_socket(conexiune, server_hostname=hostname) as tls:
            certificat = tls.getpeercert()

    data_text = certificat["notAfter"]
    secunde = ssl.cert_time_to_seconds(data_text)

    expirare = datetime.fromtimestamp(secunde, timezone.utc)
    acum = datetime.now(timezone.utc)

    diferenta = expirare - acum

    return diferenta.days


# Executarea exercitiilor
if __name__ == "__main__":

    # Exercitiul 35
    print("Ex. 35 - Componentele URL:")
    url_parts("https://cybercor.org/path?x=1#top")

    # Exercitiul 36
    linkuri = ["/about", "contact.html", "../index.html"]
    print("Ex. 36 - Adrese complete:", make_urls(BASE_URL, linkuri))

    # Exercitiul 37
    response = requests.get(BASE_URL, timeout=TIMEOUT)
    links = extract_links(response.text)
    print("Ex. 37 - Linkuri:", links)

    # Exercitiul 38
    interne, externe = split_links(links, "cybercor.org")

    print("Ex. 38 - Linkuri interne:", len(interne))
    print("Linkuri externe:", len(externe))

    # Exercitiul 39
    exemplu_html = '<img src="/logo.png"><img src="poza.jpg">'

    finder = ImageFinder()
    finder.feed(exemplu_html)

    print("Ex. 39 - Imagini test:", finder.images)

    finder = ImageFinder()
    finder.feed(response.text)

    print("Imagini gasite pe site:", finder.images)

    # Exercitiul 40
    primul = page_fingerprint(BASE_URL)
    al_doilea = page_fingerprint(BASE_URL)

    print("Ex. 40 - Primul hash:", primul)
    print("Al doilea hash:", al_doilea)
    print("Hashuri identice:", primul == al_doilea)

    # Exercitiul 41
    save_headers(BASE_URL)
    print("Ex. 41 - Fisierul headers.json a fost creat.")

    # Exercitiul 42
    print("Ex. 42 - Adresa IP:", resolve("cybercor.org"))

    # Exercitiul 43
    print("Ex. 43 - Zile pana la expirarea certificatului:",
          cert_days_left("cybercor.org"))

    print("\nAm terminat exercitiile 35-43.")

