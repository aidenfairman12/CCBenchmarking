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
    "source": "IPCC AR6 WG1 Chapter 4 Section 4.3.1.1",
    "category": "Projections and Uncertainty",
    "difficulty": "easy | medium | hard",
    "generated_by": "Gemini"
  }
]
```

## Example of a good vs. bad distractor

**Topic:** Climate sensitivity

Bad distractor (obviously wrong): "The Earth's temperature cannot change due to CO2 because CO2 is a natural gas."
Good distractor (plausibly wrong): "Climate sensitivity is defined as the equilibrium warming per doubling of CO2, typically estimated at 0.5–1.0°C." *(off by a factor — plausible to someone with partial knowledge)*

## Source Passage

The AR5 assessed from CMIP5 simulations and other lines of evidence that GSAT will continue to rise over the 21st century if greenhouse gas (GHG) concentrations continue increasing (Collins et al., 2013). The AR5 concluded that GSAT for 2081–2100, relative to 1986–2005 will likely be in the 5–95% range of 0.3°C–1.7°C under RCP2.6 and 2.6°C–4.8°C under RCP8.5. The corresponding ranges for the intermediate emissions scenarios with emissions peaking around 2040 (RCP4.5) and 2060 (RCP6.0) are 1.1°C–2.6°C and 1.4°C–3.1°C, respectively. The AR5 further assessed that GSAT averaged over the period 2081–2100 are projected to likely exceed 1.5°C above 1850–1900 for RCP4.5, RCP6.0 and RCP8.5 (high confidence) and are likely to exceed 2°C above 1850–1900 for RCP6.0 and RCP8.5 (high confidence). Global surface temperature changes above 2°C under RCP2.6 were deemed unlikely (medium confidence).

Here, for continuity’s sake, we assess the CMIP6 simulations of GSAT in a fashion similar to the AR5 assessment of the CMIP5 simulations. From these, we compute anomalies relative to 1995–2014 and display the evolution of ensemble means and 5–95% ranges (Figure 4.2). We also use the ensemble mean GSAT difference between 1850–1900 and 1995–2014, 0.82°C, to provide an estimate of the changes since 1850–1900 (Figure 4.2, right axis). Finally, we tabulate the ensemble mean changes between 1995–2014 and 2021–2040, 2041–2060, and 2081–2100 respectively (Figure 4.2).

The CMIP6 models show a 5–95% range of GSAT change for 2081–2100, relative to 1995–2014, of 0.6°C–2.0°C under SSP1-2.6 where CO2 concentrations peak between 2040 and 2060 (see Table 4.2). The corresponding range under the highest overall emissions scenario (SSP5-8.5) is 2.7°C–5.7°C. The ranges for the intermediate and high emissions scenarios (SSP2-4.5 and SSP3-7.0), where CO2 concentrations increase to 2100, but less rapidly than SSP5-8.5, are 1.4°C–3.0°C and 2.2°C–4.7°C, respectively. The range for the lowest emissions scenario (SSP1-1.9) is 0.2°C–1.3°C.

---

## Usage Notes

- Run this prompt in a fresh chat session — do not reuse sessions across batches
- After generation, review each question: verify the correct answer against the source, check that distractors are unambiguous, and cut any question where you are uncertain about the answer
- Target acceptance rate: ~60% of generated candidates
- When multiple models generate questions on the same concept, keep the version with tighter or more plausible distractors and discard the duplicate
