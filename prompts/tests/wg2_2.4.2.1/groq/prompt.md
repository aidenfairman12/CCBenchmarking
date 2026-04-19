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
    "source": "IPCC AR6 WG2 Chapter 2 Section 2.4.2.1",
    "category": "Impacts and Vulnerabilities",
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

Poleward and upward range shifts were already attributable to climate warming with high confidence in AR5. Publication of observed range shifts in accord with climate change have accelerated since AR5 and strengthened attribution. Ongoing latitudinal and elevational range shifts driven by regional climate trends are now well-established globally across many groups of organisms, and attributable to climate change with very high confidence due to very high consistency across a now very large body of species and studies and an in-depth understanding of mechanisms underlying physiological and ecological responses to climate drivers (Table 2.2; Table 2.3, Table SM2.1) (Pöyry et al., 2009; Chen et al., 2011; Grewe et al., 2013; Gibson-Reinemer and Rahel, 2015; MacLean and Beissinger, 2017; Pacifici et al., 2017; Anderegg et al., 2019). Range shifts stem from local population extinctions along warm-range boundaries (Anderegg et al., 2019) as well as from the colonisation of new regions at cold-range boundaries (Ralston et al., 2017).

Many studies since AR4 have tended not to be designed as attribution studies, particularly recent large-scale, multi-species meta-analyses. That is to say, all the data available was included in such studies (from both undisturbed and highly degraded lands and including very short-term data sets of <20 years), with little attempt to design the studies to differentiate the effects of climate change from those of other potential confounding variables. These studies tended to find greater lag and a lower proportion of species changing in the directions expected from climate change, with the authors concluding that LULCC, particularly habitat loss and fragmentation, was impeding wild species from effectively tracking climate change (Lenoir and Svenning, 2015; Rumpf et al., 2019; Lenoir et al., 2020).

Attribution is strong for species and species-interactions for which there is a robust mechanistic understanding of the role of climate on biological processes (high confidence). Unprecedented outbreaks of spruce beetles occurring from Alaska to Utah in the 1990s were attributed to warm weather that, in Alaska, facilitated a halving of the insect’s life cycle from two years to one (Logan et al., 2003). Milder winters and warmer growing seasons were likewise implicated in poleward expansions and increasing outbreaks of several forest pests (Weed et al., 2013), leading to the current prediction that 41% of major insect pest species will further increase their damage as climate warms, and only 4% will reduce their impacts, while the rest will show mixed responses (Lehmann et al., 2020).

---

## Usage Notes

- Run this prompt in a fresh chat session — do not reuse sessions across batches
- After generation, review each question: verify the correct answer against the source, check that distractors are unambiguous, and cut any question where you are uncertain about the answer
- Target acceptance rate: ~60% of generated candidates
- When multiple models generate questions on the same concept, keep the version with tighter or more plausible distractors and discard the duplicate
