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
    "source": "IPCC AR6 WG1 Chapter 9 Section 9.6.3.1",
    "category": "Projections and Uncertainty",
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

There is high agreement across published GMSL projections for 2050, and there is little sensitivity to emissions scenario (Figure 9.25, left panel). Up to 2050, projections are broadly consistent with extrapolation of the observed acceleration of GMSL rise (Sections 2.3.3.3, 9.6.1.1 and 9.6.1.2). Considering only projections incorporating ice-sheet processes in whose quantification there is at least medium confidence, the GMSL projections for 2050, across all emissions scenarios, fall between 0.1 and 0.4 m (5th–95th percentile range). Projections incorporating MICI or SEJ do not extend this range under RCP2.6 or RCP4.5 but do extend the upper part of the range to 0.6 m under RCP8.5. On the basis of these studies, we therefore have high confidence that GMSL in 2050 will be between 0.1 and 0.4 m higher than in 1995–2014 under low- and moderate-emissions scenarios, and between 0.1 and 0.6 m under high-emissions scenarios.

Conversely, there is low agreement across published GMSL projections for 2100, particularly for higher-emissions scenarios, as well as a higher degree of sensitivity to the choice of emissions scenario (Figure 9.25, right panel). Considering only projections representing processes in whose quantification there is at least medium confidence, the GMSL projections for 2100 fall between 0.2 and 1.0 m (5th–95th percentile range) under RCP2.6 and RCP4.5, and between 0.3 and 1.6 m under RCP8.5. Considering also projections incorporating MICI or SEJ (low confidence), the projections for 2100 fall between 0.2 and 1.0 m (5th–95th percentile range) under RCP2.6, 0.2, and 1.6 m under RCP4.5, and 0.4 and 2.4 m under RCP8.5. In summary, RCP-based projections published since AR5 show high agreement for 2050, but exhibit broad ranges and low agreement for 2100, particularly under RCP8.5.

---

## Usage Notes

- Run this prompt in a fresh chat session — do not reuse sessions across batches
- After generation, review each question: verify the correct answer against the source, check that distractors are unambiguous, and cut any question where you are uncertain about the answer
- Target acceptance rate: ~60% of generated candidates
- When multiple models generate questions on the same concept, keep the version with tighter or more plausible distractors and discard the duplicate
