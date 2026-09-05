# AI Team Intern Assignment — Experiment Log

## Part A — Baseline

### A2 Baseline: Original fertility.py

**Corpus:** FLORES-200 devtest

**Languages:** English, Hindi, Kannada, Telugu

**Tokenizer:** GPT-2

**Script:** `partA/fertility.py` (original, unchanged)

**Command:**

python partA\fertility.py --corpus eng=partA\data\flores_devtest\eng_Latn.txt --corpus hin=partA\data\flores_devtest\hin_Deva.txt --corpus kan=partA\data\flores_devtest\kan_Knda.txt --corpus tel=partA\data\flores_devtest\tel_Telu.txt --tokenizer gpt2


**Result:**

| Language | Fertility (tok/word) | Tok/char |
| -------- | -------------------: | -------: |
| English  |                 1.29 |    0.214 |
| Hindi    |                 7.87 |    1.529 |
| Kannada  |                22.57 |    2.660 |
| Telugu   |                20.57 |    2.645 |

**Reported ratios:**

* Hindi: 6.11× English
* Kannada: 17.53× English
* Telugu: 15.97× English

**Purpose:** Establish the baseline behavior of the supplied implementation before making any changes.

---

## A2 Experiment 1 — Whitespace splitting

### Hypothesis

The use of `split(" ")` may incorrectly handle repeated spaces or other whitespace, causing the word denominator to be incorrect.

### Before

Original implementation:


words = line.split(" ")


**Command:**


python partA\fertility.py --corpus eng=partA\data\flores_devtest\eng_Latn.txt --corpus hin=partA\data\flores_devtest\hin_Deva.txt --corpus kan=partA\data\flores_devtest\kan_Knda.txt --corpus tel=partA\data\flores_devtest\tel_Telu.txt --tokenizer gpt2


| Language | Fertility |
| -------- | --------: |
| English  |      1.29 |
| Hindi    |      7.87 |
| Kannada  |     22.57 |
| Telugu   |     20.57 |

### Change

Changed only:


words = line.split(" ")


to:


words = line.split()


### After

**Command:**


python partA\fertility_fixed.py --corpus eng=partA\data\flores_devtest\eng_Latn.txt --corpus hin=partA\data\flores_devtest\hin_Deva.txt --corpus kan=partA\data\flores_devtest\kan_Knda.txt --corpus tel=partA\data\flores_devtest\tel_Telu.txt --tokenizer gpt2


| Language | Fertility |
| -------- | --------: |
| English  |      1.29 |
| Hindi    |      7.87 |
| Kannada  |     23.02 |
| Telugu   |     20.83 |

### Delta

| Language | Absolute change | Relative change |
| -------- | --------------: | --------------: |
| English  |            0.00 |           0.00% |
| Hindi    |            0.00 |           0.00% |
| Kannada  |           +0.45 |          +1.99% |
| Telugu   |           +0.26 |          +1.26% |

### Conclusion

Replacing `split(" ")` with `split()` changes the measured fertility for Kannada and Telugu, but not English or Hindi, on this corpus. The correction increases fertility because the original implementation can count empty fields created by repeated spaces as words. This is a real implementation issue, but its measured effect is modest on this corpus.

**Evidence boundary:** The experiment establishes that the implementation change affects the aggregate fertility metric. It does not by itself establish which exact whitespace patterns in the corpus caused the observed language-specific deltas.

---

## A2 Experiment 2 — Character denominator definition

### Hypothesis

The `tok/char` metric depends on how a "character" is defined. Python's `len()` on a Unicode string counts Unicode code points, which may differ from user-perceived characters (grapheme clusters). UTF-8 byte count is another possible denominator.

### Change

The original implementation uses:


chars = len(line)


The audit script compares three denominators:

* Unicode code points
* Unicode grapheme clusters
* UTF-8 bytes

**Script:** `partA\audit_chars.py`

**Command:**


python partA\audit_chars.py


### Result

| Language | tok/codepoint | tok/grapheme | tok/byte |
| -------- | ------------: | -----------: | -------: |
| English  |        0.2049 |       0.2049 |   0.2047 |
| Hindi    |        1.5296 |       2.3332 |   0.5947 |
| Kannada  |        2.6616 |       4.0655 |   0.9788 |
| Telugu   |        2.6479 |       4.5811 |   0.9918 |

### Conclusion

The same token counts produce substantially different normalized values depending on the denominator. This effect is especially large for the Indic languages because Unicode code points, grapheme clusters, and UTF-8 bytes represent different quantities.

Therefore, `tok/char` should not be treated as a tokenizer-independent measure of "character efficiency" without explicitly defining what a character means.

**Evidence boundary:** This experiment demonstrates that the denominator definition materially changes the reported metric. It does not imply that one denominator is universally correct; the appropriate denominator depends on the question being asked.

---

## A2 Experiment 3 — Per-line average vs aggregate ratio

### Hypothesis

The original implementation calculates fertility as the mean of per-line ratios:


sum(per_line_fertility) / n


An alternative is to calculate one aggregate ratio:


total tokens / total words


These are mathematically different estimators and may produce different results.

### Script

`partA\audit_aggregator.py`

### Command


python partA\audit_aggregator.py


### Result

| Language | Per-line average | Aggregate | Difference |
| -------- | ---------------: | --------: | ---------: |
| English  |           0.2070 |    0.2049 |    -0.0021 |
| Hindi    |           1.5289 |    1.5296 |    +0.0007 |
| Kannada  |           2.6598 |    2.6616 |    +0.0018 |
| Telugu   |           2.6445 |    2.6479 |    +0.0034 |

### Relative difference

| Language | Relative difference |
| -------- | ------------------: |
| English  |              -1.01% |
| Hindi    |             +0.046% |
| Kannada  |             +0.068% |
| Telugu   |             +0.129% |

### Conclusion

Per-line averaging and aggregate token/denominator ratios are mathematically different. On this corpus, however, their effect is small for Hindi, Kannada, and Telugu and approximately 1% for English.

This is primarily a metric-definition/statistical choice rather than evidence of a severe implementation bug.

**Evidence boundary:** The experiment establishes that the two aggregation methods produce different values. The measured differences on this corpus are small, so this should not be presented as the main source of the large multilingual fertility gap.

---

## A2 Experiment 4 — Lowercasing before tokenization

### Hypothesis

The original implementation lowercases every line before tokenization:


line = line.lower()


This changes the actual text passed to the tokenizer. If the goal is to measure the supplied workload faithfully, silently lowercasing may change the token counts.

### Raw token-count experiment

**Script:** `partA\audit_lower.py`

**Result:**

| Language | Original tokens | Lowercased tokens | Delta | Lines changed |
| -------- | --------------: | ----------------: | ----: | ------------: |
| English  |         270,044 |           270,994 |  +950 |           469 |
| Hindi    |         200,467 |           200,475 |    +8 |            14 |
| Kannada  |         367,405 |           367,427 |   +22 |            29 |
| Telugu   |         350,763 |           350,863 |  +100 |            66 |

### Fertility comparison

The corrected script was also run with and without lowercasing.

**With lowercasing:**

| Language | Fertility | Tok/char |
| -------- | --------: | -------: |
| English  |      1.29 |    0.214 |
| Hindi    |      7.87 |    1.529 |
| Kannada  |     23.02 |    2.660 |
| Telugu   |     20.83 |    2.645 |

**Without lowercasing:**

| Language | Fertility | Tok/char |
| -------- | --------: | -------: |
| English  |      1.24 |    0.207 |
| Hindi    |      7.87 |    1.529 |
| Kannada  |     23.02 |    2.660 |
| Telugu   |     20.82 |    2.644 |

### Delta in fertility

| Language | Absolute change |      Relative change |
| -------- | --------------: | -------------------: |
| English  |           -0.05 |               -3.88% |
| Hindi    |            0.00 |                0.00% |
| Kannada  |            0.00 |                0.00% |
| Telugu   |           -0.01 | approximately -0.05% |

### Conclusion

Lowercasing changes the input workload before tokenization and produces a measurable change in English fertility on this corpus. It should therefore be treated as an explicit preprocessing choice rather than an invisible part of the audit.

The effect is language-dependent: it is material for English in this experiment but negligible for the three Indic languages.

**Evidence boundary:** The experiment demonstrates that lowercasing changes tokenization behavior. It does not establish that lowercasing is universally incorrect; whether it is appropriate depends on whether the production workload itself is normalized to lowercase.

---

## A2 Experiment 5 — Random seed

### Hypothesis

The original script sets:


random.seed(1337)


This looks potentially relevant to reproducibility, but the script does not appear to perform any random operations.

### Change

Created `partA\fertility_no_seed2.py` by removing only:


random.seed(1337)


No other code changes were made.

### Command


python partA\fertility_no_seed2.py --corpus eng=partA\data\flores_devtest\eng_Latn.txt --corpus hin=partA\data\flores_devtest\hin_Deva.txt --corpus kan=partA\data\flores_devtest\kan_Knda.txt --corpus tel=partA\data\flores_devtest\tel_Telu.txt --tokenizer gpt2


### Result

| Language | Original fertility | Without seed | Delta |
| -------- | -----------------: | -----------: | ----: |
| English  |               1.29 |         1.29 |  0.00 |
| Hindi    |               7.87 |         7.87 |  0.00 |
| Kannada  |              22.57 |        22.57 |  0.00 |
| Telugu   |              20.57 |        20.57 |  0.00 |

The other reported metric values also matched the baseline.

### Conclusion

The seed is currently unused because the script contains no random operation affecting the result. Removing it therefore has no measurable effect.

This is a suspicious-looking line that is **not a bug in the current execution path**.

---

## A2 Experiment 6 — Special-token handling

### Hypothesis

The Hugging Face tokenizer branch explicitly uses:


add_special_tokens=False


This could look suspicious because many transformer tokenizers normally add special tokens.

### Experiment

A simple sentence was tokenized with `bert-base-multilingual-cased` with and without automatically added special tokens.

**Input:**


This is a simple test sentence.


### Result

| Configuration              | Token count |
| -------------------------- | ----------: |
| `add_special_tokens=False` |           7 |
| `add_special_tokens=True`  |           9 |

The special-token version added two sequence-boundary tokens.

### Conclusion

For a fertility audit, `add_special_tokens=False` is appropriate because the objective is to measure the tokens required to represent the supplied text itself. Automatically added sequence-boundary tokens are tokenizer formatting overhead rather than tokens present in the input text.

Therefore, this is another suspicious-looking implementation detail that is actually correct for the stated measurement.

---

# Part A3 — Corrected Cross-Language Comparison

## A3 Experiment 1 — Tokenizer and denominator comparison

### Objective

Compare an English-oriented tokenizer with an Indic-aware tokenizer using the same corpus and consistent denominator definitions across all four languages.

**Corpus:** FLORES-200 devtest

**Languages:** English, Hindi, Kannada, Telugu

**Number of aligned sentences:** 1,012

**Tokenizers:**

* GPT-2
* `google/muril-base-cased` (MuRIL)

**Script:** `partA\a3_compare.py`

**Command:**


python partA\a3_compare.py


### Results

| Language | GPT-2 tok/word | MuRIL tok/word | GPT-2 tok/grapheme | MuRIL tok/grapheme | GPT-2 tok/byte | MuRIL tok/byte |
| -------- | -------------: | -------------: | -----------------: | -----------------: | -------------: | -------------: |
| English  |          1.235 |          1.259 |              0.205 |              0.209 |          0.205 |          0.209 |
| Hindi    |          7.818 |          1.247 |              2.332 |              0.372 |          0.595 |          0.095 |
| Kannada  |         22.820 |          1.826 |              4.066 |              0.325 |          0.979 |          0.078 |
| Telugu   |         20.709 |          1.959 |              4.581 |              0.433 |          0.992 |          0.094 |

### Interpretation

Relative to GPT-2, MuRIL reduces tokens per word by approximately:

* Hindi: 6.3× fewer
* Kannada: 12.5× fewer
* Telugu: 10.6× fewer

English changes by only approximately 2%, with MuRIL producing slightly more tokens per word.

This shows that the large Indic-language tokenization gap is strongly tokenizer-dependent rather than simply a property of the languages themselves.

---

## A3 Experiment 2 — Parallel-sentence denominator

Because FLORES-200 is a parallel corpus, each language contains the same 1,012 aligned sentence positions.

Tokens per parallel sentence therefore provides a denominator that is held constant across languages.

### Results

| Language | GPT-2 tok/sentence | MuRIL tok/sentence | Approx. reduction |
| -------- | -----------------: | -----------------: | ----------------: |
| English  |             26.723 |             27.254 |             -2.0% |
| Hindi    |            198.090 |             31.602 |             84.0% |
| Kannada  |            363.048 |             29.056 |             92.0% |
| Telugu   |            346.604 |             32.790 |             90.5% |

### Interpretation

The large Indic-language difference remains when using the parallel-sentence denominator.

For Hindi, MuRIL reduces tokens per sentence from 198.090 to 31.602, an approximately 84.0% reduction.

For Kannada, MuRIL reduces tokens per sentence from 363.048 to 29.056, an approximately 92.0% reduction.

For Telugu, MuRIL reduces tokens per sentence from 346.604 to 32.790, an approximately 90.5% reduction.

English changes only slightly, from 26.723 to 27.254 tokens per sentence.

Therefore, the observed Indic tokenization gap is not simply an artifact of using whitespace word count as the denominator.

---

## Routing and Cost Metric

For production routing and cost estimation, the most useful single number is **actual input/output tokens per request for the deployed tokenizer/model pair**.

Metrics such as tok/word, tok/grapheme, and tok/byte are useful diagnostic measures, but serving systems process tokenized sequences. Actual tokens per request therefore directly reflects context usage and token-based serving cost.

For controlled cross-language corpus comparison, **tokens per parallel sentence** is the most useful normalized diagnostic in this experiment because the denominator is held constant at the same aligned sentence count.

The measurements support routing Indic-language traffic through an Indic-aware tokenizer/model stack rather than assuming an English-oriented tokenizer provides comparable tokenization efficiency.

---

# Part A4 — Routing and Cost Memo

## Corrected headline numbers

On the 1,012-sentence FLORES-200 devtest corpus, GPT-2 produced 200,467 Hindi tokens, 367,405 Kannada tokens, and 350,763 Telugu tokens. MuRIL produced 31,981, 29,405, and 33,183 respectively.

Using the aligned-sentence denominator:

| Language | GPT-2 tok/sentence | MuRIL tok/sentence | Reduction |
| -------- | -----------------: | -----------------: | --------: |
| Hindi    |            198.090 |             31.602 |     84.0% |
| Kannada  |            363.048 |             29.056 |     92.0% |
| Telugu   |            346.604 |             32.790 |     90.5% |
| English  |             26.723 |             27.254 |     -2.0% |

The results show a large tokenization-efficiency gap for the three Indic languages with GPT-2, while MuRIL remains approximately comparable on English.

## Routing recommendation

Indic-language traffic should be routed to an Indic-aware tokenizer/model stack such as MuRIL rather than using the GPT-2 tokenizer as a common multilingual baseline.

The measured token reduction is large enough to justify further serving-level validation. However, this experiment measured token counts rather than end-to-end latency or monetary serving cost.

## Biggest caveat

FLORES-200 is a general-domain parallel translation corpus rather than a representative sample of conversational production traffic. It contains limited evidence about code-switching, spelling variation, informal language, and real user prompts.

Therefore, the measured tokenization gap should be treated as strong corpus-level evidence rather than as a direct estimate of production savings.

## Production metric

The primary production metric should be **input tokens per request**, segmented by language and tokenizer/model route.

Output tokens per request should be tracked separately.

This directly measures the tokenized workload entering the serving system and provides a production quantity that can be connected to context usage and token-based serving cost.


### Current completion

With this version, **Part A is complete**:

- A1 ✅
- A2 baseline ✅
- A2 experiments ✅
- A3 comparison ✅
- A4 memo ✅

Next we should start **Part B1: KV-cache calculation** from `model_spec.md`.

