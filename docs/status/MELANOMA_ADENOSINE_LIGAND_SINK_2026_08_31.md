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
5. does not create an uncovered dissemination or host-safety failure.
```

Until that object exists, the correct graph node is the functional ligand-level constraint rather than a particular receptor, enzyme inhibitor, antibody, or drug.

## Boundary

```text
BOUNDARY :=
not proved that a single source-independent extracellular-adenosine control
closes melanoma immune escape safely and durably
```

## Evidence anchors

- Exosomal CD73 from serum of patients with melanoma suppresses lymphocyte functions and is associated with anti-PD-1 resistance; A2A antagonism reversed the exosome/AMP-mediated T-cell suppression in vitro.
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC8915288/
  - https://pubmed.ncbi.nlm.nih.gov/35273100/
- A2B receptor blockade reduced MDSC-associated immune suppression and delayed melanoma growth in a murine melanoma model.
  - https://pubmed.ncbi.nlm.nih.gov/24403862/
- Monocytic MDSCs exhibit superior immune suppression via adenosine; PEG-ADA depleted intratumoral adenosine, increased functional CD8-positive T-cell responses, and enhanced anti-PD-1 activity in preclinical solid-tumor models; the study also included B16-F10 melanoma in its CD73/MDSC analyses.
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC10313166/
  - https://pubmed.ncbi.nlm.nih.gov/37390211/
- General adenosine-pathway review documenting multiple production routes and complementary A2A/A2B signaling.
  - https://www.nature.com/articles/s41571-020-0382-2
- 2025 pharmacology review of A2A/A2B adenosine signaling and dual-receptor strategies.
  - https://pubmed.ncbi.nlm.nih.gov/41101027/

## Next bounded action

```text
NEXT_ACTIONS :=
1. Search specifically for melanoma experiments that directly deplete
   extracellular adenosine rather than only inhibiting CD73 or one receptor.
2. Require simultaneous measurement of intratumoral adenosine and functional
   CD8/T-cell output.
3. If no melanoma-specific ligand-sink experiment exists, retain
   C_ADENOSINE_LIGAND as an abstract missing control and return to the full
   residual graph for the next uncovered non-ApoE state.
```
