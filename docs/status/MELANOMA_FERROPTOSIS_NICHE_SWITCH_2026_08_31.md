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

The same study showed that GPX4 protein is rapidly restored after reoxygenation following a low-oxygen interval.

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

```text
lymph / LN niche
  -> low oxidative stress / hypoxia
  -> reduced GPX4 abundance / reliance
  -> FSP1 reliance

reoxygenation / blood transition
  -> GPX4 protein recovers
  -> ferroptosis-surveillance state changes
```

A static hitting set over `{GPX4, FSP1}` therefore does not by itself establish continuous coverage during dissemination.

## Transition literature audit

`TRANSITION_RESOLVED_SEARCH := NO DIRECT CERTIFICATE IDENTIFIED`

A targeted search found direct evidence for rapid GPX4 recovery after reoxygenation, but did not identify a direct experiment establishing whether FSP1 dependency:

```text
persists,
disappears,
or overlaps with restored GPX4 dependency
```

during the reoxygenation / LN-to-blood transition.

The endpoint niches are experimentally distinguishable; the dependency handoff itself remains unresolved.

## Weakest missing object

```text
MISSING_OBJECT :=
a transition-compatible melanoma ferroptosis certificate proving that the
niche-conditioned control remains effective across:

S_LN_HYPOXIC -> reoxygenation -> S_HEMATO

without an interval in which surveillance switches faster than control coverage.
```

A direct experimental certificate would track the same lineage or matched metastatic population while measuring:

1. oxygen / niche state,
2. GPX4 abundance and functional dependency,
3. FSP1 abundance and functional dependency,
4. ferroptosis susceptibility,
5. metastatic survival during LN-to-blood transition.

## Residual object

```text
R_FERROPTOSIS_SWITCH :=
state-dependent surveillance switching between GPX4- and FSP1-dominant niches
```

This is now the first unresolved non-ApoE metastatic-state boundary in the current graph.

## Boundary

```text
BOUNDARY :=
not proved that one static ferroptosis intervention set closes metastatic
melanoma across lymph-node, transition, and hematogenous niches
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
1. Retain R_FERROPTOSIS_SWITCH as the first unresolved non-ApoE metastatic-state
   boundary.
2. Do not collapse GPX4 and FSP1 into one static universal ferroptosis target.
3. Next, test whether any published paired-niche lineage data constrain the
   timing of the GPX4/FSP1 handoff enough to produce a transition invariant.
```
