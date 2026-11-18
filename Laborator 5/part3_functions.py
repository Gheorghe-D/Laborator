
import requests
import time

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10


def fetch(url: str, timeout: int = 10):
    """Trimite o cerere GET si returneaza raspunsul."""
    time.sleep(1)
    return requests.get(url, timeout=timeout)


def get_status(url: str) -> int:
    """Returneaza codul de stare HTTP."""
    raspuns = fetch(url)
    return raspuns.status_code


def get_title(html: str) -> str:
    """Extrage titlul unei pagini HTML."""
    start = html.lower().find("<title>")
    stop = html.lower().find("</title>")

    if start == -1 or stop == -1:
        return "Titlu negasit"

    start = start + len("<title>")
    return html[start:stop].strip()


def page_exists(url: str) -> bool:
    """Verifica daca o pagina poate fi accesata."""
    try:
        raspuns = fetch(url)
        return raspuns.ok
    except requests.RequestException:
        return False


def check_paths(base: str, paths: list) -> dict:
    """Verifica o lista de cai si returneaza codurile HTTP."""
    rezultate = {}

    for cale in paths:
        try:
            adresa = base.rstrip("/") + cale
            rezultate[cale] = get_status(adresa)
        except requests.RequestException:
            rezultate[cale] = None

    return rezultate


def get_header(url: str, name: str, default: str = "lipseste") -> str:
    """Returneaza valoarea unui antet HTTP."""
    raspuns = fetch(url)
    return raspuns.headers.get(name, default)


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


def score_headers(results: dict) -> str:
    """Calculeaza cate antete de securitate sunt prezente."""
    prezente = sum(results.values())
    total = len(results)

    return str(prezente) + "/" + str(total)


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
    """Extrage caile marcate cu Disallow."""
    cai = []

    if robots_text is None:
        return cai

    for linie in robots_text.splitlines():
        if linie.lower().startswith("disallow:"):
            cale = linie.split(":", 1)[1].strip()

            if cale:
                cai.append(cale)

    return cai


def response_times(*urls: str) -> dict:
    """Masoara timpul de raspuns pentru mai multe adrese."""
    rezultate = {}

    for url in urls:
        time.sleep(1)

        try:
            start = time.perf_counter()
            requests.get(url, timeout=TIMEOUT)
            durata = time.perf_counter() - start

            rezultate[url] = round(durata, 3)

        except requests.RequestException:
            rezultate[url] = None

    return rezultate


def log(message: str, **details) -> None:
    """Afiseaza un mesaj si detaliile primite."""
    text = message

    for nume, valoare in details.items():
        text = text + " | " + nume + "=" + str(valoare)

    print(text)


if __name__ == "__main__":
    raspuns = fetch(BASE_URL)
    print("Ex. 21 - Status:", raspuns.status_code)

    for cale in ["/", "/robots.txt", "/sitemap.xml"]:
        print("Ex. 22:", cale, get_status(BASE_URL + cale))

    print("Ex. 23 - Timeout implicit:", fetch(BASE_URL).status_code)
    print("Ex. 23 - Timeout 3:", fetch(BASE_URL, timeout=3).status_code)

    print("Ex. 24 - Titlu:", get_title(raspuns.text))

    print("Ex. 25 - Documentatia functiei:")
    help(get_title)

    try:
        get_status(123)
    except (TypeError, ValueError, requests.RequestException) as eroare:
        print("Ex. 26 - Eroare:", type(eroare).__name__)

    print("Ex. 27 - Pagina exista:", page_exists(BASE_URL))
    print("Domeniu invalid:",
          page_exists("https://this-domain-does-not-exist.invalid"))

    cai = ["/", "/robots.txt", "/sitemap.xml"]
    print("Ex. 28:", check_paths(BASE_URL, cai))

    print("Ex. 29 - Server:", get_header(BASE_URL, name="Server"))

    rezultate = security_headers(BASE_URL)
    print("Ex. 30:", rezultate)

    print("Ex. 31 - Scor:", score_headers(rezultate))
    print("Apel combinat:", score_headers(security_headers(BASE_URL)))

    robots = fetch_robots(BASE_URL)
    print("Ex. 32:", disallowed_paths(robots))

    print("Ex. 33:", response_times(BASE_URL, BASE_URL + "/robots.txt"))

    log("Ex. 34 - Verificat", url=BASE_URL, status=raspuns.status_code)

    print("\nAm terminat exercitiile 21-34.")

