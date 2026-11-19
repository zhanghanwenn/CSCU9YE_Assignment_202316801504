"""Shared helper for the development-stage scripts."""
import numpy as np

def load_workload_instance(path):
    with open(path, "r") as fh:
        tok = fh.read().split()
    n, m = int(tok[0]), int(tok[1]); i = 2
    p = np.array([float(t) for t in tok[i:i+n]]); i += n
    R = np.zeros((m, n))
    for r in range(m):
        R[r] = [float(t) for t in tok[i:i+n]]; i += n
    b = np.array([float(t) for t in tok[i:i+m]])
    return n, m, p, R, b

def repair(x, p, R, b):
    x = x.copy().astype(bool); bs = np.where(b <= 0, 1.0, b)
    while x.any() and not np.all(R @ x <= b + 1e-9):
        sel = np.flatnonzero(x)
        cons = np.sum(R[:, sel] / bs[:, None], axis=0)
        eff = p[sel] / (cons + 1e-12)
        x[sel[int(np.argmin(eff))]] = False
    return x
