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

    print("Eveniment:", e1.id)
    print("Suspect:", e1.e_suspect())

    print("Eveniment:", e2.id)
    print("Suspect:", e2.e_suspect())


    print("Proces:" , p1.nume)
    print("Suspect:", p1.e_suspect())

    print("Proces:", p2.nume)
    print("Suspect:", p2.e_suspect())

    
