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
    "source": "IPCC AR6 WG1 Chapter 7 Section 7.3.2",
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

High spectral resolution radiative transfer models provide the most accurate calculations of radiative perturbations due to greenhouse gases (GHGs), with errors in the instantaneous radiative forcing (IRF) of less than 1% (Mlynczak et al., 2016; Pincus et al., 2020). They can calculate IRFs with no adjustments, or SARFs by accounting for the adjustment of stratospheric temperatures using a fixed dynamical heating. It is not possible with offline radiation models to account for other adjustments. The high-resolution model calculations of SARF for carbon dioxide, methane and nitrous oxide have been updated since AR5, which were based on Myhre et al. (1998). The new calculations include the shortwave forcing from methane and updates to the water vapour continuum (increasing the total SARF of methane by 25%) and account for the absorption band overlaps between carbon dioxide and nitrous oxide (Etminan et al., 2016). The associated simplified expressions, from a re-fitting of the Etminan et al. (2016) results by Meinshausen et al. (2020), are given in Supplementary Material, Table 7.SM.1. The shortwave contribution to the IRF of methane has been confirmed independently (Collins et al., 2018). Since they incorporate known missing effects we assess the new calculations as being a more appropriate representation than Myhre et al. (1998).

As described in (Section 7.3.1, ERFs can be estimated using ESMs, however the radiation schemes in climate models are approximations to high spectral resolution radiative transfer models with variations and biases in results between the schemes (Pincus et al., 2015). Hence ESMs alone are not sufficient to establish ERF best estimates for the well-mixed GHGs (WMGHGs). This assessment therefore estimates ERFs from a combined approach that uses the SARF from radiative transfer models and adds the tropospheric adjustments derived from ESMs.

In AR5, the main information used to assess components of ERFs beyond SARF was from Vial et al. (2013) who found a near-zero non-stratospheric adjustment (without correcting for near-surface temperature changes over land) in 4×CO2 CMIP5 model experiments, with an uncertainty of ±10% of the total CO2 ERF. No calculations were available for other WMGHGs, so ERF was therefore assessed to be approximately equal to SARF (within 10%) for all WMGHGs.

The effect of WMGHGs in ESMs can extend beyond their direct radiative effects to include effects on ozone and aerosol chemistry and natural emissions of ozone and aerosol precursors, and in the case of CO2 to vegetation cover through physiological effects. In some cases these can have significant effects on the overall radiative budget changes from perturbing WMGHGs within ESMs (Myhre et al., 2013b; Zarakas et al., 2020; O’Connor et al., 2021; Thornhill et al., 2021a). These composition adjustments are further discussed in (Chapter 6 (Section 6.4.2).

---

## Usage Notes

- Run this prompt in a fresh chat session — do not reuse sessions across batches
- After generation, review each question: verify the correct answer against the source, check that distractors are unambiguous, and cut any question where you are uncertain about the answer
- Target acceptance rate: ~60% of generated candidates
- When multiple models generate questions on the same concept, keep the version with tighter or more plausible distractors and discard the duplicate
