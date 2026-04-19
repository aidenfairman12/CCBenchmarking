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
    "source": "IPCC AR6 WG1 Chapter 7 Section 7.4.2.3",
    "category": "Physical Climate Science Fundamentals",
    "difficulty": "easy | medium | hard",
    "generated_by": "Claude Sonnet"
  }
]
```

## Example of a good vs. bad distractor

**Topic:** Climate sensitivity

Bad distractor (obviously wrong): "The Earth's temperature cannot change due to CO2 because CO2 is a natural gas."
Good distractor (plausibly wrong): "Climate sensitivity is defined as the equilibrium warming per doubling of CO2, typically estimated at 0.5–1.0°C." *(off by a factor — plausible to someone with partial knowledge)*

## Source Passage

Surface albedo is determined primarily by reflectance at Earth’s surface, but also by the spectral and angular distribution of incident solar radiation. Changes in surface albedo result in changes in planetary albedo that are roughly reduced by two-thirds, owing to atmospheric absorption and scattering, with variability and uncertainty arising primarily from clouds (Bender, 2011; Donohoe and Battisti, 2011; Block and Mauritsen, 2013). Temperature change induces surface-albedo change through several direct and indirect means. In the present climate and at multi-decadal time scales, the largest contributions by far are changes in the extent of sea ice and seasonal snow cover, as these media are highly reflective and are located in regions that are close to the melting temperature (Sections 2.3.2.1 and 2.3.2.2). Reduced snow cover on sea ice may contribute as much to albedo feedback as reduced extent of sea ice (Zhang et al., 2019). Changes in the snow metamorphic rate, which generally reduces snow albedo with warmer temperature, and warming-induced consolidation of light-absorbing impurities near the surface, also contribute secondarily to the albedo feedback (Flanner and Zender, 2006; Qu and Hall, 2007; Doherty et al., 2013; Tuzet et al., 2017). Other contributors to albedo change include vegetation state (assessed separately in (Section 7.4.2.5), soil wetness and ocean roughness.

Several studies have attempted to derive surface-albedo feedback from observations of multi-decadal changes in climate, but only over limited spatial and inconsistent temporal domains, inhibiting a purely observational synthesis of global surface-albedo feedback ( α A). Flanner et al. (2011) applied satellite observations to determine that the northern hemisphere (NH) cryosphere contribution to global α Aover the period 1979–2008 was 0.48 [likely range 0.29 to 0.78] W m–2°C–1, with roughly equal contributions from changes in land snow cover and sea ice. Since AR5, and over similar periods of observation, Crook and Forster (2014) found an estimate of 0.8 ± 0.3 W m–2°C–1(one standard deviation) for the total NH extratropical surface-albedo feedback, when averaged over global surface area. For Arctic sea ice alone, Pistone et al. (2014) and Cao et al. (2015) estimated the contribution to global α Ato be 0.31 ± 0.04 W m–2°C–1(one standard deviation) and 0.31 ± 0.08 W m–2°C–1(one standard deviation), respectively, whereas Donohoe et al. (2020) estimated it to be only 0.16 ± 0.04 W m–2°C–1(one standard deviation). Much of this discrepancy can be traced to different techniques and data used for assessing the attenuation of surface-albedo change by Arctic clouds. For the NH land snow, Chen et al. (2016) estimated that observed changes during 1982–2013 contributed (after converting from NH temperature change to global mean temperature change) by 0.1 W m–2°C–1to global α A, smaller than the estimate of 0.24 W m–2°C–1from Flanner et al. (2011). The contribution of the Southern Hemisphere (SH) to global α A is expected to be small because seasonal snow cover extent in the SH is limited, and trends in SH sea ice extent are relatively flat over much of the satellite record (Section 2.3.2).

---

## Usage Notes

- Run this prompt in a fresh chat session — do not reuse sessions across batches
- After generation, review each question: verify the correct answer against the source, check that distractors are unambiguous, and cut any question where you are uncertain about the answer
- Target acceptance rate: ~60% of generated candidates
- When multiple models generate questions on the same concept, keep the version with tighter or more plausible distractors and discard the duplicate
