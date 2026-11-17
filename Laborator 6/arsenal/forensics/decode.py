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

print(ghici_strat("%2Fetc"))
print(ghici_strat("48656c6c6f"))
print(ghici_strat("U2FsdXQ="))
print(desfa("U2FsdXQ="))
print(desfa("48656c6c6f"))
print(desfa("Salut%20lume"))
