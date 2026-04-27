#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
STATUS_DOC = ROOT / "docs/status/CONDITIONAL_FRONTIER_STATUS_2026_04_27.md"
FORMAL_DOC = ROOT / "docs/status/FORMAL_STATUS_2026_04_27.md"

PATTERNS = {
    "axiom": re.compile(r"^\s*axiom\s+"),
    "admit": re.compile(r"\badmit\b"),
    "sorry": re.compile(r"\bsorry\b"),
}

def lean_files():
    return [
        p for p in ROOT.rglob("*.lean")
        if ".lake" not in p.parts and ".git" not in p.parts
    ]

def counts() -> dict[str, int]:
    out = {k: 0 for k in PATTERNS}
    for p in lean_files():
        for line in p.read_text(encoding="utf-8", errors="ignore").splitlines():
            for name, rx in PATTERNS.items():
                if rx.search(line):
                    out[name] += 1
    return out

def main() -> int:
    if not STATUS_DOC.exists():
        print(f"missing status document: {STATUS_DOC.relative_to(ROOT)}")
        return 1

    if not FORMAL_DOC.exists():
        print(f"missing formal status document: {FORMAL_DOC.relative_to(ROOT)}")
        return 1

    text = STATUS_DOC.read_text(encoding="utf-8", errors="ignore")
    formal_text = FORMAL_DOC.read_text(encoding="utf-8", errors="ignore")
    c = counts()

    required = [
        "Status: Conditional Framework / Frontier Claims",
        "This repository contains conditional formalization work.",
        "Any result depending on high-girth, non-coboundary, quotient-independence, project axioms, admits, or sorries is not an unconditional theorem.",
        "If `axiom + admit + sorry > 0`, no unconditional theorem-closure claim is allowed.",
        "Axiom count: " + str(c["axiom"]),
        "Admit count: " + str(c["admit"]),
        "Sorry count: " + str(c["sorry"]),
    ]

    missing = [s for s in required if s not in text]
    if missing:
        print("conditional frontier status check failed")
        for s in missing:
            print(f"missing: {s}")
        return 1

    formal_required = [
        "Status: Conditional Framework / Frontier Claims",
        "The repository builds, but build success is not theorem verification.",
        "`axiom` is a trusted assumption, not a proof.",
        "`admit` is a proof hole.",
        "`sorry` is a proof hole.",
        "If `axiom + admit + sorry > 0`, no unconditional theorem-closure claim is allowed.",
    ]
    formal_missing = [s for s in formal_required if s not in formal_text]
    if formal_missing:
        print("frontier formal-status boundary check failed")
        for s in formal_missing:
            print(f"missing: {s}")
        return 1

    print({
        "status": "PASS",
        "classification": "Conditional Framework / Frontier Claims",
        "axiom_count": c["axiom"],
        "admit_count": c["admit"],
        "sorry_count": c["sorry"],
        "status_doc": str(STATUS_DOC.relative_to(ROOT)),
        "formal_status_doc": str(FORMAL_DOC.relative_to(ROOT)),
    })
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
