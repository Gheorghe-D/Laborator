GTFO = {
      "find", "vim.basic", "vim", "nmap", "cp",
      "bash" , "less",  "awk" ,"python3", "perl"
    }
def nume(cale):

    return cale.rsplit("/", 1)[1]

def citeste_linii(cale):
  
    rezultat = []
    with open(cale, encoding="utf-8") as f:
        for linie in f:
            linie = linie.strip()
            if linie and not linie.startswith("#"):
                rezultat.append(linie)
    return rezultat
def suid_constatari(cale):
    cai = citeste_linii(cale)



cai = citeste_linii("arsenal/privesc/start/suid.txt") 
print("linii SUID:", len(cai))         
print("Primul executabil:", nume(cai[0]))  
nume_unice = {nume(c) for c in cai}
print("SUID dinstincte:", len(nume_unice))
print("find este periculos?", "find" in GTFO)
print("passwd este periculos?", "passwd" in GTFO)  