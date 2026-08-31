# Melanoma mTOR/PI3K–Polκ antagonistic coupling — 2026-08-31

## Status

`CONDITIONAL / LITERATURE-BOUNDED MODEL`

This document records a bounded cross-control interaction in a melanoma drug-tolerance / resistance graph. It is not clinical guidance, a treatment recommendation, or evidence of a cure.

## Question

After adding functional controls for PI3K/AKT survival and mTOR-supported ATF4/MTHFD2 persistence, does suppressing PI3K/mTOR create another melanoma stress-tolerance state that must be tracked?

## Result

`RESULT := PI3K/mTOR SUPPRESSION CAN INDUCE NUCLEAR Polκ; WHETHER THAT STATE OFFSETS THE DESIRED CONTROL REMAINS UNPROVED`

Temprine et al. showed in BRAF-V600E A375 melanoma cells that BRAF/MEK/ERK inhibition reduced mTORC1 output and drove DNA polymerase kappa (Polκ / POLK) from the cytoplasm into the nucleus. Direct inhibition of the PI3K/mTOR pathway with rapamycin, PP242, or LY294002 produced a similar nuclear Polκ shift, and did so more rapidly.

The observed state transition can be represented as:

```text
MAPK inhibition
  OR
PI3K/mTOR suppression
  OR
nutrient/ER stress
     -> nuclear Polκ enrichment
```

The same study showed that increasing nuclear Polκ reduced vemurafenib cytotoxicity in BRAF-V600E melanoma cells, whereas CRISPR-mediated POLK loss increased sensitivity at lower vemurafenib doses.

Therefore the graph must track a potential antagonistic coupling:

```text
implementation of C_RTK_SURVIVAL or C_ISR_MTHFD2
via PI3K/mTOR suppression
     -> nuclear Polκ stress state
     -> modest BRAF-inhibitor tolerance in the tested melanoma model
```

## Important correction: do not call this a proved mutator route

Polκ is an error-prone translesion polymerase in general biology, but the melanoma experiments did not show strong Polκ-driven mutagenesis in A375 cells.

The authors specifically reported little evidence that elevated Polκ was highly mutagenic in this melanoma context and suggested that noncatalytic or other functions may contribute to resistance.

Therefore:

```text
RETIRE :=
"Polκ is established as a melanoma resistance-generating mutator under MAPKi"
```

and:

```text
KEEP :=
"nuclear Polκ is an evidence-backed stress-tolerance / modest BRAFi-resistance state"
```

This distinguishes the route from the separately retained eIF4A -> 53BP1/NHEJ adaptive-mutability mechanism.

## Why this matters for the existing graph

Two current functional controls can plausibly be implemented through pathway suppression that was shown to induce nuclear Polκ:

```text
C_RTK_SURVIVAL := control PI3K/AKT-associated survival
C_ISR_MTHFD2  := control mTOR-supported ATF4/MTHFD2 persistence
```

The literature does not justify the implication:

```text
control(PI3K/mTOR)
  => all downstream melanoma stress-tolerance routes decrease
```

because nuclear Polκ moves in the opposite direction under PI3K/mTOR suppression in the tested A375 system.

## What is proved versus unproved

### Proved in the cited melanoma model

```text
PI3K/mTOR inhibition -> nuclear Polκ enrichment

forced/nuclear Polκ increase -> reduced vemurafenib cytotoxicity

POLK loss -> increased sensitivity to lower-dose vemurafenib
```

### Not proved

The study did not directly establish the complete causal composition:

```text
PI3K/mTOR inhibition
  -> Polκ induction
  -> failure of an mTOR/PI3K-based persister-control strategy in vivo
```

Nor did it test the 2026 mTOR->ATF4->MTHFD2 persister model with and without POLK in the same experiment.

Therefore:

```text
ANTAGONISTIC_COUPLING_STATUS := CONDITIONAL
```

## Functional safety constraint

Do not add a named Polκ inhibitor as a universal graph target. Instead retain an implementation-safety condition:

```text
C_IMPL_P3K_MTOR_SAFE :=
any implementation used to satisfy C_RTK_SURVIVAL or C_ISR_MTHFD2 must not
create a Polκ-associated stress-tolerant survivor population that preserves
or increases functional melanoma persistence
```

This is a model constraint, not a drug recommendation.

## Relationship to adaptive mutability

The current graph separately contains:

```text
C_TRANSLATION_PERSIST :=
control eIF4A-dependent persister survival and 53BP1/NHEJ adaptive mutability
```

The Polκ result must not be merged into that object at present:

```text
DO_NOT_COLLAPSE :=
Polκ stress tolerance into eIF4A/53BP1 adaptive mutability
```

because strong Polκ-driven mutagenesis was not demonstrated in the cited melanoma cells.

## Weakest missing object

```text
MISSING_OBJECT :=
a same-context melanoma epistasis experiment testing PI3K/mTOR-directed
persister control with POLK intact versus POLK suppressed, while measuring:

1. PI3K/mTOR pathway engagement,
2. nuclear Polκ abundance/localization,
3. ATF4 and MTHFD2 where C_ISR_MTHFD2 is being implemented,
4. short-term persister survival,
5. long-term resistant outgrowth,
6. mutation burden / resistance-genotype acquisition,
7. in vivo relapse or tumor-control outcome.
```

This experiment would determine whether Polκ is merely a biomarker of stress or a functionally important escape route from PI3K/mTOR-based control.

## Boundary

```text
BOUNDARY :=
PI3K/mTOR suppression can induce a nuclear Polκ state associated with modest
BRAF-inhibitor resistance in melanoma cells, but it is not proved that this
state defeats the current functional PI3K/mTOR control requirements in vivo
```

## Evidence anchors

- Temprine et al., Science Signaling (2020), `Regulation of the error-prone DNA polymerase Polκ by oncogenic signaling and its contribution to drug resistance`.
  - https://pubmed.ncbi.nlm.nih.gov/32345725/
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC7428051/
- Cai et al., Cell Death & Disease (2026), `mTOR inhibition enhances the antitumor efficacy of pan-RAF-MEK blockade by inhibiting the ATF4-MTHFD2 pathway`.
  - https://www.nature.com/articles/s41419-026-08836-5
  - https://pubmed.ncbi.nlm.nih.gov/42091854/

## Next bounded action

```text
NEXT_ACTIONS :=
1. Keep Polκ as a conditional antagonistic-coupling state, not a proved mutator node.
2. Add C_IMPL_P3K_MTOR_SAFE to the implementation-level graph.
3. Do not alter the abstract C_RTK_SURVIVAL or C_ISR_MTHFD2 requirements yet.
4. Recompute the residual graph using interaction-aware controls rather than
   assuming every control monotonically reduces all escape routes.
```
