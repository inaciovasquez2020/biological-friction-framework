# Melanoma pigmented MITF-high/OXPHOS residual — 2026-08-31

## Status

`CONDITIONAL / LITERATURE-BOUNDED MODEL`

This document records a bounded structural result for a melanoma minimal-residual-disease / therapy-escape graph. It is not clinical guidance, a treatment recommendation, or evidence of a cure.

## Question

After separately encoding the SOX10-low invasive state, the CD36+ starved-like melanoma cell (SMC) state, and the conditionally compressed NCSC route, does the remaining pigmented / MITF-high MRD state require its own control object?

## Result

`RESULT := THE PIGMENTED MITF-HIGH STATE REMAINS A DISTINCT METABOLIC RESIDUAL`

MAPK-pathway inhibition can induce an early, reversible MITF-high drug-tolerant state. In the Rambow MRD decomposition, a pigmented/hyperdifferentiated population with high MITF activity coexists with invasive, NCSC, and SMC states.

A useful state abstraction is:

```text
S_PIGMENTED :=
MAPKi-tolerant pigmented / MITF-high melanoma state
  -> MITF / PAX3-supported lineage-survival program
  -> PPARGC1A / PGC1alpha-high mitochondrial program
  -> elevated oxidative phosphorylation / oxidative-stress tolerance
  -> persistence under MAPK pressure
```

## Distinction from the CD36+ SMC state

Huang et al. reanalyzed the Rambow single-cell dataset and found that:

```text
SMC state       -> CD36-high, peroxisome/UGCG-associated metabolism
pigmented state -> PPARGC1A/PGC1alpha-enriched mitochondrial metabolism
```

PPARGC1A was predominantly expressed in the pigmented MITF-high state and did not correlate with CD36 in the cited TCGA analysis.

Therefore:

```text
DO_NOT_COLLAPSE := S_PIGMENTED into S_SMC
```

The two states share broad metabolic adaptation but use separable dominant programs.

## Why existing controls do not automatically close S_PIGMENTED

### MAPK control

MITF upregulation is observed after BRAF/MEK-pathway inhibition, so MAPK suppression itself does not prove elimination of this state.

### SOX10-low / TAZ-TEAD control

The pigmented state is MITF-high and differentiated, whereas the encoded SOX10-low state is invasive/mesenchymal-like. Phenotype identity does not support collapsing them.

### SMC peroxisome/UGCG control

The JCI analysis specifically separates PPARGC1A-enriched pigmented cells from CD36+ peroxisome/UGCG-dependent SMCs.

### FAK/AKT NCSC control

No evidence reviewed here establishes that the NCSC FAK/AKT dependency removes the MITF-high pigmented population.

Therefore:

```text
S_PIGMENTED remains a distinct residual state in the current graph.
```

## Evidence-backed vulnerability classes

Two mechanistically different vulnerability classes have preclinical support.

### State-regulatory vulnerability

Smith et al. showed that PAX3-mediated MITF induction drives an early reversible nonmutational MAPKi-tolerant state. MITF depletion resensitized melanoma cells to MAPK inhibition.

### Mitochondrial vulnerability

MITF can drive PGC1alpha and mitochondrial oxidative metabolism. MITF-high / PGC1alpha-high melanoma cells show increased mitochondrial capacity and oxidative-stress tolerance, and prior preclinical work found that mitochondrial/OXPHOS interference can sensitize MAPK-inhibited melanoma cells.

For the graph, keep the requirement functional rather than naming a drug:

```text
C_PIGMENTED :=
prevent persistence of the MITF-high pigmented state by either
state-regulatory suppression or a validated state-selective metabolic
vulnerability, without merely redistributing cells into another MRD state
```

Do not promote a specific MITF, PAX3, PGC1alpha, or mitochondrial intervention to universal control.

## Redistribution boundary

The strongest unresolved issue is state plasticity.

Suppressing one MRD state can increase another. This was directly observed for NCSC-directed manipulation, and the Rambow atlas shows transitions among SMC, pigmented, invasive, and NCSC states.

Therefore:

```text
DO_NOT_INFER :=
loss(S_PIGMENTED) => loss(all MRD)
```

A pigmented-state control is useful only if it does not create an uncovered transition into another tolerant state.

## Weakest missing object

Smith et al. provides a stronger functional control surface than a simple association between MITF and pigmentation. In tested melanoma systems, PAX3/MITF suppression or MITF depletion sensitized cells to MAPK inhibition; combined PAX3/MITF suppression with MAPK inhibition prevented resistant colony outgrowth in drug-tolerant A375 derivatives; and in A375 xenografts the combination abolished treatment-induced PAX3/MITF upregulation while producing substantial tumor regression. Related sensitization was also demonstrated in tested NRAS-mutant melanoma models.

A 2026 Nature Communications study further shows that MITF dependence can persist after acquired MAPK-inhibitor resistance rather than being restricted to the early adaptive-tolerance phase. MELHO cells made resistant by prolonged dabrafenib/trametinib exposure remained strongly sensitive to inducible MITF knockdown. The same qualitative dependence was retained in an additional BRAF-mutant acquired-resistant model (UACC-257) and an NRAS-mutant model (SK-MEL-30) adapted to trametinib. In resistant MELHO cells, acquisition of resistance reduced the aggregate MITF transcriptional signature and increased AXL / epithelial-mesenchymal-transition programs, yet the cells retained enough MITF and MITF-target activity for MITF knockdown to suppress survival and the same major transcriptional programs seen in treatment-naive cells.

```text
ESTABLISHED :=
the MITF lineage-survival program can remain functionally required after
prolonged acquisition of MAPK-inhibitor resistance in tested BRAF- and
NRAS-associated melanoma models

RETIRE :=
"MITF dependence is supported only in the early reversible MAPKi-tolerant phase"
```

This stronger result also prevents a state-identification shortcut. Acquired-resistant cells can show an AXL/EMT-shifted transcriptome while remaining MITF-dependent, so functional MITF dependence alone is not a certificate that the surviving population is the transcriptomically defined Rambow pigmented / MITF-high state.

```text
DO_NOT_INFER :=
MITF-dependent survival => S_PIGMENTED identity

DO_NOT_INFER :=
MITF knockdown sensitivity => selective depletion of S_PIGMENTED
```

The remaining object is therefore not another bulk demonstration that MITF matters before or after resistance. It is state-resolved survivor accounting after a functionally validated MITF/pigmented-state control:

```text
MISSING_OBJECT :=
a matched post-control MRD state-composition / transition certificate showing
that a validated PAX3/MITF- or pigmented-state control, in the same residual
population under continued MAPK pressure:

1. depletes the transcriptomically defined pigmented / MITF-high persister state,
2. distinguishes selective S_PIGMENTED depletion from broader MITF-dependent
   killing in AXL/EMT-shifted or other melanoma states,
3. does not merely convert or enrich survivors into SMC, NCSC, or
   invasive/SOX10-low states,
4. preserves the effect through long-term residual outgrowth,
5. generalizes across relevant melanoma genotypes and MRD contexts,
6. preserves the already retained immune/metastatic boundaries.
```

The minimum informative experiment is therefore state-resolved survivor mapping after a functionally validated pigmented/MITF control, rather than another demonstration that MITF suppression sensitizes bulk melanoma cells or acquired-resistant cultures to MAPK inhibition.

## Four-state Rambow coverage status

At the abstraction level, the four classic MRD states are now represented:

```text
invasive / SOX10-low -> C_SOX10_LOW
SMC / CD36+          -> C_SMC_METABOLIC
NCSC                 -> conditional C_FAK_STATE + C_MAPK compression
pigmented / MITF-high-> C_PIGMENTED
```

This is a state-accounting milestone only.

```text
DO_NOT_INFER := four-state abstraction => melanoma MRD closure
```

Additional persister programs, state transitions, immune escape, metastatic niche effects, and genetically acquired resistance remain outside this statement.

## Boundary

```text
BOUNDARY :=
the pigmented MITF-high / PPARGC1A-high state has separable preclinical
vulnerabilities, but no matched transition-safe control certificate proves
its elimination without redistribution into another MRD state
```

## Evidence anchors

- Smith et al., Cancer Cell (2016), `Inhibiting Drivers of Non-mutational Drug Tolerance Is a Salvage Strategy for Targeted Melanoma Therapy`.
  - https://pubmed.ncbi.nlm.nih.gov/26977879/
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC4796027/
- Rambow et al., Cell (2018), `Toward Minimal Residual Disease-Directed Therapy in Melanoma`.
  - https://pubmed.ncbi.nlm.nih.gov/30017245/
- Huang et al., J Clin Invest (2023), `Peroxisome disruption alters lipid metabolism and potentiates antitumor response with MAPK-targeted therapy in melanoma`.
  - https://www.jci.org/articles/view/166644
  - https://pubmed.ncbi.nlm.nih.gov/37616051/
- Vazquez et al., Cancer Cell (2013), `PGC1alpha expression defines a subset of human melanoma tumors with increased mitochondrial capacity and resistance to oxidative stress`.
  - https://pubmed.ncbi.nlm.nih.gov/23416000/

## Next bounded action

```text
NEXT_ACTIONS :=
1. Add C_PIGMENTED as a distinct state-specific functional control.
2. Treat the classic four-state Rambow MRD atlas as represented, not closed.
3. Move beyond the four-state atlas and test newer independent persister
   programs for survivors not subsumed by these state controls.
4. First test the immediate CSE/H2S/persulfide transsulfuration program reported
   in BRAF-V600E drug-tolerant persisters.
```
