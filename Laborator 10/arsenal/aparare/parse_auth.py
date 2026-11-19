import re
from collections import Counter


TIPAR = re.compile(
    r"Failed password for (?:invalid user )?(\S+) from (\S+) port"

)

def esec(linie):
    m = TIPAR.search(linie)

    if m is None:
        return None


    return (m.group(1), m.group(2))

def citeste_esecuri(cale):
    esecuri = []

    try:
        f = open(cale, encoding="utf-8")
    except FileNotFoundError:
        print("nu gasesc", cale)
        return esecuri  

    with f:
        for linie in f:
            r = esec(linie)

            if r is not None:
                esecuri.append({
                    "user": r[0],
                    "ip": r[1]
                })
    return esecuri                 

esecuri = citeste_esecuri(
    "Laborator 10/arsenal/aparare/start/auth.log"
)

print("esecuri:", len(esecuri))

def pe_ip(esecuri):
    return Counter(e["ip"] for e in esecuri)



print(esec("Failed password for root from 203.0.113.9 port  51230 ssh2"))
print(esec("linie stricata fara structura"))
esecuri = citeste_esecuri(
    "Laborator 10/arsenal/aparare/start/auth.log"
)

print("esecuri:", len(esecuri))
counts = pe_ip(esecuri)

for ip, n in counts.most_common():
    print(f"{ip}:{n}")

   