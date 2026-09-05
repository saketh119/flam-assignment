# Part A4 — Routing and Cost Memo

## Corrected headline numbers

On the 1,012-sentence FLORES-200 devtest corpus, GPT-2 produced 200,467 Hindi tokens, 367,405 Kannada tokens, and 350,763 Telugu tokens. MuRIL produced 31,981, 29,405, and 33,183 respectively.

Using the aligned-sentence denominator, this corresponds to:

| Language | GPT-2 tok/sentence | MuRIL tok/sentence | Reduction |
|---|---:|---:|---:|
| Hindi | 198.090 | 31.602 | 84.0% |
| Kannada | 363.048 | 29.056 | 92.0% |
| Telugu | 346.604 | 32.790 | 90.5% |
| English | 26.723 | 27.254 | -2.0% |

The results show a large tokenization-efficiency gap for the three Indic languages with GPT-2, while MuRIL remains approximately comparable on English.

## Routing recommendation

Indic-language traffic should be routed to an Indic-aware tokenizer/model stack such as MuRIL rather than using the GPT-2 tokenizer as a common multilingual baseline. The measured token reduction is large enough that it can materially reduce the number of tokens entering the model for Indic requests.

This recommendation should be validated with the actual production serving stack before making a direct cost claim, because this audit measured token counts rather than end-to-end serving cost.

## Biggest caveat

FLORES-200 is a general-domain parallel translation corpus rather than a representative sample of conversational production traffic. It contains limited evidence about code-switching, spelling variation, informal language, and real user prompts. Therefore, the measured tokenization gap should be treated as strong corpus-level evidence, not as a direct estimate of production savings.

## Production metric

The primary production metric should be **input tokens per request**, segmented by language and tokenizer/model route. This directly measures the quantity of tokenized input that drives context usage and token-based serving cost. Output tokens/request should be tracked separately.