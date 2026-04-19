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
    "data_source": "IPCC AR6 WG1 Chapter 9 Section 9.6.3.3",
    "scenario_type": "trend_identification | anomaly_interpretation | comparison | index_reading | projection_reading",
    "category": "Climate Data and Trend Interpretation",
    "difficulty": "easy | medium | hard",
    "generated_by": "ChatGPT"
  }
]
```

## Data Context

Base all scenario values on the following real-world data anchor. Do not invent values — use or derive from what is provided below.

Source: IPCC AR6 WG1 Chapter 9, Table 9.9
Topic: Global mean sea level projections for five SSP scenarios
Baseline: 1995–2014
Units: metres (m) unless noted. Format: median (likely range).
Rates in mm yr⁻¹. Individual contributions shown for year 2100.
Note: SSP5-8.5 Low Confidence column incorporates low-confidence processes (SEJ/MICI); its range is 17th–83rd percentile, not an assessed likely range.

--- INDIVIDUAL CONTRIBUTIONS AT 2100 (metres) ---

Component             SSP1-1.9          SSP1-2.6          SSP2-4.5          SSP3-7.0          SSP5-8.5          SSP5-8.5 (Low Conf.)
Thermal expansion     0.12 (0.09–0.15)  0.14 (0.11–0.18)  0.20 (0.16–0.24)  0.25 (0.21–0.30)  0.30 (0.24–0.36)  0.30 (0.24–0.36)
Greenland             0.05 (0.00–0.09)  0.06 (0.01–0.10)  0.08 (0.04–0.13)  0.11 (0.07–0.16)  0.13 (0.09–0.18)  0.18 (0.09–0.59)
Antarctica            0.10 (0.03–0.25)  0.11 (0.03–0.27)  0.11 (0.03–0.29)  0.11 (0.03–0.31)  0.12 (0.03–0.34)  0.19 (0.02–0.56)
Glaciers              0.08 (0.06–0.10)  0.09 (0.07–0.11)  0.12 (0.10–0.15)  0.16 (0.13–0.18)  0.18 (0.15–0.21)  0.17 (0.11–0.21)
Land-water storage    0.03 (0.01–0.04)  0.03 (0.01–0.04)  0.03 (0.01–0.04)  0.03 (0.02–0.04)  0.03 (0.01–0.04)  0.03 (0.01–0.04)

--- TOTAL SEA LEVEL RISE BY YEAR (metres) ---

Year    SSP1-1.9          SSP1-2.6          SSP2-4.5          SSP3-7.0          SSP5-8.5          SSP5-8.5 (Low Conf.)
2030    0.09 (0.08–0.12)  0.09 (0.08–0.12)  0.09 (0.08–0.12)  0.10 (0.08–0.12)  0.10 (0.09–0.12)  0.10 (0.09–0.15)
2050    0.18 (0.15–0.23)  0.19 (0.16–0.25)  0.20 (0.17–0.26)  0.22 (0.18–0.27)  0.23 (0.20–0.29)  0.24 (0.20–0.40)
2090    0.35 (0.26–0.49)  0.39 (0.30–0.54)  0.48 (0.38–0.65)  0.56 (0.46–0.74)  0.63 (0.52–0.83)  0.71 (0.52–1.30)
2100    0.38 (0.28–0.55)  0.44 (0.32–0.62)  0.56 (0.44–0.76)  0.68 (0.55–0.90)  0.77 (0.63–1.01)  0.88 (0.63–1.60)
2150    0.57 (0.37–0.86)  0.68 (0.46–0.99)  0.92 (0.66–1.33)  1.19 (0.89–1.65)  1.32 (0.98–1.88)  1.98 (0.98–4.82)

--- AVERAGE RATES OF TOTAL SEA LEVEL CHANGE (mm yr⁻¹) ---

Period       SSP1-1.9        SSP1-2.6        SSP2-4.5        SSP3-7.0        SSP5-8.5        SSP5-8.5 (Low Conf.)
2040–2060    4.1 (2.8–6.0)   4.8 (3.5–6.8)   5.8 (4.4–8.0)   6.4 (5.0–8.7)   7.2 (5.6–9.7)   7.9 (5.6–16.1)
2080–2100    4.2 (2.4–6.6)   5.2 (3.2–8.0)   7.7 (5.2–11.6)  10.4 (7.4–14.8) 12.1 (8.6–17.6) 15.8 (8.6–30.1)

---

## Usage Notes

- Run this prompt in a fresh chat session — do not reuse sessions across batches
- After generation, verify that the data values in each scenario are consistent with the provided data context
- Check that the correct answer is the only defensible conclusion from the data — if a second option could be argued, cut or revise
- Target acceptance rate: ~50% (slightly lower than standard due to scenario construction complexity)
- When multiple models generate questions on the same data feature, keep the version with tighter distractors
