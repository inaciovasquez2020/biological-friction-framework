#!/usr/bin/env python3
"""Exact rational 5-state dissipative observer test. No scientific-data claims."""
from fractions import Fraction as Q
from itertools import product

if not __debug__:
    raise SystemExit('INCOMPLETE: optimized execution disables assertions')

N = 5
DECAY = tuple(Q(10 - j, 10) for j in range(1, N + 1))  # 9/10 ... 1/2
assert DECAY == (Q(9,10), Q(4,5), Q(7,10), Q(3,5), Q(1,2))

def propagate(state, t):
    return tuple(DECAY[j] ** t * state[j] for j in range(N))

def measure4(state):
    return state[:4]

def measure5(state):
    return state

def energy(state):
    return sum((v*v for v in state), Q(0)) / 2

def rank(rows, cols):
    a = [[Q(c) for c in row] for row in rows]
    pos = 0
    for j in range(cols):
        pivot = next((i for i in range(pos, len(a)) if a[i][j] != 0), None)
        if pivot is None:
            continue
        a[pos], a[pivot] = a[pivot], a[pos]
        p = a[pos][j]
        a[pos] = [v/p for v in a[pos]]
        for i in range(len(a)):
            if i != pos:
                m = a[i][j]
                a[i] = [a[i][k] - m*a[pos][k] for k in range(cols)]
        pos += 1
    return pos

def observation_rows(channels, times):
    return [tuple(DECAY[j] ** t if j == c else Q(0) for j in range(N))
            for t in range(times) for c in range(channels)]

def main():
    kernel = (Q(0),Q(0),Q(0),Q(0),Q(1))
    assert measure4(kernel) == (0,0,0,0)
    assert energy(kernel) != energy((Q(0),)*N)
    for steps in (1,2,3,5,9,20):
        assert rank(observation_rows(4, steps), 5) == 4
        assert rank(observation_rows(5, steps), 5) == 5
        for t in range(steps):
            assert measure4(propagate(kernel, t)) == (0,0,0,0)
    checked = 0
    for raw in product(range(-2,3), repeat=N):
        x = tuple(map(Q,raw))
        for t in range(8):
            now = propagate(x, t)
            after = propagate(x,t+1)
            assert energy(after) <= energy(now)
            if any(x):
                assert energy(after) < energy(now)
            assert measure5(now) == now
            checked += 1
    print('STATE_DIMENSION := 5')
    print('OBSERVABILITY_RANK_FOUR_CHANNELS := 4')
    print('OBSERVABILITY_RANK_FIVE_CHANNELS := 5')
    print('FULL_TIME_SERIES_HIDDEN_STATE_COUNTEREXAMPLE := PASS')
    print('ENERGY_STRICT_DECREASE_NONZERO := PASS')
    print('EXACT_RATIONAL_TRANSITIONS :=', checked)
    print('SPATIAL_FIFTH_DIMENSION := NOT_ESTABLISHED')
    print('BIOLOGICAL_EMPIRICAL_VALIDATION := NOT_RUN')
    print('RESULT := COMPUTATION_PASS')

if __name__ == '__main__':
    main()
