#!/usr/bin/env python3
"""
build_review.py
---------------
Flattens all generated response.json files into a single review/questions.csv,
one row per question, ready for manual curation in Excel or any CSV editor.

Usage:
    python build_review.py            # create/update review/questions.csv
    python build_review.py --overwrite  # reset all status/notes to defaults

Columns in output CSV:
    id            — unique stable ID: {folder}_{model}_q{n}  e.g. wg1_2.3.1.1.3_chatgpt_q1
    batch_id      — e.g. cat2_batch1
    folder        — e.g. wg1_2.3.1.1.3
    model         — claude | chatgpt | gemini | groq
    prompt_type   — standard | data_interpretation
    category      — benchmark category
    source        — IPCC source reference
    difficulty    — easy | medium | hard
    scenario_type — trend_identification etc. (Cat2 only, else blank)
    scenario      — embedded data scenario text (Cat2 only, else blank)
    question      — question text
    option_A      — answer option A
    option_B      — answer option B
    option_C      — answer option C
    option_D      — answer option D
    correct_answer — A | B | C | D
    explanation   — one-sentence explanation
    generated_by  — exact model ID string
    passage       — full passage/data context from passages/{batch_id}.txt
    status        — pending | accept | reject  (preserved on re-run)
    notes         — reviewer notes            (preserved on re-run)
"""

import argparse
import csv
import json
import os
import sys


MODELS = ["claude", "chatgpt", "gemini", "groq"]

CSV_COLUMNS = [
    "id", "batch_id", "folder", "model", "prompt_type",
    "category", "source", "difficulty",
    "scenario_type", "scenario",
    "question", "option_A", "option_B", "option_C", "option_D",
    "correct_answer", "explanation", "generated_by",
    "passage", "status", "notes",
]


# ── Helpers ───────────────────────────────────────────────────────────────────

def section_to_folder(wg, section):
    """Matches the logic in generate_prompts.py."""
    wg_prefix = wg.lower()
    section_safe = str(section).replace(" ", "_").replace("/", "_")
    return f"{wg_prefix}_{section_safe}"


def load_xlsx_index(script_dir):
    """
    Returns two dicts:
      folder_to_meta[folder] = {batch_id, category, source_ref, prompt_type}
      batch_to_passage[batch_id] = passage_text (or '' if file missing)
    """
    try:
        import openpyxl
    except ImportError:
        print("Error: openpyxl is required. Run: pip install openpyxl")
        sys.exit(1)

    xlsx_path = os.path.join(script_dir, "section_list.xlsx")
    if not os.path.exists(xlsx_path):
        print(f"Error: section_list.xlsx not found at {xlsx_path}")
        sys.exit(1)

    wb = openpyxl.load_workbook(xlsx_path)
    ws = wb["Section List"]
    rows = list(ws.iter_rows(values_only=True))
    header = rows[0]
    col = {name: i for i, name in enumerate(header)}

    folder_to_meta = {}
    batch_to_passage = {}
    passages_dir = os.path.join(script_dir, "passages")

    for row in rows[1:]:
        batch_id = row[col["batch_id"]]
        if not batch_id:
            continue
        wg          = row[col["wg"]]
        section     = str(row[col["section"]])
        source_ref  = row[col["source_ref"]]
        category    = row[col["category"]]
        prompt_type = row[col["prompt_type"]]

        folder = section_to_folder(wg, section)
        folder_to_meta[folder] = {
            "batch_id":    batch_id,
            "category":    category,
            "source_ref":  source_ref,
            "prompt_type": prompt_type,
        }

        passage_path = os.path.join(passages_dir, f"{batch_id}.txt")
        if os.path.exists(passage_path):
            batch_to_passage[batch_id] = open(passage_path, encoding="utf-8").read().strip()
        else:
            batch_to_passage[batch_id] = ""

    return folder_to_meta, batch_to_passage


def load_existing_statuses(csv_path):
    """
    Returns dict: {id: (status, notes)} from an existing CSV.
    Used to preserve reviewer work on re-runs.
    """
    statuses = {}
    if not os.path.exists(csv_path):
        return statuses
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            qid = row.get("id", "")
            if qid:
                statuses[qid] = (row.get("status", "pending"), row.get("notes", ""))
    return statuses


def extract_question_rows(folder, model, meta, passage, questions):
    """
    Convert a list of question dicts from response.json into CSV row dicts.
    Handles both standard (no 'scenario') and Cat2 (has 'scenario') schemas.
    """
    rows = []
    batch_id    = meta["batch_id"]
    prompt_type = meta["prompt_type"]
    source_ref  = meta.get("source_ref", "")

    for i, q in enumerate(questions, start=1):
        qid = f"{folder}_{model}_q{i}"

        # Source field differs between standard and Cat2
        source = q.get("source") or q.get("data_source") or source_ref

        options = q.get("options", {})

        row = {
            "id":            qid,
            "batch_id":      batch_id,
            "folder":        folder,
            "model":         model,
            "prompt_type":   prompt_type,
            "category":      q.get("category", meta.get("category", "")),
            "source":        source,
            "difficulty":    q.get("difficulty", ""),
            "scenario_type": q.get("scenario_type", ""),
            "scenario":      q.get("scenario", ""),
            "question":      q.get("question", ""),
            "option_A":      options.get("A", ""),
            "option_B":      options.get("B", ""),
            "option_C":      options.get("C", ""),
            "option_D":      options.get("D", ""),
            "correct_answer": q.get("correct_answer", ""),
            "explanation":   q.get("explanation", ""),
            "generated_by":  q.get("generated_by", ""),
            "passage":       passage,
            "status":        "pending",
            "notes":         "",
        }
        rows.append(row)
    return rows


# ── Core ──────────────────────────────────────────────────────────────────────

def build(script_dir, overwrite=False):
    folder_to_meta, batch_to_passage = load_xlsx_index(script_dir)

    tests_dir = os.path.join(script_dir, "prompts", "tests")
    review_dir = os.path.join(script_dir, "review")
    os.makedirs(review_dir, exist_ok=True)
    csv_path = os.path.join(review_dir, "questions.csv")

    # Load existing statuses so we can preserve reviewer work
    existing = {} if overwrite else load_existing_statuses(csv_path)

    all_rows = []
    stats = {"loaded": 0, "missing": 0, "empty": 0, "preserved": 0}

    folders = sorted(os.listdir(tests_dir)) if os.path.exists(tests_dir) else []

    for folder in folders:
        folder_path = os.path.join(tests_dir, folder)
        if not os.path.isdir(folder_path):
            continue

        meta = folder_to_meta.get(folder)
        if not meta:
            print(f"  ⚠  {folder:<30}  not found in section_list.xlsx — skipping")
            continue

        batch_id = meta["batch_id"]
        passage  = batch_to_passage.get(batch_id, "")

        for model in MODELS:
            response_path = os.path.join(folder_path, model, "response.json")
            if not os.path.exists(response_path):
                stats["missing"] += 1
                continue

            content = open(response_path, encoding="utf-8").read().strip()
            if not content or content in ("[]", "{}"):
                stats["empty"] += 1
                continue

            try:
                questions = json.loads(content)
            except json.JSONDecodeError as e:
                print(f"  ✗ {folder}/{model}: JSON parse error — {e}")
                stats["empty"] += 1
                continue

            rows = extract_question_rows(folder, model, meta, passage, questions)

            for row in rows:
                qid = row["id"]
                if qid in existing:
                    row["status"] = existing[qid][0]
                    row["notes"]  = existing[qid][1]
                    stats["preserved"] += 1

            all_rows.extend(rows)
            stats["loaded"] += len(rows)

    # Write CSV
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"\n── Build Review CSV ────────────────────────────────────────────")
    print(f"  Questions loaded:    {stats['loaded']}")
    print(f"  Missing responses:   {stats['missing']}  (response.json not yet generated)")
    print(f"  Empty/invalid:       {stats['empty']}")
    print(f"  Statuses preserved:  {stats['preserved']}  (from previous review pass)")
    print(f"\n  Output: review/questions.csv  ({len(all_rows)} rows)\n")

    if stats["missing"]:
        print(f"  Tip: run `python generate_responses.py` to fill missing responses,")
        print(f"       then re-run build_review.py to pick them up.\n")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Flatten all response.json files into review/questions.csv."
    )
    parser.add_argument(
        "--overwrite", action="store_true",
        help="Reset all status/notes to defaults (discard any prior review work)"
    )
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    build(script_dir, overwrite=args.overwrite)


if __name__ == "__main__":
    main()
