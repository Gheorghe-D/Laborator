import json
from dataclasses import dataclass, asdict
import json

CAI_SUSPECTE = ("\\Temp\\", "\\Roaming\\")
SUSPECTE_ID = {4625, 1102, 7045}

@dataclass
class Proces:
    pid: int
    nume: str
    user: str
    cale: str

    def e_suspect(self):
        return any(cale in self.cale for cale in CAI_SUSPECTE)

@dataclass
class Eveniment:
    id: int
    nivel: str
    sursa: str
    cont: str
    mesaj: str    

    def e_suspect(self):
        return self.id in SUSPECTE_ID or self.nivel == "critical"

def procese_din_json(cale):
    with open(cale, encoding="utf-8") as f:
        return [Proces(**d) for d in json.load(f)]

def evenimente_din_json(cale):
    with open(cale, encoding="utf-8") as f:
        return [Eveniment(**d) for d in json.load(f)]   


@dataclass
class Inventar:
    procese: list

    @classmethod
    def din_json(cls, cale):
        with open(cale, encoding="utf-8") as f:
            return cls([Proces(**d) for d in json.load(f)])

    def __len__(self):
        return len(self.procese)

    def suspecte(self):
        return [p for p in self.procese if p.e_suspect()]

    def pe_user(self):
        rezultat = {}

        for p in self.procese:
            rezultat.setdefault(p.user, []).append(p.nume)

        return rezultat



if __name__ == "__main__":
    p1 = Proces(
        3120,
        "update.exe",
        "ana",
        r"C:\Users\ana\AppData\Local\Temp\update.exe"

    )
    p2 = Proces(
        612,
        "svchost.exe",
        "SYSTEM",
        r"C:\Windows\System32\svchost.exe"
    )
    e1 = Eveniment(
        4625,

        "warning",
        "Security",
        "administrator",
        "An account failed to log on." 

    )

    e2 = Eveniment(
        4624,
        "info",
        "Security",
        "ana",
        "An account was successfully logged on."
    )

 
    from pathlib import Path

    folder_start = Path(__file__).resolve().parent / "start"

    procese = procese_din_json(folder_start / "procese.json")
    evenimente = evenimente_din_json(folder_start / "evenimente.json")


    print("Procese:", len(procese))
    print("suspecte:" ,sum(1 for p in procese if p.e_suspect()))

    print("Evenimente:", len(evenimente))
    print("suspecte:", sum(1 for e in evenimente if e.e_suspect()))


    print("Eveniment:", e1.id)
    print("Suspect:", e1.e_suspect())

    print("Eveniment:", e2.id)
    print("Suspect:", e2.e_suspect())


    print("Proces:" , p1.nume)
    print("Suspect:", p1.e_suspect())

    print("Proces:", p2.nume)
    print("Suspect:", p2.e_suspect())



    
    inv = Inventar.din_json(folder_start / "procese.json")

    print("B1 - Inventar")
    print("procese:", len(inv))

    print("B2 - Procese suspecte")

    for p in inv.suspecte():
        print(f"[{p.pid}] {p.nume} {p.cale}")

    print("B2 - Procese pe utilizatori")
    print(inv.pe_user())

