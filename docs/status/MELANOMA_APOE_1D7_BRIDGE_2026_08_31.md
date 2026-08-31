# Melanoma ApoE 1D7 / Blocking-Antibody Bridge — 2026-08-31

## Status

`CONDITIONAL / LITERATURE-BOUNDED MODEL`

This document records a bounded mechanistic narrowing in a melanoma residual-disease model. It is not clinical guidance, a treatment recommendation, or evidence of a cure.

## Question

Can the previously unresolved ApoE signed tradeoff be narrowed by requiring extracellular ApoE-blocking perturbations across ferroptosis, immune function, invasion, and endothelial recruitment?

## Result

`RESULT := BLOCKING-ANTIBODY BRIDGE EXTENDED TO THE IMMUNE EDGE`

Independent melanoma studies support all four outcome classes under extracellular ApoE-blocking perturbations, but not in one matched experiment and not with one proven-identical antibody reagent.

### 1. Ferroptosis edge

In MITF-high / MITF-low melanoma coculture and conditioned-media experiments, ApoE-neutralizing antibody `1D7` restored ferroptosis susceptibility of invasive melanoma cells protected by secreted ApoE.

### 2. Invasion / endothelial-recruitment edges

In metastatic melanoma models, extracellular ApoE neutralization with `1D7` increased melanoma-cell invasion and endothelial recruitment.

### 3. Immune edge

In B16-F10 melanoma/splenocyte coculture, a reported anti-APOE blocking antibody increased IFNγ production approximately threefold in the immunogenic tumor-cell/splenocyte reaction.

The same study independently showed that tumor-secreted ApoE suppresses T-cell function using ApoE knockout/conditioned-media experiments and implicated LRP8 in the suppressive pathway.

Therefore the previous statement that the immune edge lacked an extracellular ApoE-blocking-antibody experiment is retired.

## Corrected signed perturbation map

```text
extracellular ApoE blocking
 ├─ 1D7 -> increases ferroptosis susceptibility      favorable for killing
 ├─ 1D7 -> increases melanoma invasion              unfavorable for dissemination
 ├─ 1D7 -> increases endothelial recruitment        unfavorable for dissemination
 └─ anti-APOE blocking antibody -> increases IFNγ    favorable for immune activation
```

This is stronger than the prior three-edge bridge.

However:

```text
DO_NOT_INFER :=
anti-APOE blocking antibody in the B16 immune study = 1D7
```

## Public reagent-identity audit

`REAGENT_IDENTITY_AUDIT := NOT RESOLVED FROM PUBLIC PAPER/PATENT`

The 2022 B16-F10 paper describes the immune-assay reagent only as a `human anti-APOE antibody` / `anti-APOE blocking antibody` and gives assay concentrations. The paper does not provide a clone name, vendor, catalog number, isotype, epitope, sequence, or other identifier sufficient to reproduce the exact antibody identity.

The related patent `WO2023086777A1`, which reproduces the same B16/splenocyte anti-APOE blocking-antibody experiment, likewise does not identify a clone, vendor, catalog number, or epitope for the experimental antibody and contains no `1D7` identifier.

Therefore:

```text
UNRESOLVED_REAGENT_METADATA :=
clone + vendor + catalog + isotype + epitope + sequence/species-reactivity metadata
```

The functional immune result remains a reported blocking-antibody result, but the public record inspected here does not establish molecular identity or equivalence to `1D7`.

This distinction matters because `1D7` is a historically characterized monoclonal antibody whose epitope lies within the ApoE receptor-binding region, approximately residues 139–169 and most likely near 140–150. Historical work also reported reagent-specific complications in some `1D7` IgG preparations.

## Matched-context closure remains failed

`MATCHED_CONTEXT_CLOSURE := FAILED`

No single melanoma experiment identified in this audit jointly measures, under one validated extracellular ApoE-blocking perturbation:

1. ferroptotic melanoma death,
2. functional antitumor CD8/T-cell activity,
3. melanoma invasion/metastatic behavior,
4. endothelial recruitment/angiogenesis.

The studies differ in melanoma model, immune context, endpoint, timing, and antibody/reagent characterization. Their effect directions therefore cannot be collapsed into a proved scalar net-benefit sign.

## Weakest missing object

```text
MISSING_OBJECT :=
a single melanoma experimental context using one molecularly identified,
validated extracellular ApoE-blocking perturbation that jointly measures:

1. ferroptotic melanoma death,
2. functional antitumor CD8/T-cell activity,
3. melanoma invasion/metastatic behavior,
4. endothelial recruitment/angiogenesis,

with controls sufficient to establish on-target ApoE blockade.
```

The reagent-level boundary is now precise:

```text
BOUNDARY_REAGENT :=
¬ molecular identity/equivalence(B16 immune antibody, 1D7) established
from the public article or related patent
```

The biological boundary remains:

```text
BOUNDARY :=
¬ net-antitumor sign(extracellular ApoE blockade) established
```

ApoE remains a signed environmental coupling, not an admissible monotone treatment/control node in the current no-escape model.

## Evidence anchors

- Secreted ApoE rewires melanoma cell-state vulnerability to ferroptosis; `1D7` restores ferroptosis sensitivity in coculture/conditioned-media experiments.
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC11808924/
  - https://pubmed.ncbi.nlm.nih.gov/39413195/
- Pencheva et al., Cell (2012); extracellular ApoE neutralization with `1D7` increases melanoma invasion and endothelial recruitment.
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC3753115/
  - https://pubmed.ncbi.nlm.nih.gov/23142051/
- Tumor ApoE immune checkpoint study; anti-APOE blocking antibody increases IFNγ in immunogenic B16/splenocyte coculture, while the public methods do not molecularly identify that antibody.
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC9626815/
  - https://pubmed.ncbi.nlm.nih.gov/36341364/
- Related patent reproducing the B16 anti-APOE blocking-antibody experiment without resolving the experimental antibody clone/identity.
  - https://patents.google.com/patent/WO2023086777A1/en
- Ostendorf et al., Nature Medicine (2020); APOE2/APOE4 knock-in melanoma models jointly connect genotype to progression, immunity, invasion and endothelial recruitment, but not ferroptosis.
  - https://pubmed.ncbi.nlm.nih.gov/32451497/
- Historical `1D7` receptor-binding and reagent literature.
  - https://pubmed.ncbi.nlm.nih.gov/6313653/
  - https://pubmed.ncbi.nlm.nih.gov/2754339/

## Next bounded action

```text
NEXT_ACTIONS :=
1. Retire public clone-identification as closed-by-literature unless new primary
   reagent metadata appears; do not assume the B16 antibody is 1D7.
2. Search for a melanoma model measuring both immune activation and
   invasion/metastatic behavior under the same molecularly identified
   extracellular ApoE blockade.
3. Do not rerun the no-escape optimizer as though the ApoE net sign were closed.
```
