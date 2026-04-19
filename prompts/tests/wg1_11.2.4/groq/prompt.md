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
    "source": "IPCC AR6 WG1 Chapter 11 Section 11.2.4",
    "category": "Attribution Science",
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

The most important quantity used to characterize past and future climate change is global warming relative to its pre-industrial level. Changes in global warming are linked quasi-linearly to global cumulative carbon dioxide (CO2) emissions (IPCC, 2013), and for their part, changes in regional climate, including many types of extremes, scale quasi-linearly with changes in global warming, often independently of the underlying emissions scenarios (SR1.5 Chapter 3; Seneviratne et al., 2016; Matthews et al., 2017; Wartenburger et al., 2017; Kharin et al., 2018; Y. Sun et al., 2018a; Tebaldi and Knutti, 2018; Beusch et al., 2020; Li et al., 2021). In addition, the use of global warming levels in the context of global policy documents – in particular the 2015 Paris Agreement (UNFCCC, 2016) implies that information on changes in the climate system, and specifically extremes, as a function of global warming are of particular policy relevance. Cross-Chapter Box 11.1 provides an overview on the translation between information at global warming levels (GWLs) and scenarios.

The assessment of projections of future changes in extremes as function of GWL has an advantage in separating uncertainty associated with the global warming response (see Chapter 4) from the uncertainty resulting from the regional climate response as a function of GWLs (Seneviratne and Hauser, 2020). If the interest is in the projection of regional changes at certain GWLs, such as those defined by the Paris Agreement, projections based on time periods and emissions scenarios have unnecessarily larger uncertainty due to differences in model global transient climate responses. To take advantage of this feature and to provide easy comparison with SR1.5, assessments of projected changes in this chapter are largely provided in relation to future GWLs, with a focus on changes at +1.5°C, +2°C, and +4°C of global warming above pre-industrial levels (e.g., Tables 11.1 and 11.2 and regional tables in Section 11.9). These encompass a scenario compatible with the lowest limit of the Paris Agreement (+1.5°C), a scenario slightly overshooting the aims of the Paris Agreement (+2°C), and a ‘worst-case’ scenario with no mitigation (+4°C). Cross-Chapter Box 11.1 provides a background on the GWL sampling approach used in AR6, for the computation of GWL projections from climate models contributing to Phase 6 of the Coupled Model Intercomparison Project (CMIP6) as well as for the mapping of existing scenario-based literature for CMIP6 and the CMIP Phase 5 (CMIP5) to assessments as function of GWLs (see also Section 11.9. and Table 11.3 for an example).

---

## Usage Notes

- Run this prompt in a fresh chat session — do not reuse sessions across batches
- After generation, review each question: verify the correct answer against the source, check that distractors are unambiguous, and cut any question where you are uncertain about the answer
- Target acceptance rate: ~60% of generated candidates
- When multiple models generate questions on the same concept, keep the version with tighter or more plausible distractors and discard the duplicate
