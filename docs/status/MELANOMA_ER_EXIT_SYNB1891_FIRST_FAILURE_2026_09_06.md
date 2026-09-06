# Melanoma ER-exit SYNB1891 candidate — first failed clause — 2026-09-06

## Status

`CONDITIONAL / EVIDENCE-GATE AUDIT`

This document tests a separate B16.F10 engineered-bacteria candidate against the ordered `EXIT_EVIDENCE_ADMISSIBLE` gate used by the spiderweb / ER-exit geometry. It does not modify the earlier IL-12+ADA candidate, identify a treatment recommendation, establish clinical efficacy, or claim cure.

## Candidate and evidence anchor

Leventhal et al., Nature Communications 2020, DOI `10.1038/s41467-020-16602-0`, evaluated the engineered *E. coli* Nissle strain SYNB1891 in B16.F10 melanoma.

For the single-dose pharmacology experiment, the paper reports that SYNB1891 produced undetectable tumors in some animals and that, at the high-dose arm, some scheduled day-7/day-10 tumor analyses could not recover a visible tumor mass on dissection. Figure 4 describes these animals as `N.T.D.` (`no tumor detected`).

In a separate repeated-dose B16.F10 efficacy experiment, SYNB1891 produced durable tumor rejections in approximately 30–40% of animals. That long-term experiment is supportive evidence but is not merged with the single-dose dissection cohort as if they were the same animals.

## Ordered gate test

The first evidence clause is:

```text
CLAUSE_1 :=
absence of viable malignant state on the declared measurement surface
```

SYNB1891 supplies a stronger measurement surface than the regression-only candidate:

```text
MEASUREMENT_SURFACE := gross primary-tumor site at dissection
OBSERVATION := no visible tumor mass / N.T.D. in some animals
TIMEPOINTS := study day 7 and/or day 10 as reported for the single-dose experiment
```

However, gross absence of a visible tumor mass is not a direct viable-melanoma assay. The retrieved report does not establish, for those same N.T.D. animals, a melanoma-cell viability assay, histopathologic clearance certificate, molecular residual-disease assay, or another measurement with a declared sensitivity sufficient to exclude sub-visible viable melanoma on the sampled surface.

Therefore:

```text
NO_VISIBLE_TUMOR_MASS_AT_DISSECTION
  !=
CERTIFIED_ABSENCE_OF_VIABLE_MALIGNANT_STATE
```

and

```math
EXIT\_EVIDENCE\_CLAUSE_1(SYNB1891,B16.F10)=\mathrm{UNPROVED}.
```

## Detection-scale interpretation

Let

```math
B(t) \ge 0
```

denote viable malignant burden on the relevant biological surface, and let a measurement modality `A` have detection threshold

```math
\delta_A > 0.
```

A negative observation from that modality supports only

```math
A(B(t))=\mathrm{negative}
\quad\Longrightarrow\quad
B_A(t)<\delta_A,
```

under the assay's stated operating assumptions. It does not imply

```math
B(t)=0.
```

For the reported SYNB1891 gross-dissection endpoint, the admissible interpretation is therefore

```math
B_{\mathrm{gross}}(t)<\delta_{\mathrm{gross}},
```

not biological zero.

This distinction is useful for the spiderweb / ER framework because an apparent exit can now be represented as a censored near-exit until an evidence surface with sufficient viable-disease sensitivity is supplied.

## Relative strengthening

```text
REGRESSION_ONLY_NEAR_EXIT
  <
NO_VISIBLE_TUMOR_AT_DISSECTION
  <
ASSAY-CERTIFIED_NO_DETECTABLE_VIABLE_MALIGNANCY
```

The SYNB1891 result therefore advances the candidate closer to the ER exit boundary without crossing it.

The separate repeated-dose B16.F10 durable-rejection result may become relevant to later recurrence/no-return clauses, but the ordered gate does not assign those clauses closure credit while Clause 1 is unresolved.

## Supplementary / protocol audit

The published Supplementary Information was inspected specifically for measurements that could discharge Clause 1.

For B16.F10, Supplementary Figure 4 adds:

```text
individual tumor volumes
bacterial abundance in tumor homogenates and blood
SYNB1891-specific qPCR for bacterial DNA in blood
```

These measurements characterize tumor size and bacterial pharmacology; they are not melanoma-cell viability or residual-disease assays for the N.T.D. animals.

Supplementary Figure 5 defines B16.F10 complete responders using a gross/palpation endpoint:

```text
C.R. := mice having no palpable tumor at the stated study timepoint
```

This remains a detection-limited near-exit rather than a viable-melanoma clearance certificate.

A text search of the retrieved Supplementary Information found no matched B16.F10 N.T.D. result under the terms:

```text
histology / histopathology
H&E
viability
microscopy
necrosis
```

The later phase-I SYNB1891 clinical-development report does include human tumor core biopsies and multiplex immunofluorescence, but those observations are from human subjects and cannot be transferred to the earlier B16.F10 N.T.D. animals.

The Nature Communications data-availability statement says additional data underlying figures and supplementary information are available from the corresponding authors on reasonable request. Therefore this audit establishes only that the required same-animal residual-viability certificate is absent from the retrieved public article/supplement/protocol surface; it does not establish that unpublished data do not exist.

Thus:

```text
PUBLIC_SUPPLEMENT_AUDIT_RESULT :=
no retrieved same-animal melanoma-directed measurement discharges CLAUSE_1
```

## Weakest missing object

```text
MISSING_OBJECT :=
a matched residual-viability certificate for the SYNB1891 B16.F10 N.T.D. animals
that declares the sampled tissue/compartments, melanoma-directed assay modality,
detection threshold, and observation time and establishes no detectable viable
malignant melanoma on that declared measurement surface
```

## Boundary

```text
BOUNDARY :=
SYNB1891 B16.F10 provides a stronger gross-dissection near-exit than regression alone,
but the retrieved article, Supplementary Information, and later clinical protocol/report
do not provide a same-animal viability-sensitive melanoma measurement establishing
Clause 1; therefore this candidate cannot yet instantiate the ER absorbing exit set H
```

## Next bounded action

```text
NEXT_ACTIONS :=
No admissible next step on this candidate from the retrieved public record without
additional same-animal residual-disease data from the original B16.F10 experiment.
```
