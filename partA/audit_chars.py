import regex
import tiktoken
from pathlib import Path


LANGUAGES = {
    "eng": "partA/data/flores_devtest/eng_Latn.txt",
    "hin": "partA/data/flores_devtest/hin_Deva.txt",
    "kan": "partA/data/flores_devtest/kan_Knda.txt",
    "tel": "partA/data/flores_devtest/tel_Telu.txt",
}


def grapheme_count(text):
    return len(regex.findall(r"\X", text))


def analyze(path, encode):
    total_tokens = 0
    total_codepoints = 0
    total_graphemes = 0
    total_bytes = 0

    lines = Path(path).read_text(encoding="utf-8").splitlines()

    for line in lines:
        tokens = encode(line)

        total_tokens += len(tokens)
        total_codepoints += len(line)
        total_graphemes += grapheme_count(line)
        total_bytes += len(line.encode("utf-8"))

    return (
        total_tokens / total_codepoints,
        total_tokens / total_graphemes,
        total_tokens / total_bytes,
    )


enc = tiktoken.get_encoding("gpt2")

print(f"{'lang':<6} {'tok/codepoint':>15} {'tok/grapheme':>15} {'tok/byte':>12}")
print("-" * 52)

for lang, path in LANGUAGES.items():
    codepoint, grapheme, byte = analyze(path, enc.encode)
    print(f"{lang:<6} {codepoint:>15.4f} {grapheme:>15.4f} {byte:>12.4f}")