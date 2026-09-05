import tiktoken
from pathlib import Path


LANGUAGES = {
    "eng": "partA/data/flores_devtest/eng_Latn.txt",
    "hin": "partA/data/flores_devtest/hin_Deva.txt",
    "kan": "partA/data/flores_devtest/kan_Knda.txt",
    "tel": "partA/data/flores_devtest/tel_Telu.txt",
}


def analyze(path, encode):
    lines = Path(path).read_text(encoding="utf-8").splitlines()

    per_line_ratios = []
    total_tokens = 0
    total_chars = 0

    for line in lines:
        tokens = encode(line)
        chars = len(line)

        per_line_ratios.append(len(tokens) / chars)
        total_tokens += len(tokens)
        total_chars += chars

    per_line_average = sum(per_line_ratios) / len(per_line_ratios)
    aggregate_ratio = total_tokens / total_chars

    return per_line_average, aggregate_ratio


enc = tiktoken.get_encoding("gpt2")

print(f"{'lang':<6} {'per-line avg':>15} {'aggregate':>15} {'difference':>15}")
print("-" * 55)

for lang, path in LANGUAGES.items():
    per_line, aggregate = analyze(path, enc.encode)
    difference = aggregate - per_line

    print(f"{lang:<6} {per_line:>15.4f} {aggregate:>15.4f} {difference:>15.4f}")