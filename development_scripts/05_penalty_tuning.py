"""DEV STAGE 5 - penalty coefficient tuning (failure -> grid search).

lambda=0.5 completely failed: the population never reached the feasible region
(all final utilities were zero). A grid search over lambda = 1,2,5,10,20,40
was run and lambda=20 was selected for the empirical study.
"""
import numpy as np
from stage_util import load_workload_instance
from importlib import import_module
ga_mod = import_module("04_genetic_algorithm")
Instance, GA, Budget = ga_mod.Instance, ga_mod.GA, ga_mod.Budget
PenaltyHandler = ga_mod.PenaltyHandler

n, m, p, R, b = load_workload_instance("../multi_resource_n90_m5.txt")
inst = Instance(p, R, b)

if __name__ == "__main__":
    for lam in [1, 2, 5, 10, 20, 40]:
        vals = [GA(inst, PenaltyHandler(inst, lam), s).run(Budget(6000))[0]
                for s in [1000, 1001, 1002]]
        print("lambda=%3d  mean=%9.1f  median=%9.1f" %
              (lam, np.mean(vals), np.median(vals)))
