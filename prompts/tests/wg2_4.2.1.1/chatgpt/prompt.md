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
    "source": "IPCC AR6 WG2 Chapter 4 Section 4.2.1.1",
    "category": "Impacts and Vulnerabilities",
    "difficulty": "easy | medium | hard",
    "generated_by": "ChatGPT"
  }
]
```

## Example of a good vs. bad distractor

**Topic:** Climate sensitivity

Bad distractor (obviously wrong): "The Earth's temperature cannot change due to CO2 because CO2 is a natural gas."
Good distractor (plausibly wrong): "Climate sensitivity is defined as the equilibrium warming per doubling of CO2, typically estimated at 0.5–1.0°C." *(off by a factor — plausible to someone with partial knowledge)*

## Source Passage

Large numbers of people live in regions where the annual mean precipitation is now ‘unfamiliar’ compared to the mean and variability between 1891 and 2016 (Figure 4.3c). “Unfamiliar” is defined as the long-term change being greater than one standard deviation in the annual data (Figure 4.3b). In 2020, approximately 498 million people lived in unfamiliarly wet areas, where the long-term average precipitation is as high as previously seen in only about one in 6 years (medium confidence) (Figure 4.3c). These areas are primarily in mid and high latitudes (Hawkins et al., 2020). On the other hand, approximately 163 million people lived in unfamiliarly dry areas, mostly in low latitudes (medium confidence). Due to high variability over time, the signal of long-term change in annual mean precipitation is not distinguishable from the noise of variability in many areas (Hawkins et al., 2020), implying that the local annual precipitation cannot yet be defined ‘unfamiliar’ by the above definition.

Notably, many regions have seen increased precipitation for part of the year and decreased precipitation at other times (high confidence) (Figure 4.3d,e), leading to small changes in the annual mean precipitation. Therefore, the numbers of people seeing unfamiliar seasonal precipitation levels are expected to be higher than those quoted above for unfamiliar annual precipitation changes (medium confidence). Still, quantified analysis of this is not yet available.

The intensity of heavy precipitation has increased in many regions (high confidence), including much of North America, most of Europe, most of the Indian sub-continent, parts of northern and southeastern Asia, much of southern South America, parts of southern Africa and parts of central, northern and western Australia (Figure 4.3 f) (Dunn et al., 2020; Sun et al., 2020). Conversely, heavy precipitation has decreased in some regions, including eastern Australia, northeastern South America and western Africa. The length of dry spells has also changed, with increases in annual mean consecutive dry days (CDD) in large areas of western, eastern and southern Africa, eastern and southwestern South America, and Southeast Asia, and decreases across much of North America (Figure 4.3g). Precipitation extremes have changed in some places where annual precipitation shows no trend. Some regions such as southern Africa and parts of southern South America are seeing increased heavy precipitation and longer dry spells. Many regions with changing extremes are highly populated, such as the Indian sub-continent, Southeast Asia, Europe and parts of North America, South America and southern Africa (Figure 4.3h,i). Substantially more people (~709 million) live in regions where annual maximum one-day precipitation has increased than in regions where it has decreased (~86 million) (medium confidence). However, more people are experiencing longer dry spells than shorter dry spells: approximately 711 million people live in places where annual mean CDD is longer than in the 1950s, and ~404 million in places with shorter CDD (medium confidence) (Figure 4.3i).

---

## Usage Notes

- Run this prompt in a fresh chat session — do not reuse sessions across batches
- After generation, review each question: verify the correct answer against the source, check that distractors are unambiguous, and cut any question where you are uncertain about the answer
- Target acceptance rate: ~60% of generated candidates
- When multiple models generate questions on the same concept, keep the version with tighter or more plausible distractors and discard the duplicate
