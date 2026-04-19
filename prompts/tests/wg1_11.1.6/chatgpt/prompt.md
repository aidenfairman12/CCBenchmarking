# Data Interpretation Question Generation Prompt
# Use for: Category 2 — Climate Data & Trend Interpretation only
# Paste this into your LLM chat interface

---

You are a rigorous question writer for a climate science benchmark. Your task is to generate data interpretation questions — questions that require reasoning over a described dataset, time series, or anomaly table rather than recalling facts.

## How these questions work

Each question contains an embedded data scenario (a small table, a described trend, or a set of values). The reader must interpret or reason about that data to answer correctly. These questions test quantitative and analytical reasoning, not memory.

## Requirements

- Generate exactly 5 questions
- Each question must embed a self-contained data scenario — no external chart or image needed
- Base all scenario values on the data context provided below — do not invent values outside those ranges
- 4 answer options (A, B, C, D), exactly one is correct
- No "all of the above", "none of the above", or "both A and B" options
- Distractors should represent plausible misreadings of the data (e.g. confusing absolute value with anomaly, misreading a trend direction, off-by-one decade errors)
- The correct answer must follow directly and unambiguously from the data provided
- Do not require knowledge beyond what is presented in the scenario
- Vary difficulty: aim for roughly 2 easy, 2 medium, 1 hard per 5 questions. If you find yourself writing a third easy question, convert it to medium instead
- Ensure each question tests a distinct aspect of the data — do not generate two questions about the same feature

**Easy:** Direct reading of a value or obvious trend from the data
**Medium:** Requires comparing, computing a simple difference, or interpreting what a pattern means
**Hard:** Requires identifying a non-obvious pattern, distinguishing between two plausible interpretations, or reasoning about what the data implies

## Scenario types to use (vary across your batch)

1. **Trend identification** — a time series table; ask about direction, rate, or magnitude of change
2. **Anomaly interpretation** — anomalies relative to a baseline; ask what they indicate
3. **Comparison** — two regions or time periods side by side; ask which is warmer/wetter/more variable
4. **Index reading** — a climate index value (e.g. ENSO, NAO); ask what climate conditions it implies
5. **Projection reading** — projections under two scenarios; ask about the spread or direction

## Output Format

Return a strict JSON array and nothing else — no preamble, no commentary.

```json
[
  {
    "scenario": "A brief prose or table description of the data, embedded directly in the question or as a preamble.",
    "question": "...",
    "options": {
      "A": "...",
      "B": "...",
      "C": "...",
      "D": "..."
    },
    "correct_answer": "B",
    "explanation": "One sentence explaining which feature of the data supports the correct answer.",
    "data_source": "IPCC AR6 WG1 Chapter 11 Section 11.1.6 Box 11.2",
    "scenario_type": "trend_identification | anomaly_interpretation | comparison | index_reading | projection_reading",
    "category": "Climate Data and Trend Interpretation",
    "difficulty": "easy | medium | hard",
    "generated_by": "ChatGPT"
  }
]
```

## Data Context

Base all scenario values on the following real-world data anchor. Do not invent values — use or derive from what is provided below.

Source: IPCC AR6 WG1 Chapter 11, Section 11.1.6, Box 11.2, Table 1
Topic: Changes in low-likelihood, high-impact extreme conditions at different global warming levels
Warming levels are relative to pre-industrial baseline.
Reference point for "+1°C (Present-day)" is approximately the current climate (~2020).

IMPORTANT NOTES FOR QUESTION WRITERS:
- Units differ across rows — do not compare values across rows
- "+3°C and Higher" column: some values are assessed at exactly 3°C, others at 4°C (noted per row)
- "Not assessed" means the study did not evaluate that warming level, not that the value is zero
- Risk ratios use +1°C present-day as the reference (risk ratio = 1)

--- TABLE: EXTREME EVENT METRICS BY WARMING LEVEL ---

METRIC 1 — Risk ratio for annual hottest daytime temperature (TXx)
Reference event: 1% probability under present-day warming (+1°C)
Region: Global land | Source: Kharin et al., 2018
+1°C:   1 (reference)
+1.5°C: 3.3  (i.e., 230% higher probability)
+2°C:   8.2  (i.e., 720% higher probability)
+3°C+:  Not assessed

METRIC 2 — Risk ratio for heavy precipitation events (Rx1day)
Reference event: 1% probability under present-day warming (+1°C)
Region: Global land | Source: Kharin et al., 2018
+1°C:   1 (reference)
+1.5°C: 1.2  (i.e., 20% higher probability)
+2°C:   1.5  (i.e., 50% higher probability)
+3°C+:  Not assessed

METRIC 3 — Number of 1–5 day duration extreme floods
Reference event: 1% probability under present-day warming (+1°C)
Region: Indian subcontinent | Source: H. Ali et al., 2019
+1°C:   Up to 3 in individual locations
+1.5°C: Up to 5 in individual locations
+2°C:   2–6 in most locations
+4°C:   Up to 12 in individual locations

METRIC 4 — Probability of 'extreme extremes' hot days
Reference event: 1/1000 probability at end of 20th century
Region: Global land | Source: Vogel et al., 2020a
+1°C:   About 20 days over 20 years in most locations
+1.5°C: About 50 days in 20 years in most locations
+2°C:   About 150 days in 20 years in most locations
+3°C:   About 500 days in 20 years in most locations

METRIC 5 — Probability of co-occurrence of extreme hot days AND extreme dry days in the same week
Reference event: Each individually has 1/1000 probability at end of 20th century
Region: Amazon | Source: Vogel et al., 2020a
+1°C:   0% probability
+1.5°C: About 1 week in 20 years
+2°C:   About 4 to 5 weeks in 20 years
+3°C:   More than 9 weeks in 20 years

METRIC 6 — Projected soil moisture drought duration per year
Region: Mediterranean region | Source: Samaniego et al., 2018
+1°C:   41 days  (+46% compared to late 20th century)
+1.5°C: 58 days  (+107% compared to late 20th century)
+2°C:   71 days  (+154% compared to late 20th century)
+3°C:   125 days (+346% compared to late 20th century)

METRIC 7 — Increase in days exposed to dangerous extreme heat (Health Heat Index >40.6°C)
Region: Global land | Source: Q. Sun et al., 2019
Baseline: 1981–2000
+1°C:   Not assessed
+1.5°C: 1.6 times higher risk of experiencing heat >40.6°C
+2°C:   2.3 times higher risk of experiencing heat >40.6°C
+4°C:   Around 80% of land area exposed to dangerous heat; tropical regions exposed ~1/3 of the year

METRIC 8 — Increase in regional mean fire season length
Region: Global land | Source: Q. Sun et al., 2019; Xu et al., 2020
Baseline: 1981–2000
+1°C:   Not assessed
+1.5°C: +6.2 days
+2°C:   +9.5 days
+4°C:   About +50 days

---

## Usage Notes

- Run this prompt in a fresh chat session — do not reuse sessions across batches
- After generation, verify that the data values in each scenario are consistent with the provided data context
- Check that the correct answer is the only defensible conclusion from the data — if a second option could be argued, cut or revise
- Target acceptance rate: ~50% (slightly lower than standard due to scenario construction complexity)
- When multiple models generate questions on the same data feature, keep the version with tighter distractors
