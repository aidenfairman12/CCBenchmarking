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
    "source": "IPCC AR6 WG1 Chapter 4 Section 4.2.2",
    "category": "Projections and Uncertainty",
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

This chapter draws on model simulations from CMIP6 (Eyring et al., 2016) using a new range of scenarios based on Shared Socio-economic Pathways (SSPs; O’Neill et al., 2016). The set of SSPs is described in detail in Chapter 1 (Section 1.6) and recognizes that global radiative forcing levels can be achieved by different pathways of CO2, non-CO2 greenhouse gases (GHGs), aerosols (Amann et al., 2013; Rao et al., 2017) and land use; the set of SSPs therefore establishes a matrix of global forcing levels and socio-economic storylines. ScenarioMIP (O’Neill et al., 2016) identifies four priority (tier-1) scenarios that participating modelling groups are asked to perform, SSP1-2.6 for sustainable pathways, SSP2-4.5 for middle-of-the-road, SSP3-7.0 for regional rivalry, and SSP5-8.5 for fossil fuel-rich development. This chapter focuses its assessment on these, plus the SSP1-1.9 scenario, which is directly relevant to the assessment of the 1.5°C Paris Agreement goal. Further, this chapter discusses these scenarios and their extensions past 2100 in the context of the very long-term climate change in Section 4.7.1. Projections of short-lived climate forcers (SLCFs) are assessed in more detail in Chapter 6 (Section 6.7).

In presenting results and evidence, this chapter tries to be as comprehensive as possible. In tables we show multi-model mean change and 5–95% range for all five SSPs, while in time series figures we show multi-model mean change for all five SSPs but for clarity 5–95% range only for SSP1-2.6 and SSP3-7.0. Where maps are presented, due to space restrictions we focus on showing multi-model mean change for SSP1-2.6 and SSP3-7.0. SSP1-2.6 is preferred over SSP1-1.9 because the latter has far fewer simulations available. The high-end scenarios RCP8.5 or SSP5-8.5 have recently been argued to be implausible to unfold (e.g., Hausfather and Peters, 2020; see Chapter 3 of the AR6 WGIII). However, where relevant we show results for SSP5-8.5, for example to enable backwards compatibility with AR5, for comparison between emissions-driven and concentration-driven simulations, and because there is greater data availability of daily output for SSP5-8.5. When presenting low-likelihood, high-warming storylines we also show results from the high-end SSP5-8.5 scenario.

---

## Usage Notes

- Run this prompt in a fresh chat session — do not reuse sessions across batches
- After generation, review each question: verify the correct answer against the source, check that distractors are unambiguous, and cut any question where you are uncertain about the answer
- Target acceptance rate: ~60% of generated candidates
- When multiple models generate questions on the same concept, keep the version with tighter or more plausible distractors and discard the duplicate
