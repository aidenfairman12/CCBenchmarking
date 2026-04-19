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
    "source": "IPCC AR6 WG3 Chapter 13 Section 13.2.1",
    "category": "Policy and Governance",
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

National laws that govern climate action often set the legal basis for climate action (Averchenkova et al. 2021). This legal basis can serve several functions: establish a platform for transparent target setting and implementation (Bennett 2018); provide a signal to actors by indicating intent to harness state authority behind climate action (Scotford and Minas 2019); promise enhanced regulatory certainty (Scotford et al. 2017); create law-backed agencies for coordination, compliance and accountability (Scotford and Minas 2019); provide a basis for mainstreaming mitigation into sector action, and create focal points for social mobilisation (medium evidence, high agreement ) (Dubash et al. 2013). For lower/middle income countries, in particular, the existence of a law may also attract international finance by serving as a signal of credibility (Fisher et al. 2017). The realisation of these potential governance gains depends on local context, legal design, successful implementation, and complementary action at different scales.

There are both narrow and broad definitions of what counts as ‘climate laws’. The literature distinguishes direct climate laws that explicitly considers climate change causes or impacts – for example through mention of greenhouse gas reductions in its objectives or title (Dubash et al. 2013) – from indirect laws that have ‘the capacity to affect mitigation or adaptation’ through the subjects they regulate, for example, through promotion of co-benefits, or creation of reporting protocols (Scotford and Minas 2019). Closely related is a ‘sectoral approach’ based on the layering of climate considerations into existing laws in the absence of an overarching framework law (Rumble 2019). Many countries also adopt executive climate strategies (discussed in Section 13.2), which may either coexist with or substitute for climate laws, and that may also be related to a country’s NDC process under the Paris Agreement.

The prevalence of both direct and indirect climate laws has increased considerably since 2007, although definitional differences across studies complicate a clear assessment of their relative importance (medium evidence, high agreement ) (Iacobuta et al. 2018; Nachmany and Setzer 2018). Direct climate laws – with greenhouse gas limitation as a direct objective – had been passed in 56 countries (of 194 studied) covering 53% of emissions in 2020, with most of that rise happening between 2010 and 2015 (Figure 13.1). Both direct and indirect laws – those that have an effect on mitigation even if this is not the primary outcome – is most closely captured by the ‘Climate Change Laws of the World’ database, which illustrates the same trend of growing prevalence, documenting 694 mitigation-related laws by 2020 versus 558 in 2015 and 342 in 2010 (Nachmany and Setzer 2018; LSE Grantham Research Institute on Climate Change and the Environment 2021). 1 Among these, the majority are accounted for by sectoral indirect laws. For example, a study of Commonwealth countries finds that a majority of these countries have not taken the route of a single overarching law, but rather have an array of laws across different areas, for example, Indian laws on energy efficiency and Ghana’s laws on renewable energy promotion (Scotford et al. 2017).

---

## Usage Notes

- Run this prompt in a fresh chat session — do not reuse sessions across batches
- After generation, review each question: verify the correct answer against the source, check that distractors are unambiguous, and cut any question where you are uncertain about the answer
- Target acceptance rate: ~60% of generated candidates
- When multiple models generate questions on the same concept, keep the version with tighter or more plausible distractors and discard the duplicate
