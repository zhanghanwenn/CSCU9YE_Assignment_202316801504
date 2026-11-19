"""DEV STAGE 1 - parse and validate the supplied instances.

Earliest working code: confirm the text format and check that the
'deploy everything' solution is infeasible (i.e. constraints are active).
"""
import numpy as np


def load_workload_instance(path):
    with open(path, "r") as fh:
        tok = fh.read().split()
    n, m = int(tok[0]), int(tok[1])
    i = 2
    p = np.array([float(t) for t in tok[i:i+n]]); i += n
    R = np.zeros((m, n))
    for r in range(m):
        R[r] = [float(t) for t in tok[i:i+n]]; i += n
    b = np.array([float(t) for t in tok[i:i+m]])
    return n, m, p, R, b


if __name__ == "__main__":
    for f in ["multi_resource_n28_m2.txt", "multi_resource_n90_m5.txt"]:
        n, m, p, R, b = load_workload_instance(f)
        print(f, "n=", n, "m=", m, "p.shape=", p.shape, "R.shape=", R.shape)
        print("   all-in usage:", (R @ np.ones(n)).astype(int), "capacity:", b.astype(int))
        print("   feasible:", bool(np.all(R.sum(axis=1) <= b)))
