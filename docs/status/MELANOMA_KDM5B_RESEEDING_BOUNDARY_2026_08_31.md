# Melanoma KDM5B-high reseeding boundary — 2026-08-31

## Status

`CONDITIONAL / LITERATURE-BOUNDED MODEL`

This document records a bounded structural result for a melanoma drug-tolerant-persister / minimal-residual-disease graph. It is not clinical guidance, a treatment recommendation, or evidence of a cure.

## Question

After representing the classic Rambow MRD states and adding cross-state metabolic/stress controls, can the KDM5B-high slow-cycling melanoma persister state be collapsed into the existing pigmented/MITF-high control?

## Result

`RESULT := DO NOT COLLAPSE KDM5B-HIGH PERSISTENCE INTO THE PIGMENTED-STATE CONTROL`

KDM5B/JARID1B-high melanoma cells form a reversible slow-cycling persister reservoir. They can survive MAPK-pathway pressure and later repopulate the tumor while re-establishing KDM5B expression heterogeneity.

A bounded state abstraction is:

```text
S_KDM5B :=
KDM5B-high slow-cycling melanoma persister
  -> reversible growth arrest / cytokinesis delay
  -> survival under targeted-therapy pressure
  -> later KDM5B downshift / heterogeneity restoration
  -> tumor repopulation
```

## Why pigmented-state identity is insufficient

Forced KDM5B expression can drive melanoma cells toward a melanocytic/MITF-high differentiated program, including increased MITF and pigmentation-lineage genes.

However, that experiment also shows that the KDM5B-high state is dynamic and reversible. Natural tumor maintenance depends on re-establishing heterogeneous KDM5B states rather than remaining permanently fixed in one differentiated endpoint.

Therefore:

```text
DO_NOT_INFER :=
KDM5B-high => permanently pigmented/MITF-high

DO_NOT_INFER :=
C_PIGMENTED => control(S_KDM5B reseeding)
```

The existing pigmented-state constraint may intersect the KDM5B trajectory, but it does not certify elimination of the slow-cycling reservoir or prevention of reseeding.

## Directionality paradox

The KDM5B axis cannot be represented as a monotone `block KDM5B` or `increase KDM5B` rule.

Evidence supports two context-dependent manipulations:

```text
1. reduce / exploit KDM5B-high metabolic survival
   -> suppress the slow-cycling resistant subpopulation

2. force sustained KDM5B-high differentiation
   -> reduce proliferation / plasticity
   -> create a lineage-directed vulnerability
```

These are not contradictory once the control objective is stated correctly: the unwanted object is not KDM5B expression itself, but reversible KDM5B-state plasticity that preserves a reseeding reservoir.

Therefore retire a monotone node:

```text
RETIRE := KDM5B_HIGH as intrinsically good or intrinsically bad
```

## Functional repair

Introduce a state-dynamics constraint:

```text
C_KDM5B_RESEED :=
prevent KDM5B-high slow-cycling persisters from surviving therapy pressure
and later reseeding a proliferative heterogeneous melanoma population
```

This can be satisfied by any experimentally validated implementation that either:

```text
A. eliminates the KDM5B-high reservoir,
OR
B. locks the reservoir in a non-reseeding state and then eliminates it through
   a matched state-specific vulnerability.
```

No drug or directional KDM5B manipulation is promoted as universal.

## Evidence-backed subclasses

### Mitochondrial vulnerability

In NF1-mutant melanoma under ERK inhibition, the KDM5B-positive population expanded and showed increased oxidative-metabolic dependence. Mitochondrial complex-I interference suppressed the KDM5B-positive population and reduced emergence of resistant clones in long-term culture.

### State-lock / lineage-directed vulnerability

Genetic or chemical enforcement of sustained KDM5B-high expression delayed proliferation, reduced tumor-repopulation properties, shifted cells toward melanocytic differentiation, and produced a lineage-specific vulnerability in preclinical models.

These represent distinct implementation classes of `C_KDM5B_RESEED`, not a universal treatment prescription.

## Relationship to existing controls

```text
C_PIGMENTED
  -> targets persistence of the MITF-high/pigmented state
  -> does not prove reseeding control

C_ISR_MTHFD2
  -> targets mTOR/ATF4/MTHFD2 stress/DNA-repair tolerance
  -> does not prove KDM5B-state control

C_SMC_METABOLIC
  -> targets CD36+ peroxisome/UGCG persisters
  -> does not prove KDM5B-state control
```

Therefore `S_KDM5B` remains separately represented.

## Weakest missing object

```text
MISSING_OBJECT :=
a matched-lineage melanoma experiment showing that a candidate
C_KDM5B_RESEED implementation:

1. identifies the KDM5B-high persister population under therapy,
2. prevents later repopulation after continued treatment or withdrawal,
3. does not merely shift survivors into another uncovered MRD state,
4. preserves the already retained metastatic and immune boundaries,
5. generalizes beyond one genotype/model before any universal claim is made.
```

## Boundary

```text
BOUNDARY :=
KDM5B-high persistence is a reversible reseeding problem, not a monotone target;
current pigmented-state coverage does not prove control of that dynamics
```

## Evidence anchors

- Chauvistré et al., Nature Communications (2022), `Persister state-directed transitioning and vulnerability in melanoma`.
  - https://www.nature.com/articles/s41467-022-30641-9
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC9160289/
  - https://pubmed.ncbi.nlm.nih.gov/35650266/
- Tsoi / NF1-metabolic follow-up (2017), `Phenformin enhances the efficacy of ERK inhibition in NF1-mutant melanoma`.
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC5392423/
  - https://pubmed.ncbi.nlm.nih.gov/28143781/
- Shah et al., Cancer Science (2026), `MAPK Inhibitor-Tolerant Persister Cells in Melanoma: Mechanisms and Therapeutic Vulnerabilities`.
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC13394650/

## Next bounded action

```text
NEXT_ACTIONS :=
1. Retain C_KDM5B_RESEED as a distinct state-dynamics requirement.
2. Do not merge it into C_PIGMENTED without a reseeding certificate.
3. Re-run the residual graph with C_KDM5B_RESEED abstractly covered.
4. Test m6A/eIF4A selective translation next as a cross-state survival program.
```
