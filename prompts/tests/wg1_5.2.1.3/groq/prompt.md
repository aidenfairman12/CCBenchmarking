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
    "source": "IPCC AR6 WG1 Chapter 5 Section 5.2.1.3",
    "category": "Physical Climate Science Fundamentals",
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

Since AR5 and SROCC, major advances in globally coordinated ocean CO2 observations (Surface Ocean CO2 Atlas, SOCAT; and Global Ocean Data Analysis Project, GLODAP), the harmonization of ocean and coastal-observation-based products, atmospheric and oceanic inversion models and forced global ocean biogeochemical models (GOBMs) have increased the level of confidence in the assessment of trends and variability of air–sea fluxes and storage of CO2 in the ocean during the historical period (1960–2018; see also Supplementary Materials 5.SM.1; Ciais et al., 2013; Bakker et al., 2016; Landschützer et al., 2016, 2020; Bindoff et al., 2019; DeVries et al., 2019; Gregor et al., 2019; Gruber et al., 2019a, b; Tohjima et al., 2019; Friedlingstein et al., 2020; Hauck et al., 2020; Olsen et al., 2020). A major advance since SROCC is that, for the first time, all six published observational product fluxes used in this assessment, are made more comparable using a common ocean and sea ice cover area, integration of climatological coastal fluxes scaled to increasing atmospheric CO2 and an ensemble mean of ocean fluxes calculated from three re-analysis wind products (Supplementary Materials 5.SM.2; Landschützer et al., 2014, 2020; Rödenbeck et al., 2014; Zeng et al., 2014; Denvil-Sommer et al., 2019; Gregor et al., 2019; Iida et al., 2021). From a process point of view, the ocean uptake of anthropogenic carbon is a two-step set of abiotic processes that involves the exchange of CO2, first across the air–sea boundary into the surface mixed layer, followed by its transport into the ocean interior where it is stored for decades to millennia, depending on the depth of storage (Gruber et al., 2019b). Two definitions of air–sea fluxes of CO2 are used in this assessment for both observational products and models: Socean is the global mean ocean CO2 sink and Fnet denotes the net spatially varying CO2 fluxes (Hauck et al., 2020). Adjustment of the mean global Fnet for the pre-industrial sea-to-air CO2 flux associated with land-to-ocean carbon flux term makes Fnet comparable to Socean (Jacobson et al., 2007; Resplandy et al., 2018; Hauck et al., 2020).

There are multiple lines of observational and modelling evidence that support with high confidence the finding that, in the historical period (1960–2018), air–sea fluxes and storage of anthropogenic CO2 are largely influenced by atmospheric CO2 concentrations, physical ocean processes and physicochemical carbonate chemistry, which determines the unique properties of CO2 in seawater (Chapter 9 and Cross-Chapter Box 5.3; Wanninkhof, 2014; DeVries et al., 2017; McKinley et al., 2017, 2020, Gruber et al., 2019a, b; Hauck et al., 2020). Here we assess three different approaches (Figures 5.8a,b and 5.9) that together provide high confidence that, during the historical period (1960–2018), the ocean carbon sink (Socean) and its associated ocean carbon storage have grown in response to global anthropogenic CO2 emissions (Gruber et al., 2019a; Hauck et al., 2020; McKinley et al., 2020).

---

## Usage Notes

- Run this prompt in a fresh chat session — do not reuse sessions across batches
- After generation, review each question: verify the correct answer against the source, check that distractors are unambiguous, and cut any question where you are uncertain about the answer
- Target acceptance rate: ~60% of generated candidates
- When multiple models generate questions on the same concept, keep the version with tighter or more plausible distractors and discard the duplicate
