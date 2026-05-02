#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]

REGISTRY_DOC = ROOT / "docs/status/BFF_TERMINAL_FRONTIER_REGISTRY_2026_05_02.md"
CONDITIONAL_DOC = ROOT / "docs/status/CONDITIONAL_FRONTIER_STATUS_2026_04_27.md"
FULL_REGISTRY = ROOT / "docs/status/FULL_COMPLETION_REGISTRY.json"
README = ROOT / "README.md"

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

def counts():
    out = {k: 0 for k in PATTERNS}
    for path in lean_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        for line in text.splitlines():
            for name, rx in PATTERNS.items():
                if rx.search(line):
                    out[name] += 1
    return out

def require(path, tokens):
    text = path.read_text(encoding="utf-8", errors="ignore")
    missing = [t for t in tokens if t not in text]
    if missing:
        raise SystemExit(
            f"{path.relative_to(ROOT)} missing required tokens:\n"
            + "\n".join(f"- {m}" for m in missing)
        )
    return text

def main():
    for path in [REGISTRY_DOC, CONDITIONAL_DOC, FULL_REGISTRY, README]:
        if not path.exists():
            raise SystemExit(f"missing required file: {path.relative_to(ROOT)}")

    c = counts()

    require(CONDITIONAL_DOC, [
        "Status: Conditional Framework / Frontier Claims",
        "If `axiom + admit + sorry > 0`, no unconditional theorem-closure claim is allowed.",
        "Axiom count: " + str(c["axiom"]),
        "Admit count: " + str(c["admit"]),
        "Sorry count: " + str(c["sorry"]),
    ])

    require(REGISTRY_DOC, [
        "Registry ID: BFF-TFR-2026-05-02",
        "Status: Conditional Framework / Repository-Surface Closed",
        "If `axiom + admit + sorry > 0`, no unconditional theorem-level closure claim is allowed.",
        "No theorem-level closure is asserted.",
        "repository-surface closed; theorem-level claims conditional on the recorded formal-gap inventory.",
    ])

    reg = json.loads(FULL_REGISTRY.read_text(encoding="utf-8"))
    items = reg["items"]
    complete = sum(1 for item in items if item.get("status") == "complete")
    total = len(items)

    if reg.get("scope") != "repository-surface":
        raise SystemExit("FULL_COMPLETION_REGISTRY scope must remain repository-surface")

    if reg.get("expected_percent") != (100 * complete // total):
        raise SystemExit("FULL_COMPLETION_REGISTRY expected_percent mismatch")

    require(README, [
        "## Formal Status",
        "Status: Conditional Framework / Frontier Claims",
        "Strongest verified theorem: none asserted at repository level",
        "Weakest missing theorem: replace each load-bearing axiom/admit/sorry with a proof or quarantine it as an explicit assumption",
    ])

    print("BFF terminal frontier registry verification OK.")
    print({
        "registry": "BFF-TFR-2026-05-02",
        "classification": "repository-surface closed; theorem-level conditional",
        "axiom_count": c["axiom"],
        "admit_count": c["admit"],
        "sorry_count": c["sorry"],
    })

if __name__ == "__main__":
    main()
