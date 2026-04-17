# Data Interpretation Question Generation Prompt
# Use for: Category 2 — Climate Data & Trend Interpretation only
# This prompt works differently — the LLM constructs a data scenario first, then writes a question around it

---

You are a rigorous question writer for a climate science benchmark. Your task is to generate data interpretation questions — questions that require reasoning over a described dataset, time series, or anomaly table rather than recalling facts.

## How these questions work

Each question contains an embedded data scenario (a small table, a described trend, or a set of values). The reader must interpret or reason about that data to answer correctly. These questions test quantitative and analytical reasoning, not memory.

## Requirements

- Generate exactly {N} questions (recommend 5 per batch)
- Each question must embed a self-contained data scenario — no external chart or image needed
- Scenarios must use realistic, plausible climate values (anchor to ERA5, NOAA GHCN, or IPCC observed ranges — do not invent implausible numbers)
- 4 answer options (A, B, C, D), exactly one is correct
- No "all of the above", "none of the above", or "both A and B" options
- Distractors should represent plausible misreadings of the data (e.g. confusing absolute value with anomaly, misreading a trend direction, off-by-one decade errors)
- The correct answer must follow directly and unambiguously from the data provided
- Do not require knowledge beyond what is presented in the scenario

## Scenario types to use (vary across your batch)

1. **Trend identification** — a time series table of a climate variable; ask about direction, rate, or magnitude of change
2. **Anomaly interpretation** — a set of temperature or precipitation anomalies relative to a baseline; ask what they indicate
3. **Comparison** — two regions or two time periods side by side; ask which is warmer/wetter/more variable
4. **Index reading** — a described climate index value (e.g. ENSO, NAO); ask what climate conditions it implies
5. **Projection reading** — a small table of model projections under two scenarios; ask about the spread or direction

## Output Format

Return a strict JSON array and nothing else — no preamble, no commentary.

```json
[
  {
    "scenario": "A brief prose or table description of the data, embedded directly in the question or as a preamble to it.",
    "question": "...",
    "options": {
      "A": "...",
      "B": "...",
      "C": "...",
      "D": "..."
    },
    "correct_answer": "B",
    "explanation": "One sentence explaining which feature of the data supports the correct answer.",
    "data_source": "ERA5 / NOAA GHCN / IPCC AR6 WG1 Chapter X — indicate what real-world values the scenario is based on",
    "scenario_type": "trend_identification | anomaly_interpretation | comparison | index_reading | projection_reading",
    "category": "Climate Data & Trend Interpretation",
    "difficulty": "easy | medium | hard",
    "generated_by": "{MODEL_NAME}"
  }
]
```

## Example

```json
{
  "scenario": "The following table shows global mean surface temperature anomalies (°C) relative to the 1850–1900 baseline, averaged per decade:\n\n1950s: +0.10\n1970s: +0.17\n1990s: +0.40\n2010s: +0.87\n2015–2022: +1.09",
  "question": "Based on the data above, which of the following best describes the rate of warming across these decades?",
  "options": {
    "A": "Warming has been roughly constant at about 0.15°C per decade since the 1950s.",
    "B": "Warming has accelerated, with each successive period showing a larger anomaly than the last.",
    "C": "Warming peaked in the 2010s and has begun to level off in recent years.",
    "D": "The data shows a cooling trend in the 1950s followed by rapid warming after 1990."
  },
  "correct_answer": "B",
  "explanation": "Each successive decade in the table shows a larger anomaly than the previous one, indicating accelerating warming rather than a constant rate.",
  "data_source": "IPCC AR6 WG1 Chapter 2, observed GMST anomalies",
  "scenario_type": "trend_identification",
  "category": "Climate Data & Trend Interpretation",
  "difficulty": "easy",
  "generated_by": "Claude Sonnet"
}
```

## Usage Notes

- Run this prompt using each generation model separately; fill in {N} and {MODEL_NAME} before each run
- After generation, verify that the data values in each scenario are physically plausible against the cited real-world source
- Check that the correct answer is the only defensible conclusion from the data — if a second option could be argued, cut or revise the question
- Target acceptance rate: ~50% (slightly lower than standard questions due to scenario construction complexity)
