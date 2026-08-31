# Melanoma HGF/MET–PI3K/AKT Residual Escape — 2026-08-31

## Status

`CONDITIONAL / LITERATURE-BOUNDED MODEL`

This document records a bounded update to a melanoma residual-disease escape model. It is not clinical guidance, a treatment recommendation, or evidence of a cure.

## ApoE handoff

A bounded search did not identify a single melanoma experiment in which one molecularly identified extracellular ApoE-blocking perturbation jointly measures both immune activation and metastatic/dissemination behavior. The ApoE node therefore remains signed/non-monotone and is not treated as a closed intervention node.

The model is advanced by moving to the next retained escape family rather than assuming ApoE closure.

## Result

`RESULT := FIRST NON-APOE RESIDUAL ESCAPE IDENTIFIED IN THE CURRENT CONTROL GRAPH`

Under the current abstract control set:

```text
C1 := metabolic-persister control
C2 := FAK/NCSC control
C3 := MAPK-reactivation control
C4 := ferroptosis induction/sensitization
C5 := non-metastasis-promoting ferroptosis-rescue control
C6 := hypoxic-LN/FSP1 control
```

the following stromal escape remains reachable:

```text
CAF / stromal HGF
  -> MET
  -> PI3K
  -> AKT
  -> survival under MAPK-pathway therapy
```

HGF/MET can activate both MAPK and PI3K/AKT signaling in BRAF-mutant melanoma. Therefore covering the MAPK-reactivation arm does not by itself eliminate the parallel PI3K/AKT survival arm.

## Why existing controls do not hit this route

```text
C3 MAPK-reactivation control
  hits: HGF -> MET -> MAPK arm
  misses: HGF -> MET -> PI3K -> AKT arm

C2 FAK/NCSC control
  hits: FAK-dependent NCSC survival branch
  does not imply: MET-driven PI3K/AKT suppression
```

The distinction is structural: control of one upstream route into AKT does not establish control of another independent upstream route into AKT.

## Evidence anchor

Established melanoma studies report that stromal HGF activates MET and reactivates both MAPK and PI3K/AKT signaling, producing resistance to RAF inhibition. In one BRAF-mutant melanoma study, combined BRAF+MEK inhibition was insufficient to eliminate HGF-induced resistance because AKT signaling remained active, while combined MEK+AKT inhibition suppressed most of the HGF-mediated resistance.

A separate fibroblast-niche study found HGF/NRG/fibronectin-dependent PI3K/AKT survival signaling during BRAF inhibition. In that context, BRAF/MET/HER inhibition was insufficient to reverse the fibroblast-mediated escape, whereas BRAF+PI3K inhibition overcame resistance in vitro and enhanced antitumor effects in a xenograft model.

These are preclinical/model-system results. They do not establish a safe or effective human treatment combination.

## Shared-node reduction

Three retained resistance families in the encoded graph are:

```text
R4  RTK -> PI3K -> AKT -> mTOR
R5  PTEN loss -> PI3K -> AKT -> mTOR
R10 HGF/MET -> PI3K -> AKT
```

Within this graph, their shared internal segment is:

```text
PI3K -> AKT
```

Therefore the narrow structural repair is not to add HGF/MET as a uniquely sufficient target. It is to add an abstract control constraint on the shared PI3K/AKT survival branch.

```text
REPAIR :=
C_RTK_SURVIVAL := PI3K/AKT survival-control constraint
```

This is a model constraint, not a drug recommendation.

## Important non-closure

The fibroblast-niche evidence also shows why `MET blockade` cannot be promoted to a universal closure object: resistance can be supported by additional stromal signals such as NRG and matrix/fibronectin coupling. Likewise, a recent melanoma resistance review describes c-MET/HGF signaling as feeding MAPK, PI3K/AKT, GAB1, STAT3 and Rac1/PAK signaling.

Thus:

```text
DO_NOT_INFER :=
HGF/MET blockade alone closes the stromal resistance family
```

## First surviving state

```text
FIRST_SURVIVING_STATE :=
BRAF-mutant melanoma
x HGF-responsive stromal niche
x MAPK arm controlled
x PI3K/AKT arm still active
```

or, in path form:

```text
HGF -> MET -> PI3K -> AKT -> survival
```

## Boundary

```text
BOUNDARY :=
¬ current six-control graph blocks the HGF/MET -> PI3K/AKT survival route
```

and:

```text
BOUNDARY_CLINICAL :=
¬ safe/effective human PI3K/AKT control established by this model
```

## Evidence anchors

- Straussman et al., Nature (2012), tumor microenvironment HGF/MET-mediated innate RAF-inhibitor resistance in BRAF-mutant melanoma:
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC3711467/
  - https://pubmed.ncbi.nlm.nih.gov/22763439/
- Fedorenko et al., Journal of Investigative Dermatology (2015), fibroblast-derived HGF/NRG/fibronectin PI3K/AKT survival niche:
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC4648653/
  - https://pubmed.ncbi.nlm.nih.gov/26302068/
- Caenepeel et al. (2017), MAPK inhibition primes BRAF-mutant melanoma for HGF/MET rescue:
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC5392287/
  - https://pubmed.ncbi.nlm.nih.gov/28147313/
- Current molecular-targeted-therapy review (2026), c-MET/HGF downstream MAPK, PI3K/AKT, GAB1, STAT3 and Rac1/PAK signaling:
  - https://pubmed.ncbi.nlm.nih.gov/42512373/

## Next bounded action

```text
NEXT_ACTIONS :=
1. Insert C_RTK_SURVIVAL as an abstract PI3K/AKT control constraint.
2. Re-run the retained route cover for R4, R5 and R10.
3. Keep MET-specific closure retired because stromal NRG/matrix escape remains possible.
4. Return the first route that survives after PI3K/AKT is treated as covered.
5. Do not interpret the graph cover as a treatment regimen or clinical efficacy claim.
```
