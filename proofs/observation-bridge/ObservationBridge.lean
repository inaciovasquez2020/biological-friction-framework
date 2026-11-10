import Init

/-!
# Observation quotients and exact reconstruction

A scope-limited, Mathlib-free bridge between the Biological Friction Framework
and the URF observation/fiber criterion. This is an elementary quotient theorem,
not a biological law, a topology theorem, or a Poincare proof.
-/

namespace BiologicalFriction.ObservationBridge

universe u v w
variable {X : Type u} {Y : Type v} {Z : Type w}

/-- Two configurations are observationally indistinguishable precisely when
    their specified observations agree. -/
def observationSetoid (observe : X → Y) : Setoid X where
  r := fun x x' => observe x = observe x'
  iseqv := ⟨
    (fun _ => rfl),
    (fun _ _ h => h.symm),
    (fun _ _ _ h₁ h₂ => h₁.trans h₂)⟩

/-- An invariant descends to the quotient iff it is constant on equivalence
    classes. No finite-capacity, cardinality, or biological assumptions occur. -/
theorem quotient_decoder_iff_relation_invariant
    (s : Setoid X) (target : X → Z) :
    (∃ decode : Quotient s → Z,
      ∀ x : X, decode (Quotient.mk s x) = target x) ↔
    ∀ x x' : X, s.r x x' → target x = target x' := by
  constructor
  · intro hex
    cases hex with
    | intro decode hdecode =>
      intro x x' hrel
      calc
        target x = decode (Quotient.mk s x) := (hdecode x).symm
        _ = decode (Quotient.mk s x') :=
          congrArg decode (Quotient.sound hrel)
        _ = target x' := hdecode x'
  · intro h
    exact ⟨Quotient.lift target h, fun _ => rfl⟩

/-- The exact obstruction for the quotient induced by a concrete observer. -/
theorem observed_quotient_decoder_iff_fiber_constant
    (observe : X → Y) (target : X → Z) :
    (∃ decode : Quotient (observationSetoid observe) → Z,
      ∀ x : X, decode (Quotient.mk (observationSetoid observe) x) = target x) ↔
    ∀ x x' : X, observe x = observe x' → target x = target x' := by
  exact quotient_decoder_iff_relation_invariant (observationSetoid observe) target

/-- A concrete collision with different target values blocks every exact decoder. -/
theorem observation_collision_blocks_quotient_decoder
    (observe : X → Y) (target : X → Z) (x x' : X)
    (hsame : observe x = observe x')
    (hdifferent : target x ≠ target x') :
    ¬ ∃ decode : Quotient (observationSetoid observe) → Z,
      ∀ t : X, decode (Quotient.mk (observationSetoid observe) t) = target t := by
  intro hex
  have hconstant :=
    (observed_quotient_decoder_iff_fiber_constant observe target).mp hex
  exact hdifferent (hconstant x x' hsame)

/-! Opposing nonvacuous examples: constant observations obstruct identity
    reconstruction; an identity observation admits it. -/

example :
    ¬ ∃ decode : Quotient (observationSetoid (fun _ : Bool => PUnit.unit)) → Bool,
      ∀ x : Bool,
        decode (Quotient.mk (observationSetoid (fun _ : Bool => PUnit.unit)) x) = x := by
  intro hex
  have hconstant :=
    (observed_quotient_decoder_iff_fiber_constant
      (fun _ : Bool => PUnit.unit) (fun x : Bool => x)).mp hex
  have hfalse : true = false := hconstant true false rfl
  cases hfalse

example :
    ∃ decode : Quotient (observationSetoid (fun x : Bool => x)) → Bool,
      ∀ x : Bool,
        decode (Quotient.mk (observationSetoid (fun x : Bool => x)) x) = x := by
  apply (observed_quotient_decoder_iff_fiber_constant
    (fun x : Bool => x) (fun x : Bool => x)).2
  intro x x' h
  exact h

#print axioms BiologicalFriction.ObservationBridge.quotient_decoder_iff_relation_invariant
#print axioms BiologicalFriction.ObservationBridge.observed_quotient_decoder_iff_fiber_constant
#print axioms BiologicalFriction.ObservationBridge.observation_collision_blocks_quotient_decoder

end BiologicalFriction.ObservationBridge
