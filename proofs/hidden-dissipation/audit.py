import pathlib,re,sys
root=pathlib.Path(__file__).resolve().parent
src=(root/"receipt/HiddenDissipation.lean").read_text()
log=pathlib.Path(sys.argv[1]).read_text()

expected={
    "BFF.HiddenDissipation."+n
    for n in re.findall(r"^#print axioms (\w+)$",src,re.M)
}
required={
    "BFF.HiddenDissipation.generator_stationary",
    "BFF.HiddenDissipation.equilibrium_driven_collision",
    "BFF.HiddenDissipation.ring_observation_minimax"
}
assert len(expected)==41
required.update({
    "BFF.HiddenDissipation.returnCurvature_expansion",
    "BFF.HiddenDissipation.curvatureWeight_pos",
    "BFF.HiddenDissipation.returnCurvature_eq",
    "BFF.HiddenDissipation.current_sq_recover",
    "BFF.HiddenDissipation.entropy_identified_by_curvature",
    "BFF.HiddenDissipation.mode_recover",
    "BFF.HiddenDissipation.mode_identifiable",
    "BFF.HiddenDissipation.mode_zero_invisible"
})
assert required <= expected

found={}
for n,a in re.findall(
    r"'([^']+)' depends on axioms: \[([^\]]*)\]",log
):
    found[n]={x.strip() for x in a.split(",") if x.strip()}

for n in re.findall(
    r"'([^']+)' does not depend on any axioms",log
):
    found[n]=set()

allowed={"propext","Classical.choice","Quot.sound"}
assert set(found)==expected,(expected-set(found),set(found)-expected)
assert all(a<=allowed for a in found.values()),found
assert not re.search(
    r"\b(?:axiom|opaque|sorry|admit|native_decide)\b",src
)
assert not re.search(r"\b(?:sorryAx|sorry|admit)\b",log)
assert not re.search(r"(?m)^.*error(?:\([^)]*\))?:",log)

print("AXIOM_AUDIT := PASS_41_OF_41")
