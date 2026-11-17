from checker import build_url, is_https, show_response, check_site, scan_sites, check_headers, retry_check

print("=== Partea 1: build_url și is_https ===")
print("Caz normal (fără /):", build_url("example.com", "login"))
print("Caz limită (cu /):", build_url("example.com", "/login"))
print("Verificare HTTPS (True):", is_https("https://example.com"))
print("Verificare HTTP (False):", is_https("http://example.com"))
print()

print("=== Partea 2: show_response ===")
print("Test pentru https://example.com:")
show_response("https://example.com")
print()

print("=== Partea 3: check_site ===")
print("Site funcțional:", check_site("https://example.com"))
print("Site inexistent (limită):", check_site("http://this-site-does-not-exist.invalid"))
print()

print("=== Partea 4: scan_sites ===")
scan_sites()
print()

print("=== Partea 5: check_headers ===")
print("Toate antetele lipsă:", check_headers("https://example.com"))
print("Anteturi prezente (mix majuscule):", check_headers("https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff"))
print()

print("=== Partea 6: retry_check ===")
print("Status 200 (1 încercare):", retry_check("https://httpbin.org/status/200"))
print("Status 404 (1 încercare):", retry_check("https://httpbin.org/status/404"))
print("Status 500 (3 încercări):", retry_check("https://httpbin.org/status/500", attempts=3))
print("Site inexistent (3 încercări + eroare):", retry_check("http://this-site-does-not-exist.invalid"))
print()


