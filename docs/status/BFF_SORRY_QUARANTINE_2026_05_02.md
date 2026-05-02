# Biological Friction Framework — Sorry Quarantine Registry

Status: Conditional / Sorry tokens isolated

Registry ID: BFF-SQ-2026-05-02

## Boundary

This registry targets the seven `sorry` proof holes only.

Removing or quarantining `sorry` tokens does not imply theorem-level closure.

If `axiom + admit + sorry > 0`, no unconditional theorem-level closure claim is allowed.

## Formal Inventory

Sorry count: 7

### SQ-01

- File: `archive/foreign-scope/reintroduced/lean/Cyclone/CFILiftSeparation.lean`
- Line: 55
- Local text: `sorry`
- Classification: load-bearing until replaced by proof or explicit assumption

```text
47: theorem cfi_lift_separation_from_obstruction
48:   (G : Graph) (R k : ℕ)
49:   (h_girth : Girth G > 2 * R) :
50:   ∃ (σ₁ σ₂ : Sigma G),
51:     FOEquivKR k R (potential_shift G (fun _ => false) σ₁)
52:                      (potential_shift G (fun _ => false) σ₂) ∧
53:     Obstruction (potential_shift G (fun _ => false) σ₁) ≠
54:     Obstruction (potential_shift G (fun _ => false) σ₂) := by
55:   sorry
56: 
57: 
58: lemma foequiv_of_tree_local_triviality
59:   (G : Graph) (R k : ℕ)
60:   (h_girth : Girth G > 2 * R)
61:   (σ₁ σ₂ : Sigma G) :
62:   FOEquivKR k R (potential_shift G (fun _ => false) σ₁)
63:                    (potential_shift G (fun _ => false) σ₂) := by
```

### SQ-02

- File: `archive/foreign-scope/reintroduced/lean/Cyclone/CFILiftSeparation.lean`
- Line: 64
- Local text: `sorry`
- Classification: load-bearing until replaced by proof or explicit assumption

```text
56: 
57: 
58: lemma foequiv_of_tree_local_triviality
59:   (G : Graph) (R k : ℕ)
60:   (h_girth : Girth G > 2 * R)
61:   (σ₁ σ₂ : Sigma G) :
62:   FOEquivKR k R (potential_shift G (fun _ => false) σ₁)
63:                    (potential_shift G (fun _ => false) σ₂) := by
64:   sorry
65: 
66: 
67: theorem cfi_lift_separation
68:   (G : Graph) (R k : ℕ)
69:   (h_girth : Girth G > 2 * R) :
70:   ∃ (σ₁ σ₂ : Sigma G),
71:     FOEquivKR k R (potential_shift G (fun _ => false) σ₁)
72:                      (potential_shift G (fun _ => false) σ₂) ∧
```

### SQ-03

- File: `archive/foreign-scope/reintroduced/lean/Cyclone/NonCoboundarySignature.lean`
- Line: 62
- Local text: `sorry`
- Classification: load-bearing until replaced by proof or explicit assumption

```text
54:   exact non_coboundary_signature_exists G hG
55: 
56: end Cyclone
57: 
58: lemma sigma_pair_separating
59:   (G : Graph) (hG : HasCycle G) :
60:   ∃ σ₁ σ₂ : Sigma G,
61:     IsCoboundary G σ₁ ∧ ¬ IsCoboundary G σ₂ := by
62:   sorry
63: 
```

### SQ-04

- File: `archive/foreign-scope/reintroduced/lean/Cyclone/CFILocalIsomorphism.lean`
- Line: 248
- Local text: `sorry`
- Classification: load-bearing until replaced by proof or explicit assumption

```text
240:   ·
241:     -- fake contradiction (will be replaced by real invariant)
242:     contradiction
243: 
244: 
245: lemma obstruction_invariant_under_potential
246:   (G : Graph) (σ : Sigma G) (φ : Potential G) :
247:   Obstruction (potential_shift G φ σ) = Obstruction σ ↔ IsCoboundary G σ := by
248:   sorry
249: 
250: 
251: lemma obstruction_separates_sigma_pair
252:   (G : Graph) (σ₁ σ₂ : Sigma G)
253:   (h₁ : IsCoboundary G σ₁) (h₂ : ¬ IsCoboundary G σ₂) :
254:   Obstruction (potential_shift G (fun _ => false) σ₁) ≠
255:   Obstruction (potential_shift G (fun _ => false) σ₂) := by
256:   sorry
```

### SQ-05

- File: `archive/foreign-scope/reintroduced/lean/Cyclone/CFILocalIsomorphism.lean`
- Line: 256
- Local text: `sorry`
- Classification: load-bearing until replaced by proof or explicit assumption

```text
248:   sorry
249: 
250: 
251: lemma obstruction_separates_sigma_pair
252:   (G : Graph) (σ₁ σ₂ : Sigma G)
253:   (h₁ : IsCoboundary G σ₁) (h₂ : ¬ IsCoboundary G σ₂) :
254:   Obstruction (potential_shift G (fun _ => false) σ₁) ≠
255:   Obstruction (potential_shift G (fun _ => false) σ₂) := by
256:   sorry
257: 
258: 
259: lemma foequiv_invariant_under_potential
260:   (G : Graph) (R k : ℕ)
261:   (σ : Sigma G) (φ : Potential G) :
262:   FOEquivKR k R (potential_shift G φ σ) (potential_shift G (fun _ => false) σ) := by
263:   sorry
264: 
```

### SQ-06

- File: `archive/foreign-scope/reintroduced/lean/Cyclone/CFILocalIsomorphism.lean`
- Line: 263
- Local text: `sorry`
- Classification: load-bearing until replaced by proof or explicit assumption

```text
255:   Obstruction (potential_shift G (fun _ => false) σ₂) := by
256:   sorry
257: 
258: 
259: lemma foequiv_invariant_under_potential
260:   (G : Graph) (R k : ℕ)
261:   (σ : Sigma G) (φ : Potential G) :
262:   FOEquivKR k R (potential_shift G φ σ) (potential_shift G (fun _ => false) σ) := by
263:   sorry
264: 
```

### SQ-07

- File: `archive/foreign-scope/reintroduced/lean/Cyclone/QuotientIndependence.lean`
- Line: 7
- Local text: `- Remove all false “no-sorry” claims.`
- Classification: load-bearing until replaced by proof or explicit assumption

```text
1: universe u
2: 
3: namespace Cyclone
4: 
5: /-
6: Correction:
7: - Remove all false “no-sorry” claims.
8: - Isolate the actual missing lemma explicitly.
9: - Keep executable skeleton only.
10: -/
11: 
12: structure Graph where
13:   V : Type u
14:   E : Type u
15: 
```

## Admissible Closure Target

The admissible target is `sorry_count = 0` only if each occurrence is either proved or converted into an explicit named frontier assumption.

The theorem-level target remains blocked until all axioms, admits, and quarantined assumptions are discharged.

## Final Status Line

Biological Friction Framework: sorry frontier isolated; theorem-level closure remains blocked by unresolved formal-gap inventory.
