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
    "source": "IPCC AR6 WG2 Chapter 2 Section 2.3.1",
    "category": "Climate-Ecosystem Interactions",
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

Extreme events are a natural and important part of many ecosystems, and many organisms have adapted to cope with long-term and short-term climate variability within the disturbance regime experienced during their evolutionary history (high confidence). However, climate changes, disturbance regime changes and the magnitude and frequency of extreme events such as floods, droughts, cyclones, heat waves and fire have increased in many regions (high confidence). These disturbances affect ecosystem functioning, biodiversity and ecosystem services (high confidence), but are, in general, poorly captured in impact models (Albrich et al., 2020b), although this should improve as higher-resolution climate models that better capture smaller-scale processes and extreme events become available (Seneviratne et al., 2021). Extreme events pose huge challenges for EbA (IPCC, 2012). Ecosystem functionality, on which such adaptation measures rely, may be altered or destroyed by extreme episodic events (Handmer et al., 2012; Lal et al., 2012; Pol et al., 2017).

There is high confidence that the combination of internal variability, superimposed on longer-term climate trends, is pushing ecosystems to tipping points, beyond which abrupt and possibly irreversible changes are occurring (Harris et al., 2018a; Jones et al., 2018; Hoffmann et al., 2019b; Prober et al., 2019; Berdugo et al., 2020; Bergstrom et al., 2021). Increases in the frequency and severity of heat waves, droughts and aridity, floods, fires and extreme storms have been observed in many regions (Seneviratne et al., 2012; Ummenhofer and Meehl, 2017), and these trends are projected to continue (high confidence) (Section 3.2.2.1, Cross-Chapter Box EXTREMES this Chapter) (Hoegh-Guldberg et al., 2018; Seneviratne et al., 2021).

While the major climate hazards at the global level are generally well described with high confidence, there is less understanding about the importance of hazards on ecosystems when they are superimposed (Allen et al., 2010; Anderegg et al., 2015; Seidl et al., 2017; Dean et al., 2018), and the outcomes are difficult to quantify in future projections (Handmer et al., 2012). Simultaneous or sequential events (coincident or compounding events) can lead to an extreme event or impact, even if each event is not in themselves extreme (Denny et al., 2009; Hinojosa et al., 2019). For example, the compounding effects of SLR, extreme coastal high tide, storm surge, and river flow can substantially increase flooding hazard and impacts on freshwater systems (Moftakhari et al., 2017). On land, changing rainfall patterns and repeated heat waves may interact with biological factors such as altered plant growth and nutrient allocation under elevated CO2, affecting herbivore rates and insect outbreaks leading to the widespread dieback of some forests (e.g., in Australian eucalypt forests) (Gherlenda et al., 2016; Hoffmann et al., 2019a). Risk assessments typically only consider a single climate hazard with no changing variability, thereby potentially underestimating the actual risk (Milly et al., 2008; Sadegh et al., 2018; Zscheischler et al., 2018; Terzi et al., 2019; Stockwell et al., 2020).

---

## Usage Notes

- Run this prompt in a fresh chat session — do not reuse sessions across batches
- After generation, review each question: verify the correct answer against the source, check that distractors are unambiguous, and cut any question where you are uncertain about the answer
- Target acceptance rate: ~60% of generated candidates
- When multiple models generate questions on the same concept, keep the version with tighter or more plausible distractors and discard the duplicate
