# Melanoma SOX10-low AP-1 molecular bridge — 2026-08-31

## Status

`CONDITIONAL / LITERATURE-BOUNDED MODEL`

This document records the result of the bounded public-transcriptomic follow-up requested by `MELANOMA_SOX10_LOW_DUAL_VULNERABILITY_2026_08_31.md`. It does not establish functional redundancy between TEAD and cIAP vulnerabilities, and it is not clinical guidance or evidence of a cure.

## Question

Do the public matched-clone TAZ/TEAD datasets resolve whether the TAZ/TEAD and cIAP2/BIRC3 vulnerability programs in SOX10-low melanoma are transcriptionally coupled?

## Result

`RESULT := AP-1 PROVIDES A PARTIAL MOLECULAR BRIDGE; BIRC3 RESPONSE TO TAZ/TEAD PERTURBATION REMAINS UNRESOLVED`

The public GEO design is directly matched to the A375 SOX10-knockout clones used in the dual-vulnerability work:

```text
GSE259388
  A375 parental
  A375 crSOX10 #2.18
  A375 crSOX10 #4.21

  each with:
    no siRNA
    siCTRL
    siTAZ #1
    siTAZ #2
    siYAP1 #1
    siYAP1 #2

  triplicate samples
```

A separate public series, `GSE259389`, contains TEAD-inhibitor expression profiling from the same 2025 study.

The published analysis establishes that SOX10 loss increases AP-1 activity and c-Jun expression, and that c-Jun depletion reduces the canonical TEAD outputs CTGF and CYR61. Thus:

```text
SOX10 loss
  -> AP-1 / c-Jun increase
  -> supports TAZ/TEAD transcriptional output
```

The independent cIAP2 study establishes that, in the same SOX10-knockout clone family, BIRC3/cIAP2 is transcriptionally upregulated and the AP-1 component JUND is required for cIAP2 expression:

```text
SOX10 loss
  -> AP-1 / JUND activity
  -> BIRC3 / cIAP2 expression
  -> MAPKi tolerance
```

Therefore the two vulnerability programs share an evidence-backed AP-1 regulatory layer:

```text
                    -> c-Jun -> TEAD output
SOX10 loss -> AP-1 -|
                    -> JUND  -> BIRC3/cIAP2
```

## What this does and does not establish

This is a mechanistic bridge, not a redundancy certificate.

The published 2025 TAZ/TEAD analysis shows that TAZ depletion causes a large transcriptomic shift in SOX10-knockout A375 cells and that TAZ is the dominant co-activator for the measured TEAD transcriptome. However, the paper does not report a validated result that TAZ knockdown or TEAD inhibition suppresses JUND or BIRC3/cIAP2.

Likewise, the cIAP2 paper shows that JUND is required for BIRC3/cIAP2 expression, but it does not establish that cIAP perturbation suppresses the TAZ/TEAD transcriptional program.

Therefore:

```text
ESTABLISHED := shared AP-1 regulatory neighborhood

NOT_ESTABLISHED := V_TEAD -> loss(BIRC3/cIAP2)
NOT_ESTABLISHED := V_CIAP -> loss(TAZ/TEAD output)
NOT_ESTABLISHED := V_TEAD and V_CIAP functional redundancy
```

## Public-data extraction boundary

GSE259388 provides per-sample normalized-count files and the exact matched perturbation design needed for a direct BIRC3/JUND/c-Jun comparison. The public article also states that GSE259389 contains TEAD-inhibitor expression data.

The present audit verified the dataset design and the published AP-1/TEAD and JUND/BIRC3 relationships, but did not obtain an authoritative differential-expression result for `BIRC3` or `JUND` after TAZ/TEAD perturbation from the published text itself.

Accordingly:

```text
MOLECULAR_COUPLING_STATUS := PARTIAL / DIRECTION UNRESOLVED
```

Do not infer a BIRC3 fold-change or significance value that has not been directly extracted from the deposited expression matrix or an author-supplied differential-expression table.

## Executable-graph consequence

No executable reachability change is justified.

```text
KEEP_REACHABLE := sox10_dual_vulnerability_gap
```

The existing graph-level abstraction remains:

```text
C_SOX10_LOW := V_TEAD OR V_CIAP
```

with no claim that either molecular implementation alone covers the complete SOX10-low residual population.

## Weakest missing object

The remaining mechanistic object is narrower:

```text
MISSING_OBJECT_L1 :=
a direct differential-expression extraction from GSE259388 and/or GSE259389
for BIRC3, JUND, JUN, FOSL2 and canonical TEAD targets in the matched A375
crSOX10 #2.18/#4.21 backgrounds after TAZ knockdown or TEAD inhibition.
```

Even if this shows transcriptional coupling, the functional object remains:

```text
MISSING_OBJECT_L2 :=
same-clone residual-survivor comparison of V_TEAD alone, V_CIAP alone,
and combined/sequential perturbation under MAPK-targeted pressure.
```

## Evidence anchors

- Ott et al., Nature Communications (2025), `Targeting TAZ-TEAD in minimal residual disease enhances the duration of targeted therapy in melanoma models`.
  - https://www.nature.com/articles/s41467-025-64682-7
  - https://pubmed.ncbi.nlm.nih.gov/41193428/
  - GSE259388: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE259388
  - GSE259389: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE259389
- Glasheen et al., Molecular Cancer Therapeutics (2023), `Targeting Upregulated cIAP2 in SOX10-Deficient Drug Tolerant Melanoma`.
  - https://pubmed.ncbi.nlm.nih.gov/37343247/
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC10527992/

## Boundary

```text
BOUNDARY :=
AP-1 is an evidence-backed shared regulatory layer connecting the TEAD and
cIAP2 programs in SOX10-low melanoma, but direct BIRC3/JUND response to
TAZ/TEAD perturbation and functional survivor redundancy remain unproved.
```

## Next bounded action

```text
NEXT_ACTIONS :=
1. Obtain the deposited normalized-count matrices or author differential tables
   for GSE259388/GSE259389.
2. Compute matched-clone BIRC3/JUND/JUN/FOSL2 response to siTAZ and TEADi.
3. Keep sox10_dual_vulnerability_gap reachable regardless of transcript-only
   coupling until the functional survivor comparison exists.
4. If matrix extraction remains blocked, move to the next executable unresolved
   state rather than claiming an unmeasured fold-change.
```
