# BFF ↔ URF observation quotient: isolated formal candidate

**Status:** CI PENDING until the exact commit's Lean compilation, axiom audit,
and independent kernel checker succeed. This status must not be promoted from
Python tests, workflow startup, or repository source inspection.

## Mathematical statement

For an observer `O : X → Y`, define the equivalence relation
`x ~ x'` iff `O x = O x'`. Any invariant `I : X → Z` has an exact decoder
on the observation quotient `X / ~` if and only if `I` is constant on
each observation fiber. A collision `O x = O x'` with `I x ≠ I x'`
is therefore a certificate that no such exact decoder exists.

For a general setoid, the converse uses quotient elimination rather than
the choice of arbitrary representatives. The underlying fact is standard;
the repository contribution is an isolated formal interface and strict
claim-boundary tracking, not theorem novelty.

## Repository connections

- Local biological quotient interface: `BiologicalFriction/QuotientLinear.lean`
  currently proves the sufficient condition `K ⊓ S = ⊥` for injectivity.
  This standalone bridge does **not** import Mathlib or establish a new
  equality between that submodule quotient and this observation quotient.
- URF core: `https://github.com/inaciovasquez2020/urf-core`; the
  observation/fiber factorization criterion is the abstract connection.
- Biological interaction graph: `infra/certificates/melanoma_interaction_graph.json`
  is a **conditional**, evidence-bounded computational model, not a
  clinical claim and not implied by the quotient theorem.
- Poincaré: No global JIID, descent, recognition or sphere result follows
  from this theorem.

## Reproduction

From this directory with Lean v4.29.0 already installed:

```sh
lake build ObservationBridge
lean ObservationBridge.lean
```

The standalone Lake package avoids touching either existing root
`lakefile.lean` or `lakefile.toml`. CI should check
`proofs/observation-bridge` through `leanprover/lean-action`, with
`leanchecker` and `axiom-audit`. Only `propext`, `Classical.choice`
and `Quot.sound` are permitted in audited theorems.

## Independent finite adversarial check (not a Lean proof)

Enumerate all observations `O : [n] → [m]`, all targets
`I : [n] → [k]` and all decoders `D : [m] → [k]`, comparing the
decoder-existence predicate with fiber constancy:

| (n,m,k) | (O,I) pairs | Factorable | Obstructed | Mismatches |
|---|---:|---:|---:|---:|
| (2,1,2) | 4 | 2 | 2 | 0 |
| (3,2,2) | 64 | 28 | 36 | 0 |
| (4,3,3) | 6561 | 1359 | 5202 | 0 |

This calculation checks decoders on the full observation codomain; it
therefore also checks the standard `Y`-decoder version of the theorem
for these finite nonempty codomains.

No scientific/clinical outcome or independent mathematical review
has been established by this candidate.
