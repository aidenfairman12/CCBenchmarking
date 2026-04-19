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
    "source": "IPCC AR6 WG1 Chapter 3 Section 3.2.1",
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

Regression-based methods, also known as fingerprinting methods, have been widely used for detection of climate change and attribution of the change to different external drivers. Initially, these methods were applied to detect changes in global surface temperature, and were then extended to other climate variables at different time and spatial scales (e.g., Hegerl et al., 1996; Hasselmann, 1997; Allen and Tett, 1999; Gillett et al., 2003b; Zhang et al., 2007; Min et al., 2008a, 2011). These approaches are based on multivariate linear regression and assume that the observed change consists of a linear combination of externally forced signals plus internal variability, which generally holds for large-scale variables (Hegerl and Zwiers, 2011). The regressors are the expected space–time response patterns to different climate forcings (fingerprints), and the residuals represent internal variability. Fingerprints are usually estimated from climate model simulations following spatial and temporal averaging. A regression coefficient which is significantly greater than zero implies that a detectable change is identified in the observations. When the confidence interval of the regression coefficient includes unity and is inconsistent with zero, the magnitude of the model simulated fingerprints is assessed to be consistent with the observations, implying that the observed changes can be attributed in part to a particular forcing. Variants of linear regression have been used to address uncertainty in the fingerprints due to internal variability (Allen and Stott, 2003) as well as structural model uncertainty (Huntingford et al., 2006).

In order to improve the signal-to-noise ratio, observations and model-simulated responses are usually normalized by an estimate of internal variability derived from climate model simulations. This procedure requires an estimate of the inverse covariance matrix of the internal variability, and some approaches have been proposed for more reliable estimation of this (Ribes et al., 2009). A signal can be spuriously detected due to too-small noise, and hence simulated internal variability needs to be evaluated with care. Model-simulated variability is typically checked through comparing modelled variance from unforced simulations with the observed residual variance using a standard residual consistency test (Allen and Tett, 1999), or an improved one (Ribes and Terray, 2013). Imbers et al. (2014) tested the sensitivity of detection and attribution results to different representations of internal variability associated with short-memory and long-memory processes. Their results supported the robustness of previous detection and attribution statements for the global mean temperature change but they also recommended the use of a wider variety of robustness tests.

Some recent studies focused on the improved estimation of the scaling factor (regression coefficient) and its confidence interval. Hannart et al. (2014) described an inference procedure for scaling factors which avoids making the assumption that model error and internal variability have the same covariance structure. An integrated approach to optimal fingerprinting was further suggested in which all uncertainty sources (i.e., observational error, model error, and internal variability) are treated in one statistical model without a preliminary dimension reduction step (Hannart, 2016). Katzfuss et al. (2017) introduced a similar integrated approach based on a Bayesian model averaging. On the other hand, DelSole et al. (2019) suggested a bootstrap method to better estimate the confidence intervals of scaling factors even in a weak-signal regime. It is notable that some studies do not optimize fingerprints, as uncertainty in the covariance introduces a further layer of complexity, but results in only a limited improvement in detection (Polson and Hegerl, 2017).

---

## Usage Notes

- Run this prompt in a fresh chat session — do not reuse sessions across batches
- After generation, review each question: verify the correct answer against the source, check that distractors are unambiguous, and cut any question where you are uncertain about the answer
- Target acceptance rate: ~60% of generated candidates
- When multiple models generate questions on the same concept, keep the version with tighter or more plausible distractors and discard the duplicate
