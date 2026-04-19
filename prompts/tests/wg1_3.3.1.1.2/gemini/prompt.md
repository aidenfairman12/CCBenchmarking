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
    "source": "IPCC AR6 WG1 Chapter 3 Section 3.3.1.1.2",
    "category": "Attribution Science",
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

Looking at periods preceding the instrumental record, AR5 assessed with high confidence that the 20th century annual mean surface temperature warming reversed a 5000-year cooling trend in Northern Hemisphere mid- to high latitudes caused by orbital forcing, and attributed the reversal to anthropogenic forcing with high confidence (see also (Section 2.3.1.1). Since AR5, the combined response to solar, volcanic and greenhouse gas forcing was detected in all Northern Hemisphere continents (PAGES 2k-PMIP3 group, 2015) over the period 864 to 1840. In contrast, the effect of those forcings was not detectable in the Southern Hemisphere (Neukom et al., 2018). Global and Northern Hemisphere temperature changes from reconstructions over this period have been attributed mostly to volcanic forcing (Schurer et al., 2014; McGregor et al., 2015; Otto-Bliesner et al., 2016; PAGES 2k Consortium, 2019; Büntgen et al., 2020), with a smaller role for changes in greenhouse gas forcing, and solar forcing playing a minor role (Schurer et al., 2014; PAGES 2k Consortium, 2019).

Focusing now on warming over the historical period, AR5 assessed that it was extremely likely that human influence was the dominant cause of the observed warming since the mid-20th century, and that it was virtually certain that warming over the same period could not be explained by internal variability alone. Since AR5 many new attribution studies of changes in global surface temperature have focused on methodological advances (see also (Section 3.2). Those advances include better accounting for observational and model uncertainties, and internal variability (Ribes and Terray, 2013; Hannart, 2016; Ribes et al., 2017; Schurer et al., 2018); formulating the attribution problem in a counterfactual framework (Hannart and Naveau, 2018); and reducing the dependence of the attribution on uncertainties in climate sensitivity and forcing (Otto et al., 2015; Haustein et al., 2017, 2019). Studies now account for uncertainties in the statistics of internal variability, either explicitly (Hannart, 2016; Hannart and Naveau, 2018; Ribes et al., 2021) or implicitly (Ribes and Terray, 2013; Schurer et al., 2018; Gillett et al., 2021), thus addressing concerns about over-confident attribution conclusions. Accounting for observational uncertainty increases the range of warming attributable to greenhouse gases by only 10 to 30% (Jones and Kennedy, 2017; Schurer et al., 2018). While some attribution studies estimate attributable changes in globally-complete GSAT (Schurer et al., 2018; Gillett et al., 2021; Ribes et al., 2021), others attribute changes in observational GMST, but this makes little difference to attribution conclusions (Schurer et al., 2018). Moreover, based on a synthesis of observational and modelling evidence, Cross-Chapter Box 2.3 assesses that the current best estimate of the scaling factor between GMST and GSAT is one, and therefore attribution studies of GMST and GSAT are here treated together in deriving assessed warming ranges. Studies also increasingly validate their multi-model approaches using imperfect model tests (Schurer et al., 2018; Gillett et al., 2021; Ribes et al., 2021). Alternative techniques, based purely on statistical or econometric approaches, without the need for climate modelling, have also been applied (Estrada et al., 2013; Stern and Kaufmann, 2014; Dergiades et al., 2016) and match the results of physically-based methods. The larger range of attribution techniques and improvements to those techniques increase confidence in the results compared to AR5.

---

## Usage Notes

- Run this prompt in a fresh chat session — do not reuse sessions across batches
- After generation, review each question: verify the correct answer against the source, check that distractors are unambiguous, and cut any question where you are uncertain about the answer
- Target acceptance rate: ~60% of generated candidates
- When multiple models generate questions on the same concept, keep the version with tighter or more plausible distractors and discard the duplicate
