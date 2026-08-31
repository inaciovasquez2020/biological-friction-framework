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

In fact, the CD36+ SMC state is described as a transitory MRD state that can feed emergence of other drug-tolerant states. Selective removal of S_SMC can therefore strengthen the graph without proving global closure.

## Weakest missing object

```text
MISSING_OBJECT :=
a matched-MRD state-coverage certificate showing whether C_SMC_METABOLIC:

1. eliminates CD36+ SMCs in the same MRD population,
2. prevents transition from SMC into other tolerant states,
3. does not merely redistribute surviving cells into NCSC, invasive, or
   pigmented residual states,
4. remains effective in clinically relevant BRAF-, NRAS-, and NF1-associated
   MAPK-inhibited contexts,
5. does not create an uncovered metastatic / immune-escape phenotype.
```

Until that object exists, S_SMC receives its own state-specific control requirement.

## Boundary

```text
BOUNDARY :=
not proved that peroxisome/UGCG control closes the full melanoma MRD state space;
it is supported as a selective vulnerability of CD36+ SMC persisters
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
1. Add abstract C_SMC_METABOLIC to the retained control set.
2. Recompute the residual MRD-state graph without claiming global MRD closure.
3. Test the SOX10-positive / NGFR-high NCSC-RXRG state next, because it is
   transcriptionally distinct from both S_SMC and the already encoded SOX10-low state.
```
