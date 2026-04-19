#!/usr/bin/env python3
"""
generate_prompts.py
-------------------
Generates prompt files for all 4 generation models from source passages.

── SINGLE BATCH MODE ────────────────────────────────────────────────────────
Standard prompt (Categories 1, 3, 4, 5, 6, 7):
    python generate_prompts.py \
        --section wg1_7.4.2.1 \
        --category "Physical Climate Science Fundamentals" \
        --source "IPCC AR6 WG1 Chapter 7 Section 7.4.2.1" \
        --passage passage.txt

Data interpretation prompt (Category 2):
    python generate_prompts.py \
        --section wg1_2.3.1.1 \
        --category "Climate Data and Trend Interpretation" \
        --source "IPCC AR6 WG1 Chapter 2 Section 2.3.1.1" \
        --passage data_context.txt \
        --data-interpretation

── BATCH MODE ───────────────────────────────────────────────────────────────
Reads section_list.xlsx and generates prompts for all verified/locked batches
that have a matching passage file in the passages/ folder.

    python generate_prompts.py --batch [--overwrite]

Passage files must be named by batch_id, e.g.:
    passages/cat1_batch2.txt
    passages/cat2_batch1.txt

Batches with status 'generated' are skipped unless --overwrite is set.
The script prints a summary of generated vs. missing passage files.
"""

import argparse
import os
import sys

# ── Config ────────────────────────────────────────────────────────────────────

MODELS = {
    "claude":   "Claude Sonnet",
    "chatgpt":  "ChatGPT",
    "gemini":   "Gemini",
    "groq":     "Llama 3.3 70B (Groq)",
}

# Statuses to process in batch mode (skip 'generated' unless --overwrite)
BATCH_STATUSES = {"verified", "locked"}

STANDARD_TEMPLATE = """\
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

{content}

---

## Usage Notes

- Run this prompt in a fresh chat session — do not reuse sessions across batches
- After generation, review each question: verify the correct answer against the source, check that distractors are unambiguous, and cut any question where you are uncertain about the answer
- Target acceptance rate: ~60% of generated candidates
- When multiple models generate questions on the same concept, keep the version with tighter or more plausible distractors and discard the duplicate
"""

DATA_INTERP_TEMPLATE = """\
# Data Interpretation Question Generation Prompt
# Use for: Category 2 — Climate Data & Trend Interpretation only
# Paste this into your LLM chat interface

---

You are a rigorous question writer for a climate science benchmark. Your task is to generate data interpretation questions — questions that require reasoning over a described dataset, time series, or anomaly table rather than recalling facts.

## How these questions work

Each question contains an embedded data scenario (a small table, a described trend, or a set of values). The reader must interpret or reason about that data to answer correctly. These questions test quantitative and analytical reasoning, not memory.

## Requirements

- Generate exactly 5 questions
- Each question must embed a self-contained data scenario — no external chart or image needed
- Base all scenario values on the data context provided below — do not invent values outside those ranges
- 4 answer options (A, B, C, D), exactly one is correct
- No "all of the above", "none of the above", or "both A and B" options
- Distractors should represent plausible misreadings of the data (e.g. confusing absolute value with anomaly, misreading a trend direction, off-by-one decade errors)
- The correct answer must follow directly and unambiguously from the data provided
- Do not require knowledge beyond what is presented in the scenario
- Vary difficulty: aim for roughly 2 easy, 2 medium, 1 hard per 5 questions. If you find yourself writing a third easy question, convert it to medium instead
- Ensure each question tests a distinct aspect of the data — do not generate two questions about the same feature

**Easy:** Direct reading of a value or obvious trend from the data
**Medium:** Requires comparing, computing a simple difference, or interpreting what a pattern means
**Hard:** Requires identifying a non-obvious pattern, distinguishing between two plausible interpretations, or reasoning about what the data implies

## Scenario types to use (vary across your batch)

1. **Trend identification** — a time series table; ask about direction, rate, or magnitude of change
2. **Anomaly interpretation** — anomalies relative to a baseline; ask what they indicate
3. **Comparison** — two regions or time periods side by side; ask which is warmer/wetter/more variable
4. **Index reading** — a climate index value (e.g. ENSO, NAO); ask what climate conditions it implies
5. **Projection reading** — projections under two scenarios; ask about the spread or direction

## Output Format

Return a strict JSON array and nothing else — no preamble, no commentary.

```json
[
  {{
    "scenario": "A brief prose or table description of the data, embedded directly in the question or as a preamble.",
    "question": "...",
    "options": {{
      "A": "...",
      "B": "...",
      "C": "...",
      "D": "..."
    }},
    "correct_answer": "B",
    "explanation": "One sentence explaining which feature of the data supports the correct answer.",
    "data_source": "{source_ref}",
    "scenario_type": "trend_identification | anomaly_interpretation | comparison | index_reading | projection_reading",
    "category": "{category}",
    "difficulty": "easy | medium | hard",
    "generated_by": "{model_name}"
  }}
]
```

## Data Context

Base all scenario values on the following real-world data anchor. Do not invent values — use or derive from what is provided below.

{content}

---

## Usage Notes

- Run this prompt in a fresh chat session — do not reuse sessions across batches
- After generation, verify that the data values in each scenario are consistent with the provided data context
- Check that the correct answer is the only defensible conclusion from the data — if a second option could be argued, cut or revise
- Target acceptance rate: ~50% (slightly lower than standard due to scenario construction complexity)
- When multiple models generate questions on the same data feature, keep the version with tighter distractors
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


def read_file(path):
    path = os.path.expanduser(path)
    if not os.path.exists(path):
        print(f"Error: file not found: {path}")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()


def section_to_folder(wg, section):
    """Convert WG + section to a folder-safe ID, e.g. wg1_7.4.2.1"""
    wg_prefix = wg.lower().replace("wg", "wg")  # WG1 → wg1
    section_safe = section.replace(" ", "_").replace("/", "_")
    return f"{wg_prefix}_{section_safe}"


def write_prompt(output_dir, model_key, model_name, category, source_ref, content, data_interp):
    folder = os.path.join(output_dir, model_key)
    os.makedirs(folder, exist_ok=True)

    template = DATA_INTERP_TEMPLATE if data_interp else STANDARD_TEMPLATE
    filled = template.format(
        source_ref=source_ref,
        category=category,
        model_name=model_name,
        content=content,
    )

    prompt_path = os.path.join(folder, "prompt.md")
    with open(prompt_path, "w", encoding="utf-8") as f:
        f.write(filled)

    response_path = os.path.join(folder, "response.json")
    if not os.path.exists(response_path):
        with open(response_path, "w", encoding="utf-8") as f:
            f.write("")

    return prompt_path


def generate_batch(batch_id, category, wg, section, source_ref, prompt_type,
                   content, script_dir, overwrite=False):
    """Generate prompts for one batch. Returns folder path or None if skipped."""
    data_interp = (prompt_type == "data_interpretation")
    folder_name = section_to_folder(wg, section)
    output_dir = os.path.join(script_dir, "prompts", "tests", folder_name)

    # Skip if already has prompt files and not overwriting
    existing = os.path.exists(os.path.join(output_dir, "claude", "prompt.md"))
    if existing and not overwrite:
        return None, "skipped (already generated — use --overwrite to regenerate)"

    for model_key, model_name in MODELS.items():
        write_prompt(output_dir, model_key, model_name, category, source_ref,
                     content, data_interp)

    return folder_name, "ok"


# ── Batch mode ────────────────────────────────────────────────────────────────

def run_batch(script_dir, overwrite=False):
    try:
        import openpyxl
    except ImportError:
        print("Error: openpyxl is required for batch mode. Run: pip install openpyxl")
        sys.exit(1)

    xlsx_path = os.path.join(script_dir, "section_list.xlsx")
    if not os.path.exists(xlsx_path):
        print(f"Error: section_list.xlsx not found at {xlsx_path}")
        sys.exit(1)

    passages_dir = os.path.join(script_dir, "passages")
    if not os.path.exists(passages_dir):
        os.makedirs(passages_dir)

    wb = openpyxl.load_workbook(xlsx_path)
    ws = wb["Section List"]

    rows = list(ws.iter_rows(values_only=True))
    header = rows[0]
    col = {name: i for i, name in enumerate(header)}

    generated = []
    skipped_status = []
    missing_passage = []
    already_done = []

    print(f"\n── Climate Benchmark Batch Prompt Generator ────────────────────\n")
    print(f"  Reading from: section_list.xlsx")
    print(f"  Passages dir: passages/\n")

    for row in rows[1:]:
        batch_id    = row[col["batch_id"]]
        status      = row[col["status"]]
        category    = row[col["category"]]
        wg          = row[col["wg"]]
        section     = str(row[col["section"]])
        source_ref  = row[col["source_ref"]]
        prompt_type = row[col["prompt_type"]]

        if not batch_id:
            continue

        # Skip already-generated batches unless overwrite
        if status == "generated" and not overwrite:
            skipped_status.append(batch_id)
            continue

        # Only process verified/locked (and generated if overwrite)
        if status not in BATCH_STATUSES and not (overwrite and status == "generated"):
            skipped_status.append(f"{batch_id} (status={status})")
            continue

        # Look for passage file
        passage_path = os.path.join(passages_dir, f"{batch_id}.txt")
        if not os.path.exists(passage_path):
            missing_passage.append(batch_id)
            continue

        content = open(passage_path, "r", encoding="utf-8").read().strip()

        folder_name, result = generate_batch(
            batch_id, category, wg, section, source_ref, prompt_type,
            content, script_dir, overwrite=overwrite
        )

        if result == "ok":
            print(f"  ✓ {batch_id:<18}  →  prompts/tests/{folder_name}/")
            generated.append(batch_id)
        else:
            print(f"  ○ {batch_id:<18}  {result}")
            already_done.append(batch_id)

    # Summary
    print(f"\n── Summary ─────────────────────────────────────────────────────")
    print(f"  Generated:        {len(generated)}")
    print(f"  Already done:     {len(already_done)}  (use --overwrite to regenerate)")
    print(f"  Skipped (status): {len(skipped_status)}")

    if missing_passage:
        print(f"\n  ✗ Missing passage files ({len(missing_passage)} batches):")
        print(f"    Add a .txt file to passages/ for each of these:\n")
        for b in missing_passage:
            print(f"      passages/{b}.txt")
    else:
        print(f"\n  All verified batches have passage files — nothing missing.")

    print()


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generate prompt files for all 4 generation models.")
    parser.add_argument("--batch", action="store_true",
                        help="Batch mode: read section_list.xlsx and process all verified batches")
    parser.add_argument("--overwrite", action="store_true",
                        help="Batch mode: regenerate prompts even if they already exist")
    parser.add_argument("--section",  help="Section ID for folder name, e.g. wg1_7.4.2.1")
    parser.add_argument("--category", help="Benchmark category name")
    parser.add_argument("--source",   help="Full source reference string")
    parser.add_argument("--passage",  help="Path to .txt file — prose passage (standard) or data table (data-interpretation)")
    parser.add_argument("--data-interpretation", action="store_true",
                        help="Use the data interpretation prompt template (Category 2 only)")
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))

    if args.batch:
        run_batch(script_dir, overwrite=args.overwrite)
        return

    # ── Single batch mode ──────────────────────────────────────────────────────
    data_interp = args.data_interpretation
    prompt_type = "data interpretation" if data_interp else "standard"

    print(f"\n── Climate Benchmark Prompt Generator [{prompt_type}] ──────────────\n")

    section  = args.section  or prompt_input("Section ID (e.g. wg1_7.4.2.1)")
    category = args.category or prompt_input("Category name")
    source   = args.source   or prompt_input("Source reference")

    if args.passage:
        content = read_file(args.passage)
    else:
        label = "Path to data context .txt file" if data_interp else "Path to passage .txt file"
        content = read_file(prompt_input(label))

    output_dir = os.path.join(script_dir, "prompts", "tests", section)

    print(f"\nWriting {prompt_type} prompt files to: prompts/tests/{section}/\n")

    for model_key, model_name in MODELS.items():
        path = write_prompt(output_dir, model_key, model_name, category, source, content, data_interp)
        print(f"  ✓ {model_key:12s}  →  {os.path.relpath(path, script_dir)}")

    print(f"\nDone. Open each prompt.md and paste into a fresh session.\n")


if __name__ == "__main__":
    main()
