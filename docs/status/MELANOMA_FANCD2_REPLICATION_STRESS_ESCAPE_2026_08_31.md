# Melanoma FANCD2 replication-stress escape — 2026-08-31

## Status

`CONDITIONAL / LITERATURE-BOUNDED MODEL`

This document records a bounded correction to the melanoma interaction graph. It is not clinical guidance, a treatment recommendation, or evidence of a cure.

## Question

Does the retained FANCD2/Fanconi replication-stress state now have enough direct melanoma evidence to earn a functional control at the preclinical graph level, or must it remain completely uncovered?

## Result

`RESULT := LONG-TERM MELANOMA RESISTANCE CONTROL IS FUNCTIONALLY SUPPORTED; MATCHED IN-VIVO MAPKi CLOSURE REMAINS UNPROVED`

The earlier 2023 escapee-cell result established a short-timescale dependency:

```text
MAPK inhibition
  -> rare cell-cycle escape
  -> replication stress / DNA lesions
  -> FANCD2 recruitment to stalled forks and mitotic-DNA-synthesis sites
  -> successful S/G2/mitotic completion
```

In A375 BRAF-V600E melanoma cells, FANCD2 depletion under MAPK inhibition produced approximately 9-fold fewer surviving escapees and approximately 6-fold more cell death, with increased post-mitotic death and mitotic slippage.

The 2024 Cell study materially strengthens this boundary. FANCD2 was genetically inactivated in three patient-derived BRAF-V600E melanoma lines (M229, M249, M395). FANCD2 loss did not materially alter basal clonogenic growth, but consistently suppressed the emergence of acquired-resistant colonies during chronic combined vemurafenib + selumetinib treatment. The long-term assays were repeated across all three melanoma lines, and chronic MAPK-targeted therapy produced ecDNA-containing resistant populations that were sharply reduced among rare FANCD2-deficient resistant cells.

Thus the evidence now extends from acute escapee survival to long-term acquired-resistance emergence:

```text
FANCD2 / FA activity
  -> replication-stress tolerance
  -> completion of aberrant cell cycles
  -> chromothripsis / ecDNA-capable genome evolution
  -> acquired BRAFi+MEKi-resistant outgrowth
```

## Separate in-vivo melanoma evidence

An earlier Scientific Reports study independently showed that FANCD2/FANC activity supports melanoma growth and targeted-therapy tolerance.

In that work:

```text
FANCD2 depletion in B16-F10 melanoma cells
  -> strongly reduced tumor development after subcutaneous implantation in mice

FANCD2 silencing in BRAF-mutant melanoma cells
  -> improved vemurafenib effect

FANCD2 overexpression
  -> reduced / abolished the measured vemurafenib cellular effect
```

This establishes that FANCD2 dependence is not limited to one short-term A375 assay and that FANCD2 depletion can reduce melanoma tumor development in vivo.

However, the in-vivo tumor-growth experiment was not the same experiment as chronic BRAFi+MEKi resistance suppression.

## Structural consequence

The graph can now promote an abstract functional control:

```text
C_FANCD2_REPLICATION_STRESS :=
prevent FANCD2/Fanconi-mediated replication-stress tolerance and associated
genome-evolution support from sustaining MAPK-inhibited melanoma escape and
long-term acquired-resistant outgrowth
```

An experimentally supported implementation class is FANCD2/FA-pathway genetic suppression. No specific drug or clinical implementation is asserted.

The direct state can therefore be blocked in the executable abstraction:

```text
C_FANCD2_REPLICATION_STRESS blocks e_fancd2_replication_stress
```

## Why the certificate remains conditional

The strongest missing experiment is now narrower than before.

The literature does not establish, in one matched melanoma in-vivo MAPKi context:

```text
FANCD2 / FA suppression
+ BRAFi/MEKi pressure
+ reduced resistant outgrowth / delayed relapse
+ measured replication-stress / ecDNA mechanism
+ no compensatory persister-state redistribution
```

Therefore the executable graph must replace the direct uncovered FANCD2 state with a separate scope boundary:

```text
fancd2_mapki_in_vivo_gap
```

and keep that boundary reachable.

## Relationship to Polκ

Keep two separate objects:

```text
R_POLK_STRESS :=
nuclear Polκ-associated modest MAPKi tolerance / implementation antagonism

R_FA_REPLICATION_STRESS :=
FANCD2/Fanconi-mediated replication-stress tolerance and genome-evolution
support during MAPK-targeted therapy
```

The 2023 study found Polκ induction broadly in drug-treated cells and concluded that Polκ was unlikely to be the major driver of escapee-specific DNA damage/mutagenesis. FANCD2 has the stronger functional escape and long-term resistance evidence.

```text
DO_NOT_COLLAPSE := FANCD2 control into Polκ control
```

## Relationship to eIF4A / NHEJ adaptive mutability

The existing translation-control route tracks eIF4A-dependent 53BP1/NHEJ adaptive mutability. The FANCD2/FA route is mechanistically distinct and additionally supported by chromothripsis/ecDNA-mediated resistance evolution.

```text
DO_NOT_COLLAPSE :=
FANCD2/FA replication-stress control into eIF4A/53BP1/NHEJ control
```

## Updated missing object

```text
MISSING_OBJECT :=
a matched melanoma in-vivo / PDX MAPK-therapy certificate showing that
FANCD2/Fanconi suppression:

1. engages the intended FA/replication-stress mechanism in tumor tissue,
2. reduces or prevents chronic BRAFi+MEKi-resistant outgrowth,
3. delays relapse / progression in vivo,
4. reduces ecDNA / complex-genome-evolution output where that route is active,
5. does not merely redirect survivors into another retained persister state,
6. remains compatible with dynamic MAPK and immune/metastatic boundaries.
```

## Boundary

```text
BOUNDARY :=
long-term acquired-resistance suppression by FANCD2 loss is established in
multiple BRAF-V600E melanoma lines, and independent melanoma tumor-growth
support by FANCD2 is established in vivo; matched FANCD2-suppression + MAPKi
in-vivo relapse control remains unproved
```

## Evidence anchors

- Hoffman et al., Science Signaling (2023), `Multiple cancers escape from multiple MAPK pathway inhibitors and use DNA replication stress signaling to tolerate aberrant cell cycles`.
  - https://pubmed.ncbi.nlm.nih.gov/37527351/
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC10704347/
- Engel et al., Cell (2024), `The Fanconi anemia pathway induces chromothripsis and ecDNA-driven cancer drug resistance`.
  - https://pubmed.ncbi.nlm.nih.gov/39181133/
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC11490392/
  - https://doi.org/10.1016/j.cell.2024.08.001
- Bourseguin et al., Scientific Reports (2016), `FANCD2 functions as a critical factor downstream of MiTF to maintain the proliferation and survival of melanoma cells`.
  - https://pubmed.ncbi.nlm.nih.gov/27827420/
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC5101529/
  - https://doi.org/10.1038/srep36539
- Temprine et al., Science Signaling (2020), `Regulation of the error-prone DNA polymerase Polκ by oncogenic signaling and its contribution to drug resistance`.
  - https://pubmed.ncbi.nlm.nih.gov/32345725/
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC7428051/

## Next bounded action

```text
NEXT_ACTIONS :=
1. Activate C_FANCD2_REPLICATION_STRESS in the executable certificate.
2. Replace direct FANCD2-state reachability with fancd2_mapki_in_vivo_gap.
3. Keep the overall certificate conditional.
4. Search next for matched melanoma xenograft/PDX MAPKi + FANCD2/FA suppression
   with relapse or acquired-resistance endpoints.
```
