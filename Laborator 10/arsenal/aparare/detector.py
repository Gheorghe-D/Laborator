from collections import Counter


def suspecti(counts, prag=10):
    if prag < 1:
        raise ValueError(f"Pragul invalid: {prag} (cel putin 1)")


    rezultat = []

    for ip,n in counts.items():
        if n >= prag:
            rezultat.append((ip,n))


    rezultat.sort(key=lambda x: x[1], reverse=True)

    return rezultat


c = Counter({"203.0.113.9": 13, "198.51.100.7": 2})

print(suspecti(c))
print(suspecti(c, prag=2))

