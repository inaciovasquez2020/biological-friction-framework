import UniversalRecovery
import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Analysis.Convex.SpecificFunctions.Basic

open scoped BigOperators

namespace BFF.HiddenDissipation

open URF.Transfer

noncomputable def edgeEntropy
    (t u : ℝ) : ℝ :=
  Real.sqrt u * force t (Real.sqrt u)

noncomputable def entropyCoefficient
    (t : ℝ) (k : ℕ) : ℝ :=
  (2 / (2*(k : ℝ)+1)) / t^(2*k+1)

theorem edgeEntropy_hasSum
    (t u : ℝ) (hu : 0 ≤ u)
    (hst : Real.sqrt u < t) :
    HasSum
      (fun k : ℕ =>
        entropyCoefficient t k * u^(k+1))
      (edgeEntropy t u) := by
  have ht : 0 < t :=
    (Real.sqrt_nonneg u).trans_lt hst
  let r := Real.sqrt u / t
  have hr0 : 0 ≤ r :=
    div_nonneg (Real.sqrt_nonneg _) ht.le
  have hr1 : r < 1 :=
    (div_lt_one ht).2 hst
  have hr : |r| < 1 := by
    rw [abs_of_nonneg hr0]
    exact hr1
  have h :=
    Real.hasSum_log_sub_log_of_abs_lt_one hr
  have hq :
      (1+r)/(1-r) =
        (t+Real.sqrt u)/(t-Real.sqrt u) := by
    dsimp [r]
    field_simp [ne_of_gt ht,
      ne_of_gt (sub_pos.mpr hst)] <;> ring
  have hlog :
      Real.log (1+r)-Real.log (1-r) =
        force t (Real.sqrt u) := by
    rw [← Real.log_div
      (ne_of_gt (by linarith : 0 < 1+r))
      (ne_of_gt (by linarith : 0 < 1-r))]
    rw [hq]
    rfl
  have hterm :
      (fun k : ℕ =>
        Real.sqrt u *
          (2 * (1/(2*(k : ℝ)+1)) *
            r^(2*k+1))) =
      (fun k : ℕ =>
        entropyCoefficient t k * u^(k+1)) := by
    funext k
    have hp :
        Real.sqrt u * Real.sqrt u^(2*k+1) =
          u^(k+1) := by
      calc
        Real.sqrt u * Real.sqrt u^(2*k+1) =
            Real.sqrt u^(2*k+1+1) :=
          (pow_succ' _ _).symm
        _ = Real.sqrt u^(2*(k+1)) := by
          congr 1
        _ = (Real.sqrt u^2)^(k+1) := by
          rw [pow_mul]
        _ = u^(k+1) := by
          rw [Real.sq_sqrt hu]
    dsimp only [r]
    rw [div_pow]
    calc
      Real.sqrt u *
          (2 * (1/(2*(k : ℝ)+1)) *
            (Real.sqrt u^(2*k+1)/t^(2*k+1))) =
          entropyCoefficient t k *
            (Real.sqrt u * Real.sqrt u^(2*k+1)) := by
              unfold entropyCoefficient
              ring
      _ = _ := by rw [hp]
  unfold edgeEntropy
  rw [← hterm,← hlog]
  exact h.mul_left (Real.sqrt u)

theorem power_chord
    (k : ℕ) (x y z : ℝ)
    (hx : 0 ≤ x) (hxy : x ≤ y)
    (hyz : y ≤ z) :
    (z-x)*y^(k+1) ≤
      (z-y)*x^(k+1)+(y-x)*z^(k+1) := by
  by_cases he : x = z
  · have hy : y = z := by linarith
    subst x
    subst y
    simp
  · have hd : 0 < z-x :=
      sub_pos.mpr
        (lt_of_le_of_ne (hxy.trans hyz) he)
    have hz : 0 ≤ z :=
      hx.trans (hxy.trans hyz)
    have hk : (1 : ℝ) ≤ ((k+1 : ℕ) : ℝ) := by
      exact_mod_cast (Nat.succ_le_succ (Nat.zero_le k))
    have hC :
        ConvexOn ℝ (Set.Ici (0 : ℝ))
          (fun v : ℝ => v^(k+1)) := by
      simpa only [Real.rpow_natCast] using
        (_root_.convexOn_rpow hk)
    let a := (z-y)/(z-x)
    let b := (y-x)/(z-x)
    have ha : 0 ≤ a :=
      div_nonneg (sub_nonneg.mpr hyz) hd.le
    have hb : 0 ≤ b :=
      div_nonneg (sub_nonneg.mpr hxy) hd.le
    have hab : a+b = 1 := by
      dsimp [a,b]
      field_simp [ne_of_gt hd] <;> ring
    have harg : a*x+b*z = y := by
      dsimp [a,b]
      field_simp [ne_of_gt hd] <;> ring
    have hh := hC.2
      (show x ∈ Set.Ici (0 : ℝ) from hx)
      (show z ∈ Set.Ici (0 : ℝ) from hz)
      ha hb hab
    change (a*x+b*z)^(k+1) ≤
      a*x^(k+1)+b*z^(k+1) at hh
    rw [harg] at hh
    have hm :=
      mul_le_mul_of_nonneg_left hh hd.le
    have heq :
        (z-x)*(a*x^(k+1)+b*z^(k+1)) =
          (z-y)*x^(k+1)+(y-x)*z^(k+1) := by
      dsimp [a,b]
      field_simp [ne_of_gt hd] <;> ring
    rw [heq] at hm
    exact hm

theorem edgeEntropy_chord
    (t x y z : ℝ)
    (hx : 0 ≤ x) (hxy : x ≤ y)
    (hyz : y ≤ z)
    (hst : Real.sqrt z < t) :
    (z-x)*edgeEntropy t y ≤
      (z-y)*edgeEntropy t x +
      (y-x)*edgeEntropy t z := by
  have hy := hx.trans hxy
  have hz := hy.trans hyz
  have ht := (Real.sqrt_nonneg z).trans_lt hst
  have hsx :=
    edgeEntropy_hasSum t x hx
      ((Real.sqrt_le_sqrt (hxy.trans hyz)).trans_lt hst)
  have hsy :=
    edgeEntropy_hasSum t y hy
      ((Real.sqrt_le_sqrt hyz).trans_lt hst)
  have hsz :=
    edgeEntropy_hasSum t z hz hst
  refine hasSum_le ?_
    (hsy.mul_left (z-x))
    ((hsx.mul_left (z-y)).add
      (hsz.mul_left (y-x)))
  intro k
  have hc : 0 ≤ entropyCoefficient t k := by
    unfold entropyCoefficient
    positivity
  have h :=
    mul_le_mul_of_nonneg_left
      (power_chord k x y z hx hxy hyz) hc
  change
    (z-x)*(entropyCoefficient t k*y^(k+1)) ≤
      (z-y)*(entropyCoefficient t k*x^(k+1)) +
      (y-x)*(entropyCoefficient t k*z^(k+1))
  nlinarith only [h]

theorem entropySquared_chordConvex
    {n : ℕ} (t : Fin n → ℝ) (M : ℝ)
    (hM : 0 ≤ M) (ht : ∀ i, M < t i) :
    ChordConvex (entropySquared t) (M^2) := by
  intro x y z hx hxy hyz hz
  have hs : Real.sqrt z ≤ M := by
    calc
      Real.sqrt z ≤ Real.sqrt (M^2) :=
        Real.sqrt_le_sqrt hz
      _ = M := by
        rw [Real.sqrt_sq_eq_abs,abs_of_nonneg hM]
  unfold entropySquared dissipation
  simp only [Finset.mul_sum]
  rw [← Finset.sum_add_distrib]
  apply Finset.sum_le_sum
  intro i hi
  exact edgeEntropy_chord
    (t i) x y z hx hxy hyz
    (hs.trans_lt (ht i))

theorem noisy_ring_curvature_minimax_unconditional
    {n : ℕ}
    (p t : Fin (n+3) → ℝ) (M ε : ℝ)
    (hp : ∀ i, 0 < p i) (hs : ∑ i,p i = 1)
    (hM : 0 ≤ M) (ht : ∀ i, M < t i)
    (hε : 0 ≤ ε) (i : Fin (n+3)) :
    let X0 := buildRing p t M hp hs ht
      ⟨0,by simpa using hM⟩
    IsLeast
      {E : ℝ |
        Recoverable
          (Noisy
            (fun j : {j : ℝ // |j| ≤ M} =>
              returnCurvature
                (buildRing p t M hp hs ht j) i) ε)
          (fun j =>
            entropyProduction
              (buildRing p t M hp hs ht j)) E}
      ((entropySquared t (M^2) -
        entropySquared t
          (M^2-min (M^2)
            (2*ε/curvatureWeight X0 i)))/2) := by
  exact noisy_ring_curvature_minimax
    p t M ε hp hs hM ht hε i
    (entropySquared_chordConvex t M hM ht)

end BFF.HiddenDissipation

#print axioms BFF.HiddenDissipation.edgeEntropy_hasSum
#print axioms BFF.HiddenDissipation.power_chord
#print axioms BFF.HiddenDissipation.edgeEntropy_chord
#print axioms BFF.HiddenDissipation.entropySquared_chordConvex
#print axioms BFF.HiddenDissipation.noisy_ring_curvature_minimax_unconditional
