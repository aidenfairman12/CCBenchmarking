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
    "source": "IPCC AR6 WG1 Chapter 7 Section 7.4.2.1",
    "category": "Physical Climate Science Fundamentals",
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

The Planck response represents the additional thermal or longwave (LW) emission to space arising from vertically uniform warming of the surface and the atmosphere. The Planck response α P, often called the Planck feedback, plays a fundamental stabilizing role in Earth’s climate and has a value that is strongly negative: a warmer planet radiates more energy to space. A crude estimate of α Pcan be made using the normalized greenhouse effect g̃, defined as the ratio between the greenhouse effectG and the upwelling LW flux at the surface (Raval and Ramanathan, 1989). Current estimates (Section 7.2, Figure 7.2) give G= 159 W m–2 and g̃≈ 0.4. Assumingg̃ is constant, one obtains for a surface temperature Ts= 288 K, α P= (g– 1) 4σT3s≈ –3.3 W m–2°C–1, whereσ is the Stefan–Boltzmann constant. This parameter α P is estimated more accurately using kernels obtained from meteorological reanalysis or climate simulations (Soden and Held, 2006; Dessler, 2013; Vial et al., 2013; Caldwell et al., 2016; Colman and Hanson, 2017; Zelinka et al., 2020). Discrepancies among estimates primarily arise because differences in cloud distributions make the radiative kernels differ (Kramer et al., 2019). Using six different kernels, Zelinka et al. (2020) obtained a spread of ±0.1 W m–2°C–1(one standard deviation). Discrepancies among estimates secondarily arise from differences in the pattern of equilibrium surface temperature changes among ESMs. For the CMIP5 and CMIP6 models this introduces a spread of ±0.04 W m–2°C–1(one standard deviation). The multi-kernel and multi-model mean of α P is equal to –3.20 W m–2°C–1for the CMIP5 and –3.22 W m–2°C–1for the CMIP6 models (Supplementary Material, Table 7.SM.5). Overall, there is high confidence in the estimate of the Planck response, which is assessed to be α P= –3.22 W m–2°C–1 with avery likely range of –3.4 to –3.0 W m–2°C–1and a likely range of –3.3 to –3.1 W m–2°C–1.

The Planck temperature response ΔTP is the equilibrium temperature change in response to a forcing ΔF when the net feedback parameter is equal to the Planck response parameter: ΔTP= –ΔF / α P.

---

## Usage Notes

- Run this prompt in a fresh chat session — do not reuse sessions across batches
- After generation, review each question: verify the correct answer against the source, check that distractors are unambiguous, and cut any question where you are uncertain about the answer
- Target acceptance rate: ~60% of generated candidates
- When multiple models generate questions on the same concept, keep the version with tighter or more plausible distractors and discard the duplicate
