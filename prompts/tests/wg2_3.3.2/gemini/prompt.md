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
    "source": "IPCC AR6 WG2 Chapter 3 Section 3.3.2",
    "category": "Climate-Ecosystem Interactions",
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

Altered seawater carbonate chemistry (Section 3.2.3.1) affects specific processes to varying degrees. For example, higher CO2 concentrations can increase photosynthesis and growth in some phytoplankton, macroalgal and seagrass species (high confidence) (Pörtner et al., 2014; Seifert et al., 2020; Zimmerman, 2021), while lower pH levels decrease calcification (high confidence) (Pörtner et al., 2014; Falkenberg et al., 2018; Doney et al., 2020; Fox et al., 2020; Reddin et al., 2020) or silicification (low confidence) (Petrou et al., 2019). Organisms’ capacity to compensate for or resist acidification of internal fluids depends on their capacity for acid–base regulation, which differs due to organisms’ wide-ranging biological complexity and adaptive abilities (low to medium confidence) (Vargas et al., 2017; Melzner et al., 2020). Detrimental impacts of acidification include decreased growth and survival, and altered development, especially in early life stages (high confidence) (Dahlke et al., 2018; Onitsuka et al., 2018; Hancock et al., 2020), along with lowered recruitment and altered behaviour in animals (Kroeker et al., 2013a; Wittmann and Pörtner, 2013; Clements and Hunt, 2015; Cattano et al., 2018; Esbaugh, 2018; Bednaršek et al., 2019; Reddin et al., 2020). For finfish, laboratory studies of behavioural and sensory consequences of ocean acidification showed mixed results (Rossi et al., 2018; Nagelkerken et al., 2019; Stiasny et al., 2019; Velez et al., 2019; Clark et al., 2020; Munday et al., 2020). Calcifiers are generally more sensitive to acidification (e.g., for growth and survival) than non-calcifying groups (high confidence) (Kroeker et al., 2013a; Wittmann and Pörtner, 2013; Clements and Hunt, 2015; Cattano et al., 2018; Bednaršek et al., 2019; Reddin et al., 2020; Seifert et al., 2020). For calcifying primary producers, including phytoplankton and coralline algae, ocean acidification has different, often opposing effects, for example, decreasing calcification while photosynthetic rates increase (high confidence) (Riebesell et al., 2000; Van de Waal et al., 2013; Bach et al., 2015; Cornwall et al., 2017b; Gafar et al., 2019).

Oxygen concentrations affect aerobic and anaerobic processes, including energy metabolism and denitrification. Projected decreases in dissolved oxygen concentration (Section 3.2.3.2) will thus impact organisms and their biogeography in ways dependent upon their oxygen requirements (Deutsch et al., 2020), which are highest for large, multicellular organisms (Pörtner et al., 2014). The upper ocean generally contains high dissolved-oxygen concentrations due to air–sea exchange and photosynthesis, but in subsurface waters, deoxygenation may impair aerobic organisms in multiple ways (Oschlies et al., 2018; Galic et al., 2019; Thomas et al., 2019; Sampaio et al., 2021). Many processes contribute to lowered oxygen levels: altered ventilation and stratification; microbial respiration enhanced by nearshore eutrophication; and less oxygen solubility in warmer waters. For example, deoxygenation in highly eutrophic estuarine and coastal marine ecosystems (Section 3.4.2) can result from accelerated microbial activity, leading to acute organismal responses. Under hypoxia (oxygen concentrations ≤2 mg l –1; Limburg et al., 2020), physiological and ecological processes are impaired and communities undergo species migration, replacement and loss, transforming community composition (very high confidence) (Chu and Tunnicliffe, 2015; Gobler and Baumann, 2016; Sampaio et al., 2021). Hypoxia can lead to expanding OMZs, which will favour specialised microbes and hypoxia-tolerant organisms (medium confidence) (Breitburg et al., 2018; Ramírez-Flandes et al., 2019). As respiration consumes oxygen and produces CO2, lowered oxygen levels are often interlinked with acidification in coastal and tropical habitats (Rosa et al., 2013; Gobler and Baumann, 2016; Feely et al., 2018) and is an example of a compound hazard (Sections 3.2.4.1, 3.4.2.4).

---

## Usage Notes

- Run this prompt in a fresh chat session — do not reuse sessions across batches
- After generation, review each question: verify the correct answer against the source, check that distractors are unambiguous, and cut any question where you are uncertain about the answer
- Target acceptance rate: ~60% of generated candidates
- When multiple models generate questions on the same concept, keep the version with tighter or more plausible distractors and discard the duplicate
