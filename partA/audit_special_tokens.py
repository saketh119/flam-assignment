from transformers import AutoTokenizer

MODEL = "bert-base-multilingual-cased"

tokenizer = AutoTokenizer.from_pretrained(MODEL)

text = "This is a simple test sentence."

without_special = tokenizer.encode(
    text,
    add_special_tokens=False
)

with_special = tokenizer.encode(
    text,
    add_special_tokens=True
)

print("Tokenizer:", MODEL)
print("Text:", text)
print()
print("Without special tokens:")
print(without_special)
print("Count:", len(without_special))
print()
print("With special tokens:")
print(with_special)
print("Count:", len(with_special))
print()
print("Delta:", len(with_special) - len(without_special))