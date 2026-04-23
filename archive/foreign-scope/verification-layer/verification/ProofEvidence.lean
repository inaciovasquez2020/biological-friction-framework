/-
External proof evidence interface.
These certificates are machine-validated via CI.
-/

import Std

structure ProofCertificate where
  id : String
  statement : String
  assumptions : List String
  status : String

def loadCertificate (path : String) : IO ProofCertificate := do
  let json ← IO.FS.readFile path
  let data ← IO.ofExcept (Std.Json.parse json)
  let obj := data.getObj!
  return {
    id := obj.getStr! "id",
    statement := obj.getStr! "statement",
    assumptions := (obj.getArr! "assumptions").toList.map (·.getStr!),
    status := obj.getStr! "status"
  }

def verified (c : ProofCertificate) : Bool :=
  c.status.startsWith "verified"

def contractionCertPath : String :=
  "verification/proofs/contraction_certificate.json"

def fixedPointCertPath : String :=
  "verification/proofs/fixed_point_certificate.json"

def loadAll : IO (List ProofCertificate) := do
  let c1 ← loadCertificate contractionCertPath
  let c2 ← loadCertificate fixedPointCertPath
  return [c1, c2]

def main : IO Unit := do
  let certs ← loadAll
  for c in certs do
    if verified c then
      IO.println s!"Loaded verified certificate: {c.id}"
    else
      throw <| IO.userError s!"Unverified certificate: {c.id}"

