# Melanoma mTOR-ATF4-MTHFD2 unabsorbed residual — 2026-08-31

## Status

`CONDITIONAL / LITERATURE-BOUNDED MODEL`

This document records a bounded structural result for a melanoma drug-tolerant-persister / resistance graph. It is not clinical guidance, a treatment recommendation, or evidence of a cure.

## Question

Does the existing abstract PI3K/AKT control already absorb the 2026 melanoma persister pathway in which mTOR maintains ATF4 and MTHFD2 during RAF/MEK pressure, or must that pathway remain separately represented?

## Result

`RESULT := THE mTOR -> ATF4 -> MTHFD2 PERSISTER ROUTE IS CURRENTLY UNABSORBED`

Cai et al. (Cell Death & Disease, 2026) studied non-BRAF-V600 melanoma models treated with pan-RAF plus MEK inhibition. After prolonged treatment, persister cells retained/recovered ATF4 despite MAPK suppression. Addition of mTOR inhibition suppressed ATF4 and its downstream target MTHFD2, increased DNA damage, reduced persister survival, and improved tumor control in vivo.

The supported route is:

```text
RAF/MEK pressure
  -> persister state
  -> mTOR-supported ATF4 maintenance
  -> MTHFD2 / one-carbon metabolism
  -> DNA-repair support
  -> therapy tolerance / resistance
```

## Direct functional evidence

The 2026 study reports:

```text
ATF4 knockdown
  -> greater sensitivity to RAF/MEK-induced apoptosis
  -> greater DNA-damage signal

mTOR inhibition + RAF/MEK blockade
  -> ATF4 down
  -> MTHFD2 down
  -> prolonged tumor control / improved survival in tested mouse models
```

Human and murine melanoma models resistant to the RAF/MEK combination also showed elevated ATF4/MTHFD2 and remained sensitive to the mTOR-containing combination in the reported experiments.

## Why MAPK control alone is insufficient

In persister cells exposed for approximately 10 days, ATF4 was no longer suppressed by RAF/MEK treatment alone. This establishes that MAPK suppression does not by itself certify elimination of the ATF4 stress-response program.

```text
DO_NOT_INFER := C_MAPK => control(ATF4-MTHFD2 persister route)
```

## PI3K/AKT absorption test

The repository already carries an abstract PI3K/AKT survival control. mTOR is biologically connected to PI3K/AKT signaling, but the same-model result required here is stronger:

```text
NEEDED_FOR_ABSORPTION :=
in the same melanoma persister context,
C_PI3K_AKT -> suppression of mTOR-supported ATF4/MTHFD2 tolerance
```

The 2026 study demonstrates direct mTOR intervention and discusses PI3K-AKT-mTOR signaling, but it does not establish that a PI3K/AKT-directed perturbation necessarily suppresses ATF4/MTHFD2 in the tested persister state.

Therefore:

```text
ABSORPTION_STATUS := UNPROVED
```

and the route remains explicit.

## Residual object

```text
R_ISR_MTHFD2 :=
mTOR-supported ATF4/MTHFD2 stress-response and DNA-repair tolerance
under RAF/MEK pressure
```

This is a cross-state functional program rather than a Rambow phenotype label.

## Genotype/context boundary

The strongest direct 2026 experiments center on NRAS-, NF1-, and KIT-associated melanoma models treated with pan-RAF plus MEK inhibition.

```text
DO_NOT_INFER :=
universal dependence across every BRAF-V600, NRAS, NF1, KIT,
triple-wild-type, or immunotherapy-only melanoma context
```

The route should therefore be retained with its treatment/genotype context.

## Relationship to other retained metabolic programs

### CSE/H2S-persulfide

CSE-dependent sulfur/redox buffering and ATF4/MTHFD2 DNA-repair support are distinct experimentally described tolerance programs.

```text
DO_NOT_COLLAPSE := R_ISR_MTHFD2 into R_CSE_CROSS_STATE
```

### Pigmented/OXPHOS and SMC/peroxisome-UGCG

MTHFD2 participates in mitochondrial one-carbon metabolism, but that does not establish phenotype identity with MITF-high pigmented or CD36+ SMC persisters.

```text
DO_NOT_COLLAPSE := R_ISR_MTHFD2 into C_PIGMENTED
DO_NOT_COLLAPSE := R_ISR_MTHFD2 into C_SMC_METABOLIC
```

## Weakest missing object

```text
MISSING_OBJECT :=
a same-context epistasis certificate showing whether the existing abstract
PI3K/AKT control is sufficient to suppress the mTOR -> ATF4 -> MTHFD2
persister-survival route.

Required readouts:
1. PI3K/AKT pathway suppression,
2. mTOR activity,
3. ATF4 abundance/activity,
4. MTHFD2 abundance/activity,
5. DNA-damage/repair output,
6. functional persister survival,
7. in vivo relapse/tumor-control outcome.
```

If that implication is demonstrated, this route can be compressed into the existing PI3K/AKT control. If not, it requires its own functional control certificate.

## Boundary

```text
BOUNDARY :=
not proved that existing PI3K/AKT control absorbs the mTOR-ATF4-MTHFD2
melanoma persister route
```

## Evidence anchors

- Cai et al., Cell Death & Disease (2026), `mTOR inhibition enhances the antitumor efficacy of pan-RAF-MEK blockade by inhibiting the ATF4-MTHFD2 pathway`.
  - https://www.nature.com/articles/s41419-026-08836-5
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC13315934/
  - https://pubmed.ncbi.nlm.nih.gov/42091854/
- Shah et al., Cancer Science (2026), `MAPK Inhibitor-Tolerant Persister Cells in Melanoma: Mechanisms and Therapeutic Vulnerabilities`.
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC13394650/

## Next bounded action

```text
NEXT_ACTIONS :=
1. Retain R_ISR_MTHFD2 explicitly until same-context PI3K/AKT absorption is proved.
2. Search for melanoma experiments directly suppressing PI3K/AKT while measuring
   mTOR, ATF4, and MTHFD2 in persisters.
3. Compress the route immediately if that implication is demonstrated.
4. Otherwise add a distinct functional C_ISR_MTHFD2 control requirement.
```
