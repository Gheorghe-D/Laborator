import os   
import json
import argparse


GTFO = {
      "find", "vim.basic", "vim", "nmap", "cp",
      "bash" , "less",  "awk" ,"python3", "perl"
    }


def citeste_linii(cale):
  
    rezultat = []
    with open(cale, encoding="utf-8") as f:
        for linie in f:
            linie = linie.strip()
            if linie and not linie.startswith("#"):
                rezultat.append(linie)
    
    return rezultat

def nume(cale):
    return cale.rsplit("/", 1)[1]

def suid_constatari(cale):
    cai = citeste_linii(cale)
    constatari = []
    cai_unice = sorted(set(cai))

    for c in cai_unice:
        executabil = nume(c)
        if executabil in GTFO:
            risc = "mare"
        else:
            risc = "normal"    

        constatare = {
            "cale": c,
            "nume": executabil,
            "risc": risc
        }

        constatari.append(constatare)

    return constatari
def sudo_constatari(cale):
    rezultat = []

    for linie in citeste_linii(cale):
        user, drept = linie.split(" : ",1)
        if "NOPASSWD" in drept:
            risc = "mare"
        else:
            risc = "normal"   

        constatare = {
            "user": user.strip(),
            "drept": drept.strip(),
            "risc": risc
        }   

        rezultat.append(constatare)      

    return rezultat
def cron_constatari(cale):
    rezultat = []

    for linie in citeste_linii(cale): 
        campuri = linie.split()
        user = campuri[5]
        comanda = " ".join(campuri[6:])

        constatare = {
            "user": user,
            "comanda": comanda
        }

        rezultat.append(constatare)

    return rezultat
def enumereaza(d):
    return{
        "suid": suid_constatari(os.path.join(d, "suid.txt")),
        "sudo": sudo_constatari(os.path.join(d, "sudo.txt")),
        "cron": cron_constatari(os.path.join(d, "crontab.txt"))
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("capturi")
    p.add_argument("--json", action="store_true")

    a = p.parse_args()
    raport = enumereaza(a.capturi)

    if a.json:
        print(json.dumps(raport, indent=2, ensure_ascii=False))
        return


def main():
    p = argparse.ArgumentParser()
    p.add_argument("capturi")
    p.add_argument("--json", action="store_true")

    a = p.parse_args()
    raport = enumereaza(a.capturi)

    if a.json:
        print(json.dumps(raport, indent=2, ensure_ascii=False))
        return

    for categorie, lista in raport.items():
        mari = [c for c in lista if c.get("risc") == "mare"]
        print(f"{categorie}: {len(lista)} gasite, {len(mari)} cu risc mare")

    utilizatori_sudo = {c["user"] for c in raport["sudo"]}
    utilizatori_cron = {c["user"] for c in raport["cron"]}

    utilizatori = utilizatori_sudo | utilizatori_cron

    print("utilizatori implicati:", ", ".join(sorted(utilizatori)))

    with open("arsenal/privesc/enum.json", "w", encoding="utf-8") as f:
        json.dump(raport, f, indent=2, ensure_ascii=False)

    print("Raport salvat in enum.json")

if __name__ == "__main__":
    main()