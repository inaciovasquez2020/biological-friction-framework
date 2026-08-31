# Melanoma CD36+ SMC peroxisome/UGCG residual — 2026-08-31

## Status

`CONDITIONAL / LITERATURE-BOUNDED MODEL`

This document records a bounded structural result for a melanoma minimal-residual-disease / therapy-escape model. It is not clinical guidance, a treatment recommendation, or evidence of a cure.

## Question

After abstract coverage of MAPK reactivation, PI3K/AKT-associated survival, coupled RAC1/FAK states, SOX10-low MRD, extracellular adenosine escape, and the GPX4/FSP1 niche-switch boundary, is there an independent MAPKi-tolerant melanoma persister state that remains uncovered?

## Result

`RESULT := A CD36+ STARVED-LIKE METABOLIC PERSISTER REMAINS A DISTINCT RESIDUAL STATE`

The retained residual is:

```text
S_SMC :=
MAPKi-tolerant CD36+ starved-like melanoma cell state
  -> peroxisome-dependent metabolic adaptation
  -> UGCG-mediated ceramide buffering
  -> persister survival / later resistance
```

Huang et al. (JCI, 2023) showed that MAPK-pathway inhibition produces a metabolically active CD36+ persister population whose tolerance depends on peroxisome function together with UDP-glucose ceramide glycosyltransferase (UGCG).

Disrupting PEX3/peroxisome biogenesis increased proapoptotic ceramide stress, but UGCG-mediated ceramide metabolism limited that effect. Genetic/pharmacologic cotargeting of PEX3 and UGCG most efficiently eliminated the CD36+ persister population, sensitized melanoma to MAPK inhibition, delayed resistance, and restored sensitivity in multiple resistant models.

## State identity

Rambow et al. identified four coexisting MAPKi-tolerant transcriptional states in melanoma MRD:

```text
pigmented
starved-like melanoma cells (SMC)
dedifferentiated / invasive
neural-crest stem cell-like (NCSC)
```

Reanalysis in the JCI study found that the peroxisomal signature was specifically enriched in the CD36-marked SMC state.

Therefore:

```text
DO_NOT_COLLAPSE := S_SMC into SOX10-low / TAZ-TEAD MRD
DO_NOT_COLLAPSE := S_SMC into the ferroptosis GPX4/FSP1 switch
```

The current evidence supports S_SMC as a distinct metabolic persister object in the residual graph.

## Natural MRD trajectory refinement

The SMC state is not merely a parallel terminal phenotype. Pseudotime/trajectory analyses of the Rambow MRD system place SMC early in the adaptive response and support subsequent movement toward either a differentiated pigmented state or dedifferentiated NCSC/invasive states. The 2023 JCI paper explicitly describes CD36+ SMC as an important transitory state leading to emergence of other MAPKi-tolerant states.

For the executable graph, retain the natural untreated-control trajectory as:

```text
therapy pressure
  -> S_SMC
      -> pigmented / MITF-high MRD
      -> NCSC MRD
      -> invasive / SOX10-low MRD
```

These are natural state-transition edges under MAPKi adaptation. They are not asserted to be caused by PEX3/UGCG control.

```text
DO_NOT_INFER :=
SMC -> downstream MRD trajectory
=>
C_SMC_METABOLIC induces downstream-state redistribution
```

That latter implication requires a post-control composition experiment and remains unresolved.

## Why existing abstract controls do not close S_SMC

### MAPK control

The state is induced/tolerated under MAPK-pathway inhibition itself. MAPK control therefore cannot be counted as proof that this population is eliminated.

### SOX10-low state control

The SMC state is a separate member of the Rambow MRD-state decomposition. No evidence reviewed here proves that abstract SOX10-low TAZ/TEAD or cIAP coverage removes CD36+ SMCs.

### PI3K/AKT, FAK, adenosine, and GPX4/FSP1 controls

The cited SMC dependency is a peroxisome/sphingolipid-metabolism program. The current retained literature does not establish that those previously encoded controls eliminate this CD36+ persister population.

Therefore:

```text
S_SMC remains uncovered by the current abstract control set.
```

## Weakest functional repair

The strongest evidence-backed implementation tested in the cited melanoma study is joint interference with peroxisome biogenesis and UGCG-mediated ceramide disposal.

For the graph, keep the control functional rather than drug-specific:

```text
C_SMC_METABOLIC :=
eliminate or render nonpersistent the CD36+ SMC population by preventing
its peroxisome-supported / UGCG-buffered survival state under MAPK pressure
```

A sufficient experimentally motivated subclass is:

```text
C_PEX_UGCG :=
peroxisome-biogenesis disruption
AND
UGCG-mediated ceramide-buffer disruption
```

This is not asserted to be the unique or clinically appropriate implementation.

## Scope boundary

The JCI result is state-selective. It does not establish that PEX3+UGCG cotargeting eliminates every MRD state.

```text
DO_NOT_INFER :=
control(S_SMC) => control(all melanoma MRD states)
```

The 2023 study directly demonstrates selective elimination of MAPKi-induced CD36+ persister cells and delayed resistance, but it does not report a matched post-control single-cell composition showing whether remaining cells are enriched or depleted for NCSC, invasive/SOX10-low, or pigmented states.

The natural SMC trajectory is therefore now represented explicitly, while the intervention-specific redistribution question stays open.

## Weakest missing object

Huang et al. Figure 9 provides a stronger matched intervention surface than a purely in-vitro SMC endpoint. In A375M-derived melanomas kept under combined BRAF/MEK inhibition, tumors were collected after 10 days of treatment and analyzed by flow cytometry. The NNC+PPMP intervention decreased the percentage of CD36+ cells among CD45-negative tumor cells and reduced AGPS expression.

```text
ESTABLISHED :=
in the tested A375M in-vivo model under continued BRAF/MEK inhibition,
PEX3/PEX19 + UGCG pathway interference reduces the CD36+ SMC-marked
survivor fraction after 10 days
```

The matched readout reported for that experiment is CD36 abundance plus AGPS. It does not report the same post-control tumors as a four-state MRD composition measurement resolving pigmented/MITF-high, NCSC, and invasive/SOX10-low survivors.

```text
MISSING_OBJECT :=
a matched post-control MRD composition / transition certificate showing whether
C_SMC_METABOLIC, in the same treated residual population:

1. prevents or changes transition from SMC into downstream tolerant states,
2. does not merely enrich surviving NCSC, invasive/SOX10-low, or pigmented cells,
3. preserves the observed SMC depletion through long-term residual outgrowth,
4. remains effective in clinically relevant BRAF-, NRAS-, and NF1-associated
   MAPK-inhibited contexts,
5. does not create an uncovered metastatic / immune-escape phenotype.
```

The minimum informative experiment is therefore no longer merely a repeat demonstration of CD36+ depletion. It is a post-control matched MRD composition analysis under continued MAPK pressure, ideally with single-cell or lineage/barcode resolution and long-term outgrowth.

## Executable graph consequence

The certificate now distinguishes:

```text
KNOWN_NATURAL_EDGES :=
S_SMC -> pigmented_mitf_persister
S_SMC -> ncsc_nongenetic_escape
S_SMC -> sox10_low_mrd

UNRESOLVED_CONTROL_EDGE :=
C_SMC_METABOLIC -> ? redistribution / survivor-state enrichment
```

The existing destination-state controls are required to intercept the new natural incoming edges as well as the direct therapy-pressure edges. This preserves state-control semantics without pretending the SMC-control redistribution problem is solved.

## Boundary

```text
BOUNDARY :=
natural SMC-to-other-MRD trajectories are represented,
but it is not proved that peroxisome/UGCG control prevents or avoids
post-control redistribution into another tolerant state
```

## Evidence anchors

- Huang et al., J Clin Invest (2023), `Peroxisome disruption alters lipid metabolism and potentiates antitumor response with MAPK-targeted therapy in melanoma`.
  - https://www.jci.org/articles/view/166644
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC10575734/
  - https://pubmed.ncbi.nlm.nih.gov/37616051/
- Rambow et al., Cell (2018), `Toward Minimal Residual Disease-Directed Therapy in Melanoma`.
  - https://pubmed.ncbi.nlm.nih.gov/30017245/

## Next bounded action

```text
NEXT_ACTIONS :=
1. Keep the three natural SMC destination edges in the executable graph.
2. Keep smc_redistribution_gap reachable.
3. Search specifically for post-PEX3/UGCG or post-CD36-state-control single-cell,
   lineage, or marker-composition data under continued MAPKi pressure.
4. Retire smc_redistribution_gap only if those data show the intervention does
   not merely redirect the surviving reservoir into another MRD state.
```
