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
    "source": "IPCC AR6 WG3 Chapter 13 Section 13.6.1.3",
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

Estimates of the effective carbon price (as an estimate of overall stringency across policy instruments) differ greatly between countries and sectors (World Bank 2021a). Countries with higher overall effective carbon prices tend to have lower carbon intensity of energy supply and lower emissions intensity of the economy, as shown in an analysis of 42 G20 and OECD countries (OECD 2018). The carbon price that prevails under a carbon tax or ETS is not directly a measure of policy stringency across an economy, as the carbon prices typically only cover a share of total emissions, and rebates or free allowance allocations can limit effectiveness (OECD 2018). At low emissions prices, mitigation incentives are small; as of April 2021, seventeen jurisdictions with a carbon pricing policy had a tax rate or allowance price less than USD5 per tCO2 (World Bank 2021a).

Other policies, such as fossil fuel subsidies, may provide incentives to increase emissions thus limiting the effectiveness of the mitigation policy (Section 13.6.3.6). Those effects may be complex and difficult to identify. In most countries trade policy provides an implicit subsidy to CO2 emissions (Shapiro 2020). The analysis of emissions from energy use in buildings in Chapter 9 illustrates the factors that support and counteract mitigation policies.

Furthermore, emissions pricing policies encourage reduction of emissions whose marginal abatement cost is lower than the tax/allowance price, so they have limited impact on emissions with higher abatement costs such as industrial process emissions (Bataille et al. 2018a; Davis et al. 2018). EU ETS emission reductions have been achieved mainly through implementation of low cost measures such as energy efficiency and fuel switching rather than more costly industrial process emissions.

Estimating the overall effectiveness of mitigation policies is difficult because of the need to identify which observed changes in emissions and their drivers are attributable to policy effort and which to other factors. Cross-Chapter Box 10 in Chapter 14 brings together several lines of evidence to indicate that mitigation policies have had a discernible impact on mitigation for specific countries, sectors and technologies and led to avoided global emissions to date by several billion tonnes CO2-eq annually (medium evidence, medium agreement ).

---

## Usage Notes

- Run this prompt in a fresh chat session — do not reuse sessions across batches
- After generation, review each question: verify the correct answer against the source, check that distractors are unambiguous, and cut any question where you are uncertain about the answer
- Target acceptance rate: ~60% of generated candidates
- When multiple models generate questions on the same concept, keep the version with tighter or more plausible distractors and discard the duplicate
