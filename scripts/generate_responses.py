#!/usr/bin/env python3
"""
generate_responses.py
---------------------
Sends generated prompts to model APIs and saves responses to response.json.
Supports Claude (Anthropic), Gemini, Groq (Llama 3.3 70B), and OpenAI (ChatGPT).

Setup:
    pip install anthropic google-genai groq openai

API keys — set as environment variables or fill in the CONFIG section below:
    export ANTHROPIC_API_KEY="your-key-here"  # console.anthropic.com
    export GEMINI_API_KEY="your-key-here"     # aistudio.google.com (free)
    export GROQ_API_KEY="your-key-here"       # console.groq.com (free)
    export OPENAI_API_KEY="your-key-here"     # platform.openai.com

Usage:
    # Run all supported models
    python generate_responses.py

    # Run a specific model only
    python generate_responses.py --models claude
    python generate_responses.py --models gemini
    python generate_responses.py --models groq
    python generate_responses.py --models gemini groq

    # Overwrite existing responses
    python generate_responses.py --overwrite

    # Dry run — show what would be sent without calling APIs
    python generate_responses.py --dry-run
"""

import argparse
import json
import os
import re
import sys
import time

# ── Load .env if present ──────────────────────────────────────────────────────
_env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
if os.path.exists(_env_path):
    with open(_env_path) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _v = _line.split("=", 1)
                os.environ.setdefault(_k.strip(), _v.strip())

# ── CONFIG ────────────────────────────────────────────────────────────────────
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
GEMINI_API_KEY    = os.environ.get("GEMINI_API_KEY",    "")
GROQ_API_KEY      = os.environ.get("GROQ_API_KEY",      "")
OPENAI_API_KEY    = os.environ.get("OPENAI_API_KEY",    "")

CLAUDE_MODEL = "claude-sonnet-4-6"        # pinned for reproducibility
GEMINI_MODEL = "gemini-2.5-flash"        # free tier via aistudio.google.com
GROQ_MODEL   = "llama-3.3-70b-versatile" # free via console.groq.com
OPENAI_MODEL = "gpt-4o-2024-11-20"       # pinned snapshot for reproducibility

# Delay between API calls (seconds)
# Anthropic: generous rate limits — 1s is safe
# Gemini free tier: 5 RPM for gemini-2.5-flash — 13s keeps safely under
# Groq free tier: 30 RPM — 3s delay is safe
# OpenAI: well within rate limits at 1s
CLAUDE_DELAY  = 1.0
GEMINI_DELAY  = 13.0
GROQ_DELAY    = 3.0
OPENAI_DELAY  = 1.0

# ── Prompt cleaning ───────────────────────────────────────────────────────────

def clean_prompt(text):
    """
    Strip the human-facing header and usage notes from a prompt.md file.
    The actual prompt content sits between the first and last --- separators.
    """
    parts = text.split("\n---\n")
    if len(parts) >= 3:
        return "\n---\n".join(parts[1:-1]).strip()
    elif len(parts) == 2:
        return parts[1].strip()
    return text.strip()


# ── JSON extraction ───────────────────────────────────────────────────────────

def extract_json(text):
    """
    Extract a JSON array from model output.
    Models often wrap output in markdown code fences — this strips them.
    Returns parsed list or raises ValueError.
    """
    text = text.strip()

    # Try direct parse first
    try:
        result = json.loads(text)
        if isinstance(result, list):
            return result
    except json.JSONDecodeError:
        pass

    # Look for ```json ... ``` or ``` ... ``` block
    match = re.search(r"```(?:json)?\s*(\[.*?\])\s*```", text, re.DOTALL)
    if match:
        try:
            result = json.loads(match.group(1))
            if isinstance(result, list):
                return result
        except json.JSONDecodeError:
            pass

    # Look for bare [...] array anywhere in the text
    match = re.search(r"(\[.*\])", text, re.DOTALL)
    if match:
        try:
            result = json.loads(match.group(1))
            if isinstance(result, list):
                return result
        except json.JSONDecodeError:
            pass

    raise ValueError("Could not extract a JSON array from model response")


# ── API callers ───────────────────────────────────────────────────────────────

def call_claude(prompt, api_key):
    import anthropic
    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def call_gemini(prompt, api_key):
    from google import genai
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
    )
    return response.text


def call_groq(prompt, api_key):
    from groq import Groq
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return response.choices[0].message.content


def call_openai(prompt, api_key):
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return response.choices[0].message.content


# ── Core runner ───────────────────────────────────────────────────────────────

MODEL_CONFIG = {
    "claude": {
        "caller":   call_claude,
        "key_var":  "ANTHROPIC_API_KEY",
        "delay":    CLAUDE_DELAY,
        "model_id": CLAUDE_MODEL,
    },
    "gemini": {
        "caller":   call_gemini,
        "key_var":  "GEMINI_API_KEY",
        "delay":    GEMINI_DELAY,
        "model_id": GEMINI_MODEL,
    },
    "groq": {
        "caller":   call_groq,
        "key_var":  "GROQ_API_KEY",
        "delay":    GROQ_DELAY,
        "model_id": GROQ_MODEL,
    },
    "chatgpt": {
        "caller":   call_openai,
        "key_var":  "OPENAI_API_KEY",
        "delay":    OPENAI_DELAY,
        "model_id": OPENAI_MODEL,
    },
}


def find_batches(script_dir, models):
    """Return list of (batch_folder, model, prompt_path, response_path) tuples."""
    tests_dir = os.path.join(script_dir, "prompts", "tests")
    batches = []
    if not os.path.exists(tests_dir):
        return batches
    for batch in sorted(os.listdir(tests_dir)):
        batch_path = os.path.join(tests_dir, batch)
        if not os.path.isdir(batch_path):
            continue
        for model in models:
            model_path = os.path.join(batch_path, model)
            prompt_path = os.path.join(model_path, "prompt.md")
            response_path = os.path.join(model_path, "response.json")
            if os.path.exists(prompt_path):
                batches.append((batch, model, prompt_path, response_path))
    return batches


def response_is_empty(path):
    if not os.path.exists(path):
        return True
    content = open(path).read().strip()
    return content == "" or content == "[]" or content == "{}"


def run(models, overwrite=False, dry_run=False):
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Validate API keys
    keys = {}
    for model in models:
        cfg = MODEL_CONFIG[model]
        key = os.environ.get(cfg["key_var"]) or globals().get(cfg["key_var"].replace("_API_KEY", "_API_KEY"), "")
        # Re-read from globals correctly
        key_value = globals()[cfg["key_var"]]
        if not key_value and not dry_run:
            print(f"Error: {cfg['key_var']} is not set. "
                  f"Export it as an environment variable or fill it in the CONFIG section.")
            sys.exit(1)
        keys[model] = key_value

    batches = find_batches(script_dir, models)
    if not batches:
        print("No prompt files found. Run generate_prompts.py --batch first.")
        return

    print(f"\n── Climate Benchmark Response Generator ────────────────────────")
    print(f"  Models:   {', '.join(models)}")
    print(f"  Batches:  {len(batches)} prompt files found")
    print(f"  Mode:     {'DRY RUN' if dry_run else 'LIVE'}\n")

    counts = {"generated": 0, "skipped": 0, "error": 0}

    for batch, model, prompt_path, response_path in batches:
        label = f"{batch}/{model}"

        if not overwrite and not response_is_empty(response_path):
            print(f"  ○ {label:<40}  skipped (response exists)")
            counts["skipped"] += 1
            continue

        if dry_run:
            print(f"  ~ {label:<40}  would send to {model} API")
            counts["generated"] += 1
            continue

        prompt = clean_prompt(open(prompt_path, "r", encoding="utf-8").read())
        cfg = MODEL_CONFIG[model]

        try:
            print(f"  ↑ {label:<40}  sending...", end="", flush=True)
            raw = None
            # Retry up to 3 times on rate limit errors
            for attempt in range(3):
                try:
                    raw = cfg["caller"](prompt, keys[model])
                    break
                except Exception as e:
                    if attempt < 2 and ("429" in str(e) or "rate" in str(e).lower()):
                        wait = 30 * (attempt + 1)
                        print(f"\r  ⏳ {label:<40}  rate limited, waiting {wait}s...", end="", flush=True)
                        time.sleep(wait)
                    else:
                        raise

            parsed = extract_json(raw)

            # Enforce exact model ID — overwrite whatever the model wrote
            for q in parsed:
                q["generated_by"] = cfg["model_id"]

            with open(response_path, "w", encoding="utf-8") as f:
                json.dump(parsed, f, indent=2, ensure_ascii=False)

            print(f"\r  ✓ {label:<40}  {len(parsed)} questions saved")
            counts["generated"] += 1

        except Exception as e:
            print(f"\r  ✗ {label:<40}  ERROR: {e}")
            raw_path = response_path.replace("response.json", "response_raw.txt")
            try:
                with open(raw_path, "w", encoding="utf-8") as f:
                    f.write(raw if raw else str(e))
            except Exception:
                pass
            counts["error"] += 1

        time.sleep(cfg["delay"])

    print(f"\n── Summary ─────────────────────────────────────────────────────")
    print(f"  Generated: {counts['generated']}")
    print(f"  Skipped:   {counts['skipped']}")
    print(f"  Errors:    {counts['error']}")
    if counts["error"]:
        print(f"\n  Check response_raw.txt files alongside any failed response.json for raw output.")
    print()


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Send prompts to model APIs and save responses.")
    parser.add_argument("--models", nargs="+", choices=list(MODEL_CONFIG.keys()),
                        default=list(MODEL_CONFIG.keys()),
                        help="Which models to run (default: all configured)")
    parser.add_argument("--overwrite", action="store_true",
                        help="Overwrite existing response.json files")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be sent without calling any APIs")
    args = parser.parse_args()
    run(args.models, overwrite=args.overwrite, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
