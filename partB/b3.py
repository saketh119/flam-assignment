import csv

path = "bench/bench_log.csv"

with open(path, newline="") as f:
    rows = list(csv.DictReader(f))

print("CSV loaded:", len(rows), "rows")

print("\n=== Batch 24, long prompt ===")

for r in rows:
    if (
        r["batch_size"] == "24"
        and r["prompt_len"] == "3584"
        and r["gen_len"] == "512"
    ):
        batch = int(r["batch_size"])
        prompt = int(r["prompt_len"])
        gen = int(r["gen_len"])
        wall = float(r["wall_clock_s"])
        reported = float(r["reported_tok_s"])

        print("batch_size =", batch)
        print("prompt_len =", prompt)
        print("gen_len =", gen)
        print("wall_clock_s =", wall)
        print("reported_tok_s =", reported)

        total_tokens = batch * (prompt + gen)
        reconstructed = total_tokens / wall

        print("\nReported metric reconstruction:")
        print(f"{batch} * ({prompt} + {gen}) / {wall}")
        print(f"= {reconstructed:.2f} tok/s")

        goodput1 = batch * gen / wall

        print("\nMethod 1 - generated tokens / wall clock:")
        print(f"{batch} * {gen} / {wall}")
        print(f"= {goodput1:.2f} output tok/s")

        goodput2 = reported * gen / (prompt + gen)

        print("\nMethod 2 - correcting reported throughput:")
        print(f"{reported} * {gen} / ({prompt} + {gen})")
        print(f"= {goodput2:.2f} output tok/s")

        break
else:
    print("ERROR: Batch-24 long-prompt row was not found.")


print("\n=== Batch 16 comparison ===")

for r in rows:
    if r["batch_size"] == "16":
        batch = int(r["batch_size"])
        prompt = int(r["prompt_len"])
        gen = int(r["gen_len"])
        wall = float(r["wall_clock_s"])
        reported = float(r["reported_tok_s"])

        goodput = batch * gen / wall

        print(
            f"prompt={prompt}, gen={gen}, "
            f"reported={reported}, "
            f"output_goodput={goodput:.2f} tok/s"
        )