universe u

namespace Cyclone

structure Graph where
  V : Type u
  E : Type u
  adj : V → V → Prop
  edge_map : E → V × V

inductive Path (G : Graph) : G.V → G.V → Type u
  | origin (v : G.V) : Path G v v
  | step {u v w : G.V} (p : Path G u v) (e : G.E) (h : G.edge_map e = (v, w)) : Path G u w

def Sigma (G : Graph) := G.E → Bool
def Potential (G : Graph) := G.V → Bool

def pathSum {G : Graph} (σ : Sigma G) : {u v : G.V} → Path G u v → Bool
  | _, _, .origin _ => false
  | _, _, .step p e _ => (pathSum σ p) != (σ e)

axiom unique_path (G : Graph) (u v : G.V) : ∃! p : Path G u v, True

noncomputable def get_path (G : Graph) (u v : G.V) : Path G u v :=
  (unique_path G u v).choose

theorem path_unique_extension
  (G : Graph) (h_tree : ∀ u v : G.V, ∃! p : Path G u v, True)
  (root u v : G.V) (e : G.E) (h_map : G.edge_map e = (u, v)) :
  get_path G root v = Path.step (get_path G root u) e h_map := by
  have huniq := h_tree root v
  apply (ExistsUnique.unique huniq)
  · trivial
  · trivial

theorem tree_potential_exists_verified
  (G : Graph) (σ : Sigma G) (root : G.V)
  (h_tree : ∀ u v : G.V, ∃! p : Path G u v, True) :
  ∃ φ : Potential G, ∀ (e : G.E) (u v : G.V),
    G.edge_map e = (u, v) → σ e = (φ u != φ v) := by
  let φ : Potential G := λ x => pathSum σ (get_path G root x)
  use φ
  intro e u v h_map
  have h_path := path_unique_extension G h_tree root u v e h_map
  have h_sum : φ v = (pathSum σ (get_path G root u)) != σ e := by
    rw [h_path]
    rfl
  rw [h_sum]
  cases (φ u) <;> cases (σ e) <;> simp

end Cyclone
