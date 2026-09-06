# Melanoma PerturbFate convergent dedifferentiation boundary — 2026-09-06

## Status

`CONDITIONAL / PUBLIC-DATA-BOUNDED MODEL`

This document records a bounded structural correction from the public PerturbFate melanoma dataset and its peer-reviewed 2026 Nature study. It is not clinical guidance, a treatment recommendation, or evidence of a cure.

## Question

Does the current melanoma interaction graph already cover the shared drug-resistant dedifferentiated state exposed by PerturbFate through the existing SOX10-low, RAC1-coupled, NCSC/FAK, and dynamic-MAPK objects, or is a broader unresolved state required?

## Source surface

PerturbFate was applied in BRAF(V600E) A375 melanoma cells with CRISPRi perturbations targeting more than 140 vemurafenib-resistance-associated genes. The public GEO series is:

```text
GSE291147
BioProject PRJNA1231621
```

The deposited surface includes single-cell RNA, nascent/pre-existing RNA, chromatin accessibility, sgRNA identities, and parallel bulk CRISPR-screen information. The study profiled more than 300,000 melanoma cells.

## Result

`RESULT := A GENERIC CONVERGENT DEDIFFERENTIATION ESCAPE IS NOT FULLY ABSORBED BY THE CURRENT SOX10- OR RAC1-SPECIFIC OBJECTS`

PerturbFate identified a shared vemurafenib-resistant undifferentiated state reached from many functionally unrelated perturbations.

The reported resistance-inducing classes include perturbations affecting:

```text
Hippo/YAP inhibitory genes
MAPK inhibitory genes
Mediator-complex genes
SAGA-complex genes
ubiquitin/proteasome regulators
```

The convergent resistant program contains cooperative TF activity involving:

```text
FOSL1 / AP-1
TEAD1 / Hippo-YAP
SMAD2/3/4
RREB1
KLF5
ZEB1
TCF4
```

Among 24 perturbations resistant to both vemurafenib-induced growth arrest and differentiation, the study found broad convergence on these regulatory programs. Activation of the regulons correlated with drug-resistant dedifferentiation, and the same TF programs were also reported in MAPKi-resistant patient-tumour data used for validation.

## Why this is not the existing SOX10-low object

The repository already retains:

```text
S_SOX10_LOW := SOX10-low / SOX10-deficient drug-tolerant MRD
```

with TAZ/TEAD and cIAP-associated vulnerability classes.

PerturbFate strengthens the importance of YAP/TEAD-associated dedifferentiation but broadens the entry surface beyond direct SOX10 loss. Resistance-producing perturbations included NF2, LATS2, PTPN14, TAOK1, NF1, DUSP6, MED12, MED19, MED15, MED24 and other functionally distinct regulators.

Some perturbations caused dedifferentiation under baseline conditions, some became strongly resistant under vemurafenib pressure, and distinct Mediator modules showed different condition dependence.

Therefore:

```text
DO_NOT_INFER :=
all PerturbFate convergent dedifferentiation
=> direct SOX10-low / SOX10-deficient state
```

SOX10 loss remains one supported route into the broader YAP/AP-1-associated dedifferentiated phenotype, but it is not the only demonstrated route.

## Why this is not the existing RAC1 object

The retained RAC1 certificate explicitly treats RAC1-driven partial YAP/TAZ reliance as part of a coupled RAC1/FAK/MAPK phenotype and states that not every YAP/TAZ-dependent melanoma state is FAK-covered.

PerturbFate reaches a related resistant dedifferentiation program through many perturbations not defined by RAC1 activation.

Therefore:

```text
DO_NOT_COLLAPSE :=
PerturbFate convergent dedifferentiation
into rac1_coupled_observed
```

## MAPK and YAP interaction

PerturbFate found that MAPK and Hippo/YAP signalling jointly shape dedifferentiation.

Perturbations of YAP inhibitory genes strongly promoted dedifferentiation, while perturbations of MAPK inhibitory genes such as NF1 and DUSP6 produced prominent proliferation/dedifferentiation under vemurafenib. The inferred resistant regulatory network showed simultaneous AP-1 and TEAD-family activity rather than a purely MAPK-only state.

Thus the existing dynamic-MAPK control cannot be assumed to close this broader state.

```text
DO_NOT_INFER :=
C_MAPK_DYNAMIC
=> control(convergent YAP/AP1 dedifferentiated escape)
```

## Functional convergence probe

The study experimentally perturbed candidate convergent TF modules during vemurafenib treatment.

Reported results include:

```text
SMAD3 inhibition alone: limited effect
RREB1 inhibition alone: limited effect
SMAD3 + RREB1: reduced global growth advantage
KLF5 inhibition alone: reduced resistance
RREB1 + SMAD3 + KLF5: largest reported reduction,
  mean relative growth advantage decreased about 3.1-fold
```

The authors explicitly caution that the combined inhibitor experiments can include off-target effects or nonspecific additive fitness costs. These data support functional convergence but do not establish a universal or clinically admissible control.

## VEGFC downstream branch

The study identified VEGFC as a YAP/core-Mediator-associated downstream factor activated in dedifferentiated states.

VEGFC knockdown reduced AXL expression and vemurafenib-resistant growth in multiple perturbed A375 contexts, including MED12, MED19, MED15 and MED24 perturbations and several YAP-inhibitor perturbations.

However, VEGFC knockdown did not significantly remove the growth advantage of every tested Mediator perturbation; CCNC and MED13 were explicit exceptions.

Therefore:

```text
DO_NOT_PROMOTE := VEGFC as a universal convergent-state control
```

## Structural consequence

The current graph is missing a generic scope object representing the convergent resistant dedifferentiated state outside direct SOX10-low and RAC1-defined entry routes.

Define the unresolved state conceptually as:

```text
perturbfate_convergent_dediff_gap :=
therapy-associated or genetically induced melanoma dedifferentiation in which
multiple unrelated resistance perturbations converge on cooperative YAP/TEAD,
AP-1/FOSL1 and associated TF programs, without evidence that the currently
active SOX10, RAC1/FAK/MAPK, or dynamic-MAPK controls universally eliminate
that convergent state
```

This is a scope/generality state, not a new treatment target.

## Why it must remain unresolved

The PerturbFate evidence is strong for A375 BRAF(V600E) under vemurafenib and includes multimodal single-cell mechanistic resolution plus functional perturbation.

It does not establish:

```text
1. universal closure across melanoma genotypes,
2. matched minimal-residual-disease elimination in vivo,
3. long-term relapse prevention after convergent-TF control,
4. survivor-lineage coverage across coexisting MRD states,
5. immune-competent or metastatic-niche closure,
6. that VEGFC or any one TF/control is sufficient across all entry perturbations.
```

Therefore no existing control should block this state in the executable graph.

## Missing object

```text
MISSING_OBJECT :=
a state-resolved functional certificate showing that a defined convergent-state
control eliminates or durably suppresses the YAP/TEAD + AP-1/FOSL1-associated
resistant dedifferentiated population across multiple independent entry routes,
with residual-survivor and long-term outgrowth/relapse readouts and without
redistribution into another retained melanoma escape state.
```

## Boundary

```text
BOUNDARY :=
PerturbFate establishes a broad, functionally convergent vemurafenib-resistant
melanoma dedifferentiation program beyond direct SOX10-loss and RAC1-defined
entry routes, but no universal cross-entry, cross-state or in-vivo closure is
established
```

## Evidence anchors

- Xu et al., Nature (2026), `Mapping convergent regulators of melanoma drug resistance by PerturbFate`.
  - https://doi.org/10.1038/s41586-026-10367-0
  - https://pubmed.ncbi.nlm.nih.gov/41986722/
- GEO GSE291147, `Mapping convergent regulators of melanoma drug resistance by PerturbFate`.
  - https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE291147

## Next bounded action

```text
NEXT_ACTIONS :=
1. Add perturbfate_convergent_dediff_gap as a reachable malignant scope state.
2. Keep it unblocked by all currently active controls.
3. Update the exact unresolved-state test inventory.
4. Re-run the canonical verifier immediately.
5. Do not add a named treatment control from this dataset.
```
