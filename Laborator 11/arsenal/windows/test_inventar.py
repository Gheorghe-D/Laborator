

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inventar import Proces


def test_proces_din_temp_e_suspect():
    p = Proces(
        1,
        "x.exe",
        "ana",
        r"C:\Users\ana\AppData\Local\Temp\x.exe"
    )
    assert p.e_suspect() is True


def test_proces_din_windows_nu_e_suspect():
    p = Proces(
        2,
        "svchost.exe",
        "SYSTEM",
        r"C:\Windows\System32\svchost.exe"
    )
    assert p.e_suspect() is False
