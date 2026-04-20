#!/usr/bin/env python3
"""
evaluate.py
-----------
Runs each model against the curated benchmark and records per-question scores.

For every (question, evaluator_model) pair, the model is shown the question
and four options and asked to respond with a single letter. The predicted
answer is compared to the stored correct answer.

Setup:
    Same API keys as generate_responses.py — set in .env or environment.

Usage:
    python evaluate.py                          # evaluate all models
    python evaluate.py --models claude chatgpt  # specific models only
    python evaluate.py --overwrite              # re-evaluate existing results
    python evaluate.py --dry-run                # preview without API calls

Output:
    eval/results.csv     — one row per (question, model) pair
    eval/summary.json    — aggregated accuracy stats
"""

import argparse
import csv
import json
import os
import re
import sys
import time

# ── Load .env ─────────────────────────────────────────────────────────────────

_env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
if os.path.exists(_env_path):
    with open(_env_path) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _v = _line.split("=", 1)
                os.environ.setdefault(_k.strip(), _v.strip())

# ── Config ────────────────────────────────────────────────────────────────────

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
GEMINI_API_KEY    = os.environ.get("GEMINI_API_KEY",    "")
GROQ_API_KEY      = os.environ.get("GROQ_API_KEY",      "")
OPENAI_API_KEY    = os.environ.get("OPENAI_API_KEY",    "")

CLAUDE_MODEL  = "claude-sonnet-4-6"
GEMINI_MODEL  = "gemini-2.5-flash"
GROQ_MODEL    = "llama-3.3-70b-versatile"
OPENAI_MODEL  = "gpt-4o-2024-11-20"

CLAUDE_DELAY  = 1.0
GEMINI_DELAY  = 13.0
GROQ_DELAY    = 3.0
OPENAI_DELAY  = 1.0

CSV_COLUMNS = [
    "question_id", "evaluator", "evaluator_model",
    "predicted", "correct_answer", "is_correct",
    "difficulty", "category", "prompt_type",
    "generator_model", "wg", "data_source_section",
]

# Maps generator model ID → short key (for self-advantage analysis)
GENERATOR_KEY = {
    "claude-sonnet-4-6":       "claude",
    "gpt-4o-2024-11-20":       "chatgpt",
    "gemini-2.5-flash":        "gemini",
    "llama-3.3-70b-versatile": "groq",
}

# ── Prompt builder ────────────────────────────────────────────────────────────

def build_prompt(q):
    """
    Construct a minimal, unambiguous evaluation prompt.
    Includes the data scenario for Cat2 questions.
    Does NOT include the explanation or source — the model must answer cold.
    """
    lines = [
        "Answer the following multiple-choice climate science question.",
        "Respond with ONLY a single letter: A, B, C, or D. No explanation.",
        "",
    ]

    if q.get("scenario"):
        lines += [q["scenario"], ""]

    lines.append(f"Question: {q['question']}")
    lines.append("")
    for letter in ["A", "B", "C", "D"]:
        lines.append(f"{letter}. {q['options'][letter]}")
    lines += ["", "Your answer (A, B, C, or D):"]

    return "\n".join(lines)


# ── Response parser ───────────────────────────────────────────────────────────

def parse_answer(text):
    """
    Extract a single answer letter from model output.
    Handles: bare 'B', 'Answer: B', 'The answer is B', 'B.', '(B)', etc.
    Returns '?' if no valid letter found.
    """
    if not text:
        return "?"
    text = text.strip()

    # Direct single-char response
    if text.upper() in ("A", "B", "C", "D"):
        return text.upper()

    # Common patterns: "Answer: B", "The answer is B", "**B**", "(B)", "B."
    match = re.search(
        r"\b(?:answer(?:\s+is)?|option|choice)?\s*[:\-]?\s*\**\(?([ABCD])\)?\.?\**",
        text, re.IGNORECASE
    )
    if match:
        return match.group(1).upper()

    # Fallback: first standalone letter A-D in the text
    match = re.search(r"\b([ABCD])\b", text)
    if match:
        return match.group(1).upper()

    return "?"


# ── API callers (identical to generate_responses.py) ─────────────────────────

def call_claude(prompt, api_key):
    import anthropic
    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=16,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def call_gemini(prompt, api_key):
    from google import genai
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
    return response.text


def call_groq(prompt, api_key):
    from groq import Groq
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=16,
        temperature=0.0,
    )
    return response.choices[0].message.content


def call_openai(prompt, api_key):
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=16,
        temperature=0.0,
    )
    return response.choices[0].message.content


# ── Model config ──────────────────────────────────────────────────────────────

MODEL_CONFIG = {
    "claude": {
        "caller":    call_claude,
        "key_var":   "ANTHROPIC_API_KEY",
        "key_val":   ANTHROPIC_API_KEY,
        "delay":     CLAUDE_DELAY,
        "model_id":  CLAUDE_MODEL,
    },
    "gemini": {
        "caller":    call_gemini,
        "key_var":   "GEMINI_API_KEY",
        "key_val":   GEMINI_API_KEY,
        "delay":     GEMINI_DELAY,
        "model_id":  GEMINI_MODEL,
    },
    "groq": {
        "caller":    call_groq,
        "key_var":   "GROQ_API_KEY",
        "key_val":   GROQ_API_KEY,
        "delay":     GROQ_DELAY,
        "model_id":  GROQ_MODEL,
    },
    "chatgpt": {
        "caller":    call_openai,
        "key_var":   "OPENAI_API_KEY",
        "key_val":   OPENAI_API_KEY,
        "delay":     OPENAI_DELAY,
        "model_id":  OPENAI_MODEL,
    },
}


# ── I/O helpers ───────────────────────────────────────────────────────────────

def load_benchmark():
    path = os.path.join(SCRIPT_DIR, "benchmark.json")
    if not os.path.exists(path):
        print("Error: benchmark.json not found. Run collate.py first.")
        sys.exit(1)
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data["questions"]


def load_existing_results(csv_path):
    """Return set of (question_id, evaluator) pairs already evaluated."""
    done = set()
    if not os.path.exists(csv_path):
        return done
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            done.add((row["question_id"], row["evaluator"]))
    return done


def append_result(csv_path, row, write_header):
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        if write_header:
            writer.writeheader()
        writer.writerow(row)


def save_summary(csv_path, summary_path):
    """Read results CSV and write aggregated summary JSON."""
    import pandas as pd
    if not os.path.exists(csv_path):
        return

    df = pd.read_csv(csv_path)
    df["is_correct"] = df["is_correct"].astype(bool)

    summary = {
        "total_evaluations": len(df),
        "overall_accuracy":  round(df["is_correct"].mean(), 4),
        "by_evaluator":      {},
        "by_difficulty":     {},
        "by_prompt_type":    {},
        "self_vs_cross":     {},
    }

    # Per evaluator
    for model, grp in df.groupby("evaluator"):
        summary["by_evaluator"][model] = {
            "accuracy":    round(grp["is_correct"].mean(), 4),
            "correct":     int(grp["is_correct"].sum()),
            "total":       len(grp),
            "by_difficulty": {
                d: {
                    "accuracy": round(sub["is_correct"].mean(), 4),
                    "correct":  int(sub["is_correct"].sum()),
                    "total":    len(sub),
                }
                for d, sub in grp.groupby("difficulty")
                if d in ("easy", "medium", "hard")
            },
        }

    # By difficulty (across all models)
    for diff, grp in df[df["difficulty"].isin(["easy","medium","hard"])].groupby("difficulty"):
        summary["by_difficulty"][diff] = {
            "accuracy": round(grp["is_correct"].mean(), 4),
            "correct":  int(grp["is_correct"].sum()),
            "total":    len(grp),
        }

    # By prompt type
    for pt, grp in df.groupby("prompt_type"):
        summary["by_prompt_type"][pt] = {
            "accuracy": round(grp["is_correct"].mean(), 4),
            "correct":  int(grp["is_correct"].sum()),
            "total":    len(grp),
        }

    # Self vs cross-model accuracy
    # "self" = evaluator generated the question; "cross" = different model generated it
    evaluator_to_gen = {
        "claude":  "claude-sonnet-4-6",
        "chatgpt": "gpt-4o-2024-11-20",
        "gemini":  "gemini-2.5-flash",
        "groq":    "llama-3.3-70b-versatile",
    }
    for model, grp in df.groupby("evaluator"):
        gen_id = evaluator_to_gen.get(model, "")
        self_q = grp[grp["generator_model"] == gen_id]
        cross_q = grp[grp["generator_model"] != gen_id]
        summary["self_vs_cross"][model] = {
            "self_accuracy":  round(self_q["is_correct"].mean(), 4) if len(self_q) else None,
            "self_total":     len(self_q),
            "cross_accuracy": round(cross_q["is_correct"].mean(), 4) if len(cross_q) else None,
            "cross_total":    len(cross_q),
        }

    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"\n  Summary written to eval/summary.json")
    print(f"\n── Accuracy by model ───────────────────────────────────────────")
    for model, stats in sorted(summary["by_evaluator"].items(),
                                key=lambda x: -x[1]["accuracy"]):
        acc = stats["accuracy"] * 100
        cor = stats["correct"]
        tot = stats["total"]
        print(f"  {model:<10}  {cor:>3}/{tot}  ({acc:.1f}%)")

    print(f"\n── Self vs cross-model accuracy ─────────────────────────────────")
    for model, stats in summary["self_vs_cross"].items():
        s = stats["self_accuracy"]
        c = stats["cross_accuracy"]
        s_str = f"{s*100:.1f}% ({stats['self_total']} q)" if s is not None else "n/a"
        c_str = f"{c*100:.1f}% ({stats['cross_total']} q)" if c is not None else "n/a"
        print(f"  {model:<10}  self: {s_str:<20}  cross: {c_str}")


# ── Core runner ───────────────────────────────────────────────────────────────

def run(models, overwrite=False, dry_run=False):
    eval_dir     = os.path.join(SCRIPT_DIR, "eval")
    os.makedirs(eval_dir, exist_ok=True)
    csv_path     = os.path.join(eval_dir, "results.csv")
    summary_path = os.path.join(eval_dir, "summary.json")

    questions = load_benchmark()
    existing  = set() if overwrite else load_existing_results(csv_path)

    # Validate API keys
    keys = {}
    for model in models:
        cfg = MODEL_CONFIG[model]
        if not cfg["key_val"] and not dry_run:
            print(f"Error: {cfg['key_var']} is not set.")
            sys.exit(1)
        keys[model] = cfg["key_val"]

    total_pairs = len(questions) * len(models)
    skipped     = sum(1 for q in questions for m in models
                      if (q["id"], m) in existing)

    print(f"\n── ClimateQA Evaluator ─────────────────────────────────────────")
    print(f"  Questions:  {len(questions)}")
    print(f"  Models:     {', '.join(models)}")
    print(f"  Pairs:      {total_pairs}  ({skipped} already done)")
    print(f"  Mode:       {'DRY RUN' if dry_run else 'LIVE'}\n")

    counts = {"correct": 0, "wrong": 0, "unparsed": 0, "skipped": 0, "error": 0}
    first_write = not os.path.exists(csv_path) or overwrite

    if overwrite and os.path.exists(csv_path):
        os.remove(csv_path)
        first_write = True

    for q in questions:
        qid    = q["id"]
        correct = q["correct_answer"]
        wg     = qid.split("_")[0]  # e.g. wg1
        ptype  = "data_interpretation" if "scenario" in q else "standard"

        for model in models:
            pair = (qid, model)
            if pair in existing:
                counts["skipped"] += 1
                continue

            cfg   = MODEL_CONFIG[model]
            label = f"{qid[:35]:<35} / {model}"

            if dry_run:
                print(f"  ~ {label}  [would evaluate]")
                counts["correct"] += 1
                continue

            prompt = build_prompt(q)

            try:
                print(f"  ↑ {label}  sending...", end="", flush=True)
                raw = None
                for attempt in range(3):
                    try:
                        raw = cfg["caller"](prompt, keys[model])
                        break
                    except Exception as e:
                        if attempt < 2 and ("429" in str(e) or "rate" in str(e).lower()):
                            wait = 30 * (attempt + 1)
                            print(f"\r  ⏳ rate limited, waiting {wait}s...",
                                  end="", flush=True)
                            time.sleep(wait)
                        else:
                            raise

                predicted  = parse_answer(raw)
                is_correct = (predicted == correct)

                row = {
                    "question_id":      qid,
                    "evaluator":        model,
                    "evaluator_model":  cfg["model_id"],
                    "predicted":        predicted,
                    "correct_answer":   correct,
                    "is_correct":       is_correct,
                    "difficulty":       q.get("difficulty", ""),
                    "category":         q.get("category", ""),
                    "prompt_type":      ptype,
                    "generator_model":  q.get("generated_by", ""),
                    "wg":               wg,
                    "data_source_section": q.get("data_source_section", ""),
                }

                write_header = first_write and counts["correct"] + counts["wrong"] + counts["unparsed"] == 0
                append_result(csv_path, row, write_header=write_header)

                status = "✓" if is_correct else ("?" if predicted == "?" else "✗")
                detail = f"predicted={predicted}  correct={correct}"
                print(f"\r  {status} {label}  {detail}")

                if predicted == "?":
                    counts["unparsed"] += 1
                elif is_correct:
                    counts["correct"] += 1
                else:
                    counts["wrong"] += 1

            except Exception as e:
                print(f"\r  ✗ {label}  ERROR: {e}")
                counts["error"] += 1

            time.sleep(cfg["delay"])

    print(f"\n── Summary ─────────────────────────────────────────────────────")
    evaluated = counts["correct"] + counts["wrong"] + counts["unparsed"]
    if evaluated:
        acc = counts["correct"] / evaluated * 100
        print(f"  Evaluated:  {evaluated}")
        print(f"  Correct:    {counts['correct']}  ({acc:.1f}%)")
        print(f"  Wrong:      {counts['wrong']}")
        print(f"  Unparsed:   {counts['unparsed']}")
    print(f"  Skipped:    {counts['skipped']}")
    print(f"  Errors:     {counts['error']}")

    if not dry_run and os.path.exists(csv_path):
        save_summary(csv_path, summary_path)

    print()


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Evaluate models against the ClimateQA benchmark."
    )
    parser.add_argument(
        "--models", nargs="+", choices=list(MODEL_CONFIG.keys()),
        default=list(MODEL_CONFIG.keys()),
        help="Which models to evaluate (default: all)"
    )
    parser.add_argument(
        "--overwrite", action="store_true",
        help="Re-evaluate pairs that already have results"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Show what would be evaluated without calling any APIs"
    )
    args = parser.parse_args()
    run(args.models, overwrite=args.overwrite, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
