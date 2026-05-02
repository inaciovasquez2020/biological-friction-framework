#!/usr/bin/env python3
from pathlib import Path
import re
import json

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/status/BFF_SORRY_QUARANTINE_2026_05_02.md"
ART = ROOT / "artifacts/bff_sorry_inventory_2026_05_02.json"

def lean_files():
    return [
        p for p in ROOT.rglob("*.lean")
        if ".lake" not in p.parts and ".git" not in p.parts
    ]

def count_token(token):
    rx = re.compile(rf"\b{re.escape(token)}\b")
    total = 0
    hits = []
    for path in lean_files():
        for i, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), start=1):
            if rx.search(line):
                total += 1
                hits.append((str(path.relative_to(ROOT)), i, line.strip()))
    return total, hits

def require(path, tokens):
    if not path.exists():
        raise SystemExit(f"missing {path.relative_to(ROOT)}")
    text = path.read_text(encoding="utf-8", errors="ignore")
    missing = [t for t in tokens if t not in text]
    if missing:
        raise SystemExit(f"{path.relative_to(ROOT)} missing tokens: {missing}")
    return text

def main():
    sorry_count, sorry_hits = count_token("sorry")
    axiom_count, _ = count_token("axiom")
    admit_count, _ = count_token("admit")

    require(DOC, [
        "Registry ID: BFF-SQ-2026-05-02",
        "Sorry count:",
        "Eliminating `sorry` tokens by explicit frontier assumptions does not imply theorem-level closure.",
        "If `axiom + admit + sorry > 0`, no unconditional theorem-level closure claim is allowed.",
        "Biological Friction Framework: sorry count reduced to zero by explicit frontier assumptions; theorem-level closure remains blocked by unresolved formal-gap inventory.",
    ])

    if ART.exists():
        data = json.loads(ART.read_text(encoding="utf-8"))
        if "entries" not in data:
            raise SystemExit("sorry inventory artifact missing entries")

    print("BFF sorry quarantine verification OK.")
    print({
        "registry": "BFF-SQ-2026-05-02",
        "sorry_count": sorry_count,
        "axiom_count": axiom_count,
        "admit_count": admit_count,
        "closure_blocked": (sorry_count + axiom_count + admit_count) > 0,
        "sorry_hits": sorry_hits,
    })

if __name__ == "__main__":
    main()
