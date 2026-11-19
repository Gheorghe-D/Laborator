import argparse
import json

from parse_auth import citeste_esecuri, pe_ip

def suspecti(counts, prag=10):
    if prag < 1:
        raise ValueError(f"Pragul invalid: {prag} (cel putin 1)")


    rezultat = []

    for ip,n in counts.items():
        if n >= prag:
            rezultat.append((ip,n))


    rezultat.sort(key=lambda x: x[1], reverse=True)

    return rezultat


def main():
    p = argparse.ArgumentParser(
        description="Detector de atacuri brute force SSH"

    )

    p.add_argument("log")
    p.add_argument("--prag",type=int, default=10)
    p.add_argument("--json",action="store_true")

    a = p.parse_args()

    esecuri = citeste_esecuri(a.log)
    counts = pe_ip(esecuri)
    sus = suspecti(counts, a.prag)

    if a.json:
        raport = {
            "esecuri": len(esecuri),
            "pe_ip": dict(counts),
            "suspecti": [
                {"ip": ip, "incercari": n}
                for ip, n in sus
            ]
        }

        print(json.dumps(raport, indent=2))
    else:
        print(f"Esecuri de autentificare: {len(esecuri)}")

        for ip, n in counts.most_common():
            print(f" {ip}: {n}")

        print(f"Suspecti (prag {a.prag}):")

        for ip, n in sus:
            print(f" {ip} ({n} incercari) BRUTE FORCE")

if __name__ == "__main__":
    main()         