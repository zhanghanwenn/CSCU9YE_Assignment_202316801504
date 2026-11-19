"""DEV STAGE 3 - iterated local search (perturbation added).

The stage-2 climber stalled at local optima. This version adds a random kick
(perturbation) from the incumbent when no improving neighbour is found, plus
an explicit evaluation Budget so runs are comparable.
"""
import numpy as np
from stage_util import load_workload_instance, repair


class Budget:
    def __init__(self, limit):
        self.limit, self.used = int(limit), 0
    def spend(self, k=1):
        self.used += k
    def done(self):
        return self.used >= self.limit


def hill_climb_ils(p, R, b, seed, budget, kick_frac=0.15, stall_limit=12):
    rng = np.random.default_rng(seed); n = len(p)
    x = repair(rng.random(n) < 0.4, p, R, b); f = float(p @ x)
    best_x, best_f = x.copy(), f
    stall = 0
    while not budget.done():
        improved = False
        for _ in range(n):
            if budget.done(): break
            y = x.copy(); j = rng.integers(n); y[j] = ~y[j]
            yf = repair(y, p, R, b); fy = float(p @ yf); budget.spend()
            if fy > f + 1e-9:
                x, f, improved = yf, fy, True
                if fy > best_f: best_f, best_x = fy, yf.copy()
                break
        stall = 0 if improved else stall + 1
        if stall >= stall_limit:
            k = max(2, int(kick_frac * n)); y = best_x.copy()
            for j in rng.choice(n, size=k, replace=False): y[j] = ~y[j]
            x = repair(y, p, R, b); f = float(p @ x); stall = 0
            if f > best_f: best_f, best_x = f, x.copy()
    return best_f, best_x


if __name__ == "__main__":
    n, m, p, R, b = load_workload_instance("../multi_resource_n28_m2.txt")
    vals = [hill_climb_ils(p, R, b, s, Budget(6000))[0] for s in range(42, 52)]
    print("ILS 10 runs: mean=%.1f max=%.1f" % (np.mean(vals), np.max(vals)))
