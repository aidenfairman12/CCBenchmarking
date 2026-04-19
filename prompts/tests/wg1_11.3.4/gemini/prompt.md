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
    "source": "IPCC AR6 WG1 Chapter 11 Section 11.3.4",
    "category": "Attribution Science",
    "difficulty": "easy | medium | hard",
    "generated_by": "Gemini"
  }
]
```

## Example of a good vs. bad distractor

**Topic:** Climate sensitivity

Bad distractor (obviously wrong): "The Earth's temperature cannot change due to CO2 because CO2 is a natural gas."
Good distractor (plausibly wrong): "Climate sensitivity is defined as the equilibrium warming per doubling of CO2, typically estimated at 0.5–1.0°C." *(off by a factor — plausible to someone with partial knowledge)*

## Source Passage

Studies since AR5 continue to attribute the observed increase in the frequency or intensity of hot extremes and the observed decrease in the frequency or intensity of cold extremes to human influence, dominated by anthropogenic greenhouse gas emissions, on global and continental scales, and for many AR6 regions. These include attribution of changes in the magnitude of annual TXx, TNx, TXn, and TNn, based on different observational datasets including, HadEX2 and HadEX3, CMIP5 and CMIP6 simulations, and different statistical methods (Kim et al., 2016; Z. Wang et al., 2017a; Seong et al., 2021). As is the case for an increase in mean temperature (Section 3.3.1), an increase in extreme temperature is mostly due to greenhouse gas forcing, offset by aerosol forcing. The aerosols’ cooling effect is clearly detectable over Europe and Asia (Seong et al., 2021). As much as 75% of the moderate daily hot extremes (above 99.9th percentile) over land are due to anthropogenic warming (Fischer and Knutti, 2015). New results are found to be more robust due to the extended period that improves the signal-to-noise ratio. The effect of anthropogenic forcing is clearly detectable and attributable in the observed changes in these indicators of temperature extremes, even at country and sub-country scales, such as in Canada (Wan et al., 2019). Changes in the number of warm nights, warm days, cold nights, and cold days, and other indicators such as the Warm Spell Duration Index (WSDI), are also attributed to anthropogenic influence (Christidis and Stott, 2016; Hu et al., 2020).

Regional studies, including for Asia (Dong et al., 2018; Lu et al., 2018), Australia (Alexander and Arblaster, 2017), and Europe (Christidis and Stott, 2016), found similar results. A clear anthropogenic signal is also found in the trends in the Combined Extreme Index (CEI) for North America, Asia, Australia, and Europe (Dittus et al., 2016). While various studies have described increasing trends in several heatwave metrics (heatwave duration, the number of heatwave days, etc.) in different regions (e.g., Cowan et al., 2014; Bandyopadhyay et al., 2016; M. Sanderson et al., 2017), few recent studies have explicitly attributed these changes to causes; most of them stated that observed trends are consistent with anthropogenic warming. The detected anthropogenic signals are clearly separable from the response to natural forcing, and the results are generally insensitive to the use of different model samples, as well as different data availability, indicating robust attribution. Studies of monthly, seasonal, and annual records in various regions (Kendon, 2014; Lewis and King, 2015; Bador et al., 2016; Meehl et al., 2016; C. Zhou et al., 2019) and globally (King, 2017) show an increase in the breaking of hot records and a decrease in the breaking of cold records (King, 2017). Changes in anthropogenically attributablerecord-breaking rates are noted to be largest over the Northern Hemisphere land areas (Shiogama et al., 2016). Yin and Sun (2018) found clear evidence of an anthropogenic signal in the changes in the number of frost and ice days, when multiple model simulations were used. In some key wheat-producing regions of Southern Australia, increases in frost days or frost season length have been reported (Dittus et al., 2014; Crimp et al., 2016); these changes are linked to decreases in rainfall, cloud-cover, and subtropical ridge strength, despite an overall increase in regional mean temperatures (Dittus et al., 2014; Pepler et al., 2018).

---

## Usage Notes

- Run this prompt in a fresh chat session — do not reuse sessions across batches
- After generation, review each question: verify the correct answer against the source, check that distractors are unambiguous, and cut any question where you are uncertain about the answer
- Target acceptance rate: ~60% of generated candidates
- When multiple models generate questions on the same concept, keep the version with tighter or more plausible distractors and discard the duplicate
