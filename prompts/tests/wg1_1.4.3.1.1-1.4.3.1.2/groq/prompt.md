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
    "source": "IPCC AR6 WG1 Chapter 1 Section 1.4.3.1.1-1.4.3.1.2",
    "category": "Projections and Uncertainty",
    "difficulty": "easy | medium | hard",
    "generated_by": "Llama 3.3 70B (Groq)"
  }
]
```

## Example of a good vs. bad distractor

**Topic:** Climate sensitivity

Bad distractor (obviously wrong): "The Earth's temperature cannot change due to CO2 because CO2 is a natural gas."
Good distractor (plausibly wrong): "Climate sensitivity is defined as the equilibrium warming per doubling of CO2, typically estimated at 0.5–1.0°C." *(off by a factor — plausible to someone with partial knowledge)*

## Source Passage

Future radiative forcing is uncertain due to as-yet-unknown societal choices that will determine future anthropogenic emissions; this is considered ‘scenario uncertainty’. The RCP and SSP scenarios, which form the basis for climate projections assessed in this Report, are designed to span a plausible range of future pathways (Section 1.6) and can be used to estimate the magnitude of scenario uncertainty, but the real world may also differ from any one of these example pathways.

Uncertainties also exist regarding past emissions and radiative forcings. These are especially important for simulations of paleoclimate time periods, such as the Pliocene, Last Glacial Maximum or the last millennium, but are also relevant for the CMIP historical simulations of the instrumental period since 1850. In particular, historical radiative forcings due to anthropogenic and natural aerosols are less well constrained by observations than the GHG radiative forcings. There is also uncertainty in the size of large volcanic eruptions (and in the location for some that occurred before around 1850), and the amplitude of changes in solar activity, before satellite observations. The role of historical radiative forcing uncertainty was considered previously (Knutti et al., 2002; Forster et al., 2013) but, since AR5, specific simulations have been performed to examine this issue, particularly for the effects of uncertainty in anthropogenic aerosol radiative forcing (e.g., Jiménez-de-la-Cuesta and Mauritsen, 2019; Dittus et al., 2020).

Under any particular scenario (Section 1.6.1), there is uncertainty in how the climate will respond to the specified emissions or radiative forcing combinations. A range of climate models is often used to estimate the range of uncertainty in our understanding of the key physical processes and to define the ‘model response uncertainty’ (Sections 1.5.4 and 4.2.5). However, this range does not necessarily represent the full ‘climate response uncertainty’ in how the climate may respond to a particular radiative forcing or emissions scenario. This is because, for example, the climate models used in CMIP experiments have structural uncertainties not explored in a typical multi-model exercise (e.g., Murphy et al., 2004) and are not entirely independent of each other (Section 1.5.4.8; Masson and Knutti, 2011; Abramowitz et al., 2019); there are small spatial-scale features which cannot be resolved; and long time-scale processes or tipping points are not fully represented. Section 1.4.4 discusses how some of these issues can still be considered in a risk assessment context. For some metrics, such as equilibrium climate sensitivity (ECS), the CMIP6 model range is found to be broader than the very likely range assessed by combining multiple lines of evidence (Sections 4.3.4 and 7.5.6).

---

## Usage Notes

- Run this prompt in a fresh chat session — do not reuse sessions across batches
- After generation, review each question: verify the correct answer against the source, check that distractors are unambiguous, and cut any question where you are uncertain about the answer
- Target acceptance rate: ~60% of generated candidates
- When multiple models generate questions on the same concept, keep the version with tighter or more plausible distractors and discard the duplicate
