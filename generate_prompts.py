#!/usr/bin/env python3
"""
generate_prompts.py
-------------------
Generates prompt files for all 4 generation models from a single source passage.
Creates the folder structure and fills in all placeholders automatically.

Usage:
    python generate_prompts.py

Or with arguments:
    python generate_prompts.py \
        --section wg1_7.4.2.1 \
        --category "Physical Climate Science Fundamentals" \
        --source "IPCC AR6 WG1 Chapter 7, Section 7.4.2.1" \
        --passage passage.txt
"""

import argparse
import os
import sys

# ── Config ────────────────────────────────────────────────────────────────────

MODELS = {
    "claude":      "Claude Sonnet",
    "chatgpt":     "ChatGPT",
    "perplexity":  "Perplexity",
    "deepseek":    "DeepSeek",
}

PROMPT_TEMPLATE = """\
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
  {{
    "question": "...",
    "options": {{
      "A": "...",
      "B": "...",
      "C": "...",
      "D": "..."
    }},
    "correct_answer": "A",
    "explanation": "One sentence citing the specific part of the source that confirms the correct answer.",
    "source": "{source_ref}",
    "category": "{category}",
    "difficulty": "easy | medium | hard",
    "generated_by": "{model_name}"
  }}
]
```

## Example of a good vs. bad distractor

**Topic:** Climate sensitivity

Bad distractor (obviously wrong): "The Earth's temperature cannot change due to CO2 because CO2 is a natural gas."
Good distractor (plausibly wrong): "Climate sensitivity is defined as the equilibrium warming per doubling of CO2, typically estimated at 0.5–1.0°C." *(off by a factor — plausible to someone with partial knowledge)*

## Source Passage

{passage}

---

## Usage Notes

- Run this prompt in a fresh chat session — do not reuse sessions across batches
- After generation, review each question: verify the correct answer against the source, check that distractors are unambiguous, and cut any question where you are uncertain about the answer
- Target acceptance rate: ~60% of generated candidates
- When multiple models generate questions on the same concept, keep the version with tighter or more plausible distractors and discard the duplicate
"""

# ── Helpers ───────────────────────────────────────────────────────────────────

def prompt_input(label, default=None):
    if default:
        val = input(f"{label} [{default}]: ").strip()
        return val if val else default
    val = input(f"{label}: ").strip()
    while not val:
        print("  This field is required.")
        val = input(f"{label}: ").strip()
    return val


def read_passage(path):
    path = os.path.expanduser(path)
    if not os.path.exists(path):
        print(f"Error: passage file not found: {path}")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()


def write_prompt(output_dir, model_key, model_name, category, source_ref, passage):
    folder = os.path.join(output_dir, model_key)
    os.makedirs(folder, exist_ok=True)

    content = PROMPT_TEMPLATE.format(
        source_ref=source_ref,
        category=category,
        model_name=model_name,
        passage=passage,
    )

    prompt_path = os.path.join(folder, "prompt.md")
    with open(prompt_path, "w", encoding="utf-8") as f:
        f.write(content)

    # Create empty response placeholder
    response_path = os.path.join(folder, "response.json")
    if not os.path.exists(response_path):
        with open(response_path, "w", encoding="utf-8") as f:
            f.write("")

    return prompt_path


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generate prompt files for all 4 generation models.")
    parser.add_argument("--section",  help="Section ID used for folder name, e.g. wg1_7.4.2.1")
    parser.add_argument("--category", help="Benchmark category name")
    parser.add_argument("--source",   help="Full source reference, e.g. 'IPCC AR6 WG1 Chapter 7, Section 7.4.2.1'")
    parser.add_argument("--passage",  help="Path to .txt file containing the source passage")
    args = parser.parse_args()

    print("\n── Climate Benchmark Prompt Generator ──────────────────────────\n")

    # Gather inputs — use args if provided, otherwise prompt interactively
    section  = args.section  or prompt_input("Section ID (e.g. wg1_7.4.2.1)")
    category = args.category or prompt_input("Category name (e.g. Physical Climate Science Fundamentals)")
    source   = args.source   or prompt_input("Source reference (e.g. IPCC AR6 WG1 Chapter 7, Section 7.4.2.1)")

    if args.passage:
        passage = read_passage(args.passage)
    else:
        passage_path = prompt_input("Path to passage .txt file")
        passage = read_passage(passage_path)

    # Resolve output directory relative to this script's location
    script_dir  = os.path.dirname(os.path.abspath(__file__))
    output_dir  = os.path.join(script_dir, "prompts", "tests", section)

    print(f"\nWriting prompt files to: prompts/tests/{section}/\n")

    for model_key, model_name in MODELS.items():
        path = write_prompt(output_dir, model_key, model_name, category, source, passage)
        print(f"  ✓ {model_key:12s}  →  {os.path.relpath(path, script_dir)}")

    print(f"\nDone. Open each prompt.md, copy contents, paste into a fresh {len(MODELS)}-model session.\n")


if __name__ == "__main__":
    main()
