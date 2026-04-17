# Standard Question Generation Prompt
# Use for: Categories 1, 3, 4, 5, 6, 7
# Paste this into your LLM chat interface along with a source passage

---

You are a rigorous question writer for a climate science benchmark designed to evaluate how well LLMs reason about climate science. Your task is to generate multiple choice questions from the provided source passage.

## Requirements

- Generate exactly 5 questions 
- Every question must be answerable solely from the provided source text — do not draw on outside knowledge
- 4 answer options (A, B, C, D), exactly one is correct
- No "all of the above", "none of the above", or "both A and B" style options
- Distractors must be plausibly wrong — represent common misconceptions or close-but-incorrect alternatives, not obviously absurd choices
- Questions must be self-contained — a reader needs no external context beyond the question itself
- Do not write questions with contested, opinion-based, or ambiguous correct answers
- Vary difficulty within each batch: aim for roughly 2 easy, 2 medium, 1 hard per 5 questions. If you find yourself writing a third easy question, convert it to medium difficulty instead
- Ensure each question tests a distinct concept — do not generate two questions that cover the same underlying fact or mechanism

**Easy:** Tests direct recall of a clearly stated fact from the passage  
**Medium:** Requires connecting two pieces of information or interpreting a concept  
**Hard:** Requires multi-step reasoning, distinguishing between closely related concepts, or applying a principle to a novel framing

## Output Format

Return a strict JSON array and nothing else — no preamble, no commentary.

```json
[
  {
    "question": "...",
    "options": {
      "A": "...",
      "B": "...",
      "C": "...",
      "D": "..."
    },
    "correct_answer": "A",
    "explanation": "One sentence citing the specific part of the source that confirms the correct answer.",
    "source": "IPCC AR6 WG1 Chapter 6, Section 9.6.1.3",
    "category": "Projections & Uncertainty",
    "difficulty": "easy | medium | hard",
    "generated_by": "Claude Sonnet 4.6"
  }
]
```

## Example of a good vs. bad distractor

**Topic:** Climate sensitivity

Bad distractor (obviously wrong): "The Earth's temperature cannot change due to CO2 because CO2 is a natural gas."  
Good distractor (plausibly wrong): "Climate sensitivity is defined as the equilibrium warming per doubling of CO2, typically estimated at 0.5–1.0°C." *(off by a factor — plausible to someone with partial knowledge)*

## Source Passage

Regional sea level changes are resolved by both tide gauge and satellite altimetry observations (Hamlington et al., 2020a). Altimeters have the advantage of quasi-global coverage but are limited to a period (1993–present) in which the forced trend response is just emerging on regional scales (Section 9.6.1.4). An analysis of the local altimetry error budget to estimate 90% confidence intervals on regional sea level trends and accelerations reports that 98% of the ocean surface has experienced significant sea level rise over the satellite era (Prandi et al., 2021). The same study finds that sea level accelerations display a less uniform pattern, with an east–west dipole in the Pacific, a north–south dipole in the Southern Ocean and in the North Atlantic, and 85% of the ocean surface experiencing significant sea level acceleration or deceleration, above instrumental and post-processing noise. Longer records are available from tide gauges, albeit with variable coverage by basin. Regional departures from GMSL rise are primarily driven by ocean transport divergences that result from wind stress anomalies and spatial variability in atmospheric heat and freshwater fluxes (Section 9.2.4).

The SROCC (Oppenheimer et al., 2019) noted the occurrence of large multiannual sea level variations in the Pacific, associated with the Pacific Decadal Oscillation (PDO) in particular, and involving the El Niño Southern Oscillation (ENSO), North Pacific Gyre Oscillation (NPGO) and Indian Ocean Dipole (IOD; Annex IV; Royston et al., 2018; Hamlington et al., 2020b). There was intensified sea level rise during the 1990s and 2000s, with 10-year trends exceeding 20 mm yr–1in the western tropical Pacific Ocean, while sea level trends were negative on the North American west coast. During the 2010s, the situation reversed, with western Pacific sea level falling at more than 10 mm yr–1(Hamlington et al., 2020b). For the Atlantic Ocean, SROCC described regional sea level variability as being driven primarily by wind and heat flux variations associated with the North Atlantic Oscillation (NAO) and heat transport changes associated with Atlantic Meridional Overturning Circulation (AMOC) variability . During periods of subpolar North Atlantic warming, winds along the European coast are predominantly from the south and may communicate steric anomalies onto the continental shelf, driving regional sea level rise, with the reverse during periods of cooling (Chafik et al., 2019). High rates of sea level rise in the North Indian Ocean are accompanied by a weakening summer South Asian monsoon circulation (Swapna et al., 2017).

---

## Usage Notes

- Run this prompt against the same passage using each generation model (e.g. Claude Sonnet, GPT-4o) separately
- Fill in {N}, {CATEGORY_NAME}, and {MODEL_NAME} before each run
- After generation, review each question: verify the correct answer against the source, check that distractors are unambiguous, and cut any question where you are uncertain about the answer
- Target acceptance rate: ~60% of generated candidates
- When multiple models generate questions on the same concept, keep the version with tighter or more plausible distractors and discard the duplicate