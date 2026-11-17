
# Laborator: functii, metode si importuri pe web
# Student: Diacencu Gheorghe
# Grupa: SI-262
# Anul: I

import argparse
import csv
import requests
from datetime import datetime

import webtools
from webtools import get_title, security_headers
from webtools import DEFAULT_HEADERS

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10


# Exercitiul 44 - Folosirea modulului webtools
# Functiile sunt scrise in webtools.py si apelate aici.


# Exercitiul 45 - Importarea functiilor
# Pot folosi webtools.get_title() sau direct get_title().
# Daca definesc aici alta functie cu acelasi nume,
# numele importat este inlocuit in acest fisier.


# Exercitiul 47 - Constanta DEFAULT_HEADERS
# O importam din webtools.py si o afisam mai jos.


# Exercitiul 49 - Salvarea rezultatelor in CSV
def save_csv(url: str) -> None:
    """Salveaza codurile HTTP intr-un fisier CSV."""

    cai = ["/", "/robots.txt", "/sitemap.xml"]
    rezultate = webtools.check_paths(url, cai)

    with open("report.csv", "w", encoding="utf-8", newline="") as fisier:
        writer = csv.writer(fisier)

        writer.writerow(["path", "status", "checked_at"])

        for cale, status in rezultate.items():
            data = datetime.now().isoformat()
            writer.writerow([cale, status, data])

    print("Ex. 49 - Fisierul report.csv a fost creat.")


# Exercitiul 48 - Citirea URL-ului din terminal
def main() -> None:
    """Porneste programul si genereaza rapoartele."""

    parser = argparse.ArgumentParser(
        description="Raport simplu despre un site web"
    )

    parser.add_argument(
        "url",
        help="Adresa site-ului, de exemplu https://cybercor.org"
    )

    args = parser.parse_args()

    # Folosim doar site-ul permis de profesor.
    if args.url != BASE_URL:
        print("Pentru acest laborator folosim doar:", BASE_URL)
        return

    # Exercitiul 44 - Apelarea functiilor din webtools
    raspuns = webtools.fetch(args.url)

    print("Ex. 44 - Titlu:",
          webtools.get_title(raspuns.text))

    # Exercitiul 45 - Import direct
    print("Ex. 45 - Titlu prin import direct:",
          get_title(raspuns.text))

    print("Ex. 45 - Antete:",
          security_headers(args.url))

    # Exercitiul 47 - Afisarea constantei
    print("Ex. 47 - Antete implicite:", DEFAULT_HEADERS)

    # Verificam User-Agent numai pe httpbin.org.
    raspuns_test = webtools.fetch(ECHO_URL + "/headers")

    print("Ex. 47 - User-Agent testat:",
          raspuns_test.json().get("headers", {}).get("User-Agent"))

    # Exercitiul 49 - Generarea CSV
    save_csv(args.url)

    # Exercitiul 50 - Raportul final JSON
    webtools.site_report(args.url)


# Exercitiul 46 - Punctul de pornire al programului
if __name__ == "__main__":
    try:
        main()

    except (requests.RequestException, OSError, ValueError) as eroare:
        print("A aparut o eroare:", eroare)
        print("Verifica internetul si incearca din nou.")

