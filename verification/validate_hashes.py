import hashlib

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def main():
    with open("verification/proofs/manifest.sha256") as f:
        lines = f.read().strip().splitlines()

    for line in lines:
        expected, path = line.split()
        actual = sha256(path)
        assert actual == expected, f"Hash mismatch for {path}"

    print("All certificate hashes verified.")

if __name__ == "__main__":
    main()

