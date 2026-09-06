# Melanoma post-GPX4 persister FSP1 escape boundary — 2026-09-06

## Status

`CONDITIONAL / PUBLIC-DATA-BOUNDED MODEL`

This document records a bounded evidence refinement for the melanoma ferroptosis-surveillance branch. It is not clinical guidance, a treatment recommendation, or evidence of a cure.

## Question

Does independent 2026 persister-cell evidence reduce the uncertainty behind `ferroptosis_handoff_gap`, particularly the possibility that melanoma persisters surviving GPX4-axis pressure can remain protected by FSP1 or by an oxidative-state adaptation?

## Source

Higuchi et al., Science Advances (2026), `FSP1 and histone deacetylases suppress cancer persister cell ferroptosis`.

Primary identifiers:

```text
DOI := 10.1126/sciadv.aea8771
PMID := 41481741
GEO := GSE303411
```

## Result

```text
RESULT :=
INDEPENDENT MELANOMA FUNCTIONAL EVIDENCE SUPPORTS FSP1 AS A RESIDUAL
SURVIVAL AXIS DURING GPX4 CHALLENGE, BUT DOES NOT CERTIFY THE
LN-HYPOXIA -> REOXYGENATION -> BLOOD HANDOFF
```

The study examined targeted-therapy persister cells in multiple cancer models, including A375 melanoma persisters generated under dabrafenib plus trametinib.

In A375 persister cells, the study functionally tested the GPX4 inhibitor RSL3 together with the FSP1 inhibitor iFSP1. The paper's central result is that persister cells depend on residual FSP1 to survive GPX4 inhibition, despite FSP1 being downregulated relative to parental cells.

The same study also tested A375 persisters with panobinostat and RSL3 and showed that increasing oxidative pressure with HDAC inhibition can sensitize persister cells to GPX4 inhibition.

Therefore, the following narrower objection can be retired:

```text
RETIRE_SUBGAP :=
there is no independent melanoma evidence that residual FSP1 can remain
functionally load-bearing when targeted-therapy persisters are challenged
through the GPX4 axis
```

This is a real evidence improvement because it makes the GPX4/FSP1 alternative-surveillance model less hypothetical in melanoma persisters.

## Important single-cell boundary

The public GEO series `GSE303411` is not a melanoma single-cell survivor map.

Its deposited 10x single-cell experiment uses PC9 lung-cancer cells:

```text
PC9_parental
PC9_persister
PC9_parental_RSL3
PC9_persister_RSL3
PC9_parental_panobinostat
PC9_persister_panobinostat
```

The A375 melanoma results are functional treatment experiments, but A375 is not the cell line used for the deposited `GSE303411` single-cell RNA-seq series.

Therefore:

```text
DO_NOT_INFER :=
GSE303411 single-cell survivor composition
=> melanoma post-GPX4 survivor-state composition
```

and:

```text
DO_NOT_INFER :=
A375 FSP1 dependence under GPX4 challenge
=> continuous FSP1 dependence during LN-to-blood metastatic transition
```

## What this narrows

The prior niche-switch boundary established experimentally distinct endpoint-like ferroptosis dependencies:

```text
LN_HYPOXIC_ENDPOINT -> D_FSP1
HEMATO_ENDPOINT     -> D_GPX4
```

The 2026 persister study adds a separate melanoma context in which GPX4 pressure does not imply that FSP1 becomes irrelevant:

```text
MAPKi_PERSISTER + GPX4_CHALLENGE
  -> residual FSP1 can remain functionally load-bearing
```

This supports the biological plausibility of overlapping or sequential GPX4/FSP1 surveillance states.

It does not establish their timing during metastatic niche transition.

## Oxidative-state adaptation

The study also reports that persister cells surviving GPX4 inhibition can reduce oxidative phosphorylation, thereby reducing a source of mitochondrial reactive oxygen species required for ferroptotic killing.

This creates an additional caution for the existing handoff model:

```text
GPX4_AXIS_PRESSURE
  does not imply
fixed oxidative load
```

A functional handoff certificate must therefore measure ferroptosis susceptibility or relevant oxidative state directly rather than assuming that GPX4/FSP1 abundance alone fixes the death pressure.

## Handoff status

Retain the previously defined sufficient invariant:

```text
SUFFICIENT_HANDOFF_INVARIANT :=
forall t in T_transition,
  D_GPX4(t) OR D_FSP1(t)
```

The new evidence does not measure the same melanoma lineage across:

```text
S_LN_HYPOXIC
  -> reoxygenation
  -> S_HEMATO
```

and does not provide paired functional GPX4 and FSP1 dependencies at matched transition times.

Therefore:

```text
HANDOFF_INVARIANT_STATUS := UNPROVED
```

## Revised weakest missing object

The weakest remaining object is now more precise:

```text
MISSING_OBJECT :=
a matched melanoma transition experiment demonstrating, across
S_LN_HYPOXIC -> reoxygenation -> S_HEMATO, that

forall t in T_transition,
  D_GPX4(t) OR D_FSP1(t),

while also measuring ferroptosis susceptibility / oxidative state strongly
enough to rule out survival through a low-ROS post-GPX4 persister program.
```

A sufficient direct certificate would track the same lineage or matched metastatic population while measuring:

1. oxygen / niche state,
2. GPX4 functional dependency,
3. FSP1 functional dependency,
4. ferroptosis susceptibility,
5. oxidative-state change after GPX4-axis pressure,
6. metastatic survival through reoxygenation / hematogenous transit.

## Executable consequence

```text
GRAPH_STATE := ferroptosis_handoff_gap
GRAPH_CHANGE := none
CONTROL_CHANGE := none
UNRESOLVED_STATUS := retained
```

This evidence narrows the rationale for the unresolved state but does not justify removing it or adding a universal ferroptosis control.

## Boundary

```text
BOUNDARY :=
independent A375 melanoma evidence establishes residual FSP1 as a functional
survival axis during GPX4 challenge in targeted-therapy persisters, but no
matched melanoma single-cell/lineage experiment establishes continuous
GPX4/FSP1 functional coverage during LN hypoxia -> reoxygenation -> blood,
and GSE303411 single-cell sequencing is PC9 rather than melanoma
```

## Evidence anchors

- Higuchi et al., Science Advances (2026), `FSP1 and histone deacetylases suppress cancer persister cell ferroptosis`.
  - DOI: `10.1126/sciadv.aea8771`
  - PMID: `41481741`
  - GEO: `GSE303411`
- Existing niche-transition boundary:
  - `docs/status/MELANOMA_FERROPTOSIS_NICHE_SWITCH_2026_08_31.md`

## Next bounded action

```text
NEXT_ACTIONS :=
1. Retain ferroptosis_handoff_gap.
2. Do not treat GSE303411 as melanoma single-cell evidence.
3. Search specifically for melanoma post-GPX4 or post-FSP1 intervention
   single-cell / lineage-resolved survivor-state data.
4. Prefer experiments that include oxygen or metastatic-niche transition.
```
