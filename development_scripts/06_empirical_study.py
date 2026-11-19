"""DEV STAGE 6 - empirical study and non-parametric tests.

Final comparison: 30 independent runs, equal 12,000-evaluation budget, common
random numbers. Mann-Whitney U, Wilcoxon signed-rank and Cliff's delta.
"""
import numpy as np
from scipy import stats
from stage_util import load_workload_instance
from importlib import import_module
ga = import_module("04_genetic_algorithm")
Instance, GA, Budget = ga.Instance, ga.GA, ga.Budget
RepairHandler, PenaltyHandler = ga.RepairHandler, ga.PenaltyHandler

n, m, p, R, b = load_workload_instance("../multi_resource_n90_m5.txt")
inst = Instance(p, R, b)
B, M = 12000, 30
seeds = [142 + i for i in range(M)]

if __name__ == "__main__":
    hard = np.array([GA(inst, RepairHandler(inst), s).run(Budget(B))[0] for s in seeds])
    soft = np.array([GA(inst, PenaltyHandler(inst, 20), s).run(Budget(B))[0] for s in seeds])
    print("repair mean=%.1f  penalty mean=%.1f" % (hard.mean(), soft.mean()))
    U, pval = stats.mannwhitneyu(soft, hard, alternative="two-sided")
    W, pw = stats.wilcoxon(soft, hard, alternative="greater")
    delta = 2 * U / (M * M) - 1
    print("Mann-Whitney U=%.1f p=%.3g | Wilcoxon p=%.3g | Cliff delta=%.3f" %
          (U, pval, pw, delta))
