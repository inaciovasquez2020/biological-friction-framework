# Melanoma ferroptosis niche-switch boundary — 2026-08-31

## Status

`CONDITIONAL / LITERATURE-BOUNDED MODEL`

This document records a bounded structural result for a melanoma residual-disease / metastatic-escape model. It is not clinical guidance, a treatment recommendation, or evidence of a cure.

## Question

After abstract control of MAPK, PI3K/AKT, FAK-dependent states, SOX10-low MRD, and extracellular adenosine escape, can ferroptosis resistance be represented by one global control node?

## Result

`RESULT := A SINGLE GLOBAL FERROPTOSIS CONTROL NODE IS TOO COARSE`

Melanoma ferroptosis dependencies change with metastatic niche.

### Blood / hematogenous transit

Nature (2020) showed that melanoma cells transiting through blood experience greater oxidative stress and become dependent on GPX4 for ferroptosis protection, whereas cells in lymph do not show the same GPX4 dependency.

### Lymph / hypoxic lymph-node niche

Nature (2025) showed that lymph-node-derived melanoma cells in a hypoxic lymphatic niche have reduced GCLC/GSH and reduced GPX4. Low oxygen promotes GPX4 ubiquitination/proteasomal degradation, and these cells acquire increased reliance on FSP1. Selective FSP1 inhibition suppressed melanoma growth in lymph nodes in the tested models but not in subcutaneous tumors.

The same 2025 study showed that low-oxygen GPX4 reduction is reversible after reoxygenation, making the dependency dynamically state- and niche-dependent.

Therefore:

```text
RETIRE := C_FERROPTOSIS := one universal GPX4-axis control
RETIRE := C_FERROPTOSIS := one universal FSP1-axis control
```

## Structural repair

Represent ferroptosis surveillance as a niche-conditioned object:

```text
S_HEMATO := blood / hematogenous metastatic state
S_LN_HYPOXIC := hypoxic lymph-node metastatic state

V_GPX4 := GPX4-axis ferroptosis-surveillance dependency
V_FSP1 := FSP1-axis ferroptosis-surveillance dependency

C_FERROPTOSIS_NICHE :=
  (S_HEMATO -> V_GPX4-control)
  AND
  (S_LN_HYPOXIC -> V_FSP1-control)
```

This is a control abstraction. It does not select a drug, dose, delivery route, or clinical intervention.

## Transition problem

The stronger missing object is not simply a second target. Melanoma cells can move between niches whose ferroptosis surveillance programs differ.

The current evidence supports:

```text
lymph / LN niche
  -> low oxidative stress / hypoxia
  -> reduced GPX4 reliance
  -> FSP1 reliance

reoxygenation / blood transition
  -> GPX4 protein can recover
  -> ferroptosis-surveillance state changes
```

Therefore a static hitting set over `{GPX4, FSP1}` does not by itself prove closure. A cell could, in principle, switch surveillance state during dissemination.

## Weakest missing object

```text
MISSING_OBJECT :=
a transition-compatible melanoma ferroptosis certificate proving that the
niche-conditioned control remains effective across the metastatic itinerary:

S_LN_HYPOXIC -> reoxygenation -> S_HEMATO

without a time/state interval in which neither required surveillance dependency
is effectively intercepted.
```

A stronger experimental certificate would track the same lineage or matched metastatic population while measuring:

1. oxygen / niche state,
2. GPX4 abundance and dependency,
3. FSP1 abundance and dependency,
4. ferroptosis susceptibility,
5. metastatic survival during LN-to-blood transition.

## Why this matters for the residual graph

Within the current graph, `LN_hypoxic × FSP1` is a real residual state, but simply appending `FSP1` as another independent node misses the dynamic switch.

The correct residual object is:

```text
R_FERROPTOSIS_SWITCH :=
state-dependent surveillance switching between GPX4- and FSP1-dominant niches
```

Until the transition certificate exists:

```text
BOUNDARY :=
not proved that one static ferroptosis intervention set closes metastatic
melanoma across lymph-node and hematogenous niches
```

## Evidence anchors

- Ubellacker et al., Nature (2020), `Lymph protects metastasizing melanoma cells from ferroptosis`.
  - https://www.nature.com/articles/s41586-020-2623-z
  - https://pubmed.ncbi.nlm.nih.gov/32814895/
- Palma et al., Nature (2025), `Lymph node environment drives FSP1 targetability in metastasizing melanoma`.
  - https://www.nature.com/articles/s41586-025-09709-1
  - https://pubmed.ncbi.nlm.nih.gov/41193799/

## Next bounded action

```text
NEXT_ACTIONS :=
1. Search for direct evidence that FSP1 dependence persists, disappears, or is
   replaced as lymph-node melanoma re-enters oxygenated / blood environments.
2. Search for same-lineage or paired-niche measurements of GPX4 and FSP1 across
   LN-to-blood dissemination.
3. If no transition-resolved dataset exists, retain R_FERROPTOSIS_SWITCH as the
   first unresolved non-ApoE metastatic-state boundary.
```
