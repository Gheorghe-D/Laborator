def tip_real(cale):
    with open(cale, "rb") as f:
        cap = f.read(8)


    if cap.startswith(b"%PDF"):
        return "pdf"
    elif cap.startswith(b"\x89PNG"):
        return "PNG"
    elif cap.startswith(b"\xff\xd8"):
        return "JPEG"
    elif cap.startswith(b"PK\x03\x04"):
        return "ZIP/DOCX"

    return "necunoscut"


print(tip_real("probe/foto.jpg"))
print(tip_real("probe/ascuns.png"))
