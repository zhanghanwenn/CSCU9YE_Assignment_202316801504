"""DEV STAGE 4 - modular Genetic Algorithm.

Switched from single-trajectory local search to a population method for the
90-model instance. Constraint handler injected as a parameter so the repair
vs penalty strategies can be swapped without changing the search loop.
"""
import numpy as np
from stage_util import load_workload_instance, repair


class Instance:
    def __init__(self, p, R, b):
        self.p, self.R, self.b = p, R, b
        self.n, self.m = len(p), len(b)
        self.scale = float(np.mean(p))
        self.bs = np.where(b <= 0, 1.0, b)
    def utility(self, x): return float(self.p @ x)
    def rel_violation(self, x):
        return float(np.sum(np.maximum(0, self.R @ x - self.b) / self.bs))
    def feasible(self, x): return bool(np.all(self.R @ x <= self.b + 1e-9))


class RepairHandler:
    name = "repair"
    def __init__(self, inst): self.inst = inst
    def evaluate(self, x, budget):
        budget.spend()
        xf = repair(x, self.inst.p, self.inst.R, self.inst.b)
        return self.inst.utility(xf), xf


class PenaltyHandler:
    name = "penalty"
    def __init__(self, inst, lam): self.inst, self.lam = inst, lam
    def evaluate(self, x, budget):
        budget.spend()
        return (self.inst.utility(x) - self.lam * self.inst.scale * self.inst.rel_violation(x)), x


def tournament(pop, fits, rng, k=3):
    idx = rng.integers(0, len(pop), size=k)
    return pop[idx[int(np.argmax(fits[idx]))]].copy()

def uniform_crossover(a, b, rng):
    m = rng.random(len(a)) < 0.5; c = a.copy(); c[m] = b[m]; return c

def bit_flip(x, rng, rate):
    x = x.copy(); m = rng.random(len(x)) < rate; x[m] = ~x[m]; return x


class GA:
    def __init__(self, inst, handler, seed, pop_size=40):
        self.inst, self.h, self.rng = inst, handler, np.random.default_rng(seed)
        self.pop_size = pop_size
    def run(self, budget):
        inst, h, rng = self.inst, self.h, self.rng
        pop = rng.random((self.pop_size, inst.n)) < 0.5
        fits = np.zeros(self.pop_size); incumbent = 0.0; curve = []
        for i in range(self.pop_size):
            fit, xf = h.evaluate(pop[i], budget); fits[i] = fit; pop[i] = xf
            if inst.feasible(xf):
                incumbent = max(incumbent, inst.utility(xf))
        curve.append((budget.used, incumbent))
        while not budget.done():
            order = np.argsort(fits)[::-1]
            new = [pop[i].copy() for i in order[:2]]
            while len(new) < self.pop_size and not budget.done():
                pa = tournament(pop, fits, rng); pb = tournament(pop, fits, rng)
                c = bit_flip(uniform_crossover(pa, pb, rng), rng, 1.0 / inst.n)
                new.append(c)
            pop = np.array(new); fits = np.zeros(len(pop))
            for i in range(len(pop)):
                fit, xf = h.evaluate(pop[i], budget); fits[i] = fit; pop[i] = xf
                if inst.feasible(xf): incumbent = max(incumbent, inst.utility(xf))
            curve.append((budget.used, incumbent))
        return incumbent, curve


class Budget:
    def __init__(self, limit): self.limit, self.used = int(limit), 0
    def spend(self, k=1): self.used += k
    def done(self): return self.used >= self.limit


if __name__ == "__main__":
    n, m, p, R, b = load_workload_instance("../multi_resource_n90_m5.txt")
    inst = Instance(p, R, b)
    best, _ = GA(inst, RepairHandler(inst), 42).run(Budget(8000))
    print("GA repair best:", best)
