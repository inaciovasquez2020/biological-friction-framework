import Mathlib

namespace URF

-- Core abstract objects (interface)
constant H : Type
constant L : H → H
constant defectSpace : Set H
constant epsilon0 : ℝ

-- Spectral notions (minimal stubs)
constant inf_spec : (H → H) → ℝ
constant restrict : (H → H) → Set H → (H → H)

-- Binding theorem (interface)
axiom spectral_gap_core :
  inf_spec (restrict L defectSpaceᶜ) ≥ epsilon0

end URF

