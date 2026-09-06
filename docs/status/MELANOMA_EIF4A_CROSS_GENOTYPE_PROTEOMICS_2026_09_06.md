# Melanoma eIF4A cross-genotype proteomics boundary — 2026-09-06

## Status

`CONDITIONAL / PUBLIC-DATA-BOUNDED MODEL`

This document records a bounded correction to the melanoma eIF4A/eIF4F evidence surface. It is not clinical guidance, a treatment recommendation, or evidence of a cure.

## Question

Does newly public 2026 proteomics materially narrow the existing `eif4a_cross_state_gap` by extending direct protein-level eIF4F-perturbation evidence beyond BRAF-V600 melanoma?

## Result

`RESULT := CROSS-GENOTYPE PROTEIN-LEVEL eIF4F PERTURBATION EVIDENCE ESTABLISHED; RESIDUAL-STATE CLOSURE REMAINS UNPROVED`

ProteomeXchange dataset `PXD073251`, linked to Vadovicova et al. (Cell Communication and Signaling, 2026), directly profiles two human melanoma genetic backgrounds:

```text
A375   := BRAF-mutant melanoma
MelJuso := NRAS-mutant melanoma
```

The deposited LC-MS experiment contains DMSO control, the eIF4A/eIF4F inhibitor rocaglamide A, the MEK inhibitor PD184352/CI-1040, and their combination. Cells were collected approximately 20 hours after treatment.

The peer-reviewed study reports that rocaglamide A produced protein-level effects in both A375 and MelJuso cells. Proteomic analysis identified 57 proteins downregulated in common across the two melanoma models after eIF4F inhibition, including regulators spanning cell-cycle/DNA-replication and metabolic functions. The same study also reports eIF4F-inhibition-associated AMPK activation in both BRAF-mutant A375 and NRAS-mutant MelJuso cells.

Therefore the previous broad uncertainty

```text
"direct protein-level eIF4F perturbation evidence is confined to BRAF-V600 melanoma"
```

is too strong.

## What this retires

```text
RETIRE :=
absence of direct NRAS-mutant melanoma protein-level response data after
eIF4A/eIF4F perturbation
```

The admissible cross-genotype statement is now:

```text
ESTABLISHED :=
acute eIF4A/eIF4F perturbation produces measurable protein-level responses in
both BRAF-mutant A375 and NRAS-mutant MelJuso melanoma cells
```

This is stronger than an RNA-only generalization because the deposited surface is LC-MS proteomics.

## What this does not establish

The experiment is acute and bulk. It does not provide the matched residual-disease surface required to close the existing graph gap.

```text
DO_NOT_INFER :=
acute NRAS proteomic response
=> NRAS persister elimination

DO_NOT_INFER :=
shared protein response
=> shared 53BP1/NHEJ adaptive-mutability dependence

DO_NOT_INFER :=
RocA + MEKi exposure
=> long-term resistance-delay or relapse control in NRAS melanoma

DO_NOT_INFER :=
bulk proteomics
=> state-resolved coverage of SOX10-low, NCSC, pigmented/MITF-high, CD36+ SMC,
or other retained MRD states
```

The 2026 Fabbri et al. adaptive-mutability result remains the stronger matched residual-disease evidence for the 53BP1/NHEJ branch, but that work is centered on BRAF-V600 melanoma. `PXD073251` extends the protein-level eIF4F perturbation surface across genotype without supplying the missing NRAS residual-state, mutability, or relapse certificate.

## Structural consequence

No executable graph edge or control changes.

```text
KEEP := C_TRANSLATION_PERSIST
KEEP := eif4a_cross_state_gap reachable
```

The weakest remaining eIF4A closure object is sharpened from a generic request for any non-BRAF protein-level evidence to a matched functional residual-disease comparison.

```text
MISSING_OBJECT :=
a cross-genotype and state-resolved melanoma residual-disease certificate that,
under matched MAPK-targeted pressure:

1. identifies residual-state composition,
2. perturbs eIF4A/eIF4F function,
3. measures translation/protein outputs tied to the operative dependency,
4. measures persister survival and/or 53BP1/NHEJ mutability where applicable,
5. follows resistant outgrowth or relapse,
6. tests whether survivors redistribute into another retained MRD state,
7. includes at least one non-BRAF context before any universal claim.
```

## Evidence anchors

- ProteomeXchange / PRIDE dataset `PXD073251`, `LC-MS analysis of human melanoma cell line response to eIF4F inhibition and MEK inhibition`.
  - announced 2026-06-15
  - A375 and MelJuso
  - DMSO, rocaglamide A, PD184352/CI-1040, and combination conditions
  - 64 deposited files
  - https://proteomecentral.proteomexchange.org/cgi/GetDataset?ID=PXD073251
- Vadovicova et al., Cell Communication and Signaling (2026), `Translational control of AMPK activity in melanoma`.
  - DOI: 10.1186/s12964-026-02901-4
  - reports common protein-level responses to eIF4F inhibition in BRAF-mutant A375 and NRAS-mutant MelJuso cells
- Fabbri et al., EMBO Molecular Medicine (2026), `Selective mRNA translation determines adaptative mutability of melanoma cells to anti-BRAF/MEK combination therapy`.
  - retained as the stronger BRAF-V600 residual-disease / 53BP1-NHEJ adaptive-mutability evidence surface

## Boundary

```text
BOUNDARY :=
PXD073251 establishes direct NRAS-mutant as well as BRAF-mutant melanoma
protein-level response to eIF4A/eIF4F perturbation, narrowing the genotype
scope uncertainty; it does not establish state-resolved residual-cell coverage,
NRAS 53BP1/NHEJ dependency, long-term resistance suppression, or relapse control
```

## Next bounded action

```text
NEXT_ACTIONS :=
1. Keep eif4a_cross_state_gap reachable.
2. Do not promote PXD073251 to an executable closure control.
3. Search next for matched non-BRAF melanoma residual-disease eIF4A/eIF4F
   perturbation with protein/translation plus resistant-outgrowth endpoints.
4. If none exists, stop the eIF4A lane at this sharpened boundary.
```
