# Melanoma ApoE 1D7 Bridge — 2026-08-31

## Status

`CONDITIONAL / LITERATURE-BOUNDED MODEL`

This document records a bounded mechanistic narrowing in a melanoma residual-disease model. It is not clinical guidance, a treatment recommendation, or evidence of a cure.

## Question

Can the previously unresolved ApoE signed tradeoff be narrowed by requiring a common perturbation across ferroptosis, immune function, invasion, and endothelial recruitment?

## Result

`RESULT := PARTIAL MATCHED-PERTURBATION BRIDGE FOUND`

Two independent melanoma studies use the same nominal ApoE-neutralizing monoclonal antibody, `1D7`, which targets the ApoE receptor-binding region:

1. **Ferroptosis edge**
   - In MITF-high / MITF-low melanoma coculture and conditioned-media experiments, ApoE-neutralizing antibody `1D7` restored ferroptosis susceptibility of the invasive melanoma population that had been protected by secreted ApoE.

2. **Invasion / endothelial-recruitment edges**
   - In metastatic melanoma models, extracellular ApoE neutralization with `1D7` increased melanoma-cell invasion and endothelial recruitment.

Therefore three previously separate signed outcomes share a common nominal perturbation class:

```text
1D7 / extracellular ApoE neutralization
 ├─ increases ferroptosis susceptibility          favorable for killing
 ├─ increases melanoma invasion                  unfavorable for dissemination
 └─ increases endothelial recruitment            unfavorable for dissemination
```

This is stronger than combining studies that manipulate ApoE by unrelated methods, but it is not a matched-context experiment: the studies use different melanoma models, endpoints, schedules, and experimental contexts.

## Immune edge remains unmatched

The melanoma T-cell study supports:

```text
tumor ApoE -> suppresses T-cell activation / antitumor immunity
```

but establishes that edge using ApoE knockout and ApoE-secreting conditioned media rather than `1D7` neutralization.

No melanoma study identified in this audit directly measures functional antitumor T-cell activity under the same `1D7` ApoE-neutralization perturbation while also measuring ferroptosis, invasion, and endothelial recruitment.

## Supporting same-model evidence

A separate human APOE2-versus-APOE4 knock-in melanoma study jointly demonstrates that APOE genotype can affect:

- melanoma progression/metastasis,
- antitumor immune activation,
- melanoma-cell invasion,
- endothelial recruitment / tumor vascular density.

However, that study does not measure ferroptosis and does not represent ApoE reduction/neutralization. It therefore narrows biological coupling but does not close the net sign of ApoE blockade.

## Reagent boundary

`1D7` is an old monoclonal antibody directed at the ApoE receptor-binding region. Historical biochemical work reported that some `1D7` IgG preparations could contain mouse ApoE-associated activity capable of perturbing LDL-receptor binding independently of simple ApoE immunoreactivity.

Therefore:

```text
DO_NOT_INFER :=
identical biological perturbation merely from the shared antibody name across studies
```

A future matched experiment must validate the actual reagent preparation and on-target ApoE neutralization in its assay context.

## Weakest missing object

```text
MISSING_OBJECT :=
a single melanoma experimental context using a validated extracellular ApoE
neutralization perturbation that jointly measures:

1. ferroptotic melanoma death,
2. functional antitumor CD8/T-cell activity,
3. melanoma invasion/metastatic behavior,
4. endothelial recruitment/angiogenesis,

with reagent controls sufficient to establish on-target ApoE neutralization.
```

The narrowest unmeasured edge under the common nominal `1D7` perturbation is currently:

```text
1D7 ApoE neutralization -> functional antitumor T-cell response
```

## Boundary

```text
BOUNDARY :=
¬ net-antitumor sign(extracellular ApoE neutralization) established
```

The prior decision remains unchanged: ApoE is a signed environmental coupling, not an admissible monotone treatment/control node in the current no-escape model.

## Evidence anchors

- Secreted ApoE rewires melanoma cell-state vulnerability to ferroptosis; `1D7` restores ferroptosis sensitivity in coculture/conditioned-media experiments.
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC11808924/
  - https://pubmed.ncbi.nlm.nih.gov/39413195/
- Pencheva et al., Cell (2012); extracellular ApoE neutralization with `1D7` increases melanoma invasion and endothelial recruitment.
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC3753115/
  - https://pubmed.ncbi.nlm.nih.gov/23142051/
- Tumor ApoE immune checkpoint study; ApoE knockout/conditioned-media evidence for suppression of T-cell activation in B16-F10 melanoma.
  - https://pubmed.ncbi.nlm.nih.gov/36341364/
- Ostendorf et al., Nature Medicine (2020); APOE2/APOE4 knock-in melanoma models jointly connect genotype to progression, immunity, invasion and endothelial recruitment, but not ferroptosis.
  - https://pubmed.ncbi.nlm.nih.gov/32451497/
- Historical `1D7` reagent caveat.
  - https://pubmed.ncbi.nlm.nih.gov/2754339/

## Next bounded action

```text
NEXT_ACTIONS :=
1. Search specifically for melanoma T-cell assays using 1D7 or another validated
   extracellular ApoE-neutralization perturbation.
2. If none exists, retain the immune edge as the first unmatched outcome.
3. Do not rerun the no-escape optimizer as though ApoE blockade were closed.
```
