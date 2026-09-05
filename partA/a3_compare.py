import regex
import tiktoken
from transformers import AutoTokenizer
from pathlib import Path


LANGUAGES = {
    "eng": "partA/data/flores_devtest/eng_Latn.txt",
    "hin": "partA/data/flores_devtest/hin_Deva.txt",
    "kan": "partA/data/flores_devtest/kan_Knda.txt",
    "tel": "partA/data/flores_devtest/tel_Telu.txt",
}


def graphemes(text):
    return len(regex.findall(r"\X", text))


def analyze(path, encode):
    lines = Path(path).read_text(encoding="utf-8").splitlines()

    total_tokens = 0
    total_words = 0
    total_graphemes = 0
    total_bytes = 0

    for line in lines:
        tokens = encode(line)

        total_tokens += len(tokens)
        total_words += len(line.split())
        total_graphemes += graphemes(line)
        total_bytes += len(line.encode("utf-8"))

    return {
        "tok/word": total_tokens / total_words,
        "tok/grapheme": total_tokens / total_graphemes,
        "tok/byte": total_tokens / total_bytes,
        "tok/sentence": total_tokens / len(lines),
        "tokens": total_tokens,
        "words": total_words,
        "graphemes": total_graphemes,
        "bytes": total_bytes,
    }


# GPT-2
gpt2 = tiktoken.get_encoding("gpt2")

# MuRIL
muril = AutoTokenizer.from_pretrained("google/muril-base-cased")


def muril_encode(text):
    return muril.encode(text, add_special_tokens=False)


print("=== GPT-2 ===")
print(
    f"{'lang':<6}"
    f"{'tok/word':>12}"
    f"{'tok/grapheme':>15}"
    f"{'tok/byte':>12}"
    f"{'tok/sentence':>15}"
    f"{'tokens':>12}"
)

print("-" * 75)

for lang, path in LANGUAGES.items():
    r = analyze(path, gpt2.encode)

    print(
        f"{lang:<6}"
        f"{r['tok/word']:>12.3f}"
        f"{r['tok/grapheme']:>15.3f}"
        f"{r['tok/byte']:>12.3f}"
        f"{r['tok/sentence']:>15.3f}"
        f"{r['tokens']:>12}"
    )


print()
print("=== MuRIL ===")
print(
    f"{'lang':<6}"
    f"{'tok/word':>12}"
    f"{'tok/grapheme':>15}"
    f"{'tok/byte':>12}"
    f"{'tok/sentence':>15}"
    f"{'tokens':>12}"
)

print("-" * 75)

for lang, path in LANGUAGES.items():
    r = analyze(path, muril_encode)

    print(
        f"{lang:<6}"
        f"{r['tok/word']:>12.3f}"
        f"{r['tok/grapheme']:>15.3f}"
        f"{r['tok/byte']:>12.3f}"
        f"{r['tok/sentence']:>15.3f}"
        f"{r['tokens']:>12}"
    )