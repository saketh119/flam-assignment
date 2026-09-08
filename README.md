# FLAM Assignment — Progress Log

> For detailed methodology, commands, scripts, and full result tables, see [NOTEBOOK.md](./NOTEBOOK.md).

---

## Part A — Tokenizer Fertility Audit

### Step 1 · Baseline (A2)
Ran the original `fertility.py` on the FLORES-200 devtest corpus (English, Hindi, Kannada, Telugu) using the GPT-2 tokenizer.

**Result:** Hindi was 6.1×, Kannada 17.5×, and Telugu 16.0× more expensive than English in tokens-per-word.

---

### Step 2 · Experiment 1 — Whitespace splitting
Changed `split(" ")` → `split()` to correctly handle repeated/varied whitespace.

**Result:** Fertility for Kannada increased by +0.45 (≈+2%) and Telugu by +0.26 (≈+1.3%). English and Hindi were unaffected. Confirmed as a real implementation bug with a modest measured effect on this corpus.

---

### Step 3 · Experiment 2 — Character denominator definition
Compared tok/codepoint, tok/grapheme-cluster, and tok/UTF-8-byte as denominators using `audit_chars.py`.

**Result:** The three denominators produce substantially different values for Indic languages (e.g., Hindi tok/char: 1.53 → 2.33 → 0.59 across the three definitions). The `tok/char` metric is not comparable across languages without an explicit denominator definition.

---

### Step 4 · Experiment 3 — Aggregation method
Compared per-line average vs. aggregate (total tokens / total words) using `audit_aggregator.py`.

**Result:** Differences were small on this corpus (< 1% for all languages). This is a metric-definition choice rather than a critical bug.

---

### Step 5 · Experiment 4 — Lowercasing before tokenization
Measured the effect of the silent `line.lower()` call using `audit_lower.py`.

**Result:** Lowercasing adds +950 English tokens across 469 lines (≈−3.9% fertility when removed). Effect is negligible for Indic languages. Identified as an implicit preprocessing choice that should be made explicit.

---

### Step 6 · Experiment 5 — Random seed
Removed the unused `random.seed(1337)` call and re-ran.

**Result:** Zero change in any fertility value. The seed is currently unused — the script performs no random operations. Suspicious-looking but not a bug in the current execution path.

---

### Step 7 · Experiment 6 — Special-token handling
Tested `add_special_tokens=False` vs `True` on a sample sentence with `bert-base-multilingual-cased`.

**Result:** `add_special_tokens=True` adds 2 boundary tokens per sentence. For a fertility audit the `False` setting is correct — boundary tokens are tokenizer formatting overhead, not tokens present in the input text.

---

### Step 8 · Corrected Cross-Language Comparison (A3)
Ran `a3_compare.py`: compared GPT-2 vs MuRIL on the same 1,012 aligned FLORES-200 sentences using consistent denominators (tok/word, tok/grapheme, tok/byte, tok/sentence).

**Result:**
- MuRIL reduces Indic tokens-per-sentence by ~84% (Hindi), ~92% (Kannada), ~90.5% (Telugu).
- English changes by only ~2%.
- The large Indic fertility gap is strongly tokenizer-dependent, not merely a property of the languages.

---

### Step 9 · Routing and Cost Memo (A4)
Summarized findings and issued a routing recommendation.

**Result:** Indic-language traffic should be routed to an Indic-aware tokenizer/model stack (e.g., MuRIL). The primary production metric to track is **input tokens per request**, segmented by language and tokenizer/model route. Caveat: FLORES-200 is a general-domain corpus and may not fully represent production traffic patterns.

---
