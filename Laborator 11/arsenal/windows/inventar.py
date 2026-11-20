import argparse
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




def main():
    parser = argparse.ArgumentParser(
        description="Inventar procese Windows si evenimente de securitate"
    )

    parser.add_argument("capturi", help="Folderul cu fisierele JSON")
    parser.add_argument("--json", action="store_true")

    args = parser.parse_args()

    
    inv = Inventar.din_json(args.capturi + "/procese.json")
    evenimente = evenimente_din_json(
        args.capturi + "/evenimente.json"
    )

    
    procese_suspecte = inv.suspecte()
    alarma = [e for e in evenimente if e.e_suspect()]

    if args.json:
        raport = {
            "procese_suspecte": [asdict(p) for p in procese_suspecte],
            "evenimente_alarma": [asdict(e) for e in alarma]
        }

        print(json.dumps(raport, indent=2, ensure_ascii=False))

    else:
        print(f"Procese: {len(inv)} | suspecte: {len(procese_suspecte)}")

        for p in procese_suspecte:
            print(f" [{p.pid}] {p.nume} ({p.user}) {p.cale}")

        print(f"Evenimente: {len(evenimente)} | alarma: {len(alarma)}")

        for e in alarma:
            print(f" {e.id} [{e.nivel}] {e.cont}: {e.mesaj}")
    



if __name__ == "__main__":
    main()