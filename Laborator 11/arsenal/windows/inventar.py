from dataclasses import dataclass, asdict
import json

CAI_SUSPECTE = ("\\Temp\\", "\\Roaming\\")

@dataclass
class Proces:
    pid: int
    nume: str
    user: str
    cale: str

    def e_suspect(self):
        return any(cale in self.cale for cale in CAI_SUSPECTE)


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


    print("Proces:" , p1.nume)
    print("Suspect:", p1.e_suspect())

    print("Proces:", p2.nume)
    print("Susppect:", p2.e_suspect())

    
