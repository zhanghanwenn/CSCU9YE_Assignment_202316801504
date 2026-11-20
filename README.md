# Proof of Process — CSCU9YE Assessment

**Candidate:** 202316801504
**Module:** CSCU9YE
**Assessment:** Metaheuristics for Multi-Resource Workload Allocation
**Due:** Friday 20 November, 11:59

This repository contains the submitted work and the supporting development record for the
assessment. It is provided as **proof of process / version control** evidence, as recommended
by the module team on the assessment coversheet.

## Contents

| File | Description |
|------|-------------|
| `202316801504_CSCU9YE_AI_Assignment.ipynb` | Main submission — self-contained, executable Jupyter notebook containing Parts 1–3, all code, technical rationale and analysis. |
| `202316801504_CSCU9YE_AI_Assignment.html` | Read-only HTML export of the fully executed notebook. |
| `202316801504_CSCU9YE_Assessment Coversheet.pdf` | Completed assessment coversheet, including the AI-use declaration. |
| `Development_Log_Proof_of_Process.pdf` | Development log: timeline, algorithm design evolution, parameter-tuning record and verification steps. |
| `multi_resource_n28_m2.txt` | Supplied problem instance 1 (n=28, m=2). |
| `multi_resource_n90_m5.txt` | Supplied problem instance 2 (n=90, m=5). |
| `workload_data_loader.py` | Supplied dataset parsing utility. |

## How the work was developed

The `Development_Log_Proof_of_Process.pdf` documents the process in detail: the brief was
analysed and the problem formulated as a 0-1 multi-dimensional knapsack problem; a baseline
hill climber was built first, then a modular genetic algorithm; the penalty coefficient was
tuned empirically (a grid search over λ = 1–40, with λ = 20 selected); and a 30-run controlled
study compared two structurally distinct constraint-handling strategies. The notebook was
executed in full and verified with zero errors before export.

## AI use

Work was produced with AI assistance (WorkBuddy / Tencent Hunyuan Hy) at **Level 3 — AI
Collaboration**, the level permitted for this assessment. This is declared on the coversheet
and in the development log, in line with the University's requirement that all sources,
including AI, are acknowledged appropriately.
