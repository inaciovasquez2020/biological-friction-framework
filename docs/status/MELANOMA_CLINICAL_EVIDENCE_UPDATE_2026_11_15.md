# Melanoma clinical evidence update — 2026-11-15

Status: **PRIMARY-SOURCE REVIEWED / BFF MODEL NOT REVALIDATED**
Repository: `inaciovasquez2020/biological-friction-framework`
Baseline `main`: `27da717b3e6dadb86fe98d3a3f1acf5532471430`

## 1. INTerpath-001: individualized neoantigen therapy after resection

Primary publication: Long et al., *Intismeran Autogene plus Pembrolizumab for Resected Stage IIB to IV Melanoma*, *New England Journal of Medicine*, November 11, 2026. DOI: https://doi.org/10.1056/NEJMoa2609762

- Double-blind randomized phase 3 trial in completely resected stage IIB–IV cutaneous melanoma.
- Total randomized: **1,137**; intismeran autogene plus pembrolizumab: **757**; placebo plus pembrolizumab: **380**. Median follow-up: **24.6 months**.
- **24-month recurrence-free survival:** 82.2% vs 70.0%; absolute difference **12.2 percentage points**, two-sided **p<0.001**.
- The publication uses **piecewise hazard ratios**: before six months **0.99** (95% CI 0.66–1.49), after six months **0.42** (95% CI 0.30–0.58). Do not report a single proportional-hazards HR of 0.58 as though it were the published result.
- **24-month distant-metastasis-free survival:** 88.5% vs 80.2%, p=0.002; piecewise HRs **1.01** (95% CI 0.58–1.79) before six months and **0.50** (95% CI 0.34–0.73) thereafter.
- Grade ≥3 adverse events: 23.6% vs 20.3%. Overall survival benefit is not established by these endpoints; the therapy remained investigational as of this record.

**BFF relevance (hypothesis only):** Adjuvant neoantigen-specific immune stimulation is a candidate intervention on residual-disease recurrence dynamics. It does not establish or calibrate BFF escape routes, patient-level state transitions, or predictive accuracy. The completely resected adjuvant population must remain distinct from advanced-disease response cohorts.

## 2. Tudriqev plus nivolumab after anti-PD-1 progression

Primary regulator: FDA, August 6, 2026:
https://www.fda.gov/drugs/cancer-approvals/fda-grants-accelerated-approval-vusolimogene-oderparepvec-wtpg-combination-nivolumab-melanoma

FDA product entry: https://www.fda.gov/vaccines-blood-biologics/tudriqev

- FDA granted **accelerated approval** to intratumoral vusolimogene oderparepvec-wtpg (Tudriqev) **plus nivolumab** for adults with unresectable advanced cutaneous melanoma progressing on prior anti-PD-1-based therapy.
- IGNYTE was **open-label and single-arm**: 140 enrolled; **91** with ≥1 noninjected lesion constituted the efficacy-evaluable population.
- Objective response rate **24.2%** (95% CI 15.8–34.3); median duration of response **14.1 months** (95% CI 10.7–not reached).
- The FDA requires confirmatory clinical-benefit evidence. The ongoing IGNYTE-3 randomized confirmatory study evaluates overall survival. The single-arm response rate does not establish superiority to nivolumab or a causal effect of the viral component.
- Confirmatory obligation: https://www.fda.gov/drugs/cancer-approvals/ongoing-cancer-accelerated-approvals

**BFF relevance (hypothesis only):** Prior PD-1 treatment failure and local viral therapy plus immunotherapy may motivate an explicitly labeled intervention/state-graph question. Aggregate ORR and DOR are not measurements of BFF-specific route elimination, resistance topology, individual prognosis, or clinical utility.

## 3. Validation gates and compatibility with existing records

1. Keep cohort strata distinct: `adjuvant_resected_stage_IIB_IV` vs `advanced_unresectable_prior_PD1_progression`.
2. Preserve endpoint semantics: RFS, DMFS, ORR, DOR and overall survival are not interchangeable; hazard ratios and 24-month proportions cannot be interchanged.
3. Record the population denominators and source dates before any replication.
4. Do not assign graph edges, fit transition probabilities, recalibrate the frozen seven-marker route-burden feature, or claim response prediction from aggregate trial endpoints.
5. Preserve the negative external validation already documented in `docs/status/MELANOMA_GSE294273_UNTESTED_SOURCE_2026_11_02.md`: GSE91061 frozen-v2 AUROC 0.4913 and failure of its promotion gate.
6. A future biological inference requires patient-level longitudinal intervention, tissue-state and outcome data with frozen endpoints, sampling plans and independent testing.

## 4. Evidence/status ledger

```text
SOURCE_RETRIEVAL_DATE := 2026-11-15
NEJM_PRIMARY_PUBLICATION_REVIEWED := TRUE
FDA_PRIMARY_REGULATORY_RECORD_REVIEWED := TRUE
INTerpath001_PHASE3_RFS_DIFFERENCE_REPORTED := TRUE
INTISMERAN_FDA_APPROVED := FALSE
TUDRIQEV_ACCELERATED_APPROVAL := TRUE
TUDRIQEV_CONFIRMATORY_BENEFIT_ESTABLISHED := FALSE
BFF_PATIENT_LEVEL_REANALYSIS := NOT_RUN
BFF_STATE_TRANSITIONS_IDENTIFIED := FALSE
BFF_PREDICTIVE_EXTERNAL_VALIDATION := NOT_ESTABLISHED
BFF_CLINICAL_UTILITY := NOT_ESTABLISHED
BFF_CURE_CLAIM := FALSE
```

**BOUNDARY:** This is a sourced literature update and hypothesis-registration note, not a BFF biological mechanism proof, clinical validation, therapeutic recommendation or cure certificate.
