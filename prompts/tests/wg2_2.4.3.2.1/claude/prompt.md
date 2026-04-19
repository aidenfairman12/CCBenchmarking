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
    "source": "IPCC AR6 WG2 Chapter 2 Section 2.4.3.2.1",
    "category": "Climate-Ecosystem Interactions",
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

AR5 and a meta-analysis found that vegetation at the biome level shifted poleward latitudinally and upward altitudinally due to anthropogenic climate change in at least 19 sites in boreal, temperate and tropical ecosystems from 1700 to 2007 (Gonzalez et al., 2010; Settele et al., 2014). In these areas, temperature increased to 0.4°C–1.6°C above the pre-industrial period (Gonzalez et al., 2010; Settele et al., 2014). Field research since the AR5 detected additional poleward and upslope biome shifts over periods of 24–210 years at numerous sites (described below), but were not directly attributed to anthropogenic climate change as the studies were not designed or conducted properly for full attribution assessment.

Many of the recently detected shifts are nevertheless consistent with climate change-induced temperature increases and observed in areas without agriculture, livestock grazing, timber harvesting and other anthropogenic land uses. For example, in the Andes Mountains in Ecuador, a biome shift was detected by comparing a survey by Alexander von Humboldt in 1802 to a re-survey in 2012, making this the longest time span in the world for this type of data (Morueta-Holme et al., 2015; Moret et al., 2019). Over 210 years, temperature increased by 1.7°C (Morueta-Holme et al., 2015) and the upper edge of alpine grassland shifted 100–450 m upslope (Moret et al., 2019).

Other biome shifts consistent with climate change and not substantially affected by local land use include: northward shifts in Canada of deciduous forest into boreal conifer forest, 5 km from 1970–2012 (Sittaro et al., 2017) and 20 km from 1970–2014 (Boisvert-Marsh et al., 2019) and of temperate conifer into boreal conifer forest, 21 km from 1970–2015 (Boisvert-Marsh and de Blois, 2021). Research detected upslope shifts of boreal and sub-alpine conifer forest into alpine grassland at 143 sites on four continents (41 m from 1901–2018) (Lu et al., 2021) and at individual sites in Canada (54 m from 1900–2010) (Davis et al., 2020); China (300 m from 1910–2000) (Liang et al., 2016) (33 m from 1985–2014) (Du et al., 2018); Nepal (50 m from 1860–2000) (Sigdel et al., 2018); Russia (150 m from 1954–2006) (Gatti et al., 2019); and the USA (19 m from 1950–2016) (Smithers et al., 2018) (38 m from 1953–2015) (Terskaia et al., 2020). Other upslope cases include shifts of temperate conifer forest in Canada (Jackson et al., 2016) and the USA (Lubetkin et al., 2017), temperate deciduous forest in Switzerland (Rigling et al., 2013) and temperate shrubland in the USA (Donato et al., 2016).

In summary, anthropogenic climate change caused latitudinal and elevational biome shifts in at least 19 sites in boreal, temperate and tropical ecosystems between 1700 and 2007, where temperature increased to 0.4°C–1.6°C above the pre-industrial period (robust evidence, high agreement ). Additional cases of 5–20 km northward and 20–300 m upslope biome shifts between 1860 and 2016, under a mean global temperature increase of approximately 0.9°C above the pre-industrial period, are consistent with climate change (medium evidence, high agreement ).

---

## Usage Notes

- Run this prompt in a fresh chat session — do not reuse sessions across batches
- After generation, review each question: verify the correct answer against the source, check that distractors are unambiguous, and cut any question where you are uncertain about the answer
- Target acceptance rate: ~60% of generated candidates
- When multiple models generate questions on the same concept, keep the version with tighter or more plausible distractors and discard the duplicate
