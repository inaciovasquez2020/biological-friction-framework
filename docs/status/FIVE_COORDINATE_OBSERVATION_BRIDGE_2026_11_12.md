# Five-coordinate dissipative observation bridge

Status: **COMPUTATION_PASS (exact rational finite certificate)** and **mathematical deduction (elementary)**; no new Lean formalization. This is a five-dimensional *state space*, not an extra spacetime dimension.

Base repository `main` inspected at `88dd078cec6a8e3d32adfb252cfdda67c0e686d7`. The pre-existing `proofs/observation-bridge/ObservationBridge.lean` gives an abstract observation-fiber criterion for exact decoding and a collision obstruction. This file specializes the criterion to a concrete linear/dynamical model without changing the biological or formal claim boundary.

## Defined five-dimensional state model

Let `X = Q^5`; write `x=(x1,x2,x3,x4,x5)`. Choose a rational diagonal evolution `T = diag(9/10,8/10,7/10,6/10,1/2)`. This equals `I - (1/10) diag(1,2,3,4,5)` and represents an **abstract** uncoupled dissipative toy model. Its energy is `E(x)=1/2 sum_i x_i^2`.

Every nonzero `x` satisfies `E(Tx)<E(x)` because each diagonal coefficient has magnitude strictly between zero and one. Iteration gives `T^t x` coordinatewise with rational powers. No biological process is identified with the five coordinates.

Define a four-channel observer `O4(x)=(x1,x2,x3,x4)` and a full five-channel observer `O5(x)=x`.

## Non-observability theorem and obstruction

For every integer `t>=0`,
`O4(T^t(x+q e5)) = O4(T^t x)` for every rational `q`.
Consequently even the full time series of four-channel observations cannot reconstruct the fifth initial coordinate.

The stacked time-observation matrix over any positive number `m` of time samples has rank exactly 4 for `O4`: the first four coordinate columns are independent at time zero and the fifth column vanishes at every time. The corresponding stack for `O5` has rank 5, since its time-zero block is the identity.

For `x=0` and `x'=e5`, observations agree for every time `t`, but `E(x)=0` while `E(x')=1/2`. Thus no exact decoder of **initial energy** exists from all four-channel observations. The repository's existing abstract observation-fiber theorem precisely explains this obstruction.

These are elementary algebraic deductions, with an independent exact finite regression checker. They do not require the universal quantifiers to be established by the finite sweep; the proof is the displayed diagonal form.

## Reproducibility

Run `python3 tools/verify_five_channel_observability.py`; standard library only, no data fetches. The enumerator checks all `5^5 = 3125` integer input vectors with coordinates in `[-2,2]` for eight transitions each: **25,000 exact rational transition checks**. It separately computes rational Gaussian-elimination ranks for time series with 1,2,3,5,9,20 samples, verifies the explicit observation collision, and checks strict energy decrease away from zero.

Optimized `python3 -O` execution exits with `INCOMPLETE` rather than silently bypassing assertions.

## Bridge and limits

The bridge is **BFF observation quotient ↔ five-coordinate dissipative geometry ↔ URF fiber obstruction**. It supplies a falsifiable mathematical modeling constraint: dynamics alone do not restore an unobserved coordinate when the dynamics preserve the observation kernel. This is a *counterexample* to automatic identifiability, not evidence for a biological fifth dimension.

**OPEN:** a justified map from measured biological features to five independent state coordinates, identification of the physical dissipation matrix from biological data, any spatial/temporal fifth-dimensional interpretation, and a Lean-verified theorem specialized to the five-coordinate system. No clinical, causal, therapeutic or empirical validation is claimed. Existing repository formalization dependencies and status locks remain unchanged.
