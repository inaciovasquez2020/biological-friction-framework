import Mathlib.LinearAlgebra.Quotient.Basic

noncomputable section

namespace BiologicalFriction

variable {R M : Type*}
variable [Ring R] [AddCommGroup M] [Module R M]

def quotientMapFromSubmodule
    (K S : Submodule R M) :
    K →ₗ[R] M ⧸ S :=
  S.mkQ.comp K.subtype

theorem quotientMapFromSubmodule_eq_zero_iff
    (K S : Submodule R M)
    (x : K) :
    quotientMapFromSubmodule K S x = 0 ↔ (x : M) ∈ S := by
  constructor
  · intro hx
    have hx' :
        S.mkQ (x : M) = S.mkQ (0 : M) := by
      simpa [quotientMapFromSubmodule] using hx
    have hmem : (x : M) - 0 ∈ S := by
      exact (Submodule.Quotient.eq S).mp hx'
    simpa using hmem
  · intro hx
    have hx' :
        S.mkQ (x : M) = S.mkQ (0 : M) := by
      exact (Submodule.Quotient.eq S).mpr (by simpa using hx)
    simpa [quotientMapFromSubmodule] using hx'

theorem quotientMapFromSubmodule_injective_of_inf_bot
    (K S : Submodule R M)
    (hKS : K ⊓ S = ⊥) :
    Function.Injective (quotientMapFromSubmodule K S) := by
  intro x y hxy
  apply Subtype.ext
  have hdiffS : (x : M) - (y : M) ∈ S := by
    exact (Submodule.Quotient.eq S).mp hxy
  have hdiffK : (x : M) - (y : M) ∈ K := by
    exact K.sub_mem x.property y.property
  have hdiffKS : (x : M) - (y : M) ∈ K ⊓ S := by
    exact ⟨hdiffK, hdiffS⟩
  have hzero : (x : M) - (y : M) = 0 := by
    exact (Submodule.mem_bot R).mp (by simpa [hKS] using hdiffKS)
  exact sub_eq_zero.mp hzero

theorem quotientMapFromSubmodule_injective_of_right_bot
    (K S : Submodule R M)
    (hS : S = ⊥) :
    Function.Injective (quotientMapFromSubmodule K S) := by
  apply quotientMapFromSubmodule_injective_of_inf_bot
  rw [hS]
  simpa using (inf_bot_eq : K ⊓ (⊥ : Submodule R M) = ⊥)

def LocalSpanFromFamily
    {ι : Type*}
    (L : ι → Submodule R M) :
    Submodule R M :=
  iSup L

theorem quotientMapFromSubmodule_injective_of_forall_local_bot
    {ι : Type*}
    (K : Submodule R M)
    (L : ι → Submodule R M)
    (hL : ∀ i, L i = ⊥) :
    Function.Injective (quotientMapFromSubmodule K (LocalSpanFromFamily L)) := by
  apply quotientMapFromSubmodule_injective_of_right_bot
  simp [LocalSpanFromFamily, hL]

end BiologicalFriction
