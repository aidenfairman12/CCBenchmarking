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
    "source": "IPCC AR6 WG2 Chapter 5 Section 5.4.1.1",
    "category": "Impacts and Vulnerabilities",
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

AR5 Chapter 7 (Porter et al., 2014) stated with confidence that warmer temperatures have benefited agriculture in the high latitudes, and more evidence has been published to support this statement. Typical examples include pole-ward expansion of growing areas and reduction of cold stress in East Asia and North America (Table SM5.1).

Recent warming trends have generally shortened the life cycle of major crops (high confidence) (Zhang et al., 2014; Shen and Liu, 2015; Ahmed et al., 2018; Liu et al., 2018c; Tan et al., 2021). Some studies, however, observed prolonged crop growth duration despite the warming trends (Mueller et al., 2015; Tao et al., 2016; Butler et al., 2018; Zhu et al., 2018b) because of shifts in planting dates and/or adoption of longer-duration cultivars in mid-to-high latitudes. Conversely, in mid-to-low latitudes in Asia, a review study found that farmers favoured early maturing cultivars to reduce risks of damages due to drought, flood and/or heat (Shaffril et al., 2018), suggesting that region-specific adaptations are already occurring in different parts of the world (high confidence).

Global yields of major crops per unit land area have increased 2.5- to 3-fold since 1960. Plant breeding, fertilisation, irrigation and integrated pest management have been the major drivers, but many studies have found significant impacts from recent climate trends on crop yield (high confidence) (Figure 5.3; see Section 5.2.1 for the change attributable to anthropogenic climate change).

Climate impacts for the past 20–50 years differ by crops and regions. Positive effects have been identified for rice and wheat in Eastern Asia, and for wheat in Northern Europe. The effects are mostly negative in Sub-Saharan Africa, South America and Caribbean, Southern Asia, and Western and Southern Europe. Climate factors that affected long-term yield trends also differ between regions. For example, in Western Africa, 1°C warming above preindustrial climate has increased heat and rainfall extremes, and reduced yields by 10–20% for millet and 5–15% for sorghum (Sultan et al., 2019). In Australia, declined rainfall and increased temperatures reduced yield potential of wheat by 27%, accounting for the low yield growth between 1990 and 2015 (Hochman et al., 2017). In Southern Europe, climate warming has negatively impacted yields of almost all major crops, leading to recent yield stagnation (Moore and Lobell, 2015; Agnolucci and De Lipsis, 2020; Brás et al., 2021).

Ortiz-Bobea et al. (2021) analysed agricultural total factor productivity (TFP), defined as the ratio of all agricultural outputs to all agricultural inputs, and found that, while TFP has increased between 1961 and 2015, the climate change trends reduced global TFP growth by a cumulative 21% over a 55-year period relative to TFP growth under counterfactual non-climate change conditions. Greater effects (30–33%) were observed in Africa, Latin America and the Caribbean (Figure 5.3).

---

## Usage Notes

- Run this prompt in a fresh chat session — do not reuse sessions across batches
- After generation, review each question: verify the correct answer against the source, check that distractors are unambiguous, and cut any question where you are uncertain about the answer
- Target acceptance rate: ~60% of generated candidates
- When multiple models generate questions on the same concept, keep the version with tighter or more plausible distractors and discard the duplicate
