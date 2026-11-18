
from httptools import PATHS, report


def main():
    results = []

    for path in PATHS:
        result = report(path)
        result["path"] = path
        results.append(result)

    successful = [r for r in results if r["status"] == 200]
    successful.sort(key=lambda r: r["seconds"], reverse=True)

    for r in successful:
        print(r["path"], "->", r["status"], r["seconds"], "secunde")

    print("Reusite:", len(successful))
    print("Esuate:", len(results) - len(successful))


if __name__ == "__main__":
    main()
