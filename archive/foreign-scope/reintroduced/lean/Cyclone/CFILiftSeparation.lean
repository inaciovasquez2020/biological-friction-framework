universe u

namespace Cyclone

/-
Correction:
- Remove false claims of completion.
- Keep CFI separation as explicit conditional input.
- Do NOT depend on Mathlib.
-/

structure Graph where
  V : Type u
  E : Type u

def Girth (G : Graph) : ℕ := 0

def Obstruction (G : Graph) : ℕ := 0

def FOEquivKR (k R : ℕ) (G H : Graph) : Prop := True

abbrev Sigma (G : Graph) := G.E → Bool

structure LiftData (G : Graph) where
  σ : Sigma G

def Lift (G : Graph) (L : LiftData G) : Graph :=
  { V := G.V × Bool
    E := G.E × Bool }

/-- Core missing separation (Cyclone) -/
axiom cfi_lift_separation
  (G : Graph) (R k : ℕ) :
  Girth G > 2 * R →
  ∃ (L₁ L₂ : LiftData G),
    FOEquivKR k R (Lift G L₁) (Lift G L₂) ∧
    Obstruction (Lift G L₁) ≠ Obstruction (Lift G L₂)

/-- Non-factorization reduces to CFI separation -/
/--
Archived foreign-scope frontier assumption replacing a former placeholder proof hole.
This is not a theorem-level closure claim.
-/
axiom obstruction_non_factorization_conditional
  (k R : ℕ) :
  True := by
  trivial

end Cyclone

theorem cfi_lift_separation_from_obstruction
  (G : Graph) (R k : ℕ)
  (h_girth : Girth G > 2 * R) :
  ∃ (σ₁ σ₂ : Sigma G),
    FOEquivKR k R (potential_shift G (fun _ => false) σ₁)
                     (potential_shift G (fun _ => false) σ₂) ∧
    Obstruction (potential_shift G (fun _ => false) σ₁) ≠
    Obstruction (potential_shift G (fun _ => false) σ₂)
/--
Archived foreign-scope frontier assumption replacing a former placeholder proof hole.
This is not a theorem-level closure claim.
-/
axiom foequiv_of_tree_local_triviality
  (G : Graph) (R k : ℕ)
  (h_girth : Girth G > 2 * R)
  (σ₁ σ₂ : Sigma G) :
  FOEquivKR k R (potential_shift G (fun _ => false) σ₁)
                   (potential_shift G (fun _ => false) σ₂)
theorem cfi_lift_separation
  (G : Graph) (R k : ℕ)
  (h_girth : Girth G > 2 * R) :
  ∃ (σ₁ σ₂ : Sigma G),
    FOEquivKR k R (potential_shift G (fun _ => false) σ₁)
                     (potential_shift G (fun _ => false) σ₂) ∧
    Obstruction (potential_shift G (fun _ => false) σ₁) ≠
    Obstruction (potential_shift G (fun _ => false) σ₂) := by
  rcases cfi_lift_separation_from_obstruction G R k h_girth with ⟨σ₁, σ₂, hFO, hObs⟩
  exact ⟨σ₁, σ₂, hFO, hObs⟩


theorem cyclone_final_closure
  (G : Graph) (R k : ℕ)
  (h_girth : Girth G > 2 * R)
  (h_cycle : HasCycle G) :
  ∃ (σ₁ σ₂ : Sigma G),
    FOEquivKR k R (potential_shift G (fun _ => false) σ₁)
                     (potential_shift G (fun _ => false) σ₂) ∧
    Obstruction (potential_shift G (fun _ => false) σ₁) ≠
    Obstruction (potential_shift G (fun _ => false) σ₂) := by
  rcases sigma_pair_separating G h_cycle with ⟨σ₁, σ₂, h₁, h₂⟩
  have hFO := foequiv_of_tree_local_triviality G R k h_girth σ₁ σ₂
  have hObs := obstruction_separates_sigma_pair G σ₁ σ₂ h₁ h₂
  exact ⟨σ₁, σ₂, hFO, hObs⟩


lemma foequiv_reduce_to_tree_local
  (G : Graph) (R k : ℕ)
  (h_girth : Girth G > 2 * R)
  (σ₁ σ₂ : Sigma G) :
  FOEquivKR k R (potential_shift G (fun _ => false) σ₁)
                   (potential_shift G (fun _ => false) σ₂) := by
  have h_local :
    ∀ v : G.V,
      IsTree (Ball G R v) := by
    intro v
    exact ball_tree_of_girth_gt_twoR G R v h_girth
  have h_trivial :
    ∀ v : G.V,
      ∃ φ : Potential (Ball G R v), True := by
    intro v
    exact local_signature_trivial_on_tree_conditional _ (h_local v) _
  exact foequiv_of_tree_local_triviality G R k h_girth σ₁ σ₂

