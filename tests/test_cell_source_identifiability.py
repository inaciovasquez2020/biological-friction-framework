"""Exact-rational checks of a two-compartment linear mixture; not patient-data analysis."""
from fractions import Fraction as F
from itertools import product

def bulk(pi, tumor, immune):
    return pi*tumor+(1-pi)*immune

def recover(pi, observed, immune):
    assert 0 < pi <= 1
    return (observed-(1-pi)*immune)/pi

def run():
    checks = 0
    collisions = []
    # All positive compartment fractions and bounded nonnegative expression values.
    for pi in (F(1,4),F(1,3),F(1,2),F(2,3),F(3,4)):
        pairs = {}
        for tumor, immune in product(range(21), repeat=2):
            b=bulk(pi,F(tumor),F(immune))
            assert recover(pi,b,F(immune)) == tumor
            checks += 1
            if b in pairs and pairs[b][0] != tumor:
                collisions.append((pi,b,pairs[b],(tumor,immune)))
            pairs.setdefault(b,(tumor,immune))
    assert collisions
    assert bulk(F(1,2),F(20),F(0)) == bulk(F(1,2),F(0),F(20)) == 10
    # Error bound for exact pi, bounded independent observed and immune errors.
    error_checks = 0
    for pi in (F(1,4),F(1,2),F(3,4),F(1)):
        for t,i,eb,ei in product((F(0),F(7)),(F(0),F(11)),(F(-2),F(0),F(2)),(F(-3),F(0),F(3))):
            obs=bulk(pi,t,i)
            est=recover(pi,obs+eb,i+ei)
            bound=(abs(eb)+(1-pi)*abs(ei))/pi
            assert abs(est-t)<=bound
            error_checks+=1
    # If purity is unknown, even exact observed and immune compartment expression cannot identify tumor expression.
    assert recover(F(1,2),F(10),F(0)) == 20
    assert recover(F(1,4),F(10),F(0)) == 40
    print('EXACT_ARITHMETIC := PASS')
    print(f'INVERSE_CASES := {checks}')
    print(f'ERROR_BOUND_CASES := {error_checks}')
    print(f'NONIDENTIFIABLE_COLLISIONS_FOUND := {len(collisions)}')
    print('PURITY_UNKNOWN_COUNTEREXAMPLE := PASS')
    print('PATIENT_DATA := NOT_RUN')
    print('FPKM_LINEAR_MIXTURE_ASSUMPTION := NOT_ESTABLISHED')

if __name__=='__main__': run()
