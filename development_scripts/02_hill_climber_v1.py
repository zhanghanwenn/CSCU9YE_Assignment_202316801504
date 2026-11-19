"""DEV STAGE 2 - first baseline hill climber.

Added the greedy repair operator (drop least efficient item until feasible)
and a simple single-flip neighbour search. This early version stalled at
local optima, which motivated the perturbation added in stage 3.
"""
import numpy as np
from stage_util import load_workload_instance


def repair(x, p, R, b):
    x = x.copy().astype(bool)
    bs = np.where(b <= 0, 1.0, b)
    while x.any() and not np.all(R @ x <= b + 1e-9):
        sel = np.flatnonzero(x)
        cons = np.sum(R[:, sel] / bs[:, None], axis=0)
        eff = p[sel] / (cons + 1e-12)
        x[sel[int(np.argmin(eff))]] = False
    return x


def hill_climb(p, R, b, seed, max_evals):
    rng = np.random.default_rng(seed)
    n = len(p)
    x = repair(rng.random(n) < 0.4, p, R, b)
    f = float(p @ x)
    best_x, best_f = x.copy(), f
    evals = 0
    while evals < max_evals:
        y = x.copy()
        j = rng.integers(n); y[j] = ~y[j]
        yf = repair(y, p, R, b)
        fy = float(p @ yf); evals += 1
        if fy > f:
            x, f = yf, fy
            if fy > best_f:
                best_f, best_x = fy, yf.copy()
    return best_f, best_x


if __name__ == "__main__":
    n, m, p, R, b = load_workload_instance("multi_resource_n28_m2.txt")
    f, x = hill_climb(p, R, b, seed=42, max_evals=4000)
    print("baseline hill climb best:", f, "feasible:", bool(np.all(R @ x <= b)))
