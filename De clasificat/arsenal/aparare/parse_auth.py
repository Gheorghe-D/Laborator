import re

TIPAR = re.compile(r"Failed password for (?:invalid user )?(\S+) from (\S+) port")

def esec(linie):
    m = TIPAR.search(linie)
    if m is None:
        return None
    return (m.group(1), m.group(2))

if __name__ == "__main__":
    print(esec("... Failed password for root from 203.0.113.9 port 51230 ssh2"))
    print(esec("<linie stricata fara structura>"))
