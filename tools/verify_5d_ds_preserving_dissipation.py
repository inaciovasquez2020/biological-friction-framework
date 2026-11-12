#!/usr/bin/env python3
"""Exact rational dissipation respecting 5-sphere Dehn-Sommerville equations.

The evolution acts on a rational relaxation, NOT on triangulations.
No dependencies or downloads.
"""
from fractions import Fraction as Q
from itertools import combinations

if not __debug__:
    raise SystemExit("INCOMPLETE: assertion checks disabled by -O")

RELATIONS = (
    (Q(1),Q(-1),Q(1),Q(-1),Q(1),Q(-1)),
    (Q(-4),Q(4),Q(-3),Q(2),Q(-1),Q(0)),
    (Q(5),Q(-5),Q(3),Q(-1),Q(0),Q(0)),
)
ZERO = Q(0)
HALF = Q(1,2)

def ds(f):
    assert len(f) == 6
    return all(sum((a*b for a,b in zip(row,f)), ZERO) == ZERO
               for row in RELATIONS)

def boundary(n):
    return {frozenset(t) for t in combinations(range(n+1),n)}

def faces(K):
    return {frozenset(t) for s in K for j in range(len(s)+1)
            for t in combinations(sorted(s),j)}

def flip3(K,a,b):
    assert a.isdisjoint(b) and b not in faces(K)
    assert {s-a for s in faces(K) if a<=s} == faces({b-{v} for v in b})
    removed={s for s in K if a<=s}
    assert removed == {a|(b-{v}) for v in b}
    inserted={(a-{v})|b for v in a}
    assert not ((K-removed)&inserted)
    return (K-removed)|inserted

def circle(n, offset=20):
    assert n>=3
    return {frozenset((offset+i,offset+(i+1)%n)) for i in range(n)}

def fvec_join(K,C):
    assert set().union(*K).isdisjoint(set().union(*C))
    joined={a|b for a in K for b in C}
    allfaces=faces(joined)
    return tuple(Q(sum(len(s)==j for s in allfaces)) for j in range(1,7))

def step(f,anchor,lam=HALF):
    assert ds(f) and ds(anchor) and ZERO<lam<Q(1)
    return tuple(anchor[i]+lam*(f[i]-anchor[i]) for i in range(6))

def energy(f,anchor):
    return sum(((x-y)**2 for x,y in zip(f,anchor)),ZERO)/2

def main():
    K=boundary(4)
    K1=flip3(K,frozenset((0,1,2,3)),frozenset((8,)))
    K2=flip3(K1,frozenset((0,1,2)),frozenset((4,8)))
    assert list(map(len,(K,K1,K2)))==[5,8,9]
    anchor=fvec_join(K,circle(3))
    assert anchor==(8,28,55,65,45,15) and ds(anchor)
    tested=0
    for n in range(3,16):
        C=circle(n)
        for mesh in (K,K1,K2):
            f=fvec_join(mesh,C)
            assert ds(f)
            x=f
            for k in range(1,11):
                y=step(x,anchor)
                assert ds(y)
                assert energy(y,anchor)==energy(x,anchor)/4
                assert all(y[i]==anchor[i]+HALF**k*(f[i]-anchor[i])
                           for i in range(6))
                if x!=anchor:
                    assert energy(y,anchor)<energy(x,anchor)
                x=y
                tested+=1
    assert tested==390
    # A legal 1->4 base move, joined with a triangle, has 5D
    # face-count difference (1,7,21,33,27,9).
    moved=fvec_join(K1,circle(3))
    delta=tuple(moved[i]-anchor[i] for i in range(6))
    assert delta==(1,7,21,33,27,9)
    midpoint=step(moved,anchor)
    assert ds(midpoint) and any(x.denominator!=1 for x in midpoint)
    assert midpoint[0]==Q(17,2)
    assert midpoint!=anchor and midpoint!=moved
    # The independently audited prior five-channel dynamics is diagonal,
    # and fails to preserve the DS subspace when applied to full f-vectors.
    old_decay=(Q(9,10),Q(4,5),Q(7,10),Q(3,5),Q(1,2),Q(2,5))
    diagonal=tuple(old_decay[i]*moved[i] for i in range(6))
    assert not ds(diagonal)
    print("REFERENCE_F_VECTOR :=",tuple(map(int,anchor)))
    print("EXACT_RATIONAL_STEPS :=",tested)
    print("DS_PRESERVATION := PASS")
    print("ENERGY_QUARTERING := PASS")
    print("MIDPOINT_NONINTEGER_COUNTEREXAMPLE := PASS")
    print("NAIVE_DIAGONAL_DS_PRESERVATION := FAIL")
    print("REALIZABLE_TRIANGULATION_PATH := NOT_PROVED")
    print("BIOLOGICAL_GEOMETRIC_IDENTIFICATION := OPEN")
    print("LEAN_VERIFIED := NO")
    print("RESULT := COMPUTATION_PASS")

if __name__=="__main__":
    main()
