# Melanoma CD36 cellular-source identifiability — exact certificate

Date: 2026-11-15
Status: **PROVED (conditional mathematical mixture model) / COMPUTATION_PASS (synthetic exact rational checks) / PATIENT LEVEL VALIDATION OPEN**

## Scientific context and prior literature

- Chakraborty et al., *Cellular and spatial continuum of TAM functional states governs immune exclusion and dictates immune checkpoint resistance in melanoma*, *Genome Medicine* (2026). https://pmc.ncbi.nlm.nih.gov/articles/PMC13737523/ . LA-TAM melanoma macrophages show lipid-uptake programs, including CD36 and MSR1. Spatial and single-cell resources and analysis code: https://zenodo.org/records/22791840 ; https://zenodo.org/records/15124735 ; https://github.com/AG-Boerries/Melanoma_TAM_states_2026 . Candidate sources, not downloaded/tested here.
- *Scavenger Receptor CD36 in Tumor-Associated Macrophages Promotes Cancer Progression by Dampening Type I Interferon Signaling*, *Cancer Research* (2025). https://pmc.ncbi.nlm.nih.gov/articles/PMC11788022/ . Mouse melanoma evidence for CD36-high tumor-associated macrophages. Does not establish a patient-specific mixture coefficient.
- Existing BFF frozen seven-marker score includes a CD36 resistance-route *proxy*, not a uniquely identified tumor-intrinsic CD36 state. See `docs/status/MELANOMA_ROUTE_BURDEN_V2_DEFINITION_2026_09_06.md`. Its independent GSE91061 validation **failed** (AUROC 0.4913043478); that result is unchanged.

## Mathematical model and exact statements

Assume *linear molecule-count-compatible expression measurements on the same scale* and two exhaustive compartments (malignant and nonmalignant) with known effective mixing weight `0 < pi <= 1`:

```
b = pi * t + (1-pi) * i
```

Here `b` is bulk signal, `t` is tumor-compartment signal, and `i` is nonmalignant-compartment signal. `pi` is the relevant *signal contribution weight*, not automatically histologic tumor purity; per-cell RNA yield and extraction may alter its value. Nonnegative expressions are assumed in the physical examples.

**Theorem 1 (noninjectivity, 0 < pi < 1 and b > 0).** The map `(t,i) -> b` is not injective on nonnegative reals. E.g. `pi=1/2`, `(t,i)=(20,0)` and `(0,20)` both give `b=10`. More generally `0<=t<=b/pi`, `i=(b-pi*t)/(1-pi)>=0` gives infinitely many decompositions. At `b=0`, nonnegativity forces both zero. At `pi=1`, `b=t` uniquely identifies tumor expression.

**Theorem 2 (conditional inverse and stability).** If `pi>0`, `b` and `i` are known and the model holds, then

```
t = (b-(1-pi)*i)/pi
delta_t = (delta_b-(1-pi)*delta_i)/pi
|delta_t| <= (|delta_b|+(1-pi)*|delta_i|)/pi.
```

The inequality is sharp for opposing signed measurement errors. When `pi` is unknown, even exact `b=10,i=0` is consistent with `t=20,pi=1/2` and `t=40,pi=1/4`.

**Theorem 3 (interval bound under known pi).** If `0<pi<=1`, `b` is exact, `0<=i_min<=i<=i_max`, and a physically feasible decomposition exists, then

```
max(0,(b-(1-pi)*i_max)/pi) <= t
t <= (b-(1-pi)*i_min)/pi.
```

The bound is conditional on feasible nonnegative signals and fixed effective mixture coefficient. It is not a clinical estimate.

## Reproduction

`python3 -B tests/test_cell_source_identifiability.py` from repository root. Uses Python standard library only and exact rational arithmetic. Five purity fractions x 21 x 21 nonnegative expression pairs = **2,205 inverse cases**; **144 error-bound cases**; explicit equal-bulk collision and an unknown-purity counterexample.

Observed local ephemeral test (not Mac or GitHub CI), 2026-11-15:

```
EXACT_ARITHMETIC := PASS
INVERSE_CASES := 2205
ERROR_BOUND_CASES := 144
NONIDENTIFIABLE_COLLISIONS_FOUND := 1880
PURITY_UNKNOWN_COUNTEREXAMPLE := PASS
PATIENT_DATA := NOT_RUN
FPKM_LINEAR_MIXTURE_ASSUMPTION := NOT_ESTABLISHED
```

## Fail-closed translation gates

1. Do **not** apply the linear-mixture equation directly to sample-normalized FPKM/TPM/log-expression without establishing the abundance-to-expression measurement map, gene universe, sample-specific scaling, and effective mixture weights.
2. Before patient-level inference obtain source-grounded cell-type annotations, matched sample-to-patient identity, nonmalignant compartment expression, effective signal fractions, and assay uncertainty. Single-cell normalized values alone are not calibrated bulk mixture coefficients.
3. A prospective source-aware version must specify malignant and immune marker measurements, sample-level null model, cell composition control and independent validation before looking at response endpoints.
4. Do not modify v2 markers, directions, ECDF reference, calibrated coefficients, threshold or negative validation status; any successor is a separately numbered exploratory model.
5. The cited clinical associations are independent published evidence and not verification of BFF's patient-specific mechanism, treatment selection or causal impact.

```text
MATHEMATICAL_NONIDENTIFIABILITY := PROVED_CONDITIONAL
LINEAR_MIXTURE_INVERSE := PROVED_CONDITIONAL
EXACT_SYNTHETIC_TEST := COMPUTATION_PASS
PATIENT_CD36_SOURCE_DECONVOLUTION := NOT_RUN
BFF_CLINICAL_VALIDATION := OPEN
CANCER_CURE_ESTABLISHED := FALSE
```
