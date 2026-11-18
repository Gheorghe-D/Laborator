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



import re

with open("probe/ascuns.png", "rb") as f:
    val = f.read()


for mesaj in re.findall(rb"[ -~]{4,}", val):
    print(mesaj.decode())


from PIL import Image
from PIL.ExifTags import TAGS

exif = Image.open("probe/foto.jpg")._getexif() or {}

for id, valoare in exif.items():
    print(TAGS.get(id, id), "=", valoare)

gps = exif.get(34853, {})

def grade_zecimale(coordonate):
    grade, minute, secunde = coordonate
    return float(grade) +float(minute) / 60 + float(secunde) / 3600

if gps:
    lat = grade_zecimale(gps[2])
    lon = grade_zecimale(gps[4])

    if gps[1] == "S":
        lat = -lat
    if gps[3] == "W":
        lon = -lon

    print("Latitudine:", lat)
    print("Longitudine:", lon)

else:
    print("Nu exista date GPS.")

with open("probe/ascuns.png", "rb") as f:
    date = f.read()

pozitie = date.find(b"PK\x03\x04")

if pozitie != -1:
    with open("gasit.zip", "wb") as f:
        f.write(date[pozitie:])

    print("Arhiva extrasa de la octetul", pozitie)

else:
    print("Nu s-a gasit arhiva ZIP. ")

from PIL import Image

img = Image.open("probe/foto.jpg").convert("RGB")
pixeli = list(img.getdata())

mesaj = b"FLAG{ascuns_in_pixeli}\x00"
biti = "".join(f"{octet:08b}" for octet in mesaj)

canale = [canal for pixel in pixeli for canal in pixel]

if len(biti) > len(canale):
    raise ValueError("Mesajul este prea lung .")

for i,bit in enumerate(biti):
    canale[i] = (canale[i] & ~1) | int(bit)

pixeli_noi = [
    tuple(canale[i:i+3])
    for i in range(0, len(canale), 3)

]    

img.putdata(pixeli_noi)
img.save("stego.png")

print("Mesaj ascins iin stego.png")
