# Melanoma mTOR-ATF4-MTHFD2 control boundary — 2026-08-31

## Status

`CONDITIONAL / LITERATURE-BOUNDED MODEL`

This document records a bounded structural result for a melanoma drug-tolerant-persister / resistance graph. It is not clinical guidance, a treatment recommendation, or evidence of a cure.

## Question

Does the existing abstract PI3K/AKT survival control absorb the 2026 melanoma persister pathway in which mTOR maintains ATF4 and MTHFD2 during RAF/MEK pressure, or must that pathway receive its own functional control requirement?

## Result

`RESULT := PI3K/AKT ABSORPTION NOT ESTABLISHED; PROMOTE A SEPARATE FUNCTIONAL ISR/MTHFD2 CONTROL`

Cai et al. (Cell Death & Disease, 2026) studied non-BRAF-V600 melanoma models treated with pan-RAF plus MEK inhibition. After prolonged treatment, persister cells retained/recovered ATF4 despite MAPK suppression. Direct mTOR inhibition suppressed ATF4 and its downstream target MTHFD2, increased DNA damage, reduced persister survival, and improved tumor control in vivo.

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

Human and murine melanomas resistant to the RAF/MEK combination also showed elevated ATF4/MTHFD2. Direct mTOR inhibition reduced ATF4/MTHFD2 and inhibited resistant-tumor outgrowth in the reported models.

## Why MAPK control alone is insufficient

In persister cells exposed for approximately 10 days, ATF4 was no longer suppressed by RAF/MEK treatment alone.

```text
DO_NOT_INFER := C_MAPK => control(ATF4-MTHFD2 persister route)
```

Earlier melanoma work independently showed mTORC1/ATF4 enrichment during rapid escape from BRAF inhibition; rapamycin reduced ATF4 and blocked the escapee rebound.

## Targeted PI3K/AKT absorption audit

`ABSORPTION_SEARCH := NO SAME-CONTEXT CERTIFICATE IDENTIFIED`

A targeted literature search was performed for melanoma experiments in which PI3K or AKT was directly suppressed while the same persister experiment measured:

```text
mTOR activity
ATF4
MTHFD2
functional persister survival
and/or relapse / tumor-control outcome
```

No such same-context certificate was identified.

The 2026 ATF4-MTHFD2 study diagrams the PI3K/AKT/mTOR pathway and notes that NRAS/NF1/KIT signaling can activate PI3K/mTOR, but the decisive perturbation used to suppress ATF4/MTHFD2 was direct mTOR inhibition with INK128/sapanisertib, not a PI3K- or AKT-directed perturbation.

Therefore:

```text
UNPROVED :=
C_PI3K_AKT
  => mTOR suppressed
  => ATF4 suppressed
  => MTHFD2 suppressed
  => persister survival / relapse suppressed
```

## AKT-only surrogate is specifically unsafe

Older BRAF-V600E melanoma experiments provide an additional structural warning: PI3K and BRAF signaling were shown to cooperate on mTORC1-dependent protein translation through effects described as AKT-independent, while pharmacologic AKT inhibition had only modest effects in those models.

That study is not a persister/ATF4-MTHFD2 experiment and therefore cannot resolve the current route. It does, however, rule out treating an abstract `AKT inhibition` implementation as automatically equivalent to control of all PI3K-to-mTOR signaling in melanoma.

```text
DO_NOT_INFER :=
AKT control => all melanoma mTORC1 control
```

## Relationship to the existing RTK-survival constraint

The previously encoded stromal/RTK repair was:

```text
C_RTK_SURVIVAL := control the shared PI3K/AKT survival branch
```

That object was introduced to cover routes such as:

```text
RTK -> PI3K -> AKT
PTEN loss -> PI3K -> AKT
HGF/MET -> PI3K -> AKT
```

The current route is experimentally certified at:

```text
mTOR -> ATF4 -> MTHFD2 -> DNA-repair-supported persistence
```

No repository-valid biological implication currently connects the first abstract control to suppression of the second route in the relevant persister context.

Therefore the graph must not compress them merely because conventional pathway diagrams place mTOR downstream of PI3K/AKT.

## Functional repair

Promote a separate functional control requirement:

```text
C_ISR_MTHFD2 :=
prevent mTOR-supported ATF4/MTHFD2 stress-response and DNA-repair activity
from sustaining RAF/MEK-tolerant melanoma persisters
```

This is a functional model constraint. It does not specify a drug, dose, schedule, or clinical intervention.

An experimentally supported implementation class in the cited 2026 models is direct mTOR suppression, but that implementation is not asserted to be unique or universally appropriate.

## Compression rule retained

Future compression remains admissible if a same-context epistasis certificate is produced.

```text
COMPRESSION_CONDITION :=
prove in melanoma persisters that the retained PI3K/AKT control necessarily
suppresses mTOR, ATF4, MTHFD2, and functional persistence/relapse
```

If that condition is established, `C_ISR_MTHFD2` can be absorbed into the broader survival control. Until then, it remains explicit.

## Residual object

```text
R_ISR_MTHFD2 :=
mTOR-supported ATF4/MTHFD2 stress-response and DNA-repair tolerance
under RAF/MEK pressure
```

## Genotype/context boundary

The strongest direct 2026 experiments center on NRAS-, NF1-, and KIT-associated melanoma models treated with pan-RAF plus MEK inhibition.

```text
DO_NOT_INFER :=
universal dependence across every BRAF-V600, NRAS, NF1, KIT,
triple-wild-type, or immunotherapy-only melanoma context
```

## Relationship to other retained metabolic programs

```text
DO_NOT_COLLAPSE := R_ISR_MTHFD2 into R_CSE_CROSS_STATE
DO_NOT_COLLAPSE := R_ISR_MTHFD2 into C_PIGMENTED
DO_NOT_COLLAPSE := R_ISR_MTHFD2 into C_SMC_METABOLIC
```

CSE-dependent sulfur/redox buffering, MITF/PGC1alpha mitochondrial adaptation, CD36+ peroxisome/UGCG metabolism, and ATF4/MTHFD2 DNA-repair support are experimentally distinct tolerance programs at the present evidence level.

## Weakest missing object

```text
MISSING_OBJECT :=
a same-context melanoma persister epistasis certificate proving or refuting:

C_PI3K_AKT
  => mTOR suppressed
  => ATF4 suppressed
  => MTHFD2 suppressed
  => functional persister survival / relapse suppressed

Required readouts:
1. PI3K and AKT pathway engagement,
2. mTOR activity,
3. ATF4 abundance/activity,
4. MTHFD2 abundance/activity,
5. DNA-damage/repair output,
6. functional persister survival,
7. in vivo relapse/tumor-control outcome.
```

## Boundary

```text
BOUNDARY :=
existing PI3K/AKT coverage is not proved to absorb the mTOR-ATF4-MTHFD2
melanoma persister route; C_ISR_MTHFD2 is therefore retained separately
```

## Evidence anchors

- Cai et al., Cell Death & Disease (2026), `mTOR inhibition enhances the antitumor efficacy of pan-RAF-MEK blockade by inhibiting the ATF4-MTHFD2 pathway`.
  - https://www.nature.com/articles/s41419-026-08836-5
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC13315934/
  - https://pubmed.ncbi.nlm.nih.gov/42091854/
- Hangauer/rapid-escape follow-up, Nature Communications (2021), `Melanoma subpopulations that rapidly escape MAPK pathway inhibition incur DNA damage and rely on stress signalling`.
  - https://www.nature.com/articles/s41467-021-21549-x
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC7979728/
- Silva et al. / melanoma PI3K signaling study (2014), `BRAFV600E cooperates with PI3K signaling, independent of AKT, to regulate melanoma cell proliferation`.
  - https://pubmed.ncbi.nlm.nih.gov/24425783/
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC3966216/
- Shah et al., Cancer Science (2026), `MAPK Inhibitor-Tolerant Persister Cells in Melanoma: Mechanisms and Therapeutic Vulnerabilities`.
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC13394650/

## Next bounded action

```text
NEXT_ACTIONS :=
1. Retain C_ISR_MTHFD2 as a distinct functional control requirement.
2. Do not substitute AKT-only control for the mTOR/ATF4/MTHFD2 certificate.
3. Re-run the residual graph with C_ISR_MTHFD2 treated as abstractly covered.
4. Return the first independent escape program that survives that augmented set.
```
