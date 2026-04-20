#!/usr/bin/env python3
"""
analyse.py
----------
Analyses the ClimateQA curation results and produces charts + a summary report.

Usage:
    python analyse.py

Outputs:
    analysis/report.txt               — text summary
    analysis/01_model_acceptance.png  — overall acceptance rate by model
    analysis/02_model_by_difficulty.png — acceptance rate per model × difficulty
    analysis/03_passage_quality.png   — accepted questions per batch (passage signal)
    analysis/04_difficulty_dist.png   — difficulty mix of accepted questions per model
    analysis/05_batch_heatmap.png     — batch × model acceptance heatmap
"""

import os
import sys
import textwrap
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.patches import Patch

# ── Config ────────────────────────────────────────────────────────────────────

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH   = os.path.join(SCRIPT_DIR, "review", "questions.csv")
XLSX_PATH  = os.path.join(SCRIPT_DIR, "section_list.xlsx")
OUT_DIR    = os.path.join(SCRIPT_DIR, "analysis")

MODELS = ["claude", "chatgpt", "gemini", "groq"]

MODEL_LABELS = {
    "claude":  "Claude\n(Sonnet 4.6)",
    "chatgpt": "ChatGPT\n(GPT-4o)",
    "gemini":  "Gemini\n(2.5 Flash)",
    "groq":    "Llama 3.3\n(70B via Groq)",
}
MODEL_COLORS = {
    "claude":  "#c96442",
    "chatgpt": "#19c37d",
    "gemini":  "#4285f4",
    "groq":    "#7c3aed",
}
DIFF_COLORS   = {"easy": "#2ecc71", "medium": "#f1c40f", "hard": "#e74c3c"}
WG_COLORS     = {"wg1": "#3498db", "wg2": "#e67e22", "wg3": "#27ae60"}
WG_LABELS     = {"wg1": "WG1 — Physical Science",
                 "wg2": "WG2 — Impacts & Adaptation",
                 "wg3": "WG3 — Mitigation"}

DIFFICULTIES  = ["easy", "medium", "hard"]
WEAK_BATCH_THRESHOLD = 5   # batches with ≤ this many accepted questions flagged as weak

# ── Helpers ───────────────────────────────────────────────────────────────────

def load_data():
    df = pd.read_csv(CSV_PATH)
    df["accepted"] = df["status"] == "accept"
    df["wg"] = df["folder"].str.extract(r"^(wg\d+)")
    df["difficulty"] = df["difficulty"].str.strip().str.lower()
    df["difficulty"] = df["difficulty"].where(df["difficulty"].isin(DIFFICULTIES), "unknown")
    return df


def load_batch_categories():
    """Return dict {batch_id: category} from section_list.xlsx."""
    try:
        import openpyxl
    except ImportError:
        return {}
    wb = openpyxl.load_workbook(XLSX_PATH)
    ws = wb["Section List"]
    rows = list(ws.iter_rows(values_only=True))
    header = {name: i for i, name in enumerate(rows[0])}
    return {
        row[header["batch_id"]]: row[header["category"]]
        for row in rows[1:]
        if row[header["batch_id"]]
    }


def save_fig(fig, name):
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: analysis/{name}")


def pct(n, d):
    return 100 * n / d if d else 0


# ── 1. Overall model acceptance ───────────────────────────────────────────────

def fig_model_acceptance(df):
    totals = df.groupby("model")["accepted"].agg(["sum", "count"]).reindex(MODELS)
    totals.columns = ["accepted", "total"]
    totals["rate"] = totals["accepted"] / totals["total"] * 100

    fig, ax = plt.subplots(figsize=(7, 4.5))
    bars = ax.bar(
        [MODEL_LABELS[m] for m in MODELS],
        totals["rate"],
        color=[MODEL_COLORS[m] for m in MODELS],
        width=0.55, zorder=3,
    )

    # Annotate with count + %
    for bar, m in zip(bars, MODELS):
        acc = int(totals.loc[m, "accepted"])
        tot = int(totals.loc[m, "total"])
        rate = totals.loc[m, "rate"]
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.8,
                f"{acc}/{tot}\n({rate:.0f}%)",
                ha="center", va="bottom", fontsize=9)

    ax.set_ylabel("Acceptance rate (%)")
    ax.set_title("Question acceptance rate by model", fontweight="bold", pad=12)
    ax.set_ylim(0, max(totals["rate"]) * 1.25)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter())
    ax.grid(axis="y", linestyle="--", alpha=0.4, zorder=0)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    return fig


# ── 2. Acceptance rate by model × difficulty ─────────────────────────────────

def fig_model_by_difficulty(df):
    diff_df = (
        df[df["difficulty"].isin(DIFFICULTIES)]
        .groupby(["model", "difficulty"])["accepted"]
        .agg(["sum", "count"])
        .reset_index()
    )
    diff_df["rate"] = diff_df["sum"] / diff_df["count"] * 100

    fig, ax = plt.subplots(figsize=(9, 5))
    n_models = len(MODELS)
    n_diff   = len(DIFFICULTIES)
    width    = 0.22
    x        = np.arange(n_diff)

    for i, model in enumerate(MODELS):
        sub = diff_df[diff_df["model"] == model].set_index("difficulty")
        rates = [sub.loc[d, "rate"] if d in sub.index else 0 for d in DIFFICULTIES]
        offset = (i - n_models / 2 + 0.5) * width
        bars = ax.bar(x + offset, rates, width,
                      label=model.capitalize(), color=MODEL_COLORS[model],
                      zorder=3, alpha=0.9)
        for bar, rate in zip(bars, rates):
            if rate > 3:
                ax.text(bar.get_x() + bar.get_width() / 2,
                        bar.get_height() + 0.5,
                        f"{rate:.0f}%",
                        ha="center", va="bottom", fontsize=7.5)

    ax.set_xticks(x)
    ax.set_xticklabels([d.capitalize() for d in DIFFICULTIES], fontsize=11)
    ax.set_ylabel("Acceptance rate (%)")
    ax.set_title("Acceptance rate by model and difficulty", fontweight="bold", pad=12)
    ax.set_ylim(0, 105)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter())
    ax.legend(title="Model", loc="upper right", fontsize=9)
    ax.grid(axis="y", linestyle="--", alpha=0.4, zorder=0)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    return fig


# ── 3. Passage quality (accepted per batch) ───────────────────────────────────

def fig_passage_quality(df):
    batch_counts = (
        df.groupby(["folder", "wg"])["accepted"]
        .sum()
        .reset_index()
        .sort_values("accepted")
    )

    # Max possible per batch = 4 models × 5 questions = 20
    MAX_PER_BATCH = 20
    batch_counts["rate"] = batch_counts["accepted"] / MAX_PER_BATCH * 100

    n = len(batch_counts)
    fig, ax = plt.subplots(figsize=(8, max(5, n * 0.32)))

    colors = [WG_COLORS.get(wg, "#aaa") for wg in batch_counts["wg"]]
    bars = ax.barh(batch_counts["folder"], batch_counts["accepted"],
                   color=colors, zorder=3, height=0.65)

    # Shade weak batches
    weak_threshold = WEAK_BATCH_THRESHOLD
    for bar, count in zip(bars, batch_counts["accepted"]):
        ax.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height() / 2,
                str(int(count)),
                va="center", ha="left", fontsize=8.5)
        if count <= weak_threshold:
            ax.axhspan(bar.get_y() - 0.4, bar.get_y() + bar.get_height() + 0.4,
                       color="#e74c3c", alpha=0.08, zorder=0)

    ax.axvline(weak_threshold, color="#e74c3c", linestyle="--",
               linewidth=1.2, alpha=0.7, label=f"Weak threshold (≤{weak_threshold})")
    ax.set_xlabel("Accepted questions (out of 20 possible)")
    ax.set_title("Accepted questions per source batch\n"
                 "(low counts suggest a weak passage)", fontweight="bold", pad=12)
    ax.set_xlim(0, MAX_PER_BATCH + 2)

    legend_patches = [Patch(color=WG_COLORS[wg], label=WG_LABELS[wg])
                      for wg in ["wg1", "wg2", "wg3"]]
    legend_patches.append(Patch(color="#e74c3c", alpha=0.3, label=f"Weak (≤{weak_threshold})"))
    ax.legend(handles=legend_patches, loc="lower right", fontsize=8.5)
    ax.grid(axis="x", linestyle="--", alpha=0.4, zorder=0)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    return fig


# ── 4. Difficulty distribution of accepted questions per model ────────────────

def fig_difficulty_dist(df):
    accepted = df[df["accepted"] & df["difficulty"].isin(DIFFICULTIES)]
    pivot = (
        accepted.groupby(["model", "difficulty"])
        .size()
        .unstack(fill_value=0)
        .reindex(MODELS)
        [DIFFICULTIES]
    )

    fig, ax = plt.subplots(figsize=(8, 4.5))
    x      = np.arange(len(MODELS))
    bottom = np.zeros(len(MODELS))

    for diff in DIFFICULTIES:
        vals = pivot[diff].values
        bars = ax.bar(x, vals, bottom=bottom, label=diff.capitalize(),
                      color=DIFF_COLORS[diff], width=0.55, zorder=3)
        for bar, val in zip(bars, vals):
            if val > 1:
                ax.text(bar.get_x() + bar.get_width() / 2,
                        bar.get_y() + bar.get_height() / 2,
                        str(val),
                        ha="center", va="center", fontsize=9,
                        color="white", fontweight="bold")
        bottom += vals

    ax.set_xticks(x)
    ax.set_xticklabels([MODEL_LABELS[m] for m in MODELS])
    ax.set_ylabel("Number of accepted questions")
    ax.set_title("Difficulty distribution of accepted questions by model",
                 fontweight="bold", pad=12)
    ax.legend(title="Difficulty", loc="upper right")
    ax.grid(axis="y", linestyle="--", alpha=0.4, zorder=0)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    return fig


# ── 5. Batch × model acceptance heatmap ──────────────────────────────────────

def fig_batch_heatmap(df):
    pivot = (
        df.groupby(["folder", "model"])["accepted"]
        .sum()
        .unstack(fill_value=0)
        .reindex(columns=MODELS)
    )
    # Sort batches by total accepted descending
    pivot = pivot.loc[pivot.sum(axis=1).sort_values(ascending=False).index]

    n_batches = len(pivot)
    fig, ax = plt.subplots(figsize=(6, max(6, n_batches * 0.38)))

    im = ax.imshow(pivot.values, aspect="auto", cmap="YlGn",
                   vmin=0, vmax=5)

    ax.set_xticks(range(len(MODELS)))
    ax.set_xticklabels([MODEL_LABELS[m] for m in MODELS], fontsize=9)
    ax.set_yticks(range(n_batches))
    ax.set_yticklabels(pivot.index, fontsize=8)

    # Annotate cells
    for i in range(n_batches):
        for j in range(len(MODELS)):
            val = pivot.values[i, j]
            ax.text(j, i, str(val), ha="center", va="center",
                    fontsize=9, color="black" if val < 4 else "white")

    plt.colorbar(im, ax=ax, label="Accepted questions (max 5)", shrink=0.5)
    ax.set_title("Accepted questions per batch × model\n(sorted by total accepted)",
                 fontweight="bold", pad=12)
    fig.tight_layout()
    return fig


# ── Text report ───────────────────────────────────────────────────────────────

def build_report(df, batch_categories):
    lines = []
    w = lines.append

    total      = len(df)
    n_accept   = df["accepted"].sum()
    n_reject   = (~df["accepted"]).sum()
    n_batches  = df["folder"].nunique()

    w("=" * 60)
    w("ClimateQA — Curation Analysis Report")
    w("=" * 60)
    w("")
    w("── Overview ─────────────────────────────────────────────────")
    w(f"  Total questions generated:  {total}")
    w(f"  Accepted:                   {n_accept}  ({pct(n_accept, total):.1f}%)")
    w(f"  Rejected:                   {n_reject}  ({pct(n_reject, total):.1f}%)")
    w(f"  Source batches:             {n_batches}")
    w(f"  Questions per accepted set: ~{n_accept / n_batches:.1f} per batch")
    w("")

    # ── Per-model ─────────────────────────────────────────────────────────────
    w("── Acceptance rate by model ─────────────────────────────────")
    model_stats = df.groupby("model")["accepted"].agg(["sum", "count"]).reindex(MODELS)
    for m in MODELS:
        acc = int(model_stats.loc[m, "sum"])
        tot = int(model_stats.loc[m, "count"])
        w(f"  {m:<10}  {acc:>3} / {tot}  ({pct(acc, tot):.1f}%)")
    w("")

    # ── By difficulty ─────────────────────────────────────────────────────────
    w("── Acceptance rate by difficulty ────────────────────────────")
    diff_stats = (
        df[df["difficulty"].isin(DIFFICULTIES)]
        .groupby("difficulty")["accepted"]
        .agg(["sum", "count"])
        .reindex(DIFFICULTIES)
    )
    for d in DIFFICULTIES:
        acc = int(diff_stats.loc[d, "sum"])
        tot = int(diff_stats.loc[d, "count"])
        w(f"  {d:<8}  {acc:>3} / {tot}  ({pct(acc, tot):.1f}%)")
    w("")

    # ── By model × difficulty ─────────────────────────────────────────────────
    w("── Acceptance rate by model × difficulty ────────────────────")
    md = (
        df[df["difficulty"].isin(DIFFICULTIES)]
        .groupby(["model", "difficulty"])["accepted"]
        .agg(["sum", "count"])
    )
    header = f"  {'model':<10}  " + "  ".join(f"{d:<8}" for d in DIFFICULTIES)
    w(header)
    for m in MODELS:
        row_parts = []
        for d in DIFFICULTIES:
            try:
                acc = int(md.loc[(m, d), "sum"])
                tot = int(md.loc[(m, d), "count"])
                row_parts.append(f"{acc}/{tot} ({pct(acc,tot):.0f}%)")
            except KeyError:
                row_parts.append("—")
        w(f"  {m:<10}  " + "  ".join(f"{p:<8}" for p in row_parts))
    w("")

    # ── Passage quality ───────────────────────────────────────────────────────
    w("── Passage quality (accepted per batch, max 20) ─────────────")
    batch_totals = df.groupby("folder")["accepted"].sum().sort_values()
    weak = batch_totals[batch_totals <= WEAK_BATCH_THRESHOLD]
    strong = batch_totals[batch_totals >= 12]

    w(f"  Weak batches  (≤{WEAK_BATCH_THRESHOLD} accepted):  {len(weak)}")
    for folder, count in weak.items():
        cat = batch_categories.get(
            df[df["folder"] == folder]["batch_id"].iloc[0], "")
        w(f"    ✗ {folder:<30}  {count} accepted  [{cat}]")
    w("")
    w(f"  Strong batches (≥12 accepted): {len(strong)}")
    for folder, count in strong.items():
        cat = batch_categories.get(
            df[df["folder"] == folder]["batch_id"].iloc[0], "")
        w(f"    ✓ {folder:<30}  {count} accepted  [{cat}]")
    w("")

    # ── Inter-model agreement ─────────────────────────────────────────────────
    w("── Inter-model agreement (models with ≥1 accepted per batch) ─")
    model_contrib = (
        df[df["accepted"]]
        .groupby(["folder", "model"])
        .size()
        .gt(0)
        .groupby(level="folder")
        .sum()
    )
    counts = model_contrib.value_counts().sort_index()
    for n_models, n_batches_val in counts.items():
        w(f"  {n_models} model(s) contributed:  {n_batches_val} batches")
    w("")

    # ── WG source distribution ────────────────────────────────────────────────
    w("── Accepted questions by IPCC Working Group ─────────────────")
    wg_counts = df[df["accepted"]].groupby("wg").size()
    for wg, count in wg_counts.items():
        w(f"  {WG_LABELS.get(wg, wg):<40}  {count}  ({pct(count, n_accept):.1f}%)")
    w("")

    # ── Prompt type ───────────────────────────────────────────────────────────
    w("── Acceptance rate by prompt type ───────────────────────────")
    pt_stats = df.groupby("prompt_type")["accepted"].agg(["sum", "count"])
    for pt, row in pt_stats.iterrows():
        w(f"  {pt:<22}  {int(row['sum']):>3} / {int(row['count'])}  "
          f"({pct(row['sum'], row['count']):.1f}%)")
    w("")
    w("=" * 60)

    return "\n".join(lines)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    print("\n── ClimateQA Analysis ───────────────────────────────────────")
    print(f"  Reading: review/questions.csv")

    df = load_data()
    batch_categories = load_batch_categories()

    # ── Charts ────────────────────────────────────────────────────────────────
    print("\n  Generating charts...")

    save_fig(fig_model_acceptance(df),    "01_model_acceptance.png")
    save_fig(fig_model_by_difficulty(df), "02_model_by_difficulty.png")
    save_fig(fig_passage_quality(df),     "03_passage_quality.png")
    save_fig(fig_difficulty_dist(df),     "04_difficulty_dist.png")
    save_fig(fig_batch_heatmap(df),       "05_batch_heatmap.png")

    # ── Report ────────────────────────────────────────────────────────────────
    report = build_report(df, batch_categories)
    report_path = os.path.join(OUT_DIR, "report.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"  Saved: analysis/report.txt")

    print()
    print(report)


if __name__ == "__main__":
    main()
