# Melanoma CD73/adenosine residual escape — 2026-08-31

## Status

`CONDITIONAL / LITERATURE-BOUNDED MODEL`

This document records a bounded structural result for a melanoma residual-disease/resistance graph. It is not clinical guidance, a treatment recommendation, or evidence of a cure.

## Question

After representing abstract controls for MAPK reactivation, PI3K/AKT survival, FAK-dependent states, and the SOX10-low MRD state, what is the first retained non-ApoE escape route that remains uncovered?

## Result

`RESULT := CD73/ADENOSINE-MEDIATED IMMUNE PROTECTION REMAINS REACHABLE`

The retained route is:

```text
stress / inflammatory or resistant melanoma context
  -> CD73 / NT5E activity
  -> extracellular adenosine
  -> adenosine-receptor signaling on immune cells
  -> reduced effector T-cell function
  -> malignant-state survival / immune escape
```

This route is not closed merely by MAPK-pathway control.

## Why MAPK coverage is insufficient

Published melanoma studies show context-dependent CD73 behavior:

- In BRAF-mutant melanoma models that are sensitive to BRAF/MEK targeted therapy, BRAF/MEK inhibition can strongly reduce tumor-cell CD73 expression.
- However, CD73 is induced during melanoma phenotype switching and has been observed in relapse/progression under T-cell immunotherapy and immune-checkpoint blockade.
- Soluble CD73 can be released by nutritionally stressed melanoma cells and remains enzymatically capable of generating adenosine.
- Exosomal CD73 from patients with melanoma can generate adenosine and suppress activated T-cell IFN-gamma and granzyme-B responses; this suppression was reversible experimentally by blocking CD73 enzymatic activity or A2A-receptor signaling.
- Early on-treatment exosomal CD73 was elevated in anti-PD-1 nonresponders in a retrospective melanoma cohort.

Therefore:

```text
MAPK_CONTROL => CD73_ESCAPE_CLOSED
```

is not established.

## Structural repair

Do not encode the route as one fixed molecular drug target. The escape can arise through tumor-cell surface CD73, soluble/shedded CD73, exosomal CD73, and microenvironmental adenosine production.

Use the functional abstraction:

```text
S_ADENOSINE := extracellular adenosine-mediated immune-protection state

C_ADENOSINE := control sufficient to prevent S_ADENOSINE from suppressing
               antitumor effector function while preserving required host
               immune-cell fitness
```

This deliberately does not select CD73, CD39, A2A receptor, or another node as a universal intervention.

## Safety/sign boundary

Adenosine signaling and redox/metabolic pathways also participate in normal immune-cell physiology. Therefore a graph-level hit on the adenosine route is not automatically a safe or monotone biological intervention.

The model requires:

```text
ADMISSIBLE(C_ADENOSINE) :=
  decreases melanoma adenosine-mediated immune escape
  AND does not materially impair functional antitumor CD8/T-cell fitness
```

No clinical safety or efficacy closure is claimed here.

## Why this is a distinct residual from SOX10-low control

SOX10-low/mesenchymal switching and CD73 can intersect, but the adenosine route is not reducible to the SOX10-low TAZ/TEAD or cIAP2 control abstractions. CD73 can be dynamically regulated by oncogenic signaling, inflammatory cytokines, nutrient stress, and extracellular-vesicle release.

Thus abstractly covering the SOX10-low state does not prove elimination of extracellular adenosine-mediated immune suppression.

## Weakest missing object

```text
MISSING_OBJECT :=
a state-level control certificate showing that extracellular adenosine-mediated
immune protection is durably suppressed across tumor-cell, soluble/exosomal,
and relevant microenvironmental sources while preserving antitumor immune-cell
function.
```

## Evidence anchors

- Young et al., Cancer Research (2017): BRAF/MEK inhibition reduced CD73 expression in CD73-positive BRAF-mutant melanoma, while adenosine-pathway intervention combined with targeted therapy reduced tumor initiation/metastatic formation in mouse melanoma models.
  - https://pubmed.ncbi.nlm.nih.gov/28652244/
- Reinhardt et al., Cancer Research (2017): CD73 induction is linked to melanoma phenotype switching; inflammatory/MAPK signaling induces CD73, and CD73 was increased in relapse/progression during T-cell immunotherapy/immune-checkpoint therapy.
  - https://aacrjournals.org/cancerres/article/77/17/4697/622705/
- Turiello et al., Journal for ImmunoTherapy of Cancer (2022): melanoma-patient exosomal CD73 is enzymatically active, suppresses T-cell IFN-gamma/granzyme-B responses through adenosine, and early treatment elevation was associated with anti-PD-1 nonresponse.
  - https://pubmed.ncbi.nlm.nih.gov/35273100/
- 2024 melanoma study: nutritional stress promotes soluble CD73 release from melanoma cells; the released enzyme remains capable of generating extracellular adenosine.
  - https://pubmed.ncbi.nlm.nih.gov/38941889/
- 2026 review: summarizes tumor, soluble/exosomal, environmental, and immune-context regulation of the CD73-adenosine axis in melanoma.
  - https://pubmed.ncbi.nlm.nih.gov/42597984/

## Boundary

```text
BOUNDARY :=
not proved that the current control set closes CD73/adenosine-mediated immune escape
```

## Next bounded action

```text
NEXT_ACTIONS :=
1. Test whether a single functional adenosine-control abstraction can safely
   cover tumor-cell, soluble/exosomal, and microenvironmental sources.
2. If not, split S_ADENOSINE into source-specific residual states.
3. Then return to the full graph and identify the next survivor after
   C_ADENOSINE is represented abstractly.
```
