# ClimateQA: Building a Multi-Model Climate Science Benchmark

## Overview

ClimateQA is a multiple-choice benchmark designed to evaluate how well large language models reason about climate science. Questions are grounded in IPCC AR6 source passages across all three Working Groups: physical science (WG1), impacts and adaptation (WG2), and mitigation (WG3). The questions span seven categories from physical climate fundamentals to policy scenarios.

The primary goal of the project was to replicate the benchmark construction methodology used in papers like MMLU, learning the practical challenges involved: passage selection, prompt engineering for question generation, systematic curation, and model evaluation design. The project also serves as an empirical comparison of four frontier models as both question generators and answerers.

---

## Motivation

I built ClimateQA primarily to understand how benchmark construction actually works in practice. Papers like MMLU describe the methodology at a high level, but building one from scratch exposes design decisions that are easy to underestimate: how to select passages that yield testable questions, why distractor quality is harder than it looks to systematically enforce, and how generation model bias can silently contaminate a dataset. The best way to learn these things was to go through the process myself.

Climate science was the natural choice of domain, as it is something I am genuinely interest in. IPCC AR6 is a well-structured, publicly available body of primary source material spanning physical science, impacts, and mitigation. A benchmark grounded in AR6 also tests something more precise than general climate awareness: whether a model has internalised the specific findings, quantitative estimates, and mechanistic explanations contained in the reports, rather than just knowing the topic exists.

---

## Benchmark Design

### Source Material

Source passages were drawn from 29 sections of IPCC AR6, covering WG1 (18 batches), WG2 (7 batches), and WG3 (4 batches). Sections were selected to represent substantive, testable content, i.e. passages dense with quantitative findings, mechanistic explanations, or scenario comparisons. Policy and governance sections (WG3) were deliberately included despite being harder to write questions for, to ensure the benchmark was not limited to physical science.

### Question Categories

Seven categories were defined to ensure topical coverage:

| Category | Description |
|---|---|
| Physical Climate Science Fundamentals | Feedbacks, forcing, sensitivity |
| Climate Data and Trend Interpretation | Reading and reasoning over observed data tables |
| Attribution Science | Detection and attribution of observed changes |
| Radiative Forcing and Uncertainty | ERF estimates and uncertainty ranges |
| Sea Level Rise | Observations, drivers, and projections |
| Impacts and Vulnerabilities | WG2 assessed impacts by region and sector |
| Policy, Scenarios, and Mitigation | SSP scenarios, emissions pathways, WG3 findings |

### Two Prompt Templates

Two prompt templates were developed to serve different question types:

**Standard template** (categories 1, 3–7): generates questions requiring recall or reasoning from a prose passage. Distractors are designed to represent plausible misconceptions rather than obvious errors.

**Data interpretation template** (category 2): generates questions with an embedded data scenario, e.g. a small table or described time series drawn from the source passage. Questions require quantitative reasoning over the data rather than factual recall. Each question specifies a scenario type (trend identification, anomaly interpretation, comparison, projection reading, index reading).

The critical design constraint for the data interpretation template is that the scenario must be self-contained: no external chart or image is needed to answer the question. This makes the benchmark suitable for text-only model evaluation.

---

## Generation Pipeline

Questions were generated using four models: Claude Sonnet 4.6 (Anthropic), GPT-4o (OpenAI), Gemini 2.5 Flash (Google), and Llama 3.3 70B (Meta, via Groq). Each model received the same prompt for each batch, producing five candidate questions per batch: 20 candidates per batch, 580 total across 29 batches.

Using four models served two purposes: it increases question diversity (different models surface different aspects of the same passage) and enables a later analysis of whether models perform better on questions they generated themselves.

All generation used temperature > 0 to introduce variation. The `generated_by` field in each response was enforced to the exact model ID string at write time to ensure clean attribution for downstream analysis.

One early failure mode: the data interpretation prompt template had its output format instructions placed after the trailing `---` separator, which the `clean_prompt()` preprocessing function stripped before sending to the API. All four models produced markdown prose instead of JSON for every Cat2 batch until the template structure was corrected. This is a good example of how prompt pipeline bugs can silently produce systematically wrong outputs across all models simultaneously.

---

## Curation

### Process

All 580 generated questions were loaded into a Streamlit review interface (`review_app.py`) that displays four model columns side by side for each source batch, with the passage available in a collapsible expander. This layout makes it easy to identify duplicate questions across models and compare distractor quality directly.

Each question was marked `accept` or `reject`. The review pass was intentionally relaxed rather than strictly criteria-driven: the primary goal was removing clearly broken questions (wrong correct answer, obviously absurd distractors, unanswerable without external context) rather than enforcing a high quality bar uniformly.

**172 of 580 questions were accepted (29.7%).**

### Generation Quality by Model

Acceptance rates varied substantially across models:

| Model | Accepted | Total | Rate |
|---|---|---|---|
| Claude Sonnet 4.6 | 68 | 145 | **46.9%** |
| GPT-4o | 37 | 145 | 25.5% |
| Gemini 2.5 Flash | 34 | 145 | 23.4% |
| Llama 3.3 70B | 33 | 145 | 22.8% |

Claude's acceptance rate was nearly double the other three models, driven almost entirely by its hard questions: Claude had a 69% acceptance rate on hard questions versus 17–31% for others. This suggests Claude more reliably generates distractors that require genuine reasoning to eliminate, rather than distractors that are obviously wrong to anyone familiar with the domain.

Notably, Gemini's acceptance rate *decreases* with difficulty (28% easy → 22% medium → 17% hard), while every other model shows the opposite trend. This implies Gemini's nominally hard questions were not meaningfully more discriminating; likely reflecting weaker distractor construction at higher difficulty levels.

### Passage Quality Signal

Acceptance counts per batch (max 20 across four models) serve as a proxy for passage quality. Thirteen of 29 batches produced five or fewer accepted questions. Attribution Science passages (WG1 Ch. 11, Ch. 3) were consistently the weakest, with four of the five lowest-yield batches coming from that category. Policy and Governance passages (WG3) also underperformed, suggesting that normative or governance-focused text is harder to convert into unambiguous multiple-choice questions than quantitative or mechanistic passages.

No batch reached 12 accepted questions, meaning no passage was a clean sweep across all four models. The modal outcome was three models contributing at least one accepted question per batch (12 of 29 batches), with four-model agreement in another 12 batches.

### Curation Limitations

The acceptance rate (29.7%) came in well below the 50–60% target set in the prompt instructions. This is partly attributable to passage selection: several source sections, particularly Attribution Science and WG3 Policy passages, were too abstract or normative to reliably anchor unambiguous multiple-choice questions, regardless of which model attempted them. A more careful passage selection process, favouring sections with dense quantitative findings or clearly testable mechanistic claims, would likely have improved generation quality across all models before curation. The low acceptance rate is therefore at least partly a reflection of upstream passage quality rather than model capability alone. A production benchmark would require a second reviewer pass with explicit inter-annotator agreement measurement.
The curation was also not performed blind to model identity; the reviewer could see which model generated each question. This introduces potential model preference bias in the selected questions, which could confound the self vs cross-model evaluation results.

---

## Evaluation

### Setup

Each of the 172 accepted questions was presented to all four models as a zero-shot multiple-choice question. The evaluation prompt contains only the question text, the four options, and (for data interpretation questions) the embedded scenario. The source passage is deliberately excluded.

This tests whether models have *internalised* the relevant climate science knowledge from training — not whether they can extract an answer from a provided text. The tradeoff is that some questions hinge on specific IPCC AR6 values that a model could only know if it encountered that material during training. Since all evaluated models were trained after AR6's 2021–2022 publication, this is likely a minor confound but is worth noting.

Model responses were constrained to a single letter (A–D) with `max_tokens=16` and `temperature=0` to minimise variance. A regex parser extracted the answer letter from free-text responses where models did not comply with the format instruction.

**Note: Gemini evaluation hit the 20 RPD free-tier limit after 11 of 172 questions. Gemini results are excluded from the analysis below.**

### Overall Results

| Model | Correct | Total | Accuracy |
|---|---|---|---|
| Claude Sonnet 4.6 | 155 | 172 | **90.1%** |
| GPT-4o | 152 | 172 | 88.4% |
| Llama 3.3 70B | 149 | 172 | 86.6% |

All three models score in the 87–90% range, indicating strong climate science knowledge across the board. The spread is narrow (3.5 percentage points), suggesting the benchmark does not strongly differentiate the three models at this overall level.

### Performance by Difficulty

| Difficulty | Claude | GPT-4o | Llama 3.3 |
|---|---|---|---|
| Easy | 80.0% | 85.0% | 80.0% |
| Medium | 94.2% | 91.3% | 89.9% |
| Hard | **97.7%** | 88.4% | 90.7% |

Claude's accuracy *increases* sharply with difficulty, reaching 97.7% on hard questions. GPT-4o and Llama perform more uniformly. This is a notable inversion of the expected difficulty curve and likely reflects Claude's strong performance on the questions Claude itself generated — Claude contributed 69% of accepted hard questions, and Claude performs best on hard questions. This conflation of generator and evaluator is addressed in the self-advantage analysis below.

Easy questions are the hardest difficulty tier for all three models (80–85%), which is counterintuitive. One explanation: "easy" questions in this benchmark were accepted at the lowest rate (26.5% vs 36.1% for hard), meaning the easy questions that survived curation were not necessarily simpler — they may have been accepted for other reasons (cleaner distractors, well-written scenario) while genuinely hard easy-difficulty questions were rejected.

### Performance by Prompt Type

| Type | Accuracy |
|---|---|
| Standard | 89.7% |
| Data interpretation | 78.7% |

Data interpretation questions are meaningfully harder, with an 11-point accuracy gap versus standard questions. This aligns with the design intent — these questions require quantitative reasoning over an embedded scenario rather than factual recall, and they test a more precise skill.

### Self vs Cross-Model Accuracy

A key analysis enabled by this benchmark's design is whether models perform differently on questions they generated versus questions generated by other models:

| Model | Self accuracy | Cross accuracy | Δ |
|---|---|---|---|
| Claude Sonnet 4.6 | 95.6% (68q) | 86.5% (104q) | **+9.1pp** |
| GPT-4o | 83.8% (37q) | 89.6% (135q) | -5.8pp |
| Llama 3.3 70B | 78.8% (33q) | 88.5% (139q) | -9.7pp |

Claude shows a clear self-advantage: it scores 9 points higher on questions it generated than on questions from other models. This is consistent with the hypothesis that a model's question-generation style may be subtly familiar to that same model on evaluation.

More surprising is that GPT-4o and Llama show the opposite pattern, scoring *lower* on their own questions than on others. One possible explanation: these models generate harder or more adversarially constructed distractors that are difficult even for themselves to navigate. Another is that their self-generated questions are phrased in ways that do not naturally cue the correct reasoning path on the evaluation pass.

The self-advantage finding has implications for benchmark construction more broadly: if the same model is used for both generation and evaluation, self-familiarity may inflate apparent performance. A cleaner benchmark design would use a held-out model for generation that is not one of the evaluated models.

---

## Limitations

**Relaxed curation.** The review pass prioritised removing clearly broken questions over enforcing a consistent quality bar. A production benchmark would require explicit acceptance criteria, multiple reviewers, and inter-annotator agreement measurement (e.g. Cohen's κ). Acceptance rates and the resulting question difficulty distribution should be interpreted accordingly.

**Non-blind review.** The reviewer could see which model generated each question. This may have introduced bias toward Claude's question style, partially explaining Claude's higher acceptance rate and subsequently higher accuracy on its own questions.

**Training data contamination.** IPCC AR6 was published in 2021–2022. All four models were trained on data collected after that date and have almost certainly seen AR6 content. The benchmark therefore measures a combination of genuine climate reasoning and training data memorisation. Disentangling these is difficult without access to model training data.

**Gemini evaluation incomplete.** Only 11 of 172 Gemini evaluation pairs were completed before hitting the 20 RPD free-tier limit for Gemini 2.5 Flash. Gemini is excluded from all evaluation analysis.

**WG3 underrepresentation.** Only 21 of 172 accepted questions (12.2%) come from WG3 mitigation content, compared to WG3's proportional share of batches. Policy and governance passages consistently yielded fewer accepted questions, resulting in a benchmark skewed toward physical science content.

**Single-answer format.** Multiple-choice questions with four options have a 25% random baseline, and capable models may be able to eliminate distractors through surface reasoning without genuine domain understanding. More discriminating formats (free-response, multi-hop reasoning chains) would provide stronger signal.

---

## What a Production Version Would Look Like

A rigorous version of this benchmark would address the above limitations in several ways:

**Held-out generation model.** Use a model not included in the evaluation set (e.g. a fine-tuned generation model) to remove self-advantage as a confound.

**Blind, multi-annotator curation.** Present questions without model attribution and use at least two independent reviewers with explicit criteria. Compute inter-annotator agreement and adjudicate disagreements.

**Contamination mitigation.** Restrict source material to post-training-cutoff documents, or use paraphrased passages to reduce exact-match memorisation.

**Difficulty calibration.** Validate difficulty labels empirically — a question labelled "hard" should be answered correctly by fewer models at lower rates. Discard or relabel questions where empirical difficulty diverges from intended difficulty.

**Expanded coverage.** Increase WG2 and WG3 representation, and include regional assessment content from WG2 Working Group II chapters covering specific ecosystems and sectors.

---

## Tooling

The full pipeline is implemented as a set of standalone Python scripts:

| Script | Purpose |
|---|---|
| `generate_prompts.py` | Generates per-model prompt files from IPCC passages and `section_list.xlsx` |
| `generate_responses.py` | Sends prompts to model APIs and saves raw responses |
| `build_review.py` | Flattens all responses to `review/questions.csv` |
| `review_app.py` | Streamlit curation interface (4-model side-by-side, auto-save) |
| `collate.py` | Produces `benchmark.json` from accepted questions |
| `evaluate.py` | Runs benchmark evaluation across models, saves `eval/results.csv` |
| `analyse.py` | Generates curation and evaluation analysis charts and report |

All scripts support `--dry-run`, `--overwrite`, and `--models` flags. Evaluation is resumable — already-completed pairs are skipped automatically.
