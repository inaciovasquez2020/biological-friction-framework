#!/usr/bin/env python3
"""Exact 5-sphere Dehn-Sommerville/f-vector audit; stdlib only.

A 5D PL sphere has at most three independent face-number parameters.
This is not an identifiability theorem about physical biological states.
"""
from itertools import combinations
from math import comb

if not __debug__:
    raise SystemExit("INCOMPLETE: Python -O disables assertions")

def boundary_simplex(n, offset=0):
    vertices=tuple(range(offset,offset+n+1))
    return {frozenset(s) for s in combinations(vertices,n)}

def faces(facets):
    return {frozenset(s) for f in facets for k in range(len(f)+1)
            for s in combinations(sorted(f),k)}

def f_vector(facets):
    fs=faces(facets)
    assert all(len(f)==6 for f in facets)
    return tuple(sum(len(face)==k for face in fs) for k in range(1,7))

def cycle(n, offset=20):
    assert n>=3
    return {frozenset((offset+i,offset+(i+1)%n)) for i in range(n)}

def join(K,L):
    assert set().union(*K).isdisjoint(set().union(*L))
    return {a|b for a in K for b in L}

def flip3(K,a,b):
    fs=faces(K)
    assert a in fs and a.isdisjoint(b) and b not in fs
    link={s-a for s in fs if a<=s}
    want=faces({b-{v} for v in b})
    assert link==want
    old={f for f in K if a<=f}
    assert old=={a|t for t in ( {b-{v} for v in b})}
    new={(a-{v})|b for v in a}
    assert not (new & (K-old))
    return (K-old)|new

def h_vector(f):
    assert len(f)==6
    augmented=(1,)+tuple(f)
    return tuple(sum((-1)**(k-j)*comb(6-j,6-k)*augmented[j]
                     for j in range(k+1)) for k in range(7))

def ds_reconstruct(f):
    a,b,c=f[:3]
    return (a,b,c,5*a-5*b+3*c,6*a-6*b+3*c,2*a-2*b+c)

def rank(rows):
    from fractions import Fraction as Q
    mat=[[Q(x) for x in row] for row in rows]
    m=len(mat); n=len(mat[0]); piv=0
    for j in range(n):
        i=next((i for i in range(piv,m) if mat[i][j]),None)
        if i is None: continue
        mat[i],mat[piv]=mat[piv],mat[i]
        scale=mat[piv][j]
        mat[piv]=[x/scale for x in mat[piv]]
        for k in range(m):
            if k!=piv:
                c=mat[k][j]
                mat[k]=[mat[k][l]-c*mat[piv][l] for l in range(n)]
        piv+=1
        if piv==m: break
    return piv

def main():
    # Relations h_0=h_6, h_1=h_5, h_2=h_4 for a 5-sphere.
    # Three independent linear equations on the six f-numbers.
    constraints=(
       ( 1,-1, 1,-1, 1,-1),
       (-4, 4,-3, 2,-1, 0),
       ( 5,-5, 3,-1, 0, 0),
    )
    assert rank(constraints)==3
    assert rank((row[:5] for row in constraints))==3
    # In fact the first five f-numbers obey two independent constraints.
    assert rank(((-5,5,-3,1,0),(-6,6,-3,0,1)))==2
    K=boundary_simplex(4)
    K1=flip3(K,frozenset((0,1,2,3)),frozenset((8,)))
    K2=flip3(K1,frozenset((0,1,2)),frozenset((4,8)))
    base=(K,K1,K2)
    assert [len(x) for x in base]==[5,8,9]
    tests=0
    for n in range(3,16):
        C=cycle(n)
        values=[]
        for k in base:
            F=f_vector(join(k,C))
            H=h_vector(F)
            assert H==(H[6],H[5],H[4],H[3],H[2],H[1],H[0])
            assert F==ds_reconstruct(F)
            assert F[4]==3*F[5]
            facets=join(k,C)
            ridges={frozenset(s) for facet in facets for s in combinations(sorted(facet),5)}
            assert len(ridges)==F[4]
            assert all(sum(r<=facet for facet in facets)==2 for r in ridges)
            assert F[0]-F[1]+F[2]-F[3]+F[4]-F[5]==0
            values.append(F)
            tests+=1
        assert values[1][5]-values[0][5]==3*n
        assert values[2][5]-values[1][5]==n
    assert tests==39
    print("EXACT_SPHERE_JOIN_CASES := 39")
    print("F_VECTOR_RELATION_RANK := 3")
    print("FACE_COUNT_AFFINE_PARAMETER_BOUND := 3")
    print("FIVE_FACE_COUNT_CHANNELS_INDEPENDENT := FALSE")
    print("5D_F_VECTOR_DS_CHECKS := PASS")
    print("PHYSICAL_FIFTH_DIMENSION := NOT_ESTABLISHED")
    print("BIOLOGICAL_MAPPING := OPEN")
    print("LEAN_VERIFIED := NO")
    print("RESULT := COMPUTATION_PASS")

if __name__=="__main__":
    main()
