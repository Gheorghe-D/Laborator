
# Laborator: functii, metode si importuri pe web
# Student: Diacencu Gheorghe
# Grupa: SI-262
# Anul: I

import os
import json
import tempfile
import unittest
from unittest.mock import patch

import part3_functions as p3
import part4_modules as p4
import webtools


# Raspuns fals, folosit in locul unui raspuns de pe internet
class FakeResponse:

    def __init__(self, url, html, status=200):
        self.url = url
        self.text = html
        self.status_code = status

        self.headers = {
            "Strict-Transport-Security": "max-age=31536000",
            "Content-Security-Policy": "default-src 'self'"
        }

        self.history = []


# Testele pentru functiile laboratorului
class TestLocal(unittest.TestCase):

    # Testul 1 - Extragerea titlului
    def test_get_title(self):
        html = "<title> Salut </title>"

        self.assertEqual(p3.get_title(html), "Salut")

        self.assertEqual(
            webtools.get_title("<html>fara titlu</html>"),
            "Titlu negasit"
        )

    # Testul 2 - Scorul antetelor
    def test_scoring(self):
        rezultate = {"a": True, "b": False}

        self.assertEqual(p3.score_headers(rezultate), "1/2")

        self.assertEqual(
            webtools.score_headers({"a": True, "b": True}),
            "2/2"
        )

    # Testul 3 - Caile din robots.txt
    def test_robots(self):
        text = "User-agent: *\nDisallow: /admin\nDisallow: /private"

        self.assertEqual(
            p3.disallowed_paths(text),
            ["/admin", "/private"]
        )

        self.assertEqual(webtools.disallowed_paths(None), [])

    # Testul 4 - Linkuri interne si externe
    def test_links(self):
        html = (
            '<a href="/a"></a>'
            '<a href="https://exemplu.org"></a>'
            '<a href="/a"></a>'
        )

        links = p4.extract_links(html)

        self.assertEqual(
            links,
            ["/a", "https://exemplu.org"]
        )

        interne, externe = p4.split_links(links, "cybercor.org")

        self.assertEqual(len(interne), 1)
        self.assertEqual(len(externe), 1)

    # Testul 5 - Extragerea imaginilor
    def test_images(self):
        html = (
            '<img src="/logo.png">'
            '<IMG SRC="poza.jpg">'
            '<img alt="fara">'
            '<a href="/x">link</a>'
        )

        parser = p4.ImageFinder()
        parser.feed(html)

        self.assertEqual(
            parser.images,
            ["/logo.png", "poza.jpg"]
        )

    # Testul 6 - Generarea raportului JSON
    def test_report_without_internet(self):
        html = (
            '<title>Pagina test</title>'
            '<a href="/contact"></a>'
            '<a href="https://example.org"></a>'
        )

        # Inlocuim cererile reale cu raspunsuri de test.
        def fake_fetch(url, timeout=10):
            if url.endswith("/robots.txt"):
                return FakeResponse(
                    url,
                    "User-agent: *\nDisallow: /admin"
                )

            return FakeResponse("https://cybercor.org", html)

        # Folosim un folder temporar pentru raport.
        initial_dir = os.getcwd()

        with tempfile.TemporaryDirectory() as folder:
            try:
                os.chdir(folder)

                with patch.object(webtools, "fetch", side_effect=fake_fetch), \
                     patch.object(webtools, "resolve", return_value="192.0.2.1"), \
                     patch.object(webtools, "cert_days_left", return_value=24):

                    rezultat = webtools.site_report(
                        "https://cybercor.org"
                    )

                with open("report.json", encoding="utf-8") as fisier:
                    salvat = json.load(fisier)

                self.assertEqual(rezultat["titlu"], "Pagina test")
                self.assertEqual(rezultat["linkuri_interne"], 1)
                self.assertEqual(rezultat["linkuri_externe"], 1)
                self.assertEqual(salvat["cai_disallow"], ["/admin"])

            finally:
                os.chdir(initial_dir)


# Pornim testele doar cand executam acest fisier.
if __name__ == "__main__":
    unittest.main()

