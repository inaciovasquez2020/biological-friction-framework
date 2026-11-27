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

namespace BFF.HiddenDissipation

noncomputable def returnCurvature {n : ℕ}
    (X : RingModel n) (i : Fin (n+3)) : ℝ :=
  ∑ k, generator X i k * generator X k i

theorem returnCurvature_expansion {n : ℕ}
    (X : RingModel n) (i : Fin (n+3)) :
    returnCurvature X i =
      (exitRate X i)^2 +
      cw X i * ccw X (ringNext i) +
      ccw X i * cw X (ringPrev i) := by
  classical
  have hi := ringNeighbors_distinct i
  have hn := ringNeighbors_distinct (ringNext i)
  have hp := ringNeighbors_distinct (ringPrev i)
  rw [ringPrev_next] at hn
  rw [ringNext_prev] at hp
  have hnext :
      generator X (ringNext i) i =
        ccw X (ringNext i) := by
    simp [generator,ringPrev_next,
      hn.2.2.symm,hi.1.symm]
  have hprev :
      generator X (ringPrev i) i =
        cw X (ringPrev i) := by
    simp [generator,ringNext_prev,
      hp.2.2,hi.2.1.symm]
  have hrow (k : Fin (n+3)) :
      generator X i k * generator X k i =
      (if k = ringNext i then
        cw X i * generator X k i else 0) +
      (if k = ringPrev i then
        ccw X i * generator X k i else 0) -
      (if k = i then
        exitRate X i * generator X k i else 0) := by
    change
      ((if k = ringNext i then cw X i else 0) +
       (if k = ringPrev i then ccw X i else 0) -
       (if k = i then exitRate X i else 0)) *
       generator X k i = _
    simp only [sub_mul,add_mul,ite_mul,zero_mul]
  unfold returnCurvature
  simp only [hrow,Finset.sum_add_distrib,
    Finset.sum_sub_distrib]
  simp [hnext,hprev,generator_diag]
  <;> ring

noncomputable def curvatureWeight {n : ℕ}
    (X : RingModel n) (i : Fin (n+3)) : ℝ :=
  1/(4*X.p i*X.p (ringNext i)) +
  1/(4*X.p i*X.p (ringPrev i))

noncomputable def curvatureBaseline {n : ℕ}
    (X : RingModel n) (i : Fin (n+3)) : ℝ :=
  ((X.t i + X.t (ringPrev i))/(2*X.p i))^2 +
  (X.t i)^2/(4*X.p i*X.p (ringNext i)) +
  (X.t (ringPrev i))^2/(4*X.p i*X.p (ringPrev i))

theorem curvatureWeight_pos {n : ℕ}
    (X : RingModel n) (i : Fin (n+3)) :
    0 < curvatureWeight X i := by
  have h0 := X.p_pos i
  have hn := X.p_pos (ringNext i)
  have hp := X.p_pos (ringPrev i)
  unfold curvatureWeight
  positivity

theorem returnCurvature_eq {n : ℕ}
    (X : RingModel n) (i : Fin (n+3)) :
    returnCurvature X i =
      curvatureBaseline X i -
        curvatureWeight X i * X.j^2 := by
  rw [returnCurvature_expansion,exitRate_eq]
  unfold curvatureBaseline curvatureWeight cw ccw
    forward reverse
  rw [ringPrev_next]
  field_simp [
    ne_of_gt (X.p_pos i),
    ne_of_gt (X.p_pos (ringNext i)),
    ne_of_gt (X.p_pos (ringPrev i))] <;> ring

theorem current_sq_recover {n : ℕ}
    (X : RingModel n) (i : Fin (n+3)) :
    (curvatureBaseline X i - returnCurvature X i) /
      curvatureWeight X i = X.j^2 := by
  rw [returnCurvature_eq]
  have h := curvatureWeight_pos X i
  field_simp [ne_of_gt h] <;> ring

theorem entropy_identified_by_curvature {n : ℕ}
    (X Y : RingModel n) (i : Fin (n+3))
    (r : ℕ)
    (hobs : SameObservation r X Y)
    (hK : returnCurvature X i = returnCurvature Y i) :
    entropyProduction X = entropyProduction Y := by
  have hp : X.p = Y.p := hobs.1
  have ht : X.t = Y.t := by
    funext k
    rw [← traffic_eq X k,← traffic_eq Y k]
    exact hobs.2.1 k
  have hsq : X.j^2 = Y.j^2 := by
    calc
      X.j^2 =
        (curvatureBaseline X i - returnCurvature X i) /
          curvatureWeight X i :=
            (current_sq_recover X i).symm
      _ =
        (curvatureBaseline Y i - returnCurvature Y i) /
          curvatureWeight Y i := by
            simp only [
              curvatureBaseline,curvatureWeight,hp,ht,hK]
      _ = Y.j^2 := current_sq_recover Y i
  have hm : (X.j-Y.j)*(X.j+Y.j)=0 := by
    nlinarith [hsq]
  rw [entropyProduction_eq,entropyProduction_eq,ht]
  rcases mul_eq_zero.mp hm with h | h
  · have hj : X.j = Y.j := by linarith
    rw [hj]
  · have hj : X.j = -Y.j := by linarith
    rw [hj,dissipation_even]

noncomputable def modeCoeff (b n lam : ℝ) : ℝ :=
  lam*n^4/(2*b^3)

theorem mode_recover (b n lam : ℝ)
    (hb : 0 < b) (hn : n ≠ 0) :
    2*b^3*modeCoeff b n lam/n^4 = lam := by
  unfold modeCoeff
  field_simp [ne_of_gt hb,hn] <;> ring

theorem mode_identifiable (b n lam mu : ℝ)
    (hb : 0 < b) (hn : n ≠ 0)
    (h : modeCoeff b n lam = modeCoeff b n mu) :
    lam = mu := by
  calc
    lam = 2*b^3*modeCoeff b n lam/n^4 :=
      (mode_recover b n lam hb hn).symm
    _ = 2*b^3*modeCoeff b n mu/n^4 := by rw [h]
    _ = mu := mode_recover b n mu hb hn

theorem mode_zero_invisible (b lam : ℝ) :
    modeCoeff b 0 lam = 0 := by
  simp [modeCoeff]

#print axioms returnCurvature_expansion
#print axioms curvatureWeight_pos
#print axioms returnCurvature_eq
#print axioms current_sq_recover
#print axioms entropy_identified_by_curvature
#print axioms mode_recover
#print axioms mode_identifiable
#print axioms mode_zero_invisible

end BFF.HiddenDissipation

namespace URF.Transfer

def Recoverable {X Y : Type*}
    (A : X → Y → Prop) (I : X → ℝ) (E : ℝ) : Prop :=
  ∃ D : Y → ℝ, ∀ x y, A x y →
    |D y - I x| ≤ E

theorem recoverable_iff_pairwise {X Y : Type*}
    (A : X → Y → Prop) (I : X → ℝ) (E : ℝ) :
    Recoverable A I E ↔
      ∀ x z y, A x y → A z y →
        |I x - I z| ≤ 2*E := by
  constructor
  · rintro ⟨D,hD⟩ x z y hx hz
    have h1 := abs_le.mp (hD x y hx)
    have h2 := abs_le.mp (hD z y hz)
    exact abs_le.mpr ⟨by linarith,by linarith⟩
  · intro h
    let L (y : Y) : Set ℝ :=
      {v | ∃ x, A x y ∧ v = I x-E}
    refine ⟨fun y => sSup (L y),?_⟩
    intro x y hx
    have hm : I x-E ∈ L y := ⟨x,hx,rfl⟩
    have hu : ∀ v ∈ L y, v ≤ I x+E := by
      intro v hv
      obtain ⟨z,hz,rfl⟩ := hv
      have hh := (abs_le.mp (h z x y hz hx)).2
      linarith
    have hb : BddAbove (L y) := ⟨I x+E,hu⟩
    have hl := le_csSup hb hm
    have hh := csSup_le
      (show (L y).Nonempty from ⟨_,hm⟩) hu
    exact abs_le.mpr ⟨by linarith,by linarith⟩

def pairRadii {X Y : Type*}
    (A : X → Y → Prop) (I : X → ℝ) : Set ℝ :=
  {r | ∃ x z y, A x y ∧ A z y ∧
    r = |I x-I z|/2}

theorem exact_minimax {X Y : Type*}
    (A : X → Y → Prop) (I : X → ℝ)
    (hne : (pairRadii A I).Nonempty)
    (hbd : BddAbove (pairRadii A I)) :
    IsLeast {E : ℝ | Recoverable A I E}
      (sSup (pairRadii A I)) := by
  constructor
  · apply (recoverable_iff_pairwise A I _).2
    intro x z y hx hz
    have hm : |I x-I z|/2 ∈ pairRadii A I :=
      ⟨x,z,y,hx,hz,rfl⟩
    have h := le_csSup hbd hm
    linarith
  · intro E hE
    change Recoverable A I E at hE
    apply csSup_le hne
    rintro r ⟨x,z,y,hx,hz,rfl⟩
    have h :=
      (recoverable_iff_pairwise A I E).1 hE
        x z y hx hz
    linarith

theorem affine_transfer
    {X Y X' Y' : Type*}
    (eX : X ≃ X') (eY : Y ≃ Y')
    (A : X → Y → Prop) (B : X' → Y' → Prop)
    (I : X → ℝ) (J : X' → ℝ)
    (a E : ℝ) (b : Y → ℝ) (ha : a ≠ 0)
    (hA : ∀ x y, A x y ↔ B (eX x) (eY y))
    (hI : ∀ x y, A x y →
      J (eX x) = a*I x+b y) :
    Recoverable B J (|a| * E) ↔ Recoverable A I E := by
  simp only [recoverable_iff_pairwise]
  constructor
  · intro h x z y hx hz
    have hh :=
      h (eX x) (eX z) (eY y)
        ((hA x y).1 hx) ((hA z y).1 hz)
    have he :
        J (eX x)-J (eX z) = a*(I x-I z) := by
      rw [hI x y hx,hI z y hz]
      ring
    rw [he,abs_mul] at hh
    by_contra! hbad
    have hp :=
      mul_pos (abs_pos.mpr ha) (sub_pos.mpr hbad)
    nlinarith only [hp,hh]
  · intro h x z y hx hz
    obtain ⟨u,rfl⟩ := eX.surjective x
    obtain ⟨v,rfl⟩ := eX.surjective z
    obtain ⟨w,rfl⟩ := eY.surjective y
    have hu := (hA u w).2 hx
    have hv := (hA v w).2 hz
    have hh := h u v w hu hv
    have he :
        J (eX u)-J (eX v) = a*(I u-I v) := by
      rw [hI u w hu,hI v w hv]
      ring
    rw [he,abs_mul]
    have hm :=
      mul_le_mul_of_nonneg_left hh (abs_nonneg a)
    nlinarith only [hm]

def Noisy {X : Type*}
    (O : X → ℝ) (ε : ℝ) (x : X) (y : ℝ) : Prop :=
  |y-O x| ≤ ε

theorem shared_noise_iff (ε a b : ℝ) :
    (∃ y : ℝ, |y-a| ≤ ε ∧ |y-b| ≤ ε) ↔
      |a-b| ≤ 2*ε := by
  constructor
  · rintro ⟨y,hy,hz⟩
    have h1 := abs_le.mp hy
    have h2 := abs_le.mp hz
    exact abs_le.mpr ⟨by linarith,by linarith⟩
  · intro h
    have hh := abs_le.mp h
    refine ⟨(a+b)/2,?_,?_⟩
    · exact abs_le.mpr ⟨by linarith,by linarith⟩
    · exact abs_le.mpr ⟨by linarith,by linarith⟩

theorem recoverable_noisy_iff {X : Type*}
    (O I : X → ℝ) (ε E : ℝ) :
    Recoverable (Noisy O ε) I E ↔
      ∀ x z, |O x-O z| ≤ 2*ε →
        |I x-I z| ≤ 2*E := by
  rw [recoverable_iff_pairwise]
  constructor
  · intro h x z hd
    obtain ⟨y,hy,hz⟩ :=
      (shared_noise_iff ε (O x) (O z)).2 hd
    exact h x z y hy hz
  · intro h x z y hx hz
    apply h x z
    exact (shared_noise_iff ε (O x) (O z)).1
      ⟨y,hx,hz⟩

def ChordConvex (S : ℝ → ℝ) (U : ℝ) : Prop :=
  ∀ x y z : ℝ,
    0 ≤ x → x ≤ y → y ≤ z → z ≤ U →
    (z-x)*S y ≤ (z-y)*S x+(y-x)*S z

theorem convex_endpoint_increment
    (S : ℝ → ℝ) (U x y : ℝ)
    (hC : ChordConvex S U)
    (hx : 0 ≤ x) (hxy : x ≤ y) (hy : y ≤ U) :
    S y-S x ≤ S U-S (U-(y-x)) := by
  by_cases h : x = U
  · have hy' : y = U := by linarith
    subst x
    subst y
    simp
  · have hp : 0 < U-x :=
      sub_pos.mpr (lt_of_le_of_ne (hxy.trans hy) h)
    have h1 := hC x y U hx hxy hy le_rfl
    have h2 := hC x (U-(y-x)) U hx
      (by linarith) (by linarith) le_rfl
    by_contra! hn
    have hh := mul_pos hp (sub_pos.mpr hn)
    nlinarith only [h1,h2,hh]

theorem interval_noisy_minimax {X : Type*}
    (u : X → ℝ) (S : ℝ → ℝ)
    (U K c ε : ℝ)
    (hU : 0 ≤ U) (hc : 0 < c) (hε : 0 ≤ ε)
    (hu : ∀ x, 0 ≤ u x ∧ u x ≤ U)
    (hsurj : ∀ v, 0 ≤ v → v ≤ U →
      ∃ x, u x = v)
    (hmono : ∀ x y, 0 ≤ x → x ≤ y →
      y ≤ U → S x ≤ S y)
    (hC : ChordConvex S U) :
    IsLeast
      {E : ℝ |
        Recoverable
          (Noisy (fun x => K-c*u x) ε)
          (fun x => S (u x)) E}
      ((S U-S (U-min U (2*ε/c)))/2) := by
  let δ := min U (2*ε/c)
  change IsLeast
    {E : ℝ |
      Recoverable
        (Noisy (fun x => K-c*u x) ε)
        (fun x => S (u x)) E}
    ((S U-S (U-δ))/2)
  have hd0 : 0 ≤ δ :=
    le_min hU (div_nonneg (by linarith) hc.le)
  have hdU : δ ≤ U := min_le_left _ _
  have hdε : δ ≤ 2*ε/c := min_le_right _ _
  have hdC : c*δ ≤ 2*ε := by
    have h := (le_div_iff₀ hc).1 hdε
    nlinarith only [h]
  have hgap (x y : ℝ)
      (hx : 0 ≤ x) (hxy : x ≤ y) (hy : y ≤ U)
      (hd : c*(y-x) ≤ 2*ε) :
      S y-S x ≤ S U-S (U-δ) := by
    have hl : y-x ≤ δ := by
      apply le_min
      · linarith
      · apply (le_div_iff₀ hc).2
        nlinarith only [hd]
    have hm := hmono (U-δ) (U-(y-x))
      (by linarith) (by linarith) (by linarith)
    have hh := convex_endpoint_increment
      S U x y hC hx hxy hy
    linarith
  constructor
  · apply (recoverable_noisy_iff _ _ _ _).2
    intro x z hd
    change |(K-c*u x)-(K-c*u z)| ≤ 2*ε at hd
    change |S (u x)-S (u z)| ≤
      2*((S U-S (U-δ))/2)
    have he :
        (K-c*u x)-(K-c*u z) =
          c*(u z-u x) := by ring
    rw [he,abs_mul,abs_of_pos hc] at hd
    rcases le_total (u x) (u z) with h | h
    · rw [abs_of_nonneg (sub_nonneg.mpr h)] at hd
      have hh := hgap (u x) (u z)
        (hu x).1 h (hu z).2 hd
      have hm := hmono (u x) (u z)
        (hu x).1 h (hu z).2
      rw [abs_of_nonpos (sub_nonpos.mpr hm)]
      linarith
    · rw [abs_of_nonpos (sub_nonpos.mpr h)] at hd
      have hh' : c*(u x-u z) ≤ 2*ε := by
        nlinarith only [hd]
      have hh := hgap (u z) (u x)
        (hu z).1 h (hu x).2 hh'
      have hm := hmono (u z) (u x)
        (hu z).1 h (hu x).2
      rw [abs_of_nonneg (sub_nonneg.mpr hm)]
      linarith
  · intro E hE
    change Recoverable
      (Noisy (fun x => K-c*u x) ε)
      (fun x => S (u x)) E at hE
    obtain ⟨x,hx⟩ := hsurj (U-δ)
      (by linarith) (by linarith)
    obtain ⟨z,hz⟩ := hsurj U hU le_rfl
    have hd : |(K-c*u x)-(K-c*u z)| ≤ 2*ε := by
      rw [hx,hz]
      rw [show (K-c*(U-δ))-(K-c*U) = c*δ by ring]
      rw [abs_of_nonneg (mul_nonneg hc.le hd0)]
      exact hdC
    have hh :=
      (recoverable_noisy_iff _ _ _ _).1 hE x z hd
    change |S (u x)-S (u z)| ≤ 2*E at hh
    rw [hx,hz] at hh
    have hm := hmono (U-δ) U
      (by linarith) (by linarith) le_rfl
    rw [abs_of_nonpos (sub_nonpos.mpr hm)] at hh
    linarith

theorem affine_unbounded_minimax
    (k ε : ℝ) (hk : 0 < k) (hε : 0 ≤ ε) :
    IsLeast
      {E : ℝ |
        Recoverable
          (Noisy (fun x : ℝ => k*x) ε)
          (fun x : ℝ => x) E}
      (ε/k) := by
  constructor
  · apply (recoverable_noisy_iff _ _ _ _).2
    intro x z hd
    change |k*x-k*z| ≤ 2*ε at hd
    rw [← mul_sub,abs_mul,abs_of_pos hk] at hd
    have hh : |x-z| ≤ (2*ε)/k :=
      (le_div_iff₀ hk).2 (by nlinarith only [hd])
    simpa only [mul_div_assoc] using hh
  · intro E hE
    change Recoverable
      (Noisy (fun x : ℝ => k*x) ε)
      (fun x : ℝ => x) E at hE
    have hq : 0 ≤ ε/k := div_nonneg hε hk.le
    have hp : k*(ε/k) = ε := by
      field_simp [ne_of_gt hk]
    have hd : |k*(ε/k)-k*(-(ε/k))| ≤ 2*ε := by
      rw [show k*(ε/k)-k*(-(ε/k)) =
        2*ε by nlinarith only [hp]]
      rw [abs_of_nonneg (by linarith : 0 ≤ 2*ε)]
      <;> exact le_rfl
    have hh :=
      (recoverable_noisy_iff _ _ _ _).1 hE
        (ε/k) (-(ε/k)) hd
    change |ε/k - -(ε/k)| ≤ 2*E at hh
    rw [abs_of_nonneg (by linarith : 0 ≤
      ε/k - -(ε/k))] at hh
    linarith

end URF.Transfer

namespace BFF.HiddenDissipation

open URF.Transfer

noncomputable def entropySquared {n : ℕ}
    (t : Fin n → ℝ) (u : ℝ) : ℝ :=
  dissipation t (Real.sqrt u)

theorem entropySquared_mono {n : ℕ}
    (t : Fin n → ℝ) (M : ℝ)
    (hM : 0 ≤ M) (ht : ∀ i, M < t i) :
    ∀ x y, 0 ≤ x → x ≤ y → y ≤ M^2 →
      entropySquared t x ≤ entropySquared t y := by
  intro x y hx hxy hy
  have hyM : Real.sqrt y ≤ M := by
    calc
      Real.sqrt y ≤ Real.sqrt (M^2) :=
        Real.sqrt_le_sqrt hy
      _ = M := by rw [Real.sqrt_sq_eq_abs,abs_of_nonneg hM]
  have hh : |Real.sqrt x| ≤ Real.sqrt y := by
    rw [abs_of_nonneg (Real.sqrt_nonneg _)]
    exact Real.sqrt_le_sqrt hxy
  exact (dissipation_range t
    (Real.sqrt y) (Real.sqrt x)
    (Real.sqrt_nonneg _)
    (fun i => hyM.trans_lt (ht i)) hh).2

theorem noisy_ring_curvature_minimax {n : ℕ}
    (p t : Fin (n+3) → ℝ) (M ε : ℝ)
    (hp : ∀ i, 0 < p i) (hs : ∑ i,p i = 1)
    (hM : 0 ≤ M) (ht : ∀ i, M < t i)
    (hε : 0 ≤ ε) (i : Fin (n+3))
    (hC : ChordConvex (entropySquared t) (M^2)) :
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
  let X0 := buildRing p t M hp hs ht
    ⟨0,by simpa using hM⟩
  let K := curvatureBaseline X0 i
  let c := curvatureWeight X0 i
  let u : {j : ℝ // |j| ≤ M} → ℝ :=
    fun j => j.val^2
  have hc : 0 < c := curvatureWeight_pos X0 i
  have hu (j : {j : ℝ // |j| ≤ M}) :
      0 ≤ u j ∧ u j ≤ M^2 := by
    change 0 ≤ j.val^2 ∧ j.val^2 ≤ M^2
    refine ⟨sq_nonneg _,?_⟩
    have hh := mul_nonneg
      (sub_nonneg.mpr j.property)
      (add_nonneg hM (abs_nonneg j.val))
    have ha := sq_abs j.val
    nlinarith only [hh,ha]
  have hsurj (v : ℝ)
      (hv : 0 ≤ v) (hvM : v ≤ M^2) :
      ∃ j, u j = v := by
    have hj : |Real.sqrt v| ≤ M := by
      rw [abs_of_nonneg (Real.sqrt_nonneg _)]
      calc
        Real.sqrt v ≤ Real.sqrt (M^2) :=
          Real.sqrt_le_sqrt hvM
        _ = M := by
          rw [Real.sqrt_sq_eq_abs,abs_of_nonneg hM]
    exact ⟨⟨Real.sqrt v,hj⟩,Real.sq_sqrt hv⟩
  have hO :
      (fun j : {j : ℝ // |j| ≤ M} =>
        returnCurvature (buildRing p t M hp hs ht j) i) =
      (fun j => K-c*u j) := by
    funext j
    exact returnCurvature_eq
      (buildRing p t M hp hs ht j) i
  have hI :
      (fun j : {j : ℝ // |j| ≤ M} =>
        entropyProduction (buildRing p t M hp hs ht j)) =
      (fun j => entropySquared t (u j)) := by
    funext j
    rw [entropyProduction_eq]
    change dissipation t j.val =
      dissipation t (Real.sqrt (j.val^2))
    rw [Real.sqrt_sq_eq_abs]
    rcases le_total 0 j.val with hj | hj
    · rw [abs_of_nonneg hj]
    · rw [abs_of_nonpos hj,dissipation_even]
  change IsLeast
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
        (M^2-min (M^2) (2*ε/c)))/2)
  rw [hO,hI]
  exact interval_noisy_minimax u
    (entropySquared t) (M^2) K c ε
    (sq_nonneg M) hc hε hu hsurj
    (entropySquared_mono t M hM ht) hC

theorem noisy_mode_minimax (b n ε : ℝ)
    (hb : 0 < b) (hn : n ≠ 0) (hε : 0 ≤ ε) :
    IsLeast
      {E : ℝ |
        Recoverable
          (Noisy (fun lam => modeCoeff b n lam) ε)
          (fun lam => lam) E}
      (2*b^3*ε/n^4) := by
  let k := n^4/(2*b^3)
  have hn4 : 0 < n^4 := by
    calc
      0 < (n^2)^2 :=
        sq_pos_of_ne_zero (ne_of_gt (sq_pos_of_ne_zero hn))
      _ = n^4 := by ring
  have hk : 0 < k :=
    div_pos hn4 (by positivity)
  have hO :
      (fun lam => modeCoeff b n lam) =
        (fun lam : ℝ => k*lam) := by
    funext lam
    unfold modeCoeff
    dsimp [k]
    ring
  have hE : ε/k = 2*b^3*ε/n^4 := by
    dsimp [k]
    field_simp [ne_of_gt hb,hn] <;> ring
  rw [hO,← hE]
  exact affine_unbounded_minimax k ε hk hε

end BFF.HiddenDissipation

#print axioms URF.Transfer.recoverable_iff_pairwise
#print axioms URF.Transfer.exact_minimax
#print axioms URF.Transfer.affine_transfer
#print axioms URF.Transfer.shared_noise_iff
#print axioms URF.Transfer.recoverable_noisy_iff
#print axioms URF.Transfer.convex_endpoint_increment
#print axioms URF.Transfer.interval_noisy_minimax
#print axioms URF.Transfer.affine_unbounded_minimax
#print axioms BFF.HiddenDissipation.entropySquared_mono
#print axioms BFF.HiddenDissipation.noisy_ring_curvature_minimax
#print axioms BFF.HiddenDissipation.noisy_mode_minimax
