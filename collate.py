#!/usr/bin/env python3
"""
collate.py
----------
Reads review/questions.csv (curated by reviewer), filters accepted questions,
and writes benchmark.json — the final benchmark file.

Usage:
    python collate.py                      # write benchmark.json
    python collate.py --out custom.json    # write to a custom path
    python collate.py --stats-only         # print stats without writing output

Output format (benchmark.json):
    A JSON object with two top-level keys:
      "metadata"  — summary stats about the benchmark
      "questions" — list of accepted question objects

Each question object contains the curated fields from the CSV, with prompt_type,
batch_id, folder, model, passage, status, and notes stripped out (those are
internal review fields). The final schema is:

  Standard questions:
    id, category, source, difficulty, question, options {A,B,C,D},
    correct_answer, explanation, generated_by

  Cat2 (data interpretation) questions, additionally:
    scenario, scenario_type

  All questions also include:
    data_source_section  — the IPCC source reference
"""

import argparse
import csv
import json
import os
import sys
from collections import Counter


# Fields to strip from the public benchmark output (internal review metadata)
_INTERNAL_FIELDS = {
    "batch_id", "folder", "model", "prompt_type",
    "passage", "status", "notes",
}

# The 'source' column in the CSV maps to 'data_source_section' in the output
# to avoid collision with the original source passage
_SOURCE_RENAME = "data_source_section"


# ── Helpers ───────────────────────────────────────────────────────────────────

def csv_row_to_question(row):
    """Convert a CSV row dict to a clean question object for benchmark.json."""
    q = {}

    q["id"] = row["id"]
    q["category"] = row["category"]
    q[_SOURCE_RENAME] = row["source"]
    q["difficulty"] = row["difficulty"]

    # Cat2 fields (only include if non-empty)
    if row.get("scenario_type"):
        q["scenario_type"] = row["scenario_type"]
    if row.get("scenario"):
        q["scenario"] = row["scenario"]

    q["question"] = row["question"]
    q["options"] = {
        "A": row["option_A"],
        "B": row["option_B"],
        "C": row["option_C"],
        "D": row["option_D"],
    }
    q["correct_answer"] = row["correct_answer"]
    q["explanation"] = row["explanation"]
    q["generated_by"] = row["generated_by"]

    return q


def compute_metadata(questions, total_reviewed, total_pending, total_rejected):
    """Build the metadata block for benchmark.json."""
    by_category  = Counter(q["category"]  for q in questions)
    by_difficulty = Counter(q["difficulty"] for q in questions)
    by_model     = Counter(q["generated_by"] for q in questions)
    by_source    = Counter(q[_SOURCE_RENAME] for q in questions)

    # Cat2 detection
    cat2_count = sum(1 for q in questions if "scenario_type" in q)
    std_count  = len(questions) - cat2_count

    return {
        "total_questions":    len(questions),
        "standard_questions": std_count,
        "data_interp_questions": cat2_count,
        "total_reviewed":     total_reviewed,
        "total_accepted":     len(questions),
        "total_rejected":     total_rejected,
        "total_pending":      total_pending,
        "acceptance_rate":    round(len(questions) / total_reviewed, 3) if total_reviewed else None,
        "by_category":        dict(sorted(by_category.items())),
        "by_difficulty":      dict(by_difficulty),
        "by_model":           dict(sorted(by_model.items())),
        "by_source_section":  dict(sorted(by_source.items())),
    }


# ── Core ──────────────────────────────────────────────────────────────────────

def collate(script_dir, output_path, stats_only=False):
    csv_path = os.path.join(script_dir, "review", "questions.csv")
    if not os.path.exists(csv_path):
        print("Error: review/questions.csv not found. Run build_review.py first.")
        sys.exit(1)

    with open(csv_path, newline="", encoding="utf-8") as f:
        all_rows = list(csv.DictReader(f))

    accepted  = [r for r in all_rows if r["status"].strip().lower() == "accept"]
    rejected  = [r for r in all_rows if r["status"].strip().lower() == "reject"]
    pending   = [r for r in all_rows if r["status"].strip().lower() not in ("accept", "reject")]

    questions = [csv_row_to_question(r) for r in accepted]

    metadata = compute_metadata(
        questions,
        total_reviewed=len(accepted) + len(rejected),
        total_pending=len(pending),
        total_rejected=len(rejected),
    )

    print(f"\n── Collate Benchmark ───────────────────────────────────────────")
    print(f"  Total rows in CSV:  {len(all_rows)}")
    print(f"  Accepted:           {len(accepted)}")
    print(f"  Rejected:           {len(rejected)}")
    print(f"  Pending (unset):    {len(pending)}")
    if len(accepted) + len(rejected) > 0:
        rate = metadata["acceptance_rate"]
        print(f"  Acceptance rate:    {rate:.0%}  (of reviewed)")

    if len(pending) > 0 and not stats_only:
        print(f"\n  ⚠  {len(pending)} questions still marked 'pending' — these are excluded.")
        print(f"     Run build_review.py, review in Excel, then re-run collate.py.\n")

    if not accepted:
        print("\n  No accepted questions found — benchmark.json not written.\n")
        return

    if stats_only:
        print(f"\n── By Category ─────────────────────────────────────────────────")
        for cat, n in metadata["by_category"].items():
            print(f"  {cat:<50} {n:>3}")
        print(f"\n── By Difficulty ───────────────────────────────────────────────")
        for diff, n in metadata["by_difficulty"].items():
            print(f"  {diff:<10} {n:>3}")
        print(f"\n── By Model ────────────────────────────────────────────────────")
        for model, n in metadata["by_model"].items():
            print(f"  {model:<40} {n:>3}")
        print()
        return

    output = {
        "metadata":  metadata,
        "questions": questions,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    rel = os.path.relpath(output_path, script_dir)
    print(f"\n  ✓ Written: {rel}  ({len(questions)} questions)\n")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Collate accepted questions from review/questions.csv into benchmark.json."
    )
    parser.add_argument(
        "--out", default=None,
        help="Output path for benchmark.json (default: benchmark.json in project root)"
    )
    parser.add_argument(
        "--stats-only", action="store_true",
        help="Print summary statistics without writing benchmark.json"
    )
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = args.out or os.path.join(script_dir, "benchmark.json")

    collate(script_dir, output_path, stats_only=args.stats_only)


if __name__ == "__main__":
    main()
