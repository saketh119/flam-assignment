import csv

path = "bench/bench_log.csv"

rows = []

with open(path, newline="") as f:
    for row in csv.DictReader(f):
        if row["prompt_len"] == "3584":
            rows.append(row)

print(
    f"{'batch':>6} {'reported_tok_s':>16} "
    f"{'kv_util':>10} {'preempted':>12} {'ttft_ms':>12} {'e2e_p95_ms':>14}"
)

for r in rows:
    print(
        f"{r['batch_size']:>6} "
        f"{r['reported_tok_s']:>16} "
        f"{r['kv_cache_util']:>10} "
        f"{r['preempted_seqs']:>12} "
        f"{r['ttft_ms_p50']:>12} "
        f"{r['e2e_ms_p95']:>14}"
    )

# Linear-scaling comparison from batch 24
base = next(r for r in rows if r["batch_size"] == "24")

base_batch = int(base["batch_size"])
base_tp = float(base["reported_tok_s"])

for r in rows:
    batch = int(r["batch_size"])

    if batch <= base_batch:
        continue

    expected = base_tp * batch / base_batch
    observed = float(r["reported_tok_s"])
    shortfall_pct = (expected - observed) / expected * 100

    print(
        f"batch={batch}: "
        f"expected={expected:.1f}, "
        f"observed={observed:.1f}, "
        f"below_linear={shortfall_pct:.1f}%"
    )