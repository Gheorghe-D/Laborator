s = "Salut"
b = s.encode()

print(b)
print(b[0])
print(b.hex())
print(bytes.fromhex(b.hex()))

import base64
import re
from urllib.parse import unquote

def ghici_strat(s):
    if re.search(r"%[0-9A-Fa-f]{2}", s):
        return "url"

    if re.fullmatch(r"[0-9A-Fa-f]+", s) and len(s) % 2 == 0:
        return "hex"

    if re.fullmatch(r"[A-Za-z0-9+/]+={0,2}", s):
        return "base64"

    return "necunoscut" 
   
def desfa(s):
    strat = ghici_strat(s)
    
    if strat == "url":
       rezultat = unquote(s).encode()
       return strat, rezultat

    if strat == "base64":
       rezultat = base64.b64decode(s)
       return strat, rezultat
    
    if strat == "hex":
       rezultat = bytes.fromhex(s)
       return strat, rezultat

    return strat, s.encode()


def citibil(b):
    return all(32 <= c < 127 for c in b)

print(ghici_strat("%2Fetc"))
print(ghici_strat("48656c6c6f"))
print(ghici_strat("U2FsdXQ="))
print(desfa("U2FsdXQ="))
print(desfa("48656c6c6f"))
print(desfa("Salut%20lume"))
print(citibil(b"Salut"))
print(citibil(bytes([0,1])))

mesaj = b"FLAG{ok}"

val = base64.b64encode(
   base64.b64encode(mesaj.hex().encode())
).decode()

print("Mesaj codificat:", val)

for pas in range(8):
    strat = ghici_strat(val)

    if strat == "necunoscut":
       print("Mesaj final:", val)
       break

    strat, b = desfa(val)

    print("Pas:", pas + 1, "| Strat:", strat, "| Rezultat:",b)

    if not citibil (b):
       printf("Rezultat neimprimabil")
       break



    val = b.decode("ascii")


else:
    print("Limita de 8 incercari a fost atinsa")


print("\n  Test pe mesajul profesorului  ")

with open("probe/mesaj.txt", "r") as f:
    val = f.read().strip()

for pas in range(8):
    strat = ghici_strat(val)

    if strat == "necunoscut":
       print("Mesaj final:", val)
       break


    strat, b = desfa(val)
    print("Pas:", pas + 1, "| Strat:", strat)

    if not citibil(b):
       print("Rezultat neimprimibil")
       break


    val= b.decode("ascii")

else:
    print("Limita de 8 incercari a fost atinsa")



with open("probe/xor.bin", "rb") as f:
    date = f.read()

for k in range(256):
    clar = bytes(v ^ k for v in date)

    if citibil(clar) and b"FLAG{" in clar:
       print("Cheie:", k)
       print("Mesaj:", clar.decode())
 
import hashlib

with open("probe/hashuri.txt", "r") as f:
   tinta = f.readline().strip()

print("Hash tinta:", tinta)
print("Lungime:", len(tinta))

with open("probe/wordlist.txt", "r", encoding="latin1") as f:
    for cuv in f:
        cuv = cuv.strip()
  

        hash_calculat = hashlib.md5(
           cuv.encode()
        ).hexdigest()


        if hash_calculat == tinta:
           print("Parola gasita:", cuv)
           break
import argparse
import json

def main():
    p = argparse.ArgumentParser()
    p.add_argument("intrare")
    p.add_argument("--fisier", action="store_true")

    a = p.parse_args()

    print("Intrare:", a.intrare)
    print("Este fisier:", a.fisier)

    if a.fisier:
        with open(a.intrare, "r", encoding="utf-8") as f:
            valoare = f.read().strip()
    else:
        valoare = a.intrare

    strat, rezultat = desfa(valoare)

    print("strat detectat:", strat)
    print("rezultat decodat:", rezultat)

    fisa = {
        "strat": strat,
        "rezultat": rezultat.decode("utf-8")
    }

    with open("arsenal/forensics/fisa.json", "w", encoding="utf-8") as f:
        json.dump(fisa, f, indent=4, ensure_ascii=False)

    print("Fisa JSON a fost salvata.")


if __name__ == "__main__":
    main()

