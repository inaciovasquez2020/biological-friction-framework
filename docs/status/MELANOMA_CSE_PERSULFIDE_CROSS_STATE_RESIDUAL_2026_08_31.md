# Melanoma CSE/H2S-persulfide cross-state residual — 2026-08-31

## Status

`CONDITIONAL / LITERATURE-BOUNDED MODEL`

This document records a bounded structural result for a melanoma drug-tolerant-persister / minimal-residual-disease escape graph. It is not clinical guidance, a treatment recommendation, or evidence of a cure.

## Question

After representing the four classic Rambow MRD phenotypes at the abstraction level, is there a newer survival program that cuts across phenotype identity and therefore remains outside a purely state-based hitting set?

## Result

`RESULT := AN IMMEDIATE CSE/H2S-PERSULFIDE STRESS-SURVIVAL PROGRAM REMAINS A CROSS-STATE RESIDUAL`

Cell Metabolism (2025) reported that BRAF-V600E inhibition triggers rapid metabolic reprogramming in melanoma persister cells, including an immediate increase in cystathionine-gamma-lyase (CSE) activity/expression.

The supported route is:

```text
BRAF-V600E inhibition
  -> oxidative / cystine-rich stress state
  -> increased CSE-dependent cysteine/cystine catabolism
  -> H2S + persulfide production
  -> protein-thiol protection + mitochondrial energy support
  -> drug-tolerant persister survival
  -> proliferative relapse
```

CSE inhibition combined with BRAF-targeted therapy reduced proliferative relapse in culture models and increased progression-free survival in xenografted mice. CSE induction was also reported in patient samples during BRAF-V600E-targeted therapy.

## Why this is not another Rambow state

The CSE result is described as a rapid stress-response/metabolic program in drug-tolerant persisters rather than as one of the four transcriptional MRD phenotypes.

Therefore a graph that contains only:

```text
invasive / SOX10-low
SMC / CD36+
NCSC
pigmented / MITF-high
```

can still miss a cross-cutting survival mechanism that may be shared by more than one phenotype.

```text
DO_NOT_INFER :=
coverage(four MRD phenotype labels) => coverage(all persister survival programs)
```

## Relationship to existing metabolic controls

### Pigmented MITF-high / OXPHOS control

The CSE program supports mitochondrial energy production, but the cited study does not establish that it is restricted to the MITF-high / PPARGC1A-high pigmented state.

Therefore:

```text
DO_NOT_COLLAPSE := CSE/H2S-persulfide survival into C_PIGMENTED
```

### CD36+ SMC peroxisome/UGCG control

The SMC route is based on peroxisome-dependent lipid metabolism and UGCG-mediated ceramide buffering. The CSE route is a cysteine/transsulfuration/redox-buffering program.

```text
DO_NOT_COLLAPSE := CSE/H2S-persulfide survival into C_SMC_METABOLIC
```

### GPX4/FSP1 ferroptosis boundary

Persulfide-mediated thiol protection is redox-protective, but the 2025 CSE paper is not a direct GPX4/FSP1 niche-switch experiment and does not prove that CSE dependence is equivalent to either ferroptosis-surveillance dependency.

```text
DO_NOT_COLLAPSE := CSE/H2S-persulfide survival into R_FERROPTOSIS_SWITCH
```

## Weakest functional repair

The graph should represent the survival function rather than a named inhibitor:

```text
C_CSE_REDox :=
prevent CSE-dependent H2S/persulfide stress buffering from sustaining
BRAF-V600E drug-tolerant melanoma persisters under targeted-therapy pressure
```

An experimentally supported implementation class is CSE interference during BRAF-V600E inhibition, but no specific compound is promoted to a universal control.

## Genotype boundary

The direct Cell Metabolism result is specifically centered on BRAF-V600E-targeted therapy.

```text
DO_NOT_INFER :=
CSE dependence is universal across NRAS-, NF1-, BRAF-non-V600E-, or
immunotherapy-only melanoma persisters
```

This is the first major scope boundary for the route.

## State-mapping boundary

The paper establishes CSE as vital to the studied persister population but does not provide a matched four-state MRD atlas assigning functional CSE dependency separately to:

```text
pigmented
SMC
NCSC
invasive / SOX10-low
```

Therefore:

```text
MISSING_OBJECT :=
a matched single-cell / functional-dependency map showing which melanoma MRD
states require CSE/H2S-persulfide buffering, whether the dependency is shared
across states, and whether CSE control redistributes survivors into another
state rather than eliminating the persister reservoir.
```

## Cross-state residual object

```text
R_CSE_CROSS_STATE :=
therapy-induced redox/metabolic persister survival that is not certified by
phenotype-state coverage alone
```

This object is orthogonal to the statement that the four classic Rambow states are represented.

## Boundary

```text
BOUNDARY :=
CSE/H2S-persulfide buffering is an evidence-backed BRAF-V600E persister
vulnerability, but its phenotype coverage and genotype generality are not proved
```

## Evidence anchors

- Borbenyi-Galambos et al., Cell Metabolism (2025), `Realigned transsulfuration drives BRAF-V600E-targeted therapy resistance in melanoma`.
  - https://pubmed.ncbi.nlm.nih.gov/40037361/
  - https://doi.org/10.1016/j.cmet.2025.01.021
- Shah et al., Cancer Science (2026), `MAPK Inhibitor-Tolerant Persister Cells in Melanoma: Mechanisms and Therapeutic Vulnerabilities`.
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC13394650/

## Next bounded action

```text
NEXT_ACTIONS :=
1. Add C_CSE_REDox as a cross-state BRAF-V600E persister-control requirement.
2. Do not merge it with pigmented/OXPHOS, SMC/peroxisome-UGCG, or GPX4/FSP1
   without a matched dependency map.
3. Search the 2026 persister literature for the next cross-state program not
   already represented by MAPK, PI3K/AKT, FAK, state-specific metabolic, immune,
   or ferroptosis controls.
4. Prefer programs with direct functional dependency and in vivo validation.
```
