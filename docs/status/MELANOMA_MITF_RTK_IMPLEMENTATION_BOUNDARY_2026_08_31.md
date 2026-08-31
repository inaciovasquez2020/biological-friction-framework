# Melanoma MITF-reduction / RTK implementation boundary — 2026-08-31

## Status

`CONDITIONAL / MODEL-BOUNDED IMPLEMENTATION PROBE`

This document records an interaction-safety boundary for the melanoma resistance graph. It is not clinical guidance, a treatment recommendation, or evidence of a cure.

## Question

Can direct reduction of MITF be treated as a universally monotone implementation of the abstract pigmented/MITF-high state control?

## Result

`RESULT := NO — MITF REDUCTION HAS A MODEL-BOUNDED RTK-RESISTANCE ESCAPE AND CANNOT BE CREDITED AS A UNIVERSALLY SAFE MONOTONE IMPLEMENTATION`

The abstract pigmented-state control is intentionally functional:

```text
C_PIGMENTED :=
prevent persistence of the MITF-high pigmented state
without merely redistributing survival into another resistant state
```

Direct MITF reduction is only one possible implementation class and has context-dependent consequences.

## Positive antagonistic-coupling evidence

Ji et al. (J Invest Dermatol, 2015; PMID 25789707) found in BRAF-V600E melanoma models that loss of the melanocytic/MITF program correlated with EGFR activation and BRAF-inhibitor resistance. Functional MITF depletion in an EGFR-competent SK-MEL-28 system strongly increased resistance to vemurafenib and MEK inhibition and rapidly increased EGFR-family ligand output, including HB-EGF, TGF-alpha, and NRG1. Forced MITF expression instead suppressed EGFR signaling and increased MAPK-inhibitor sensitivity in tested models.

This supports the bounded implementation edge:

```text
PROBE_MITF_REDUCTION
  -> ligand-rich RTK / EGFR-family survival signaling
  -> MAPK-targeted-therapy tolerance
```

At the graph level, the downstream survival function is represented conservatively by the already retained `rtk_pi3k_survival` state rather than by a new EGFR-specific mandatory node.

## Why the edge is not universal

Sun et al. (Nature, 2014; PMID 24670642) provide an important counter-boundary. In their A375 system, SOX10 suppression induced TGF-beta signaling, EGFR/PDGFRB expression, and reversible MAPKi resistance, whereas MITF knockdown alone did **not** reproduce the EGFR/PDGFRB induction or vemurafenib-resistance phenotype in the reported extended-data experiment.

Separately, Smith et al. (Cancer Cell, 2016; PMID 26977879) found that MAPKi-induced MITF elevation itself can form an early reversible tolerant state and that reducing the PAX3/MITF program can resensitize tested melanoma models.

Therefore the sign of direct MITF reduction is not globally monotone:

```text
DO_NOT_INFER :=
MITF reduction -> universal resistance

DO_NOT_INFER :=
MITF reduction -> universal safe closure of pigmented MRD
```

The correct object is an inactive implementation probe whose escape edge is exposed only when that implementation is selected.

## Executable interpretation

```text
PROBE_MITF_REDUCTION :=
model-bounded implementation candidate for C_PIGMENTED

blocks:
  direct pigmented/MITF-high persistence edges

can induce:
  e_mitf_reduction_to_rtk
    -> rtk_pi3k_survival
```

The probe is **not** part of the default active-control set.

When the probe is selected experimentally or computationally, closure credit requires concurrent coverage of the induced RTK/PI3K survival edge. This is an application of the repository-wide interaction-aware invariant:

```text
CONTROL_CREDIT(c) :=
  intended route is suppressed
  AND
  every known control-induced malignant route is also covered
```

## Relationship to the pigmented redistribution gap

This result does not retire `pigmented_redistribution_gap`.

It identifies one concrete, model-bounded failure mode of a state-regulatory implementation. It does **not** establish the full post-control state distribution after MITF/PAX3 suppression or after mitochondrial/OXPHOS-directed pigmented-state control.

```text
pigmented_redistribution_gap := REACHABLE
```

## Evidence anchors

- Ji Z et al., J Invest Dermatol (2015), `MITF Modulates Therapeutic Resistance through EGFR Signaling`.
  - PMID 25789707
  - PMCID PMC4466007
- Sun C et al., Nature (2014), `Reversible and adaptive resistance to BRAF(V600E) inhibition in melanoma`.
  - PMID 24670642
  - DOI 10.1038/nature13121
- Smith MP et al., Cancer Cell (2016), `Inhibiting Drivers of Non-mutational Drug Tolerance Is a Salvage Strategy for Targeted Melanoma Therapy`.
  - PMID 26977879
  - PMCID PMC4796027

## Boundary

```text
BOUNDARY :=
direct MITF reduction is a context-dependent implementation, not a universally
safe monotone pigmented-state control; in an EGFR-competent melanoma context it
can expose an RTK-survival route that must itself be covered
```

## Next bounded action

```text
NEXT_ACTIONS :=
1. Keep PROBE_MITF_REDUCTION inactive by default.
2. Require RTK/PI3K coverage whenever this probe is activated.
3. Keep pigmented_redistribution_gap reachable.
4. Search for matched post-intervention single-cell/state-composition data that
   directly measures where residual cells go after pigmented-state control.
```
