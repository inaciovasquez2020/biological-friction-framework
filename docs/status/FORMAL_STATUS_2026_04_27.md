# Formal Status — 2026-04-27

Status: Conditional Framework / Frontier Claims

## Build status

The repository builds, but build success is not theorem verification.

## Theorem status

This repository currently contains project-defined axioms, admitted obligations, and `sorry` proof holes.

- `axiom` is a trusted assumption, not a proof.
- `admit` is a proof hole.
- `sorry` is a proof hole.
- Any result depending on high-girth, non-coboundary, quotient-independence, project axioms, admits, or sorries is Conditional.
- No dependency on these assumptions should be described as proved, closed, final, terminal, unconditional, or machine-verified.

## Current status

- Current classification: Conditional Framework / Frontier Claims
- Strongest verified theorem: none asserted at repository level
- Weakest missing theorem: replace each load-bearing axiom/admit/sorry with a proof or quarantine it as an explicit assumption
- Conditional inventory: `docs/status/CONDITIONAL_FRONTIER_STATUS_2026_04_27.md`

## Boundary rule

If `axiom + admit + sorry > 0`, no unconditional theorem-closure claim is allowed.
