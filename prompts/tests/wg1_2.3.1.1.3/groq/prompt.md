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
    "data_source": "IPCC AR6 WG1 Chapter 2 Section 2.3.1.1.3",
    "scenario_type": "trend_identification | anomaly_interpretation | comparison | index_reading | projection_reading",
    "category": "Climate Data and Trend Interpretation",
    "difficulty": "easy | medium | hard",
    "generated_by": "Llama 3.3 70B (Groq)"
  }
]
```

## Data Context

Base all scenario values on the following real-world data anchor. Do not invent values — use or derive from what is provided below.

Source: IPCC AR6 WG1 Chapter 2, Table 2.4
Topic: Observed increase in global mean surface temperature (GMST), land surface air temperature (LSAT), and sea surface temperature (SST)
Units: degrees Celsius (°C). Confidence ranges in square brackets where available.

DEFINITIONS:
- GMST: Global Mean Surface Temperature (blended land + ocean)
- LSAT: Land Surface Air Temperature only
- SST: Sea Surface Temperature only
- Period change (columns 1–3): total warming relative to 1850–1900 baseline
- Trend (columns 4–6): total change over stated period using ordinary least squares

COLUMN HEADERS:
Col 1: Change from 1850–1900 to 1995–2014 (°C)
Col 2: Change from 1850–1900 to 2001–2020 (°C)
Col 3: Change from 1850–1900 to 2011–2020 (°C)
Col 4: Trend over 1880–2020 (°C)
Col 5: Trend over 1960–2020 (°C)
Col 6: Trend over 1980–2020 (°C)

--- MULTI-DATASET AVERAGES (primary data for questions) ---

           Col 1  Col 2  Col 3  Col 4  Col 5  Col 6
GMST       0.85   0.99   1.09   1.11   1.04   0.76
LSAT       1.27   1.47   1.59   1.50   1.51   1.18
SST        0.67   0.79   0.88   0.96   0.86   0.60

--- SINGLE DATASET: HadCRUT5 (for single-dataset comparison questions) ---

                   Col 1              Col 2              Col 3              Col 4              Col 5              Col 6
GMST    0.87 [0.81–0.94]  1.01 [0.94–1.09]  1.12 [1.06–1.18]  1.10 [0.89–1.32]  1.04 [0.93–1.14]  0.76 [0.65–0.87]
LSAT    1.23 [1.06–1.38]  1.44 [1.26–1.59]  1.55 [1.39–1.70]  1.43 [1.16–1.70]  1.50 [1.33–1.67]  1.20 [1.04–1.36]
SST     0.73 [0.69–0.78]  0.85 [0.81–0.90]  0.94 [0.90–0.99]  1.03 [0.80–1.25]  0.90 [0.80–0.99]  0.62 [0.51–0.72]

--- KEY PATTERNS FOR QUESTION DESIGN ---
- LSAT warms faster than GMST, which warms faster than SST (consistent across all periods)
- More recent end periods show higher cumulative warming (Col 1 < Col 2 < Col 3)
- The 1880–2020 trend (Col 4) exceeds the 1960–2020 trend (Col 5), which exceeds the 1980–2020 trend (Col 6)
  — this is expected: shorter recent periods show less total change but represent faster rates

NOTE FOR QUESTION WRITERS: Write scenarios using the average rows or HadCRUT5 rows only.
Do not reference specific dataset names (HadCRUT5, GISTEMP, etc.) in question stems —
readers should not need to know what these datasets are to answer correctly.

---

## Usage Notes

- Run this prompt in a fresh chat session — do not reuse sessions across batches
- After generation, verify that the data values in each scenario are consistent with the provided data context
- Check that the correct answer is the only defensible conclusion from the data — if a second option could be argued, cut or revise
- Target acceptance rate: ~50% (slightly lower than standard due to scenario construction complexity)
- When multiple models generate questions on the same data feature, keep the version with tighter distractors
