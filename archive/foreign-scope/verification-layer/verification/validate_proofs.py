import json
import glob

def main():
    files = glob.glob("verification/proofs/*.json")
    assert files, "No proof certificates found"

    for f in files:
        with open(f) as fh:
            data = json.load(fh)

        required = ["id", "statement", "assumptions", "status"]
        for k in required:
            assert k in data, f"{f} missing field {k}"

        assert data["status"].startswith("verified"), f"{f} not verified"

    print("All proof certificates validated.")

if __name__ == "__main__":
    main()

