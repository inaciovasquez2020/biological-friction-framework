# Melanoma NCSC FAK/MAPK route compression — 2026-08-31

## Status

`CONDITIONAL / LITERATURE-BOUNDED MODEL`

This document records a bounded structural reduction for a melanoma minimal-residual-disease / therapy-escape graph. It is not clinical guidance, a treatment recommendation, or evidence of a cure.

## Question

After adding state-specific control for the CD36+ starved-like melanoma cell (SMC) residual, must the SOX10-positive / NGFR-high neural-crest stem cell-like (NCSC) state add a new mandatory control node, such as RXRG, to the retained graph?

## Result

`RESULT := THE NCSC ROUTE CAN BE CONDITIONALLY COMPRESSED INTO EXISTING FAK/AKT + MAPK CONTROL`

Rambow et al. identified an NCSC transcriptional program in melanoma MRD that was largely driven by RXRG; RXR antagonism reduced NCSC accumulation and delayed resistance.

Later Cancer Cell work sharpened the NCSC survival route in MAPK-inhibited melanoma:

```text
NCSC state
  -> GDNF-associated signaling
  -> FAK-dependent signaling
  -> AKT survival
  -> nongenetic resistance trajectory
```

FAK inhibition ablated the NCSC population and delayed relapse in patient-derived melanoma xenografts.

Critically, tumors that ultimately escaped this intervention in the tested series acquired resistance-conferring genetic alterations and showed increased sensitivity to ERK inhibition.

## Structural consequence

The current graph already retains abstract controls for:

```text
C_FAK_STATE := intercept demonstrated FAK-dependent melanoma survival states
C_MAPK := intercept MAPK/ERK-dependent genetic resistance/reactivation states
```

Therefore the observed NCSC evolutionary bifurcation can be represented as:

```text
R_NCSC_OBSERVED :=
  NCSC / nongenetic branch -> FAK/AKT-dependent
  OR
  post-FAK escape -> genetically fixed, ERK-sensitive resistance
```

and the corresponding observed-route cover is:

```text
C_NCSC_OBSERVED := C_FAK_STATE AND C_MAPK
```

No new mandatory RXRG-specific control is required by this observed route if those two abstract controls are already present.

## What is retired

```text
RETIRE :=
RXRG antagonism as a distinct mandatory control solely because the NCSC state exists
```

RXRG remains a validated state-regulatory vulnerability and possible implementation class. It is not promoted to a unique required graph node.

## Why this is only conditional

The Cancer Cell result is strong but model-bounded.

```text
DO_NOT_INFER :=
all NCSC-like melanoma states universally depend on FAK/AKT

DO_NOT_INFER :=
all resistance escaping FAK control universally returns to ERK dependence
```

The conditional compression is licensed only for the experimentally observed bifurcation.

## Relationship to SOX10-low state

The NCSC state must remain distinct from the previously encoded SOX10-low / TAZ-TEAD state.

The 2025 TAZ/TEAD work explicitly notes that NGFR expression is associated with the SOX10-expressing / MITF-low NCSC state and decreases after SOX10 knockout in A375 cells.

Therefore:

```text
DO_NOT_COLLAPSE := NCSC into SOX10-low invasive MRD
```

The route compression occurs through shared FAK/AKT control, not through phenotype identity.

## Evolutionary boundary

The important new object is not another static target but a trajectory guarantee.

```text
MISSING_OBJECT :=
a cross-model melanoma certificate showing that whenever the NCSC trajectory
escapes FAK/AKT-directed control, the surviving trajectory remains inside the
retained MAPK/ERK control basin rather than entering a third independent
nongenetic escape state.
```

Until that object exists:

```text
NCSC_ROUTE_COMPRESSION_STATUS := CONDITIONAL
```

## Boundary

```text
BOUNDARY :=
observed NCSC nongenetic resistance can be covered by existing FAK/AKT control,
and observed post-FAK escape can be covered by MAPK/ERK control,
but universal two-branch closure is not proved
```

## Evidence anchors

- Rambow et al., Cell (2018), `Toward Minimal Residual Disease-Directed Therapy in Melanoma`.
  - https://pubmed.ncbi.nlm.nih.gov/30017245/
- Marín-Béjar et al., Cancer Cell (2021), `Evolutionary predictability of genetic versus nongenetic resistance to anticancer drugs in melanoma`.
  - https://pubmed.ncbi.nlm.nih.gov/34143978/
  - https://doi.org/10.1016/j.ccell.2021.05.015
- Capparelli et al., Nature Communications (2025), `Targeting TAZ-TEAD in minimal residual disease enhances the duration of targeted therapy in melanoma models`.
  - https://www.nature.com/articles/s41467-025-64682-7

## Next bounded action

```text
NEXT_ACTIONS :=
1. Treat NCSC as conditionally covered by C_FAK_STATE + C_MAPK for the observed
   resistance bifurcation.
2. Do not add RXRG as a mandatory independent graph node.
3. Test the remaining pigmented / MITF-high MRD state for a vulnerability not
   already intercepted by the retained control set.
```
