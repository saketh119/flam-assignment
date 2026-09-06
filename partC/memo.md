# Part C — Making Multilingual Outputs Conversational

## Recommendation

Use **SFT with synthetic casualized pairs** as the primary approach.

The objective is to change response style without changing the underlying meaning. SFT directly teaches the desired conversational behavior and does not add a second inference model or an additional production inference pass.

Prompt engineering should still be tested on Day 1 as the cheapest baseline. If prompting alone reaches the launch threshold, stop there rather than spending the remaining training budget.

## Assumptions

The following are planning estimates rather than measured results:

- Six target languages: Hindi, Kannada, Tamil, Telugu, Bengali, Marathi.
- 5,000 synthetic instruction/response pairs per language.
- Total synthetic dataset: 30,000 pairs.
- Average response length: approximately 100 tokens.
- One A100-80GB is available for two weeks.
- One native reviewer is available for Hindi and Kannada for 10 hours/week.
- The reviewer is not assumed to provide equivalent human validation for Tamil, Telugu, Bengali, and Marathi.

## Back-of-the-envelope estimates

### Data volume

```text
5,000 pairs/language × 6 languages = 30,000 pairs

30,000 pairs × ~100 response tokens
≈ 3 million response tokens
```

This is a deliberately small dataset for a focused style adaptation rather than a general language-model training run.

### Training

Use parameter-efficient SFT (for example, LoRA/QLoRA) rather than full-model training.

A practical initial plan is:

```text
30,000 examples
× 2–3 epochs
= 60,000–90,000 example presentations
```

The exact wall-clock time should be measured from the first pilot run because throughput depends on sequence length, packing, precision, and implementation. The two-week budget is therefore treated as an upper bound, not as a claimed measured training time.

### Serving cost

SFT changes the existing model rather than adding a second model.

Therefore the proposed solution adds:

```text
additional model inference passes = 0
additional rewriter serving = 0
```

There can still be a small increase in inference cost if the fine-tuned model changes output length, so output tokens/request should be monitored after deployment.

### Reviewer throughput

Reserve approximately 20 reviewer-hours across the two weeks:

```text
10 hours/week × 2 weeks = 20 hours
```

At approximately one minute per reviewed output:

```text
1,000 examples × 1 minute
= 1,000 minutes
≈ 16.7 hours
```

This leaves roughly 3.3 hours for adjudicating difficult examples and regression checks.

The review budget should be concentrated on Hindi and Kannada because those are the languages for which native-speaker review is available.

## Success metric

The launch candidate should satisfy both:

**≥80% conversational acceptance**

and

**≥95% semantic preservation**

on the reviewed Hindi/Kannada evaluation set.

Conversational acceptance means the reviewer considers the answer naturally conversational rather than textbook/formal.

Semantic preservation means the response retains the intended meaning and does not introduce a material factual or instruction-following error.

A style improvement that reduces meaning preservation should not be considered a successful launch.

## Kill criterion

Stop the SFT experiment at the end of **Week 1** if either condition is true on the reviewed Hindi/Kannada evaluation:

```text
conversational acceptance < 70%
OR
semantic preservation < 95%
```

If the criterion is triggered, fall back to the strongest simpler baseline, starting with prompt engineering, rather than spending the remaining week polishing a failing fine-tune.

## Day-1 experiment

Before committing the full training budget, create a small representative evaluation set spanning all six languages.

Compare:

1. Baseline model.
2. Prompt-engineered baseline.
3. Small SFT pilot using a subset of the synthetic data.

For Hindi and Kannada, have the reviewer perform a blind comparison focused on:

- conversational/natural style;
- preservation of meaning;
- unwanted slang or awkwardness.

For the other four languages, use the same evaluation prompts and automated checks, while explicitly treating the absence of native-speaker review as a launch risk.

The Day-1 decision is:

```text
If prompt engineering already meets the target:
    use prompt engineering.

Else if the SFT pilot shows a clear improvement without
semantic regressions:
    proceed with the full SFT run.

Else:
    do not spend the remaining compute budget on SFT.
```

## Main risks

### Limited native-language validation

Only Hindi and Kannada have direct native-speaker review. Results for Tamil, Telugu, Bengali, and Marathi therefore have lower confidence.

### Synthetic-data quality

Synthetic casualization can reproduce unnatural phrasing or teach the model undesirable patterns. The reviewer should therefore inspect examples rather than treating synthetic data as ground truth.

### Meaning drift

A response can sound more casual while changing facts, instructions, or intent. Semantic preservation must therefore be a separate launch metric.

### Over-casualization

The target is conversational language, not slang everywhere. The evaluation should penalize outputs that become unprofessional, overly colloquial, or inappropriate for the user's context.

## Decision

Proceed with a small Day-1 comparison first, then use the Week-1 gate to decide whether to complete the SFT run.

The preferred final solution is **SFT with synthetic casualized pairs**, because it changes the model's behavior without introducing a separate inference-time rewriter and its recurring serving overhead.
