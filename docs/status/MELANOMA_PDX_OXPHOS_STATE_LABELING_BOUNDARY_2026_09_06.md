# Melanoma PDX OXPHOS state-labeling boundary — 2026-09-06

## Status

`CONDITIONAL / PUBLIC-DATA-BOUNDED MODEL`

This note records a state-identification boundary from longitudinal melanoma PDX spatial-transcriptomic data. It does not add a treatment, control, clinical claim, or cure claim.

## Question

Can oxidative-phosphorylation enrichment in MAPK-treated residual melanoma be used as a shortcut for identifying the Rambow pigmented / MITF-high residual state in the executable framework?

## Public source surface

```text
GSE245582
BioProject PRJNA1029019
Rubinstein et al., Cancer Research (2025)
```

The study followed BRAF(V600E) melanoma patient-derived xenografts longitudinally under continuous dabrafenib/trametinib exposure from pretreatment through maximal response and tumor regrowth, using spatial transcriptomics together with clonal/phylogenetic analysis and histopathology-linked modeling.

## Result

```text
RESULT := OXPHOS-HIGH PERSISTENCE IS NOT A SUFFICIENT CERTIFICATE OF
          THE PIGMENTED / MITF-HIGH MRD STATE
```

The longitudinal PDX analysis reports that the treatment persister state shows, in the same broad residual phase:

```text
increased oxidative phosphorylation
reduced proliferation
increased invasive capacity
```

The study also tracks state change and lineage selection through maximum response and regrowth rather than examining only an acute bulk-treatment snapshot.

This directly strengthens a state-labeling boundary already implicit in the framework: oxidative metabolism alone does not uniquely identify the transcriptomically defined Rambow pigmented / MITF-high state.

Therefore:

```text
DO_NOT_INFER :=
OXPHOS-high residual melanoma
=> S_PIGMENTED
```

and:

```text
DO_NOT_INFER :=
OXPHOS enrichment
=> absence of invasive / dedifferentiated features
```

## Structural consequence

No executable graph change is justified.

The existing states remain distinct:

```text
pigmented_mitf_persister
sox10_low_mrd
smc_cd36_persister
nsc_persister
```

and the existing redistribution gaps remain reachable.

The PDX data strengthen the reason not to collapse states by a single metabolic marker, but they do not test a validated pigmented-state control, SMC-state control, or another state-selective intervention followed by survivor accounting.

Therefore:

```text
pigmented_redistribution_gap := remains unresolved
smc_redistribution_gap       := remains unresolved
```

## Why this improves the boundary

The framework already distinguishes the pigmented MITF-high/PPARGC1A program from the CD36-positive SMC program and from invasive/SOX10-low residual disease. The PDX study adds independent in-vivo-like longitudinal evidence that oxidative persistence can coexist with increased invasive capacity during targeted therapy.

That prevents an otherwise tempting shortcut:

```text
high OXPHOS = pigmented state
```

which is not supported by the longitudinal PDX evidence.

The correct requirement remains multivariate, state-resolved identity plus functional survivor accounting.

## What the dataset does not prove

```text
1. It does not selectively perturb MITF/PAX3, PGC1A/OXPHOS, CD36, PEX3,
   UGCG, SOX10, or another retained state-specific control.
2. It does not show post-control redistribution among the framework's named
   MRD states.
3. It does not establish that the reported oxidative/invasive persister
   population is identical to a Rambow atlas state.
4. The PDX hosts are immunodeficient NSG mice, so immune-competent closure is
   not supplied.
5. The studied tumors are BRAF(V600E), so cross-genotype closure is not supplied.
```

## Weakest missing object

```text
MISSING_OBJECT :=
a matched longitudinal state-resolved survivor certificate after a validated
state-selective control, under continued MAPK pressure, showing both depletion
of the intended residual state and the destinations of surviving lineages
through long-term outgrowth/regrowth
```

For the pigmented branch specifically, that means a validated pigmented/MITF-state control followed by state-resolved accounting that distinguishes true pigmented-state depletion from persistence or enrichment of invasive, SMC, NCSC, or other residual programs.

## Boundary

```text
BOUNDARY :=
longitudinal BRAF-mutant melanoma PDX data show that oxidative persistence can
coexist with invasive features during MAPK-targeted therapy; OXPHOS enrichment
therefore cannot serve as a standalone certificate of the pigmented/MITF-high
state, and no redistribution gap is retired
```

## Evidence anchors

- Rubinstein et al., Cancer Research (2025), `Spatiotemporal Profiling Defines Persistence and Resistance Dynamics during Targeted Treatment of Melanoma`.
  - https://pubmed.ncbi.nlm.nih.gov/39700408/
  - https://doi.org/10.1158/0008-5472.CAN-24-0690
- GEO GSE245582.
  - https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE245582
- Analysis code described by the authors:
  - https://github.com/TheJacksonLaboratory/PDX-melanoma-integrated-analysis

## Next bounded action

```text
NEXT_ACTIONS :=
1. Keep the executable graph unchanged.
2. Do not use OXPHOS alone to label S_PIGMENTED.
3. Search next for public post-control survivor-composition data rather than
   additional untreated or treatment-only state atlases.
```
