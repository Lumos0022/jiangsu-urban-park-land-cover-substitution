# -*- coding: utf-8 -*-
import csv
from collections import defaultdict
f = r"G:\Codex\Jiangsu_HumanBird_Tradeoff\03_数据库\投稿前重构_20260904\Reanalysis_v2\substitution_matrix_v2\P01_v2_all_pairs_10pct_park_predictions.csv"
responses = set()
with open(f, encoding="utf-8-sig", newline="") as fh:
    for r in csv.DictReader(fh):
        responses.add(r["response"])
print("responses:", responses)
# contrast aggregation
agg = defaultdict(list)
with open(f, encoding="utf-8-sig", newline="") as fh:
    for r in csv.DictReader(fh):
        if r["response"] == "annular_contrast" and r["scenario_pct"] == "10":
            agg[(r["donor"], r["recipient"])].append(float(r["delta_pred_K"]))
res = []
for (d, rc), v in agg.items():
    v.sort()
    n = len(v)
    res.append((d, rc, n, sum(v) / n, v[int(0.025 * n)], v[int(0.975 * n) - 1]))
res.sort(key=lambda x: x[3])
for d, rc, n, m, lo, hi in res:
    print(f"{d}->{rc:6s} n={n:4d} mean={m:+.3f} [p2.5={lo:+.2f}, p97.5={hi:+.2f}]")
