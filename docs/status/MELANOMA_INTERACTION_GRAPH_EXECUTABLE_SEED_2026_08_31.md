# Melanoma interaction graph executable seed — 2026-08-31

## Status

`EXECUTABLE / CONDITIONAL CERTIFICATE`

This document records the first repository-native executable seed for the interaction-aware melanoma resistance invariant. It is a model-verification artifact, not clinical guidance, a treatment recommendation, or evidence of a cure.

## Result

`RESULT := MINIMAL INTERACTION-AWARE GRAPH CERTIFICATE IMPLEMENTED`

The repository now contains:

```text
infra/certificates/melanoma_interaction_graph.json
infra/ci/verify_melanoma_interaction_graph.py
tests/test_melanoma_interaction_graph.py
```

The certificate encodes a deliberately small evidence-bounded interaction slice rather than claiming to represent the full melanoma state space.

## Encoded baseline residuals

The current seed contains four baseline malignant routes:

```text
therapy pressure -> RTK / PI3K survival
therapy pressure -> mTOR / ATF4 / MTHFD2 persistence
therapy pressure -> NCSC nongenetic escape
therapy pressure -> dynamic ERK-pulse escape
```

## Encoded control interactions

The certificate activates four already-supported control/implementation objects:

```text
I_PI3K_SURVIVAL_CONTROL
I_MTOR_ISR_CONTROL
I_FAK_NCSC_CONTROL
C_MAPK_DYNAMIC
```

It then includes experimentally supported non-monotone interaction edges:

```text
PI3K suppression -> nuclear Polκ stress-tolerance state
mTOR suppression -> nuclear Polκ stress-tolerance state
FAK/NCSC control -> observed ERK-sensitive genetic escape trajectory
```

`C_MAPK_DYNAMIC` blocks the encoded ERK-pulse and ERK-sensitive genetic escape edges.

The two PI3K/mTOR-induced Polκ edges remain unblocked.

## Current machine-checked result

With the current active control set, fixed-point reachability leaves exactly one encoded malignant state reachable:

```text
polk_stress_tolerance
```

Therefore the certificate is intentionally:

```text
claim := conditional

declared_unresolved := [polk_stress_tolerance]
```

The verifier requires the declared unresolved set to equal the complete set of reachable malignant states in the encoded graph.

## Fail-closed behavior

The test suite checks three properties:

```text
1. the current conditional certificate passes;
2. changing the certificate to claim := closed while Polκ remains reachable fails;
3. omitting the reachable Polκ state from declared_unresolved fails.
```

Thus the executable surface cannot silently upgrade the current partial interaction graph into a closure claim.

## Evidence-file locking

Every baseline or induced biological edge in the current certificate carries one or more repository evidence paths.

The verifier rejects an edge or control if its evidence list is empty or if a referenced repository evidence file does not exist.

This does not independently validate the scientific contents of those files. It prevents machine-readable edges from becoming detached from the bounded evidence objects that motivated them.

## CI integration

PR-time canonical CI now runs:

```text
tests/test_melanoma_interaction_graph.py
```

alongside the existing canonical and spectral-gap tests.

Push-time `verify` also runs:

```text
python3 infra/ci/verify_melanoma_interaction_graph.py
```

## What this does not prove

```text
DO_NOT_INFER :=
this seed graph represents every melanoma state or resistance route

DO_NOT_INFER :=
polk_stress_tolerance is the only real biological survivor

DO_NOT_INFER :=
current active controls form a treatment regimen

DO_NOT_INFER :=
conditional machine verification implies clinical efficacy or cure
```

The checker proves only consistency of the encoded interaction slice.

## Remaining executable boundary

The previous model-level missing object is now partially constructed, not closed.

```text
MISSING_OBJECT :=
expand the interaction certificate from the minimal seed to the retained
melanoma graph while preserving evidence-linked, fail-closed semantics.
```

The next expansion should be bounded and should add only already-retained objects, such as:

```text
ApoE signed outcomes
GPX4/FSP1 niche-switch transition
KDM5B reseeding state dynamics
SOX10-low / SMC / pigmented MRD states
adenosine immune escape
CSE/H2S-persulfide cross-state persistence
translation/adaptive-mutability control
```

No new biological target should be added merely to enlarge the graph.

## Boundary

```text
BOUNDARY :=
a repository-native interaction-aware verifier now exists for a minimal
conditional melanoma slice; full retained-graph encoding remains incomplete
```

## Next bounded action

```text
NEXT_ACTIONS :=
1. Compile and run the new verifier through canonical PR CI.
2. Repair only the first authoritative failure if one appears.
3. Merge only if the fail-closed tests pass.
4. After merge, add retained graph objects incrementally rather than all at once.
```
