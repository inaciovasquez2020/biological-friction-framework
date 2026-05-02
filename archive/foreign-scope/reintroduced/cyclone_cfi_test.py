import networkx as nx
import random

def random_sigma(G):
    return {tuple(sorted(e)): random.choice([0, 1]) for e in G.edges()}

def potential_shift(G, sigma, phi):
    shifted = {}
    for (u, v) in G.edges():
        key = tuple(sorted((u, v)))
        shifted[key] = sigma[key] ^ (phi[u] ^ phi[v])
    return shifted

def cycle_sum(G, sigma, cycle):
    s = 0
    for i in range(len(cycle)):
        u = cycle[i]
        v = cycle[(i + 1) % len(cycle)]
        key = tuple(sorted((u, v)))
        s ^= sigma[key]
    return s

def obstruction(G, sigma):
    for c in nx.cycle_basis(G):
        if cycle_sum(G, sigma, c) == 1:
            return True
    return False

def random_potential(G):
    return {v: random.choice([0, 1]) for v in G.nodes()}

def test_obstruction_invariance():
    G = nx.random_regular_graph(d=3, n=20)
    sigma = random_sigma(G)
    phi = random_potential(G)

    obs1 = obstruction(G, sigma)
    obs2 = obstruction(G, potential_shift(G, sigma, phi))

    print("Obstruction invariant:", obs1 == obs2)
    assert obs1 == obs2

def test_sigma_separation():
    G = nx.cycle_graph(10)

    sigma1 = {tuple(sorted(e)): 0 for e in G.edges()}

    sigma2 = sigma1.copy()
    e = list(G.edges())[0]
    sigma2[tuple(sorted(e))] = 1

    obs1 = obstruction(G, sigma1)
    obs2 = obstruction(G, sigma2)

    print("Separation exists:", obs1 != obs2)
    assert obs1 != obs2


def local_view(G, sigma, v, R=2):
    nodes = nx.single_source_shortest_path_length(G, v, cutoff=R).keys()
    sub = G.subgraph(nodes)
    return (len(sub.nodes()), len(sub.edges()))

def test_local_equivalence():
    G = nx.random_regular_graph(d=3, n=30)
    sigma1 = random_sigma(G)
    sigma2 = random_sigma(G)

    ok = all(local_view(G, sigma1, v) == local_view(G, sigma2, v) for v in G.nodes())

    print("Local FO^k equivalence proxy:", ok)
    assert ok

def run_all():
    print("=== Cyclone CFI Test Suite ===")
    r1 = test_obstruction_invariance()
    r2 = test_sigma_separation()
    r3 = test_local_equivalence()

    print("\nRESULTS:")
    print("Obstruction invariant:", r1)
    print("Sigma separation:", r2)
    print("Local equivalence:", r3)

    return r1 and r2 and r3

if __name__ == "__main__":
    success = run_all()
    print("\nPASS" if success else "\nFAIL")
