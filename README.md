# Tehnici de programare — UTM, FCIM, SI-262

Depozit cu lucrările de laborator și evaluările practice pentru disciplina **Tehnici de programare** (Universitatea Tehnică a Moldovei, FCIM, grupa SI-262).

## Structura depozitului

```text
.
├── Laborator 2/
│   └── Raport_Laborator_PwnCollege.docx
├── Laborator 3/
│   └── Raport_laborator_Linux_nr_3.docx
├── Laborator 4/
│   └── Raport_Codédex_Python_Diacencu_Gheorghe.docx
├── Laborator 5/
│   ├── Raport_Laborator_Python_Diacencu_Gheorghe.docx
│   ├── main.py
│   ├── webtools.py
│   ├── part1_imports.py
│   ├── part2_methods.py
│   ├── part3_functions.py
│   ├── part4_modules.py
│   ├── report.csv
│   ├── report.json
│   └── test_local.py
├── Laborator 8/
│   ├── Partea A/
│   │   └── Raport Laborator 8 Partea A.docx
│   └── Partea B/
│       ├── Raport Laborator 8 Partea  B.docx
│       ├── inventar.py
│       ├── raport_inventar.json
│       └── tinte.json
├── Laborator 9/
│   └── arsenal/
│       └── privesc/
│           ├── enum.py
│           ├── enum.json
│           └── start/
├── Evaluari/
│   ├── Examen/
│   └── Examen 1/
├── De clasificat/
│   └── arsenal/
│       └── aparare/
└── README.md
```

## Lucrări de laborator

| Laborator | Tematică | Raport / Conținut |
| --- | --- | --- |
| [Laborator 2/](Laborator%202/) | PwnCollege — Familiarizarea cu mediul de lucru `pwn.college` | [Raport_Laborator_PwnCollege.docx](Laborator%202/Raport_Laborator_PwnCollege.docx) |
| [Laborator 3/](Laborator%203/) | PwnCollege / Linux — Familiarizarea cu comenzile Linux și mediul Linux Luminary | [Raport_laborator_Linux_nr_3.docx](Laborator%203/Raport_laborator_Linux_nr_3.docx) |
| [Laborator 4/](Laborator%204/) | Codédex — Studierea limbajului Python pe platforma Codédex | [Raport_Codédex_Python_Diacencu_Gheorghe.docx](Laborator%204/Raport_Cod%C3%A9dex_Python_Diacencu_Gheorghe.docx) |
| [Laborator 5/](Laborator%205/) | *Laborator Python: funcții, metode și importuri pe web* (`webtools.py`, `main.py`, teste locale) | [Raport_Laborator_Python_Diacencu_Gheorghe.docx](Laborator%205/Raport_Laborator_Python_Diacencu_Gheorghe.docx) |
| [Laborator 8/](Laborator%208/) | Git și depanare:<br>• [Partea A](Laborator%208/Partea%20A/) — GitHub, pas cu pas<br>• [Partea B](Laborator%208/Partea%20B/) — Unealta stricată, reparată cu Git (`inventar.py`) | • [Raport Laborator 8 Partea A.docx](Laborator%208/Partea%20A/Raport%20Laborator%208%20Partea%20A.docx)<br>• [Raport Laborator 8 Partea  B.docx](Laborator%208/Partea%20B/Raport%20Laborator%208%20Partea%20%20B.docx) |
| [Laborator 9/](Laborator%209/) | Colecții / analiză privilegii — analiză offline SUID, `sudo` și `crontab` | [arsenal/privesc/](Laborator%209/arsenal/privesc/) |

## Rularea proiectelor Python

### Laborator 5 — Python Web

Testele unitare offline (`test_local.py`) folosesc răspunsuri simulate și nu accesează rețeaua:

```bash
cd "Laborator 5"
python -m unittest test_local.py
```

Scripturile `main.py`, `part1_imports.py`, `part2_methods.py`, `part3_functions.py` și `part4_modules.py` efectuează cereri HTTP reale către țintele permise în laborator (de exemplu `https://cybercor.org`, `https://httpbin.org`):

```bash
cd "Laborator 5"
python main.py https://cybercor.org
```

### Laborator 8 (Partea B) — Depanare (`inventar.py`)

Procesează offline fișierul JSON de ținte și generează `raport_inventar.json`:

```bash
cd "Laborator 8/Partea B"
python inventar.py tinte.json --prag 1000
```

### Laborator 9 — Analiză privilegii (`arsenal/privesc`)

Analizează offline capturile din `arsenal/privesc/start` (`suid.txt`, `sudo.txt`, `crontab.txt`):

```bash
cd "Laborator 9"
python -m arsenal.privesc.enum arsenal/privesc/start
```

Pentru afișare directă în format JSON (fără scriere în `enum.json`):

```bash
cd "Laborator 9"
python -m arsenal.privesc.enum arsenal/privesc/start --json
```

Alternativ, din rădăcina depozitului (cu `python -P` / `py -P` pentru izolarea căii de import):

```bash
python -P "Laborator 9/arsenal/privesc/enum.py" "Laborator 9/arsenal/privesc/start"
```

## Evaluări

Folderul [Evaluari/](Evaluari/) conține materialele de evaluare:

- [Evaluari/Examen/](Evaluari/Examen/) (`checker.py`, `main.py`, `1`)
- [Evaluari/Examen 1/](Evaluari/Examen%201/) (`checker.py`, `main.py`, `readme.md`)

Scripturile din `Evaluari/` implementează verificări ale antetelor HTTP / de securitate (`Strict-Transport-Security`, `Content-Security-Policy`, `X-Frame-Options`, `X-Content-Type-Options`) prin cereri directe către URL-uri externe, nu dispun de teste offline automate și nu se execută împotriva țintelor externe.

## De clasificat

Folderul [De clasificat/](De%20clasificat/) conține [arsenal/aparare/](De%20clasificat/arsenal/aparare/) (`parse_auth.py` și `start/auth.log`), plasat aici deoarece lipsesc numărul laboratorului și raportul aferent.
