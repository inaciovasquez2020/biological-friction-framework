# Melanoma FANCD2 replication-stress escape — 2026-08-31

## Status

`CONDITIONAL / LITERATURE-BOUNDED MODEL`

This document records a bounded correction to the melanoma interaction graph. It is not clinical guidance, a treatment recommendation, or evidence of a cure.

## Question

Does tracking nuclear Polκ after MAPK or PI3K/mTOR stress adequately represent the replication-stress escape program of MAPK-inhibited melanoma cells?

## Result

`RESULT := NO; A DISTINCT FANCD2/FANCONI-ANEMIA REPLICATION-STRESS TOLERANCE STATE IS FUNCTIONALLY SUPPORTED`

Earlier work showed that MAPK inhibition or PI3K/mTOR suppression can drive Polκ into the nucleus in BRAF-V600E melanoma and that changing POLK abundance modestly alters vemurafenib sensitivity. That remains a valid implementation-level antagonistic coupling.

However, Hoffman et al. (Science Signaling, 2023) provides a stronger functional result for the escapee-cell replication-stress program.

In BRAF-driven A375 melanoma cells exposed to MAPK inhibitors, a subset of cells escaped drug-induced quiescence and resumed slow proliferation while showing replication stress, DNA lesions, and Fanconi-anemia-pathway recruitment. FANCD2 accumulated in replicating escapee cells and at mitotic DNA synthesis sites. FANCD2 deficiency combined with MAPK inhibition increased apoptosis across tested MAPK-mutant models, including BRAF-mutant melanoma evidence.

The same study measured Polκ nuclear recruitment after dabrafenib, encorafenib, binimetinib, and trametinib in A375 cells. Polκ was induced broadly in both escapees and non-escapees. The authors concluded that Polκ was unlikely to be a major contributor to the increased DNA damage or mutagenesis specific to escapees.

Therefore:

```text
RETIRE :=
"polk_stress_tolerance alone represents the functional replication-stress escape program"
```

Keep instead two separate objects:

```text
R_POLK_STRESS :=
nuclear Polκ-associated modest MAPKi tolerance / implementation antagonism

R_FA_REPLICATION_STRESS :=
FANCD2/Fanconi-mediated fork-restart and mitotic-DNA-synthesis tolerance
that permits MAPKi escapee cells to complete cell division
```

## Structural consequence

The executable graph must not mark replication-stress escape as accounted for merely because Polκ is declared unresolved.

Add a separate reachable state:

```text
fancd2_replication_stress_tolerance
```

with the evidence-backed edge:

```text
therapy_pressure
  -> fancd2_replication_stress_tolerance
```

No control is credited yet.

## Why no control is activated yet

FANCD2 loss increases apoptosis under MAPK inhibition and therefore establishes functional dependency. But the retained evidence does not provide a melanoma-specific in-vivo closure certificate showing that suppressing the FA/FANCD2 program prevents durable relapse without creating a compensatory survivor state.

Accordingly:

```text
DO_NOT_ADD_ACTIVE_CONTROL_YET := C_FA_REPLICATION_STRESS
```

The state remains reachable until a stronger same-context control certificate is established.

## Relationship to eIF4A adaptive mutability

The existing translation-control route tracks eIF4A-dependent 53BP1/NHEJ adaptive mutability. FANCD2 escapee-cell stress tolerance is a distinct mechanism:

```text
DO_NOT_COLLAPSE :=
FANCD2/FA fork-restart tolerance into eIF4A/53BP1/NHEJ mutability
```

The former enables damaged escapee cells to finish replication/mitosis; the latter supports a separate adaptive-mutability program.

## Relationship to Polκ

The 2023 study strengthens the interpretation that Polκ is a broad stress response rather than the defining escapee-specific mutational driver.

Therefore:

```text
KEEP := polk_stress_tolerance
ADD  := fancd2_replication_stress_tolerance
```

This is a refinement, not a deletion of the earlier Polκ result.

## Weakest missing object

```text
MISSING_OBJECT :=
a melanoma-specific intervention certificate showing that functional
suppression of the FANCD2/Fanconi replication-stress program under MAPK
inhibition:

1. prevents successful escapee-cell S/G2/mitotic completion,
2. reduces long-term resistant outgrowth,
3. remains effective in 3D/in-vivo melanoma,
4. does not merely redirect survivors into another retained persister state,
5. is compatible with dynamic MAPK control and the existing interaction graph.
```

## Boundary

```text
BOUNDARY :=
replication-stress tolerance is functionally supported as a distinct melanoma
escape program; no durable melanoma-specific FANCD2/FA closure certificate is
currently retained
```

## Evidence anchors

- Hoffman et al., Science Signaling (2023), `Multiple cancers escape from multiple MAPK pathway inhibitors and use DNA replication stress signaling to tolerate aberrant cell cycles`.
  - https://pubmed.ncbi.nlm.nih.gov/37527351/
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC10704347/
- Temprine et al., Science Signaling (2020), `Regulation of the error-prone DNA polymerase Polκ by oncogenic signaling and its contribution to drug resistance`.
  - https://pubmed.ncbi.nlm.nih.gov/32345725/
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC7428051/
- Hangauer/rapid-escape follow-up, Nature Communications (2021), `Melanoma subpopulations that rapidly escape MAPK pathway inhibition incur DNA damage and rely on stress signalling`.
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC7979728/

## Next bounded action

```text
NEXT_ACTIONS :=
1. Add fancd2_replication_stress_tolerance to the executable certificate.
2. Keep polk_stress_tolerance separately reachable.
3. Do not activate a FANCD2 control without a stronger melanoma closure certificate.
4. Re-run fail-closed fixed-point reachability.
```
