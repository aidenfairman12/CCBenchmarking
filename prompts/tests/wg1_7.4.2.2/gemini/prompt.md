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
    "source": "IPCC AR6 WG1 Chapter 7 Section 7.4.2.2",
    "category": "Physical Climate Science Fundamentals",
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

Two decompositions are generally used to analyse the feedbacks associated with a change in the water-vapour and temperature lapse-rate in the troposphere. As in any system, many feedback decompositions are possible, each of them highlighting a particular property or aspect of the system (Ingram, 2010; Held and Shell, 2012; Dufresne and Saint-Lu, 2016). The first decomposition considers separately the changes (and therefore feedbacks) in the lapse rate (LR) and specific humidity (WV). The second decomposition considers changes in the lapse rate assuming constant relative humidity (LR*) separately from changes in relative humidity (RH).

The specific humidity (WV) feedback, also known as the water-vapour feedback, quantifies the change in radiative flux at the TOA due to changes in atmospheric water vapour concentration associated with a change in global mean surface air temperature. According to theory, observations and models, the water vapour increase approximately follows the Clausius–Clapeyron relationship at the global scale with regional differences dominated by dynamical processes (Section 8.2.1; Sherwood et al., 2010a; Chung et al., 2014; Romps, 2014; R. Liu et al., 2018; Schröder et al., 2019). Greater atmospheric water vapour content, particularly in the upper troposphere, results in enhanced absorption of LW and SW radiation and reduced outgoing radiation. This is a positive feedback. Atmospheric moistening has been detected in satellite records (Section 2.3.1.3.3), it is simulated by climate models (Section 3.3.2.2), and the estimates agree within model and observational uncertainty (Soden et al., 2005; Dessler, 2013; Gordon et al., 2013; Chung et al., 2014). The estimate of this feedback inferred from satellite observations is α WV= 1.85 ± 0.32 W m–2°C–1(R. Liu et al., 2018). This is consistent with the value α WV= 1.77 ± 0.20 W m–2°C–1(one standard deviation) obtained with CMIP5 and CMIP6 models (Zelinka et al., 2020).

The lapse-rate (LR) feedback quantifies the change in radiative flux at the TOA due to a non­uniform change in the vertical temperature profile. In the tropics, the vertical temperature profile is mainly driven by moist convection and is close to a moist adiabat. The warming is larger in the upper troposphere than in the lower troposphere (Manabe and Wetherald, 1975; Santer et al., 2005; Bony et al., 2006), leading to a larger radiative emission to space and therefore a negative feedback. This larger warming in the upper troposphere than at the surface has been observed over the last 20 years thanks to the availability of sufficiently accurate observations (Section 2.3.1.2.2). In the extratropics, the vertical temperature profile is mainly driven by a balance between radiation, meridional heat transport and ocean heat uptake (Rose et al., 2014). Strong winter temperature inversions lead to warming that is larger in the lower troposphere (Payne et al., 2015; Feldl et al., 2017a) and a positive LR feedback in polar regions (Section 7.4.4.1; Manabe and Wetherald, 1975; Bintanja et al., 2012; Pithan and Mauritsen, 2014). However, the tropical contribution dominates, leading to a negative global mean LR feedback (Soden and Held, 2006; Dessler, 2013; Vial et al., 2013; Caldwell et al., 2016). The LR feedback has been estimated at interannual time scales using meteorological reanalysis and satellite measurements of TOA fluxes (Dessler, 2013). These estimates from climate variability are consistent between observations and ESMs (Dessler, 2013; Colman and Hanson, 2017). The mean and standard deviation of this feedback under global warming based on the cited studies are α LR= –0.50 ± 0.20 W m–2°C–1(Dessler, 2013; Caldwell et al., 2016; Colman and Hanson, 2017; Zelinka et al., 2020).

---

## Usage Notes

- Run this prompt in a fresh chat session — do not reuse sessions across batches
- After generation, review each question: verify the correct answer against the source, check that distractors are unambiguous, and cut any question where you are uncertain about the answer
- Target acceptance rate: ~60% of generated candidates
- When multiple models generate questions on the same concept, keep the version with tighter or more plausible distractors and discard the duplicate
