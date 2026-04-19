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
    "source": "IPCC AR6 WG2 Chapter 7 Section 7.2.2.1",
    "category": "Impacts and Vulnerabilities",
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

Changing climatic patterns are facilitating the spread of CHIKV, Zika, Japanese encephalitis and Rift Valley Fever in Asia, Latin America, North America and Europe (high confidence). Climate change may have facilitated the emergence of CHIKV as a significant public health challenge in some Latin American and Caribbean countries (Yactayo et al., 2016; Pineda et al., 2016) and contributed to chikungunya outbreaks in Europe (Rocklöv et al., 2019; Mascarenhas et al., 2018; Morens and Fauci, 2014). The Zika virus outbreak in South America in 2016 was preceded by 2007 outbreaks on Pacific islands and followed a period of record high temperatures and severe drought conditions in 2015 (Paz and Semenza, 2016; Tesla et al., 2018). Increased use of household water storage containers during the drought is correlated with a range expansion of Aedes aegypti during this period, increasing household exposure to the vector (Paz and Semenza, 2016). Changing climate also appears to be a risk factor for the spread of Japanese encephalitis to higher altitudes in Nepal (Ghimire and Dhakal, 2015) and in southwest China (Zhao et al., 2014). In eastern Africa, climate change may be a risk factor in the spread of Rift Valley Fever (Taylor et al., 2016a).

Changes in temperature, precipitation, and relative humidity have been implicated as drivers of West Nile fever in southeastern Europe (medium confidence). The average temperature and precipitation prior to the exceptional 2018 West Nile outbreak in Europe was above the 1981–2010 period average, which may have contributed to an early upsurge of the vector population (Marini et al., 2020; Haussig et al., 2018; Semenza and Paz, 2021). In 2019 and 2020, West Nile fever was first detected in birds and subsequently in humans in Germany and the Netherlands (Ziegler et al., 2020; Vlaskamp et al., 2020).

Climate change has contributed to the spread of the Lyme disease vectorIxodes scapularis , a corresponding increase in cases of Lyme disease in North America (high confidence) and the spread of the Lyme disease and tick-borne encephalitis vectorIxodes ricinus in Europe (medium confidence). In Canada, there has been a geographic range expansion of the black-legged tick I. scapularis, the main vector of Borrelia burgdorferi, the agent of Lyme disease. Vector surveillance of I. scapularis has identified strong correlation between temperatures and the emergence of tick populations, their range and recent geographic spread, with recent climate warming coinciding with a rapid increase in human Lyme disease cases (Clow et al., 2017; Cheng et al., 2017; Gasmi et al., 2017; Ebi et al., 2017). Ixodes ricinus, the primary vector in Europe for both Lyme borreliosis and tick-borne encephalitis is sensitive to humidity and temperature (Daniel et al., 2018; Estrada-Peña and Fernández-Ruiz, 2020) (high confidence). There has been an observed range expansion to higher latitudes in Sweden and to higher elevations in Austria and the Czech Republic.

---

## Usage Notes

- Run this prompt in a fresh chat session — do not reuse sessions across batches
- After generation, review each question: verify the correct answer against the source, check that distractors are unambiguous, and cut any question where you are uncertain about the answer
- Target acceptance rate: ~60% of generated candidates
- When multiple models generate questions on the same concept, keep the version with tighter or more plausible distractors and discard the duplicate
