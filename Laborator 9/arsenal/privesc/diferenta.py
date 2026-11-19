from  pathlib import Path
from enum_privesc import citeste_linii, nume, GTFO

START = Path(__file__).parent / "start"

def cai(fisier):
    return set(citeste_linii(START / fisier))

baza = cai("baza_suid.txt")
acum = cai("suid.txt")

print("baza:", len(baza), "acum:", len(acum))

noi = acum - baza

print (len(noi), "SUID noi fata de sistemul curat")

for c in sorted(noi):
    print(" ", c)

risc = {
    nume(c): ("mare" if nume (c) in GTFO else "normal")
    for c in noi



}

periculoase = [
    c for c in sorted(noi)
    if nume(c) in GTFO
]

print("Riscuri:", risc)
print("Periculoase NOI :", periculoase)
