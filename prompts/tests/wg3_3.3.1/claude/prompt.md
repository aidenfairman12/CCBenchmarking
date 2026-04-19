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
    "source": "IPCC AR6 WG3 Chapter 3 Section 3.3.1",
    "category": "Policy and Governance",
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

Greenhouse gas (GHG) emissions mainly originate from the use and transformation of energy, agriculture, land use (change) and industrial activities. The future development of these sources is influenced by trends in socio-economic development, including population, economic activity, technology, politics, lifestyles, and climate policy. Trends for these factors are not independent, and scenarios provide a consistent outlook for these factors together (Section 3.2). Marangoni et al. (2017) show that in projections, assumptions influencing energy intensity (e.g., structural change, lifestyle and efficiency) and economic growth are the most important determinants of future CO2 emissions from energy combustion. Other critical factors include technology assumptions, preferences, resource assumptions and policy (van Vuuren et al. 2008). As many of the factors are represented differently in specific models, the model itself is also an important factor – providing a reason for the importance of model diversity (Sognnaes et al. 2021). For land use, Stehfest et al. (2019) show that assumptions on population growth are more dominant given that variations in per capita consumption of food are smaller than for energy. Here, we only provide a brief overview of some key drivers. We focus first on so-called reference scenarios (without stringent climate policy) and look at mitigation scenarios in detail later. We use the SSPs to discuss trends in more detail. The SSPs were published in 2017, and by now, some elements will have to be updated (O’Neill et al. 2020b). Still, the ranges represent the full literature relatively well.

Historically, population and GDP have been growing over time. Scenario studies agree that further global population growth is likely up to 2050, leading to a range of possible outcomes of around 8.5–11 billion people (Figure 3.9a). After 2050, projections show a much wider range. If fertility drops below replacement levels, a decline in the global population is possible (as illustrated by SSP1 and SSP5). This typically includes scenarios with rapid development and investment in education. However, median projections mostly show a stabilisation of the world population (e.g., SSP2), while high-end projections show a continued growth (e.g., SSP3). The UN Population Prospects include considerably higher values for both the medium projection and the high end of the range than the SSP scenarios (KC and Lutz 2017; UN 2019). The most recent median UN projection reaches almost 11 billion people in 2100. The key differences are in Africa and China: here, the population projections are strongly influenced by the rate of fertility change (faster drop in SSPs). Underlying these differences, the UN approach is more based on current demographic trends while the SSPs assume a broader range of factors (including education) driving future fertility.

---

## Usage Notes

- Run this prompt in a fresh chat session — do not reuse sessions across batches
- After generation, review each question: verify the correct answer against the source, check that distractors are unambiguous, and cut any question where you are uncertain about the answer
- Target acceptance rate: ~60% of generated candidates
- When multiple models generate questions on the same concept, keep the version with tighter or more plausible distractors and discard the duplicate
