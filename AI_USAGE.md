# AI Usage

AI assistance was used selectively for validation and debugging during the assignment.

- In Part A, I used AI to sanity-check hypotheses about the audit implementation. AI helped identify the `split(" ")` word-count issue and the effect of the unused random seed. I then re-ran the code with controlled changes to verify whether these were real issues and measured the resulting deltas.
- AI was also used to sanity-check the Unicode character/grapheme denominator distinction and the effect of special tokens. These were tested independently before being used in the analysis.
- In Part B, AI was used to verify the KV-cache arithmetic, throughput calculations, and the interpretation of the benchmark columns. The resulting numbers were independently calculated from the provided model specification and benchmark log.
- AI was used for minor formatting and organization of the final documentation.

All reported experimental results are based on actual code execution and the provided benchmark data. AI-generated suggestions were not treated as evidence without independent verification.