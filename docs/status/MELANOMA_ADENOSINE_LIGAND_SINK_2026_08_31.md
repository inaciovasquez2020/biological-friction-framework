# Melanoma extracellular-adenosine ligand-sink boundary — 2026-08-31

## Status

`CONDITIONAL / LITERATURE-BOUNDED MODEL`

This document records a bounded structural result for a melanoma residual-disease / immune-escape model. It is not clinical guidance, a treatment recommendation, or evidence of a cure.

## Question

After identifying CD73/adenosine-mediated immune protection as a residual escape state, must the model split membrane CD73, soluble CD73, exosomal CD73, and other adenosine-producing pathways into separate control targets?

## Result

`RESULT := A SOURCE-INDEPENDENT CONTROL ABSTRACTION EXISTS AT THE ADENOSINE-LIGAND LEVEL`

The different production compartments need not be separate at the first functional-control layer because they converge on the same extracellular ligand: adenosine.

```text
surface CD73 ---------\
soluble CD73 ----------\
exosomal CD73 ----------> extracellular adenosine -> A2A/A2B signaling -> immune escape
noncanonical production-/
```

Therefore the current graph can replace a source-specific CD73 target with the functional state constraint:

```text
C_ADENOSINE_LIGAND :=
reduce extracellular adenosine-mediated immunosuppression in the melanoma
microenvironment while preserving functional antitumor immune cells
```

This is an abstract control certificate, not a named drug or intervention.

## Why a single receptor is not sufficient

A2A is an important downstream receptor on activated T cells, but it is not the only relevant adenosine receptor in melanoma biology.

- In serum-derived melanoma exosome experiments, exosomal CD73 generated adenosine that suppressed activated T-cell IFN-gamma / granzyme-B function. The effect was reversed by either CD73 inhibition or selective A2A receptor antagonism.
- Separately, A2B signaling in murine melanoma promotes MDSC-associated immunosuppression and tumor growth; A2B blockade increased tumor-infiltrating CD8-positive cells and Th1-like cytokines in that model.
- Broader adenosine-pathway literature supports complementary A2A and A2B roles in immune and stromal compartments.

Therefore:

```text
RETIRE := A2A-only blockade as universal adenosine-escape closure
RETIRE := A2B-only blockade as universal adenosine-escape closure
```

Dual-receptor blockade remains a possible implementation class but is not promoted to a universal or clinically sufficient control.

## Why ligand-level depletion is structurally stronger

Direct extracellular adenosine depletion acts downstream of the identity of the producing compartment and downstream of CD73 itself.

Peer-reviewed preclinical work using PEGylated adenosine deaminase (PEG-ADA) provides proof-of-principle that enzymatic depletion of intratumoral adenosine can increase functional CD8-positive T-cell responses and improve anti-PD-1 activity in solid-tumor mouse models. That study also profiled CD73-positive MDSCs in B16-F10 melanoma, but the reported PEG-ADA therapeutic efficacy experiments were primarily performed in lung and breast tumor models rather than a matched melanoma source-coverage experiment.

Thus PEG-ADA is evidence that a ligand-sink mechanism is biologically executable; it is not evidence that melanoma adenosine escape is closed.

## Melanoma-specific ligand-sink audit

`MELANOMA_LIGAND_SINK_SEARCH := NO MATCHED PEER-REVIEWED CERTIFICATE IDENTIFIED`

A targeted search for melanoma experiments directly depleting extracellular adenosine did not identify a peer-reviewed study that simultaneously demonstrates:

```text
melanoma context
+ direct extracellular-adenosine depletion
+ measured intratumoral adenosine reduction
+ functional CD8/T-cell rescue
+ coverage across the relevant adenosine-source compartments
```

The 2023 PEG-ADA study includes melanoma in its CD73-positive MDSC characterization and supports the general adenosine mechanism, but its reported direct PEG-ADA tumor-control / intratumoral-adenosine experiments were centered on non-melanoma solid-tumor models.

Therefore the melanoma-specific ligand-sink certificate remains missing.

## 2025 B16-F10 IL-12 + ADA engineered-bacteria near-miss

A 2025 Blood / ASH conference poster abstract reports a localized adenosine-depletion platform that is materially closer to the missing melanoma object.

The study engineered non-pathogenic *E. coli* to display adenosine deaminase (ADA), IL-12, or a combined IL-12+ADA construct. The abstract reports:

```text
ADA enzymatic activity -> extracellular adenosine converted to inosine in vitro
ADA-containing bacteria -> immune-function rescue in adenosine-rich AML assays
intratumoral IL-12+ADA bacteria -> complete regression in a B16-F10 melanoma arm
```

This is important melanoma-specific evidence that a localized ADA-containing platform can coexist with strong B16-F10 tumor control.

However, the available publication is a conference-poster abstract whose experimental center of gravity is AML. The B16-F10 result does not report the matched measurements required to discharge this repository boundary.

In particular, the abstract does not establish in the same melanoma experiment:

```text
1. measured intratumoral extracellular-adenosine reduction,
2. melanoma-specific CD8/T-cell functional rescue attributable to ADA,
3. decomposition of ADA versus IL-12 versus combination contribution in the
   reported B16-F10 regression result,
4. coverage of membrane, soluble/exosomal, and noncanonical adenosine sources,
5. absence of a new dissemination or host-safety failure.
```

The abstract reports ADA-alone and combination comparisons in the AML in-vivo model, but the stated B16-F10 melanoma outcome is specifically the intratumoral IL-12+ADA combination. Therefore the melanoma result cannot be promoted to an ADA-only ligand-sink certificate.

A targeted search through 2026 did not identify a full peer-reviewed melanoma follow-up resolving those missing measurements.

Thus:

```text
NEAR_MISS :=
B16-F10 + localized IL-12/ADA bacterial platform + strong tumor-control outcome

DO_NOT_INFER :=
NEAR_MISS => melanoma-specific source-independent ligand-sink closure

MELANOMA_LIGAND_SINK_SEARCH := STILL OPEN / UNRESOLVED
```

This near-miss narrows the experimental missing object: localized ADA delivery in melanoma is no longer merely hypothetical, but matched mechanistic attribution and source-independent immune restoration remain unproved.

## Source coverage

At the abstraction level:

```text
if source_i -> extracellular adenosine
and C_ADENOSINE_LIGAND removes / functionally neutralizes extracellular adenosine,
then source_i is intercepted downstream of source identity.
```

This covers, in principle:

```text
S_surface_CD73
S_soluble_CD73
S_exosomal_CD73
S_noncanonical_adenosine
```

without requiring one molecular intervention per source.

However, this statement is biochemical/graph-theoretic. It does not establish sufficient spatial penetration, kinetics, host safety, or durable melanoma control.

## Immune-fitness boundary

The existing evidence does not support the concern that all adenosine depletion necessarily suppresses effector CD8 cells. In preclinical tumor models, adenosine depletion increased IFN-gamma- and TNF-alpha-producing CD8-positive T-cell frequencies while reducing intratumoral adenosine.

But the opposite safety claim is also not established:

```text
DO_NOT_INFER :=
systemic / chronic extracellular adenosine depletion is safe or selectively tumor-restricted
```

Adenosine is a normal physiological signaling molecule, and a useful melanoma control must distinguish tumor-microenvironmental immunosuppression from systemic purinergic homeostasis.

## Weakest missing object

```text
MISSING_OBJECT :=
a melanoma-specific matched-context certificate demonstrating that one
spatially admissible extracellular-adenosine control:

1. lowers intratumoral extracellular adenosine,
2. restores or preserves functional antitumor CD8/T-cell activity,
3. suppresses both A2A-dominant lymphoid and A2B-associated myeloid escape,
4. remains effective when adenosine is supplied by membrane, soluble/exosomal,
   and noncanonical production routes,
5. separates the ligand-sink contribution from co-delivered immune stimulants,
6. does not create an uncovered dissemination or host-safety failure.
```

Until that object exists, the correct graph node is the functional ligand-level constraint rather than a particular receptor, enzyme inhibitor, antibody, drug, or combination platform.

## Boundary

```text
BOUNDARY :=
not proved that a single source-independent extracellular-adenosine control
closes melanoma immune escape safely and durably
```

The 2025 B16-F10 IL-12+ADA abstract strengthens biological plausibility but does not change that boundary.

## Evidence anchors

- Exosomal CD73 from serum of patients with melanoma suppresses lymphocyte functions and is associated with anti-PD-1 resistance; A2A antagonism reversed the exosome/AMP-mediated T-cell suppression in vitro.
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC8915288/
  - https://pubmed.ncbi.nlm.nih.gov/35273100/
- A2B receptor blockade reduced MDSC-associated immune suppression and delayed melanoma growth in a murine melanoma model.
  - https://pubmed.ncbi.nlm.nih.gov/24403862/
- Monocytic MDSCs exhibit superior immune suppression via adenosine; PEG-ADA depleted intratumoral adenosine, increased functional CD8-positive T-cell responses, and enhanced anti-PD-1 activity in preclinical solid-tumor models; the study also included B16-F10 melanoma in its CD73/MDSC analyses.
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC10313166/
  - https://pubmed.ncbi.nlm.nih.gov/37390211/
- Sendker et al., Blood 2025 supplement / ASH poster 5912, `Dual-function engineered bacteria remodel AML tumor microenvironment via IL-12 delivery and adenosine depletion to sustain NK cell immunity`; includes the reported intratumoral IL-12+ADA B16-F10 melanoma result.
  - https://www.sciencedirect.com/science/article/pii/S0006497125086598
  - https://doi.org/10.1182/blood-2025-5912
- General adenosine-pathway review documenting multiple production routes and complementary A2A/A2B signaling.
  - https://www.nature.com/articles/s41571-020-0382-2
- 2025 pharmacology review of A2A/A2B adenosine signaling and dual-receptor strategies.
  - https://pubmed.ncbi.nlm.nih.gov/41101027/

## Next bounded action

```text
NEXT_ACTIONS :=
1. Retain adenosine_ligand_sink_gap as reachable in the executable certificate.
2. Search specifically for melanoma ADA-only or mechanistically decomposed
   ligand-depletion studies measuring intratumoral adenosine plus functional
   antitumor immune rescue.
3. Retire the gap only if that matched mechanistic certificate appears.
```
