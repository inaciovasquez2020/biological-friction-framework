# Melanoma ERK-pulse dynamic MAPK boundary — 2026-08-31

## Status

`CONDITIONAL / LITERATURE-BOUNDED MODEL`

This document records a bounded structural correction to the melanoma residual-disease / persister graph. It is not clinical guidance, a treatment recommendation, or evidence of a cure.

## Question

Is the existing abstract MAPK/ERK control adequate if it is interpreted only as average or snapshot suppression of ERK activity?

## Result

`RESULT := NO — STATIC MAPK CONTROL IS TOO WEAK`

In BRAF-V600E melanoma under RAF/MEK inhibition, live-cell studies show that average ERK activity can remain strongly suppressed while a subset of drug-adapted cells experiences brief receptor-driven ERK reactivation pulses that support survival and division.

The observed route is:

```text
RAF/MEK inhibition
  -> average ERK suppression
  -> receptor / growth-factor rewiring
  -> Ras-GTP + RAF-dimer signaling
  -> brief ERK pulse
  -> escape from cell-cycle arrest / persister division
  -> resistant-clone expansion
```

Gerosa et al. measured pulses that rose to amplitudes similar to untreated cells and returned to baseline over roughly 60–90 minutes. In the reported A375 live-cell series, only a minority of cells were pERK-high at any snapshot, yet time-lapse imaging revealed repeated pulse events across the drug-adapted population.

Therefore:

```text
DO_NOT_INFER :=
low mean ERK activity
=> no functionally important ERK signaling
```

and:

```text
DO_NOT_INFER :=
a negative fixed-time pERK snapshot
=> continuous MAPK closure
```

## Independent replication at the signaling-dynamics level

Kim et al. (Cell Reports, 2023) independently showed that the magnitude and duration of receptor-tyrosine-kinase activation determine ERK reactivation and persister development under combined BRAF/MEK inhibition.

Only a subset of cells achieved effective RTK/ERK reactivation despite shared external conditions; those initially rare persisters could later become major resistant clones.

This supports the structural conclusion that **signaling kinetics and heterogeneity**, not only pathway identity, must be represented.

## Repair to the existing control

Retire the purely static interpretation:

```text
C_MAPK_STATIC := ERK is low at one time point or low on average
```

Replace it with a functional time-resolved constraint:

```text
C_MAPK_DYNAMIC :=
no receptor-driven ERK activation event has an amplitude-duration pattern
sufficient to sustain melanoma persister survival, cell-cycle escape,
or resistant-clone expansion under continued MAPK-pathway pressure
```

This is a model requirement, not a prescription to inhibit a particular receptor, SHP2, RAF dimer, or other molecule.

## Why upstream-node enumeration is insufficient

The pulse-generating system can use autocrine/paracrine growth factors and heterogeneous RTK activation.

A fixed list such as:

```text
HGF/MET
EGFR
AXL
other RTKs
```

cannot by itself establish closure unless all functionally relevant pulse-producing inputs are covered.

The dynamic invariant is therefore downstream and functional:

```text
PULSE_ESCAPE :=
exists t, interval I around t:
ERK_activity(I) supports persister survival/division

C_MAPK_DYNAMIC requires:
NOT PULSE_ESCAPE
```

## Relationship to the existing HGF/MET / PI3K-AKT boundary

The previously retained HGF/MET result concerns a parallel PI3K/AKT survival arm.

The present result concerns a different failure mode:

```text
HGF/MET-PI3K residual := parallel pathway survival
ERK-pulse residual     := time-local MAPK reactivation despite low average ERK
```

They must not be collapsed.

## Relationship to adaptive mutability

The newly retained translation/adaptive-mutability control limits one route by which drug-tolerant cells evolve genetically.

The ERK-pulse route instead permits intermittent survival and division of the reservoir itself.

```text
C_TRANSLATION_PERSIST controls mutation-generation pressure
C_MAPK_DYNAMIC controls time-local proliferative/survival escape
```

Both are required in the current abstraction.

## Weakest missing quantitative object

The literature demonstrates functionally important ERK pulses, but the model does not yet possess a universal amplitude-duration threshold separating harmless fluctuations from survival/division-supporting events.

```text
MISSING_OBJECT :=
a melanoma-specific pulse-response certificate giving a validated functional
boundary in ERK amplitude x duration x frequency space such that:

below boundary -> no persister survival/division advantage
above boundary -> quantified persister survival/division probability

with validation across relevant melanoma states and microenvironmental inputs
```

Until that object exists, `C_MAPK_DYNAMIC` remains qualitative/functional rather than a fully numerical certificate.

## Boundary

```text
BOUNDARY :=
MAPK/ERK control is not certified by snapshot or mean suppression alone;
continuous closure requires exclusion of functionally sufficient receptor-driven
ERK pulse escape
```

## Evidence anchors

- Gerosa et al., Cell Systems (2020), `Receptor-Driven ERK Pulses Reconfigure MAPK Signaling and Enable Persistence of Drug-Adapted BRAF-Mutant Melanoma Cells`.
  - https://pubmed.ncbi.nlm.nih.gov/33113355/
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC8009031/
  - https://doi.org/10.1016/j.cels.2020.10.002
- Kim et al., Cell Reports (2023), `Kinetics of RTK activation determine ERK reactivation and resistance to dual BRAF/MEK inhibition in melanoma`.
  - https://pubmed.ncbi.nlm.nih.gov/37252843/
  - https://doi.org/10.1016/j.celrep.2023.112570

## Next bounded action

```text
NEXT_ACTIONS :=
1. Replace static C_MAPK with C_MAPK_DYNAMIC in future route-cover reasoning.
2. Do not count a pathway as closed from mean/snapshot pERK suppression alone.
3. Search for a quantitative ERK pulse amplitude-duration-frequency threshold
   tied directly to melanoma persister survival/division.
4. If no transferable threshold exists, retain C_MAPK_DYNAMIC as a functional
   non-numerical boundary and move to the next independent escape route.
```
