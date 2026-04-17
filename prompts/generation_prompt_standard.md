# Standard Question Generation Prompt
# Use for: Categories 1, 3, 4, 5, 6, 7
# Paste this into your LLM chat interface along with a source passage

---

You are a rigorous question writer for a climate science benchmark designed to evaluate how well LLMs reason about climate science. Your task is to generate multiple choice questions from the provided source passage.

## Requirements

- Generate exactly {N} questions (recommend 5 per batch)
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
    "source": "IPCC AR6 WG1 Chapter X, Section X.X.X.X",
    "category": "{CATEGORY_NAME}",
    "difficulty": "easy | medium | hard",
    "generated_by": "{MODEL_NAME}"
  }
]
```

## Example of a good vs. bad distractor

**Topic:** Climate sensitivity

Bad distractor (obviously wrong): "The Earth's temperature cannot change due to CO2 because CO2 is a natural gas."  
Good distractor (plausibly wrong): "Climate sensitivity is defined as the equilibrium warming per doubling of CO2, typically estimated at 0.5–1.0°C." *(off by a factor — plausible to someone with partial knowledge)*

## Source Passage

{PASTE SOURCE TEXT HERE — recommend 300–600 words from the relevant chapter section}

---

## Usage Notes

- Run this prompt against the same passage using each generation model (e.g. Claude Sonnet, GPT-4o) separately
- Fill in {N}, {CATEGORY_NAME}, and {MODEL_NAME} before each run
- After generation, review each question: verify the correct answer against the source, check that distractors are unambiguous, and cut any question where you are uncertain about the answer
- Target acceptance rate: ~60% of generated candidates
- When multiple models generate questions on the same concept, keep the version with tighter or more plausible distractors and discard the duplicate