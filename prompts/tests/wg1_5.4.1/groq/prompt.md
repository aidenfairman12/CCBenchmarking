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
    "source": "IPCC AR6 WG1 Chapter 5 Section 5.4.1",
    "category": "Climate-Ecosystem Interactions",
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

The AR5 (WGI, Box 6.3) and SRCCL (IPCC, 2019a) concluded with high confidence that rising atmospheric CO2 increases leaf-level photosynthesis. This effect is represented in all ESMs. New studies since AR5 add evidence that the leaf-level CO2 fertilization is modulated by acclimation of photosynthesis to long-term CO2 exposure, growth temperature, seasonal drought, and nutrient availability, but these effects are not yet routinely represented in ESMs (Smith and Dukes, 2013; Baig et al., 2015; Kelly et al., 2016; Drake et al., 2017; Jiang et al., 2020a). Cross-Chapter Box 5.1 assesses multiple lines of evidence, which suggest that the ratio of plant CO2 uptake to water loss – plant water-use efficiency (WUE) – increases in near proportionality to atmospheric CO2. Despite advances in the regional coverage of field experiments, observations of the consequences of CO2 fertilization at ecosystem level are still scarce, in particular from outside the temperate zone (Song et al., 2019). New syntheses since AR5 corroborate that the effect of elevated CO2 on plant growth and ecosystem carbon storage is generally positive (high confidence), but is modulated by temperature, water and nutrient availability (Reich et al., 2014; Obermeier et al., 2017; Peñuelas et al., 2017; Hovenden et al., 2019; Song et al., 2019). Plant carbon allocation, changes in plant community composition, disturbance, and natural plant mortality are important processes affecting the magnitude of the response, but are currently poorly represented in models (De Kauwe et al., 2014; Friend et al., 2014; Reich et al., 2018; A.P. Walker et al., 2019; K. Yu et al., 2019), and thus contribute strongly to uncertainty in ESM projections (Arora et al., 2020).

Field studies with elevated CO2 have demonstrated that the initial stimulation of above-ground growth may decline if insufficient nutrients such as nitrogen or phosphorus are available (Finzi et al., 2007; Norby et al., 2010; Hungate et al., 2013; Reich and Hobbie, 2013; Talhelm et al., 2014; Terrer et al., 2018). Model-data syntheses have demonstrated that capturing the observed long-term effect of elevated CO2 depends on the ability of models to predict the effect of vegetation on soil biogeochemistry (Zaehle et al., 2014; Koven et al., 2015b; Medlyn et al., 2015; Walker et al., 2015). Meta-analyses of CO2 manipulation experiments point to increased soil microbial activity and accelerated turnover of soil organic matter (van Groenigen et al., 2017) as a result of increased below-ground carbon allocation by plants (Song et al., 2019), and increased root exudation or mycorrhizal activity due to enhanced plant nutrient requirements under elevated CO2 (Drake et al., 2011; Terrer et al., 2016; Meier et al., 2017). These effects are not considered in most ESMs. One global model that attempts to represent these processes suggests that elevated CO2 -related carbon accumulation is reduced in soils but increased in vegetation relative to more conventional models (Sulman et al., 2019).

---

## Usage Notes

- Run this prompt in a fresh chat session — do not reuse sessions across batches
- After generation, review each question: verify the correct answer against the source, check that distractors are unambiguous, and cut any question where you are uncertain about the answer
- Target acceptance rate: ~60% of generated candidates
- When multiple models generate questions on the same concept, keep the version with tighter or more plausible distractors and discard the duplicate
