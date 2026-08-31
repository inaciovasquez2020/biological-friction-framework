# Melanoma ferroptosis niche-switch boundary — 2026-08-31

## Status

`CONDITIONAL / LITERATURE-BOUNDED MODEL`

This document records a bounded structural result for a melanoma residual-disease / metastatic-escape model. It is not clinical guidance, a treatment recommendation, or evidence of a cure.

## Question

After abstract control of MAPK, PI3K/AKT, FAK-dependent states, SOX10-low MRD, and extracellular adenosine escape, can ferroptosis resistance be represented by one global control node, and can the GPX4/FSP1 handoff be certified continuously during LN-to-blood transition?

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

## Transition-resolved evidence audit

`TRANSITION_RESOLVED_SEARCH := NO DIRECT FUNCTIONAL HANDOFF CERTIFICATE IDENTIFIED`

The 2025 study provides a quantitative GPX4 protein time course. B16-F0 cells were first held at 1% oxygen for 24 hours and then re-exposed to 21% oxygen. GPX4 abundance was measured after 2, 4, and 8 hours of reoxygenation and was described as rapidly restored.

However, the study did not measure functional GPX4 dependency at those 2-, 4-, or 8-hour reoxygenation time points.

The same study also tested FSP1 loss during experimental hematogenous metastasis: intravenous injection of LN7 Fsp1-WT versus Fsp1-KO cells did not show reduced lung colonization from Fsp1 loss; if anything, colonization was modestly increased in the Fsp1-KO condition. Thus the published evidence does not support FSP1 as a required bloodstream-survival dependency in that experiment.

This sharpens the transition boundary:

```text
DO_NOT_INFER :=
GPX4 protein recovery => restored functional GPX4 dependency

DO_NOT_INFER :=
FSP1 dependency in hypoxic LN => persistent FSP1 dependency in blood
```

The endpoint niches are experimentally distinguishable; the functional dependency handoff itself remains unresolved.

## Weakest transition invariant

Let:

```text
D_GPX4(t) := melanoma survival is functionally dependent on GPX4 surveillance at time t
D_FSP1(t) := melanoma survival is functionally dependent on FSP1 surveillance at time t
T_transition := interval spanning LN hypoxia -> reoxygenation -> hematogenous transit
```

A sufficient continuity condition for the current two-state control abstraction is:

```text
SUFFICIENT_HANDOFF_INVARIANT :=
forall t in T_transition,
  D_GPX4(t) OR D_FSP1(t)
```

This is the weakest useful disjunctive invariant for continuous two-axis coverage: at every transition time, at least one of the two ferroptosis-surveillance dependencies must remain functionally active.

The literature currently establishes endpoint-like facts consistent with:

```text
LN_HYPOXIC_ENDPOINT   -> D_FSP1
HEMATO_ENDPOINT       -> D_GPX4
```

but does not establish:

```text
forall t in T_transition,
  D_GPX4(t) OR D_FSP1(t)
```

Therefore:

```text
HANDOFF_INVARIANT_STATUS := UNPROVED
```

## Temporal-resolution boundary

The earliest reported reoxygenation measurement in the GPX4 recovery experiment is 2 hours, followed by 4 and 8 hours.

But the missing interval cannot be reduced merely to `0 < t < 2 h`, because the measured quantity is GPX4 protein abundance, not GPX4 functional dependency, and FSP1 dependency was not assayed at the same reoxygenation time points.

The precise missing measurements are therefore:

```text
for t in {2 h, 4 h, 8 h} and earlier transition times:
  functional GPX4 dependency
  functional FSP1 dependency
  ferroptosis susceptibility
```

in the same transitioning melanoma population.

## Weakest missing object

```text
MISSING_OBJECT :=
a matched-lineage transition experiment demonstrating, across
S_LN_HYPOXIC -> reoxygenation -> S_HEMATO, that

forall t in T_transition,
  D_GPX4(t) OR D_FSP1(t),

using functional dependency measurements rather than protein abundance alone.
```

A direct experimental certificate would track the same lineage or matched metastatic population while measuring:

1. oxygen / niche state,
2. GPX4 abundance,
3. GPX4 functional dependency,
4. FSP1 abundance,
5. FSP1 functional dependency,
6. ferroptosis susceptibility,
7. metastatic survival during LN-to-blood transition.

## Residual object

```text
R_FERROPTOSIS_SWITCH :=
state-dependent surveillance switching between GPX4- and FSP1-dominant niches
```

This remains the first unresolved non-ApoE metastatic-state boundary in the current graph.

## Boundary

```text
BOUNDARY :=
not proved that GPX4/FSP1 surveillance provides continuous functional coverage
across lymph-node, reoxygenation, and hematogenous melanoma states
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
1. Retain SUFFICIENT_HANDOFF_INVARIANT as the exact transition requirement.
2. Do not substitute GPX4 protein recovery for functional GPX4 dependency.
3. Search for same-population reoxygenation experiments measuring GPX4- and
   FSP1-dependency simultaneously.
4. If none exists, retain R_FERROPTOSIS_SWITCH and return to the next independent
   residual state in the full escape graph.
```
