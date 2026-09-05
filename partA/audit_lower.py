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

    original_tokens = 0
    lowercase_tokens = 0

    changed_lines = 0

    for line in lines:
        original = len(encode(line))
        lowered = len(encode(line.lower()))

        original_tokens += original
        lowercase_tokens += lowered

        if original != lowered:
            changed_lines += 1

    return original_tokens, lowercase_tokens, changed_lines


enc = tiktoken.get_encoding("gpt2")

print(f"{'lang':<6} {'original tok':>15} {'lowercase tok':>15} {'delta':>10} {'changed lines':>15}")
print("-" * 67)

for lang, path in LANGUAGES.items():
    original, lowered, changed = analyze(path, enc.encode)
    delta = lowered - original

    print(f"{lang:<6} {original:>15} {lowered:>15} {delta:>10} {changed:>15}")