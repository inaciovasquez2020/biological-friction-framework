
import pathlib,re,sys

p=pathlib.Path(__file__).resolve().parent/"recovery"

allowed={"propext","Classical.choice","Quot.sound"}

def expected(path):
    src=path.read_text()
    assert not re.search(
        r"\b(?:axiom|opaque|sorry|admit|native_decide)\b",
        src
    )
    names=re.findall(r"^#print axioms (\S+)$",src,re.M)
    result={
        n if "." in n else "BFF.HiddenDissipation."+n
        for n in names
    }
    assert len(result)==len(names)
    return result

def audit(path,wanted):
    log=path.read_text()
    found={}
    for n,a in re.findall(
        r"'([^']+)' depends on axioms: \[([^\]]*)\]",
        log
    ):
        assert n not in found,n
        found[n]={x.strip() for x in a.split(",") if x.strip()}
    for n in re.findall(
        r"'([^']+)' does not depend on any axioms",log
    ):
        assert n not in found,n
        found[n]=set()
    assert set(found)==wanted,(wanted-set(found),set(found)-wanted)
    assert all(a<=allowed for a in found.values())
    assert not re.search(r"\b(?:sorryAx|sorry|admit)\b",log)
    assert not re.search(
        r"(?m)^.*error(?:\([^)]*\))?:",log
    )
    return found

u=expected(p/"UniversalRecovery.lean")
e=expected(p/"EntropyConvexity.lean")

assert len(u)==52 and len(e)==5
assert not u.intersection(e)

required={
    "URF.Transfer.recoverable_iff_pairwise",
    "URF.Transfer.exact_minimax",
    "URF.Transfer.affine_transfer",
    "URF.Transfer.shared_noise_iff",
    "URF.Transfer.recoverable_noisy_iff",
    "URF.Transfer.convex_endpoint_increment",
    "URF.Transfer.interval_noisy_minimax",
    "URF.Transfer.affine_unbounded_minimax",
    "BFF.HiddenDissipation.entropySquared_mono",
    "BFF.HiddenDissipation.noisy_ring_curvature_minimax",
    "BFF.HiddenDissipation.noisy_mode_minimax",
    "BFF.HiddenDissipation.edgeEntropy_hasSum",
    "BFF.HiddenDissipation.power_chord",
    "BFF.HiddenDissipation.edgeEntropy_chord",
    "BFF.HiddenDissipation.entropySquared_chordConvex",
    "BFF.HiddenDissipation.noisy_ring_curvature_minimax_unconditional"
}
assert required<=u|e
assert len(required)==16

a=audit(pathlib.Path(sys.argv[1]),u)
b=audit(pathlib.Path(sys.argv[2]),e)

print("AXIOM_AUDIT := PASS_57_OF_57")
