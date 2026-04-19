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
    "source": "IPCC AR6 WG3 Chapter 14 Section 14.3.2.1",
    "category": "Policy and Governance",
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

As the risks of adverse climate impacts, even with a ‘well below’ 2°C increase, are substantial, the purpose of the Paris Agreement extends to increasing adaptive capacity and fostering climate resilience (UNFCCC 2015a, Art. 2(1)(b)), as well as redirecting investment and finance flows (UNFCCC 2015a, Art. (2)(1)(c); Thorgeirsson 2017). The finance and adaptation goals are not quantified in the Paris Agreement itself but the temperature goal and the pathways they generate may, some argue, enable a quantitative assessment of the resources necessary to reach these goals, and the nature of the impacts requiring adaptation (Rajamani and Werksman 2018). The decision accompanying the Paris Agreement resolves to set a new collective quantified finance goal prior to 2025 (not explicitly limited to developed countries), with USD100 billion yr –1 as a floor (UNFCCC 2016a, para. 53; Bodansky et al. 2017b). Article 2 also references sustainable development and poverty eradication, and thus implicitly underscores the need to integrate the SDGs in the implementation of the Paris Agreement (Sindico 2016).

The Paris Agreement’s purpose is accompanied by an expectation that the Agreement ‘will be’ implemented to ‘reflect equity and the principle of common but differentiated responsibilities and respective capabilities (CBDRRC), in the light of different national circumstances’ (UNFCCC 2015a, Art. 2.2). This provision generates an expectation that Parties will implement the agreement to reflect CBDRRC, and is not an obligation to do so (Rajamani 2016a). Further, the inclusion of the term ‘in light of different national circumstances’ introduces a dynamic element into the interpretation of the CBDRRC principle. As national circumstances evolve, the application of the principle will also evolve (Rajamani 2016a). This change in the articulation of the CBDRRC principle is reflected in the shifts in the nature and extent of differentiation in the climate change regime (Maljean-Dubois 2016; Rajamani 2016a; Voigt and Ferreira 2016a), including through a shift towards ‘procedurally-oriented differentiation’ for developing countries (Huggins and Karim 2016).

Although NDCs are developed by individual state Parties, the Paris Agreement requires that these are undertaken by Parties ‘with a view’ to achieving the Agreement’s purpose and collectively ‘represent a progression over time’ (UNFCCC 2015a, Art. 3). The Paris Agreement also encourages Parties to align the ambition of their NDCs with the temperature goal through the Agreement’s ‘ambition cycle’, thus imparting operational relevance to the temperature goal (Rajamani and Werksman 2018).

Article 4.1 contains a further non-binding requirement that Parties ‘aim’ to reach global peaking of GHG ‘as soon as possible’ and to undertake rapid reductions thereafter to achieve net zero GHG emissions ‘in the second half of the century’. Some argue this implies a need to reach net zero GHG emissions in the third quarter of the 21st century (Rogelj et al. 2015; IPCC 2018b) (Chapter 2, Table 2.4 and Cross-Chapter Box 3 in Chapter 3). To reach net zero CO2 around 2050, in the short-term global net human-caused CO2 emissions would need to fall by about 45% to 60% from 2010 levels by 2030 (IPCC 2018b). Achieving the Paris Agreement’s Article 4.1 aim potentially implies that global warming will peak and then follow a gradually declining path, potentially to below 1.5°C warming (Rogelj et al. 2021).

---

## Usage Notes

- Run this prompt in a fresh chat session — do not reuse sessions across batches
- After generation, review each question: verify the correct answer against the source, check that distractors are unambiguous, and cut any question where you are uncertain about the answer
- Target acceptance rate: ~60% of generated candidates
- When multiple models generate questions on the same concept, keep the version with tighter or more plausible distractors and discard the duplicate
