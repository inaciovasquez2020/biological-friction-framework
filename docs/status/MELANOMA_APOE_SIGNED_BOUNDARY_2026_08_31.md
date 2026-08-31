# Melanoma ApoE Signed Boundary — 2026-08-31

## Status

`CONDITIONAL / LITERATURE-BOUNDED MODEL`

This document records a bounded research result for a melanoma residual-disease model. It is not clinical guidance, a treatment recommendation, or evidence of a cure.

## Question

Can tumor ApoE be treated as a monotone intervention node in a melanoma no-escape model?

## Result

`RETIRE := APOE as a monotone "block this" control node.`

Available melanoma evidence assigns at least three biologically distinct signed effects to tumor/extracellular ApoE:

1. `APOE -> + ferroptosis resistance`
   - Secreted ApoE from proliferative melanoma cells protects invasive melanoma cells from ferroptosis through lipid remodeling and later GPX4/NRF2 elevation.
   - ApoE neutralization restores ferroptosis sensitivity in the reported coculture system.

2. `APOE -> - antitumor T-cell activity`
   - In B16-F10 melanoma, tumor-secreted ApoE suppresses T-cell activation; tumor ApoE loss is associated with immune-pathway activation and tumor rejection in mice.

3. `APOE -> - invasion / - endothelial recruitment`
   - Melanoma-cell-secreted ApoE suppresses invasion through melanoma-cell LRP1 and suppresses endothelial recruitment through endothelial-cell LRP8.
   - Extracellular ApoE neutralization increases invasion and endothelial recruitment in the reported metastatic melanoma models.

Therefore reducing ApoE may improve ferroptosis susceptibility and immune activity while simultaneously removing an anti-invasive/anti-angiogenic effect.

## Matched-context audit

`MATCHED_CONTEXT_CLOSURE := FAILED`

The literature checked does not provide one matched experiment or model that measures all of the following under the same ApoE perturbation:

- ferroptotic melanoma death,
- functional antitumor CD8/T-cell activity,
- melanoma invasion/metastatic behavior,
- endothelial recruitment/angiogenesis.

Results from separate models cannot be combined into a proved scalar net-benefit sign.

## Model repair

Replace one unsigned ApoE node with three signed edges:

```text
APOE_HIGH
 ├─ protects melanoma from ferroptosis      BAD for eradication
 ├─ suppresses antitumor T-cell activity    BAD for immunity
 └─ suppresses invasion/endothelial recruitment GOOD for dissemination control
```

The optimization objective must therefore track at least three components separately:

```text
J = (tumor_survival, immune_escape, metastatic_dissemination)
```

Do not collapse `J` to a single score without a matched-context calibration.

## Weakest missing object

```text
MISSING_OBJECT :=
matched-context quantitative evidence establishing whether the benefit of
reducing tumor ApoE (restored ferroptosis susceptibility plus improved
antitumor T-cell activity) exceeds the accompanying loss of ApoE-mediated
suppression of melanoma invasion and endothelial recruitment.
```

## Boundary

```text
BOUNDARY :=
¬ net-antitumor sign(APOE reduction) established across melanoma states and niches
```

No global ApoE-neutralization control class is admissible in the current no-escape model.

## Evidence anchors

- Tsoi/related phenotype-vulnerability follow-up: secreted ApoE rewires melanoma-cell ferroptosis vulnerability and protects invasive cells.
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC11808924/
- Pencheva et al., Cell (2012): melanoma-cell-secreted ApoE suppresses invasion and endothelial recruitment through LRP1/LRP8-dependent mechanisms.
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC3753115/
  - https://pubmed.ncbi.nlm.nih.gov/23142051/
- Ostendorf et al. / tumor ApoE immune study: tumor ApoE suppresses antitumor immunity in B16-F10 melanoma.
  - https://pubmed.ncbi.nlm.nih.gov/36341364/

## Next bounded action

```text
NEXT_ACTIONS :=
1. Require one matched model measuring ferroptotic death, CD8/T-cell function,
   invasion/metastatic behavior, and endothelial recruitment under the same
   ApoE perturbation.
2. Until then, retain ApoE as a signed environmental coupling rather than a
   treatment/control node.
3. Re-run the multi-layer reachability model only after the matched-context
   sign is resolved.
```
