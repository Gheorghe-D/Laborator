
# Laborator: functii, metode si importuri pe web
# Student: Diacencu Gheorghe
# Grupa: SI-262
# Anul: I

import requests
import time
import re
import json
import socket
import ssl

from datetime import datetime, timezone
from urllib.parse import urlparse, urljoin

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10

# Exercitiul 47 - Antet personalizat pentru httpbin.org
DEFAULT_HEADERS = {"User-Agent": "WebLab-Diacencu-Gheorghe"}


# Exercitiul 44 - Functii proprii
def fetch(url: str, timeout=10):
    """Trimite o cerere GET si returneaza raspunsul."""

    # Folosim antetul personalizat numai pe httpbin.org.
    if urlparse(url).hostname == "httpbin.org":
        headers = DEFAULT_HEADERS
    else:
        headers = None

    time.sleep(1)
    return requests.get(url, timeout=timeout, headers=headers)


def get_status(url: str) -> int:
    """Returneaza codul HTTP."""
    return fetch(url).status_code


def get_title(html: str) -> str:
    """Extrage titlul din codul HTML."""

    start = html.lower().find("<title>")
    stop = html.lower().find("</title>")

    if start == -1 or stop == -1:
        return "Titlu negasit"

    start = start + len("<title>")
    return html[start:stop].strip()


def security_headers(url: str) -> dict:
    """Verifica prezenta a cinci antete de securitate."""

    raspuns = fetch(url)

    antete = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy"
    ]

    rezultate = {}

    for antet in antete:
        rezultate[antet] = antet in raspuns.headers

    return rezultate


def score_headers(rezultate: dict) -> str:
    """Calculeaza scorul antetelor de securitate."""

    prezente = sum(rezultate.values())
    total = len(rezultate)

    return str(prezente) + "/" + str(total)


def check_paths(base: str, paths: list) -> dict:
    """Verifica mai multe cai si returneaza codurile HTTP."""

    rezultate = {}

    for cale in paths:
        try:
            adresa = base.rstrip("/") + cale
            rezultate[cale] = get_status(adresa)

        except requests.RequestException:
            rezultate[cale] = None

    return rezultate


def fetch_robots(base: str):
    """Citeste continutul fisierului robots.txt."""

    try:
        adresa = base.rstrip("/") + "/robots.txt"
        raspuns = fetch(adresa)

        if raspuns.status_code == 200:
            return raspuns.text

    except requests.RequestException:
        pass

    return None


def disallowed_paths(robots_text) -> list:
    """Extrage caile Disallow din robots.txt."""

    cai = []

    if robots_text is None:
        return cai

    for linie in robots_text.splitlines():
        if linie.lower().startswith("disallow:"):
            cale = linie.split(":", 1)[1].strip()

            if cale:
                cai.append(cale)

    return cai


def resolve(hostname: str) -> str:
    """Obtine adresa IP a domeniului."""
    return socket.gethostbyname(hostname)


def cert_days_left(hostname: str) -> int:
    """Calculeaza zilele pana la expirarea certificatului TLS."""

    context = ssl.create_default_context()

    with socket.create_connection((hostname, 443), timeout=TIMEOUT) as conexiune:
        with context.wrap_socket(conexiune, server_hostname=hostname) as tls:
            certificat = tls.getpeercert()

    data_text = certificat["notAfter"]
    secunde = ssl.cert_time_to_seconds(data_text)

    expirare = datetime.fromtimestamp(secunde, timezone.utc)
    acum = datetime.now(timezone.utc)

    return (expirare - acum).days


def extract_links(html: str) -> list:
    """Extrage linkurile href si elimina duplicatele."""

    gasite = re.findall(r'href="([^"]+)"', html)
    rezultat = []

    for link in gasite:
        if link not in rezultat:
            rezultat.append(link)

    return rezultat


def split_links(links: list, domain: str):
    """Separa linkurile interne de cele externe."""

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


# Exercitiul 50 - Raportul final al site-ului
def site_report(url: str) -> dict:
    """Analizeaza site-ul si salveaza rezultatele in JSON."""

    hostname = urlparse(url).hostname

    if hostname != "cybercor.org":
        raise ValueError("Este permis doar domeniul cybercor.org")

    # Citim pagina principala.
    raspuns = fetch(url)
    titlu = get_title(raspuns.text)
    ip = resolve(hostname)

    # Verificam redirectionarea de la HTTP la HTTPS.
    redirect = fetch("http://" + hostname)

    redirectionari = []

    for pas in redirect.history:
        redirectionari.append(str(pas.status_code) + " -> " + pas.url)

    redirectionari.append(
        str(redirect.status_code) + " -> " + redirect.url
    )

    # Calculam scorul antetelor de securitate.
    antete = security_headers(url)
    scor = score_headers(antete)

    # Citim informatiile despre certificatul TLS.
    try:
        zile = cert_days_left(hostname)
    except (OSError, ssl.SSLError, KeyError, ValueError):
        zile = None

    # Numarăm linkurile.
    linkuri = extract_links(raspuns.text)
    interne, externe = split_links(linkuri, hostname)

    # Verificam robots.txt.
    robots = fetch_robots("https://" + hostname)
    cai = disallowed_paths(robots)

    # Adunam rezultatele intr-un dictionar.
    raport = {
        "url": raspuns.url,
        "status": raspuns.status_code,
        "titlu": titlu,
        "ip": ip,
        "redirectionari": redirectionari,
        "scor_securitate": scor,
        "zile_certificat": zile,
        "linkuri_interne": len(interne),
        "linkuri_externe": len(externe),
        "cai_disallow": cai
    }

    # Afisam rezultatele in consola.
    print("=== Raport site:", url, "===")
    print("Cod de stare:", raport["status"])
    print("URL final:", raport["url"])
    print("Titlu:", raport["titlu"])
    print("Adresa IP:", raport["ip"])
    print("Redirectionari:", raport["redirectionari"])
    print("Scor securitate:", raport["scor_securitate"])
    print("Certificat (zile):", raport["zile_certificat"])

    print("Linkuri:", raport["linkuri_interne"], "interne,",
          raport["linkuri_externe"], "externe")

    print("Cai interzise:", raport["cai_disallow"])

    # Salvam raportul in format JSON.
    with open("report.json", "w", encoding="utf-8") as fisier:
        json.dump(raport, fisier, indent=2, ensure_ascii=False)

    print("Salvat in report.json")

    return raport


# Exercitiul 46 - Autotest
if __name__ == "__main__":
    print("Autotest:", get_status(BASE_URL))
