#!/usr/bin/env python3
"""Exact combinatorial-vs-metric nonidentifiability witness; no physical claims."""
from itertools import combinations
from fractions import Fraction as Q

if not __debug__:
    raise SystemExit("INCOMPLETE: assertions disabled by -O")

def boundary_simplex(vertices):
    vertices=frozenset(vertices)
    return {vertices-{v} for v in vertices}

def all_faces(facets):
    return {frozenset(x) for f in facets
            for k in range(len(f)+1)
            for x in combinations(sorted(f),k)}

def gram_regular_5(edge_length):
    ell=Q(edge_length)
    assert ell>0
    return [[ell*ell if i==j else ell*ell/2
             for j in range(5)] for i in range(5)]

def det_exact(matrix):
    a=[[Q(x) for x in row] for row in matrix]
    n=len(a); ans=Q(1)
    for j in range(n):
        pivot=next((i for i in range(j,n) if a[i][j]),None)
        assert pivot is not None
        if pivot!=j:
            a[j],a[pivot]=a[pivot],a[j]
            ans=-ans
        v=a[j][j]
        ans*=v
        for k in range(j+1,n):
            coeff=a[k][j]/v
            for l in range(j,n):
                a[k][l]-=coeff*a[j][l]
    return ans

def main():
    K=boundary_simplex(range(7))
    assert len(K)==7 and all(len(f)==6 for f in K)
    F=all_faces(K)
    fvec=tuple(sum(len(x)==k for x in F) for k in range(1,7))
    assert fvec==(7,21,35,35,21,7)
    edges={s for s in F if len(s)==2}
    assert len(edges)==21
    length_models={q:{e:q for e in edges}
                   for q in (Q(1),Q(2),Q(3,2),Q(5,3))}
    assert all(set(m)==edges for m in length_models.values())
    checks=0
    unit_det=det_exact(gram_regular_5(Q(1)))
    assert unit_det==Q(3,16)
    for q, model in length_models.items():
        assert all(e in model for f in K for e in combinations(sorted(f),2))
        assert all(model[e]==q for e in edges)
        assert det_exact(gram_regular_5(q))==unit_det*q**10
        assert q>0
        checks+=1
    assert length_models[Q(1)]!=length_models[Q(2)]
    # A single unweighted face complex supports two distinct
    # consistent piecewise-Euclidean length assignments.
    # Scale factor two changes lengths by two and 5D volumes by 2^5.
    assert Q(2)**5==32
    assert det_exact(gram_regular_5(Q(2)))==1024*unit_det
    print("S5_SIMPLEX_BOUNDARY_F_VECTOR :=",fvec)
    print("SAME_COMBINATORIAL_STRUCTURE := PASS")
    print("DISTINCT_CONSISTENT_EDGE_METRICS :=",checks)
    print("LENGTH_RATIO_UNIT_TO_DOUBLE := 2")
    print("FIVE_VOLUME_RATIO_UNIT_TO_DOUBLE := 32")
    print("EXACT_GRAM_DETERMINANTS := PASS")
    print("METRIC_RECOVERABLE_FROM_UNWEIGHTED_FACES := FALSE")
    print("PHYSICAL_FIFTH_SPATIAL_DIMENSION_ESTABLISHED := NO")
    print("BIOLOGICAL_COUPLING_VALIDATED := NO")
    print("RESULT := COMPUTATION_PASS_FINITE_NONIDENTIFIABILITY_WITNESS")

if __name__=="__main__":
    main()
