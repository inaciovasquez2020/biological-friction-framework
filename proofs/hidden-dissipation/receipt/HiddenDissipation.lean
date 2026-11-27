import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic

open scoped BigOperators

namespace BFF.HiddenDissipation

noncomputable def forward (t j : ℝ) : ℝ := (t+j)/2
noncomputable def reverse (t j : ℝ) : ℝ := (t-j)/2

theorem flux_identities (t j : ℝ) :
    forward t j + reverse t j = t ∧
    forward t j - reverse t j = j := by
  unfold forward reverse
  constructor <;> ring

theorem flux_positive (t j : ℝ) (hj : |j| < t) :
    0 < forward t j ∧ 0 < reverse t j := by
  have ha := abs_lt.mp hj
  unfold forward reverse
  constructor <;> linarith

theorem stationary_balance (t u j : ℝ) :
    forward t j + reverse u j =
      forward u j + reverse t j := by
  unfold forward reverse
  ring

theorem holding_rate_invariant (t u j p : ℝ)
    (hp : 0 < p) :
    forward t j / p + reverse u j / p =
      (t+u)/(2*p) := by
  unfold forward reverse
  field_simp [ne_of_gt hp] <;> ring

noncomputable def pathPotential (d : ℕ → ℝ) : ℕ → ℝ
  | 0 => 0
  | k+1 => pathPotential d k + d k

theorem pathPotential_step (d : ℕ → ℝ) (k : ℕ) :
    pathPotential d (k+1) - pathPotential d k = d k := by
  rw [pathPotential]
  ring

theorem path_gauge_collision (a b : ℕ → ℝ) (m : ℕ) :
    ∃ g : ℕ → ℝ, ∀ k < m,
      b k - a k = g (k+1) - g k := by
  refine ⟨pathPotential (fun k => b k-a k), ?_⟩
  intro k hk
  exact (pathPotential_step (fun k => b k-a k) k).symm

noncomputable def force (t j : ℝ) : ℝ :=
  Real.log ((t+j)/(t-j))

noncomputable def dissipation {n : ℕ}
    (t : Fin n → ℝ) (j : ℝ) : ℝ :=
  j * ∑ i, force (t i) j

theorem force_nonneg (t j : ℝ)
    (hj : 0 ≤ j) (ht : j < t) :
    0 ≤ force t j := by
  unfold force
  apply Real.log_nonneg
  apply (le_div_iff₀ (by linarith : 0 < t-j)).2
  linarith

theorem force_mono (t a b : ℝ)
    (ha : 0 ≤ a) (hab : a ≤ b) (hb : b < t) :
    force t a ≤ force t b := by
  have hta : 0 < t-a := by linarith
  have htb : 0 < t-b := by linarith
  have hpa : 0 < t+a := by linarith
  have hpb : 0 < t+b := by linarith
  have hprod : 0 ≤ t*(b-a) :=
    mul_nonneg (by linarith) (sub_nonneg.mpr hab)
  unfold force
  apply Real.log_le_log (div_pos hpa hta)
  apply (div_le_div_iff₀ hta htb).2
  nlinarith

theorem dissipation_even {n : ℕ}
    (t : Fin n → ℝ) (j : ℝ) :
    dissipation t (-j) = dissipation t j := by
  have hforce (u : ℝ) :
      force u (-j) = -force u j := by
    unfold force
    have hnum : u + -j = u - j := by ring
    have hden : u - -j = u + j := by ring
    have hquot :
        (u + -j) / (u - -j) =
          ((u + j) / (u - j))⁻¹ := by
      rw [inv_div, hnum, hden]
    rw [hquot, Real.log_inv]
  unfold dissipation
  simp only [hforce, Finset.sum_neg_distrib, neg_mul_neg]

theorem dissipation_zero {n : ℕ} (t : Fin n → ℝ) :
    dissipation t 0 = 0 := by
  simp [dissipation]

theorem dissipation_range {n : ℕ}
    (t : Fin n → ℝ) (M j : ℝ)
    (hM : 0 ≤ M) (ht : ∀ i, M < t i)
    (hj : |j| ≤ M) :
    0 ≤ dissipation t j ∧
      dissipation t j ≤ dissipation t M := by
  have hsym : dissipation t j = dissipation t |j| := by
    rcases le_total 0 j with h | h
    · rw [abs_of_nonneg h]
    · rw [abs_of_nonpos h, dissipation_even]
  rw [hsym]
  have hs : 0 ≤ ∑ i, force (t i) |j| :=
    Finset.sum_nonneg (fun i _ =>
      force_nonneg (t i) |j| (abs_nonneg j)
        (hj.trans_lt (ht i)))
  have hsm :
      (∑ i, force (t i) |j|) ≤
        ∑ i, force (t i) M :=
    Finset.sum_le_sum (fun i _ =>
      force_mono (t i) |j| M (abs_nonneg j) hj (ht i))
  unfold dissipation
  exact ⟨mul_nonneg (abs_nonneg j) hs,
    mul_le_mul hj hsm hs hM⟩

theorem hidden_dissipation_minimax {n : ℕ}
    (t : Fin n → ℝ) (M : ℝ)
    (hM : 0 ≤ M) (ht : ∀ i, M < t i) :
    IsLeast {E : ℝ | ∃ estimate : ℝ,
      ∀ j : ℝ, |j| ≤ M →
        |estimate - dissipation t j| ≤ E}
      (dissipation t M / 2) := by
  have hMM : |M| ≤ M := by simp [abs_of_nonneg hM]
  have h0M : |(0 : ℝ)| ≤ M := by simpa using hM
  refine ⟨?_, ?_⟩
  · refine ⟨dissipation t M / 2, ?_⟩
    intro j hj
    obtain ⟨hl, hu⟩ := dissipation_range t M j hM ht hj
    apply abs_le.mpr
    constructor <;> linarith
  · intro E hE
    obtain ⟨e, he⟩ := hE
    have h0 := abs_le.mp (he 0 h0M)
    have h1 := abs_le.mp (he M hMM)
    rw [dissipation_zero] at h0
    linarith [h0.2, h1.1]

#print axioms flux_identities
#print axioms flux_positive
#print axioms stationary_balance
#print axioms holding_rate_invariant
#print axioms pathPotential_step
#print axioms path_gauge_collision
#print axioms force_nonneg
#print axioms force_mono
#print axioms dissipation_even
#print axioms dissipation_zero
#print axioms dissipation_range
#print axioms hidden_dissipation_minimax

end BFF.HiddenDissipation

namespace BFF.HiddenDissipation

def ringNext {n : ℕ} (i : Fin (n+3)) : Fin (n+3) :=
  if h : i.val+1 < n+3 then
    ⟨i.val+1,h⟩
  else ⟨0,by omega⟩

def ringPrev {n : ℕ} (i : Fin (n+3)) : Fin (n+3) :=
  if h : 0 < i.val then
    ⟨i.val-1,by omega⟩
  else ⟨n+2,by omega⟩

theorem ringPrev_next {n : ℕ} (i : Fin (n+3)) :
    ringPrev (ringNext i) = i := by
  apply Fin.ext
  have hi := i.isLt
  by_cases h : i.val+1 < n+3
  · have hp : 0 < i.val+1 := by omega
    simp [ringNext,ringPrev,h,hp] <;> omega
  · simp [ringNext,ringPrev,h] <;> omega

theorem ringNext_prev {n : ℕ} (i : Fin (n+3)) :
    ringNext (ringPrev i) = i := by
  apply Fin.ext
  have hi := i.isLt
  by_cases h : 0 < i.val
  · have hn : i.val-1+1 < n+3 := by omega
    simp [ringPrev,ringNext,h,hn] <;> omega
  · have hn : ¬ n+2+1 < n+3 := by omega
    simp [ringPrev,ringNext,h,hn] <;> omega

theorem ringNeighbors_distinct {n : ℕ}
    (i : Fin (n+3)) :
    ringNext i ≠ i ∧ ringPrev i ≠ i ∧
      ringNext i ≠ ringPrev i := by
  have hi := i.isLt
  refine ⟨?_,?_,?_⟩
  · intro h
    have hv := congrArg Fin.val h
    by_cases h1 : i.val+1 < n+3 <;>
      simp [ringNext,h1] at hv <;> omega
  · intro h
    have hv := congrArg Fin.val h
    by_cases h2 : 0 < i.val <;>
      simp [ringPrev,h2] at hv <;> omega
  · intro h
    have hv := congrArg Fin.val h
    by_cases h1 : i.val+1 < n+3 <;>
      by_cases h2 : 0 < i.val <;>
      simp [ringNext,ringPrev,h1,h2] at hv <;> omega

structure RingModel (n : ℕ) where
  p : Fin (n+3) → ℝ
  t : Fin (n+3) → ℝ
  j : ℝ
  p_pos : ∀ i, 0 < p i
  p_sum : ∑ i, p i = 1
  j_bound : ∀ i, |j| < t i

noncomputable def cw {n : ℕ}
    (X : RingModel n) (i : Fin (n+3)) : ℝ :=
  forward (X.t i) X.j / X.p i

noncomputable def ccw {n : ℕ}
    (X : RingModel n) (i : Fin (n+3)) : ℝ :=
  reverse (X.t (ringPrev i)) X.j / X.p i

noncomputable def fwdFlux {n : ℕ}
    (X : RingModel n) (i : Fin (n+3)) : ℝ :=
  X.p i * cw X i

noncomputable def revFlux {n : ℕ}
    (X : RingModel n) (i : Fin (n+3)) : ℝ :=
  X.p (ringNext i) * ccw X (ringNext i)

noncomputable def traffic {n : ℕ}
    (X : RingModel n) (i : Fin (n+3)) : ℝ :=
  fwdFlux X i + revFlux X i

noncomputable def exitRate {n : ℕ}
    (X : RingModel n) (i : Fin (n+3)) : ℝ :=
  cw X i + ccw X i

noncomputable def edgeForce {n : ℕ}
    (X : RingModel n) (i : Fin (n+3)) : ℝ :=
  Real.log (fwdFlux X i / revFlux X i)

theorem rates_positive {n : ℕ}
    (X : RingModel n) (i : Fin (n+3)) :
    0 < cw X i ∧ 0 < ccw X i := by
  exact ⟨div_pos
    (flux_positive _ _ (X.j_bound i)).1 (X.p_pos i),
    div_pos
    (flux_positive _ _ (X.j_bound (ringPrev i))).2
    (X.p_pos i)⟩

theorem fwdFlux_eq {n : ℕ}
    (X : RingModel n) (i : Fin (n+3)) :
    fwdFlux X i = forward (X.t i) X.j := by
  unfold fwdFlux cw
  field_simp [ne_of_gt (X.p_pos i)] <;> ring

theorem revFlux_eq {n : ℕ}
    (X : RingModel n) (i : Fin (n+3)) :
    revFlux X i = reverse (X.t i) X.j := by
  unfold revFlux ccw
  rw [ringPrev_next]
  field_simp [ne_of_gt (X.p_pos (ringNext i))] <;> ring

theorem traffic_eq {n : ℕ}
    (X : RingModel n) (i : Fin (n+3)) :
    traffic X i = X.t i := by
  unfold traffic
  rw [fwdFlux_eq,revFlux_eq]
  exact (flux_identities _ _).1

theorem exitRate_eq {n : ℕ}
    (X : RingModel n) (i : Fin (n+3)) :
    exitRate X i =
      (X.t i + X.t (ringPrev i))/(2*X.p i) := by
  exact holding_rate_invariant _ _ _ _ (X.p_pos i)

theorem edgeForce_eq {n : ℕ}
    (X : RingModel n) (i : Fin (n+3)) :
    edgeForce X i = force (X.t i) X.j := by
  unfold edgeForce force
  rw [fwdFlux_eq,revFlux_eq]
  unfold forward reverse
  have h := abs_lt.mp (X.j_bound i)
  have ht : X.t i-X.j ≠ 0 := by linarith
  apply congrArg Real.log
  field_simp [ht] <;> ring

theorem stationary_balance_ring {n : ℕ}
    (X : RingModel n) (i : Fin (n+3)) :
    fwdFlux X i + revFlux X (ringPrev i) =
      fwdFlux X (ringPrev i) + revFlux X i := by
  simp only [fwdFlux_eq,revFlux_eq]
  exact stationary_balance _ _ _

noncomputable def generator {n : ℕ}
    (X : RingModel n) (i k : Fin (n+3)) : ℝ :=
  (if k = ringNext i then cw X i else 0) +
  (if k = ringPrev i then ccw X i else 0) -
  (if k = i then exitRate X i else 0)

theorem generator_row_sum {n : ℕ}
    (X : RingModel n) (i : Fin (n+3)) :
    ∑ k, generator X i k = 0 := by
  classical
  simp [generator,Finset.sum_sub_distrib,
    Finset.sum_add_distrib,exitRate]

theorem generator_offdiag {n : ℕ}
    (X : RingModel n) (i k : Fin (n+3))
    (h : k ≠ i) : 0 ≤ generator X i k := by
  have hp := rates_positive X i
  unfold generator
  rw [if_neg h,sub_zero]
  apply add_nonneg
  · split
    · exact le_of_lt hp.1
    · exact le_rfl
  · split
    · exact le_of_lt hp.2
    · exact le_rfl

theorem generator_diag {n : ℕ}
    (X : RingModel n) (i : Fin (n+3)) :
    generator X i i = -exitRate X i := by
  have h := ringNeighbors_distinct i
  simp [generator,Ne.symm h.1,Ne.symm h.2.1]

theorem generator_stationary {n : ℕ}
    (X : RingModel n) (i : Fin (n+3)) :
    ∑ k, X.p k * generator X k i = 0 := by
  classical
  have hn (k : Fin (n+3)) :
      (i = ringNext k) ↔ k = ringPrev i := by
    constructor
    · intro h
      calc
        k = ringPrev (ringNext k) := (ringPrev_next k).symm
        _ = ringPrev i := congrArg ringPrev h.symm
    · intro h
      rw [h,ringNext_prev]
  have hp (k : Fin (n+3)) :
      (i = ringPrev k) ↔ k = ringNext i := by
    constructor
    · intro h
      calc
        k = ringNext (ringPrev k) := (ringNext_prev k).symm
        _ = ringNext i := congrArg ringNext h.symm
    · intro h
      rw [h,ringPrev_next]
  calc
    (∑ k, X.p k * generator X k i) =
        fwdFlux X (ringPrev i) + revFlux X i -
        (fwdFlux X i + revFlux X (ringPrev i)) := by
      simp [generator,mul_add,mul_sub,mul_ite,
        Finset.sum_add_distrib,Finset.sum_sub_distrib,
        hn,hp,fwdFlux,revFlux,exitRate,ringNext_prev]
    _ = 0 := by linarith [stationary_balance_ring X i]

noncomputable def entropyProduction {n : ℕ}
    (X : RingModel n) : ℝ :=
  ∑ i, (fwdFlux X i - revFlux X i) * edgeForce X i

theorem entropyProduction_eq {n : ℕ}
    (X : RingModel n) :
    entropyProduction X = dissipation X.t X.j := by
  unfold entropyProduction dissipation
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro i _
  rw [fwdFlux_eq,revFlux_eq,
    (flux_identities (X.t i) X.j).2,edgeForce_eq]

theorem detailedBalance_iff {n : ℕ}
    (X : RingModel n) :
    (∀ i, fwdFlux X i = revFlux X i) ↔ X.j = 0 := by
  constructor
  · intro h
    let i : Fin (n+3) := ⟨0,by omega⟩
    have h0 := h i
    rw [fwdFlux_eq,revFlux_eq] at h0
    linarith [(flux_identities (X.t i) X.j).2]
  · intro h i
    rw [fwdFlux_eq,revFlux_eq]
    simp [forward,reverse,h]

theorem entropyProduction_pos {n : ℕ}
    (X : RingModel n) (hj : 0 < X.j) :
    0 < entropyProduction X := by
  rw [entropyProduction_eq]
  unfold dissipation
  have hf (i : Fin (n+3)) : 0 < force (X.t i) X.j := by
    have h := abs_lt.mp (X.j_bound i)
    unfold force
    apply Real.log_pos
    apply (lt_div_iff₀ (by linarith : 0 < X.t i-X.j)).2
    linarith
  have hs : 0 < ∑ i, force (X.t i) X.j :=
    Finset.sum_pos (fun i _ => hf i) Finset.univ_nonempty
  exact mul_pos hj hs

def LocalGaugeEq {n : ℕ}
    (r : ℕ) (X Y : RingModel n) : Prop :=
  ∀ (m : ℕ), m ≤ 2*r →
    ∀ v : ℕ → Fin (n+3),
      (∀ k < m, v (k+1) = ringNext (v k)) →
      (∀ a b, a ≤ m → b ≤ m → v a = v b → a = b) →
      ∃ g : Fin (n+3) → ℝ, ∀ k < m,
        edgeForce Y (v k) - edgeForce X (v k) =
          g (ringNext (v k)) - g (v k)

theorem localGaugeEq_all {n : ℕ}
    (r : ℕ) (X Y : RingModel n) :
    LocalGaugeEq r X Y := by
  classical
  intro m hm v hadj hinj
  obtain ⟨g,hg⟩ := path_gauge_collision
    (fun k => edgeForce X (v k))
    (fun k => edgeForce Y (v k)) m
  let G : Fin (n+3) → ℝ := fun u =>
    if h : ∃ k : ℕ, k ≤ m ∧ v k = u then
      g (Classical.choose h)
    else 0
  have hG (k : ℕ) (hk : k ≤ m) : G (v k) = g k := by
    have h : ∃ a : ℕ, a ≤ m ∧ v a = v k := ⟨k,hk,rfl⟩
    dsimp only [G]
    rw [dif_pos h]
    exact congrArg g
      (hinj _ _ (Classical.choose_spec h).1 hk
        (Classical.choose_spec h).2)
  refine ⟨G,?_⟩
  intro k hk
  rw [← hadj k hk,hG (k+1) (by omega),hG k (by omega)]
  exact hg k hk

def SameObservation {n : ℕ}
    (r : ℕ) (X Y : RingModel n) : Prop :=
  X.p = Y.p ∧
  (∀ i, traffic X i = traffic Y i) ∧
  (∀ i, exitRate X i = exitRate Y i) ∧
  LocalGaugeEq r X Y

theorem sameObservation_fixed {n : ℕ}
    (X Y : RingModel n) (hp : X.p = Y.p)
    (ht : X.t = Y.t) (r : ℕ) :
    SameObservation r X Y := by
  refine ⟨hp,?_,?_,localGaugeEq_all r X Y⟩
  · intro i
    simp only [traffic_eq,ht]
  · intro i
    simp only [exitRate_eq,hp,ht]

noncomputable def buildRing {n : ℕ}
    (p t : Fin (n+3) → ℝ) (M : ℝ)
    (hp : ∀ i, 0 < p i) (hs : ∑ i,p i = 1)
    (ht : ∀ i, M < t i)
    (j : {j : ℝ // |j| ≤ M}) : RingModel n :=
  ⟨p,t,j.val,hp,hs,fun i => j.property.trans_lt (ht i)⟩

def ObservationInvariant {n : ℕ}
    (r : ℕ) (estimate : RingModel n → ℝ) : Prop :=
  ∀ X Y, SameObservation r X Y → estimate X = estimate Y

theorem ring_observation_minimax {n : ℕ}
    (p t : Fin (n+3) → ℝ) (M : ℝ) (r : ℕ)
    (hp : ∀ i, 0 < p i) (hs : ∑ i,p i = 1)
    (hM : 0 ≤ M) (ht : ∀ i, M < t i) :
    IsLeast {E : ℝ | ∃ estimate : RingModel n → ℝ,
      ObservationInvariant r estimate ∧
      ∀ j : {j : ℝ // |j| ≤ M},
        |estimate (buildRing p t M hp hs ht j) -
          entropyProduction (buildRing p t M hp hs ht j)| ≤ E}
      (dissipation t M/2) := by
  have hb := hidden_dissipation_minimax t M hM ht
  refine ⟨?_,?_⟩
  · obtain ⟨e,he⟩ := hb.1
    refine ⟨fun _ => e,?_,?_⟩
    · intro X Y h
      rfl
    · intro j
      rw [entropyProduction_eq]
      exact he j.val j.property
  · intro E hE
    obtain ⟨est,hinv,he⟩ := hE
    let j0 : {j : ℝ // |j| ≤ M} :=
      ⟨0,by simpa using hM⟩
    let X0 := buildRing p t M hp hs ht j0
    apply hb.2
    refine ⟨est X0,?_⟩
    intro j hj
    let jj : {j : ℝ // |j| ≤ M} := ⟨j,hj⟩
    let X := buildRing p t M hp hs ht jj
    have hobs : SameObservation r X0 X :=
      sameObservation_fixed X0 X rfl rfl r
    have heq := hinv X0 X hobs
    have hh := he jj
    change |est X - entropyProduction X| ≤ E at hh
    rw [← heq,entropyProduction_eq] at hh
    exact hh

theorem equilibrium_driven_collision {n : ℕ}
    (p t : Fin (n+3) → ℝ) (M : ℝ) (r : ℕ)
    (hp : ∀ i, 0 < p i) (hs : ∑ i,p i = 1)
    (hM : 0 < M) (ht : ∀ i, M < t i) :
    ∃ X Y : RingModel n,
      SameObservation r X Y ∧
      (∀ i, fwdFlux X i = revFlux X i) ∧
      ¬ (∀ i, fwdFlux Y i = revFlux Y i) ∧
      entropyProduction X = 0 ∧
      0 < entropyProduction Y := by
  let j0 : {j : ℝ // |j| ≤ M} :=
    ⟨0,by simpa using hM.le⟩
  let jm : {j : ℝ // |j| ≤ M} :=
    ⟨M,by simp [abs_of_pos hM]⟩
  let X := buildRing p t M hp hs ht j0
  let Y := buildRing p t M hp hs ht jm
  refine ⟨X,Y,sameObservation_fixed X Y rfl rfl r,?_,?_,?_,?_⟩
  · exact (detailedBalance_iff X).2 rfl
  · intro h
    have hz := (detailedBalance_iff Y).1 h
    change M = 0 at hz
    linarith
  · rw [entropyProduction_eq]
    exact dissipation_zero t
  · exact entropyProduction_pos Y hM

#print axioms ringPrev_next
#print axioms ringNext_prev
#print axioms ringNeighbors_distinct
#print axioms rates_positive
#print axioms fwdFlux_eq
#print axioms revFlux_eq
#print axioms traffic_eq
#print axioms exitRate_eq
#print axioms edgeForce_eq
#print axioms stationary_balance_ring
#print axioms generator_row_sum
#print axioms generator_offdiag
#print axioms generator_diag
#print axioms generator_stationary
#print axioms entropyProduction_eq
#print axioms detailedBalance_iff
#print axioms entropyProduction_pos
#print axioms localGaugeEq_all
#print axioms sameObservation_fixed
#print axioms ring_observation_minimax
#print axioms equilibrium_driven_collision

end BFF.HiddenDissipation
