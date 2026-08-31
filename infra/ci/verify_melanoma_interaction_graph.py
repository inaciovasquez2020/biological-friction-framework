import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CERT_PATH = ROOT / "infra" / "certificates" / "melanoma_interaction_graph.json"


def _require_unique(items, label):
    ids = [item["id"] for item in items]
    assert len(ids) == len(set(ids)), f"duplicate {label} id"
    return set(ids)


def _require_evidence(paths):
    assert paths, "missing evidence"
    for rel in paths:
        path = ROOT / rel
        assert path.is_file(), f"missing evidence file: {rel}"


def _validate_edge(edge, state_ids):
    assert edge["source"] in state_ids, f"unknown edge source: {edge['source']}"
    assert edge["target"] in state_ids, f"unknown edge target: {edge['target']}"
    _require_evidence(edge.get("evidence", []))


def load_certificate(path=CERT_PATH):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def verify_graph(cert):
    assert cert.get("schema_version") == 1, "unsupported schema_version"

    states = cert.get("states", [])
    controls = cert.get("controls", [])
    baseline_edges = cert.get("baseline_edges", [])

    state_ids = _require_unique(states, "state")
    control_ids = _require_unique(controls, "control")
    baseline_edge_ids = _require_unique(baseline_edges, "baseline edge")

    assert state_ids, "no states"
    assert control_ids, "no controls"

    initial_states = set(cert.get("initial_states", []))
    assert initial_states, "no initial states"
    assert initial_states <= state_ids, "unknown initial state"

    malignant_states = {s["id"] for s in states if s.get("malignant") is True}

    for edge in baseline_edges:
        _validate_edge(edge, state_ids)

    induced_edges = []
    for control in controls:
        assert control.get("kind") in {"functional", "implementation"}, (
            f"invalid control kind: {control['id']}"
        )
        _require_evidence(control.get("evidence", []))
        for edge in control.get("induces", []):
            _validate_edge(edge, state_ids)
            induced_edges.append(edge)

    induced_edge_ids = _require_unique(induced_edges, "induced edge")
    all_edge_ids = baseline_edge_ids | induced_edge_ids

    active_controls = set(cert.get("active_controls", []))
    assert active_controls <= control_ids, "unknown active control"

    controls_by_id = {c["id"]: c for c in controls}
    blocked_edges = set()
    active_induced_edges = []
    for control_id in active_controls:
        control = controls_by_id[control_id]
        blocked_edges.update(control.get("blocks", []))
        active_induced_edges.extend(control.get("induces", []))

    assert blocked_edges <= all_edge_ids, "control blocks unknown edge"

    active_edges = [e for e in baseline_edges if e["id"] not in blocked_edges]
    active_edges.extend(
        e for e in active_induced_edges if e["id"] not in blocked_edges
    )

    adjacency = {state_id: [] for state_id in state_ids}
    for edge in active_edges:
        adjacency[edge["source"]].append(edge["target"])

    reachable = set(initial_states)
    frontier = list(initial_states)
    while frontier:
        source = frontier.pop()
        for target in adjacency[source]:
            if target not in reachable:
                reachable.add(target)
                frontier.append(target)

    reachable_malignant = reachable & malignant_states
    declared_unresolved = set(cert.get("declared_unresolved", []))
    assert declared_unresolved <= malignant_states, "unresolved state is not malignant"

    claim = cert.get("claim")
    if claim == "closed":
        assert not reachable_malignant, (
            "closed claim invalid; reachable malignant states: "
            + ", ".join(sorted(reachable_malignant))
        )
        assert not declared_unresolved, "closed claim cannot declare unresolved states"
    elif claim == "conditional":
        assert declared_unresolved == reachable_malignant, (
            "conditional claim must declare exactly all reachable malignant states; "
            f"declared={sorted(declared_unresolved)} "
            f"reachable={sorted(reachable_malignant)}"
        )
    else:
        raise AssertionError(f"unsupported claim: {claim}")

    return {
        "valid": True,
        "claim": claim,
        "reachable": sorted(reachable),
        "reachable_malignant": sorted(reachable_malignant),
    }


if __name__ == "__main__":
    result = verify_graph(load_certificate())
    print(json.dumps(result, sort_keys=True))
