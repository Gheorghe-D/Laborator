MAGIC = {
    b"\x89PNG": "PNG",
    b"%PDF": "PDF",
    b"PK\x03\x04": "ZIP"
}

def tip(head):
    for semnatura, nume in MAGIC.items():
        if head.startswith(semnatura):
            return nume
    return "necunoscut"

print(tip(b"\x89PNG\r\n"), tip(b"%PDF-1.4"), tip(b"text"))
