#!/usr/bin/env python3
"""
review_app.py
-------------
Streamlit curation interface for the ClimateQA benchmark.

Run with:
    streamlit run review_app.py

Each "page" is one source batch — showing the passage and all four models'
questions side by side. Navigate with Prev / Next or the batch list.
Selections are saved to review/questions.csv on every navigation and on Save.

State architecture:
    st.session_state.review  — dict {id: {"status": ..., "notes": ...}}
        Authoritative in-memory store. Updated immediately via on_change
        callbacks so it's never at risk of being wiped by Streamlit's
        widget-key cleanup between reruns.

    Widget keys (status_{id}, notes_{id}) are re-synced from st.session_state.review
        whenever the batch changes, so returning to a previous batch always
        shows saved values.
"""

import os
import pandas as pd
import streamlit as st

# ── Config ────────────────────────────────────────────────────────────────────

SCRIPT_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH    = os.path.join(SCRIPT_DIR, "review", "questions.csv")
MODELS      = ["claude", "chatgpt", "gemini", "groq"]
STATUS_OPTS = ["pending", "accept", "reject"]

DIFF_ICON  = {"easy": "🟢", "medium": "🟡", "hard": "🔴"}
STATUS_ICON = {"pending": "⏳", "accept": "✅", "reject": "❌"}

MODEL_LABEL = {
    "claude":  "Claude (Sonnet 4.6)",
    "chatgpt": "ChatGPT (GPT-4o)",
    "gemini":  "Gemini 2.5 Flash",
    "groq":    "Llama 3.3 70B (via Groq)",
}

# ── Data loading ──────────────────────────────────────────────────────────────

@st.cache_data
def load_csv():
    df = pd.read_csv(CSV_PATH, dtype=str).fillna("")
    df["status"] = df["status"].apply(
        lambda s: s.strip().lower() if s.strip().lower() in STATUS_OPTS else "pending"
    )
    return df


# ── Session state ─────────────────────────────────────────────────────────────

def init():
    """One-time session initialisation."""
    if "df" not in st.session_state:
        st.session_state.df = load_csv()

    if "batch_idx" not in st.session_state:
        st.session_state.batch_idx = 0

    # Authoritative review store — survives across reruns regardless of which
    # widgets are currently rendered.
    if "review" not in st.session_state:
        review = {}
        for _, row in st.session_state.df.iterrows():
            review[row["id"]] = {
                "status": row["status"],
                "notes":  row["notes"],
            }
        st.session_state.review = review

    # Track which batch was last rendered so we know when to re-sync widgets.
    if "last_batch_idx" not in st.session_state:
        st.session_state.last_batch_idx = -1


def sync_widgets_for_batch(batch_df):
    """
    Copy review-store values into widget keys for the current batch.
    Called only when the batch changes, so in-progress edits aren't overwritten.
    """
    review = st.session_state.review
    for _, row in batch_df.iterrows():
        qid = row["id"]
        if qid in review:
            st.session_state[f"status_{qid}"] = review[qid]["status"]
            st.session_state[f"notes_{qid}"]  = review[qid]["notes"]


# ── on_change callbacks (update review store immediately) ─────────────────────

def _on_status_change(qid):
    st.session_state.review[qid]["status"] = st.session_state[f"status_{qid}"]


def _on_notes_change(qid):
    st.session_state.review[qid]["notes"] = st.session_state[f"notes_{qid}"]


# ── Persistence ───────────────────────────────────────────────────────────────

def flush_review_to_df():
    """Copy the review store into the DataFrame."""
    df     = st.session_state.df
    review = st.session_state.review
    for i, row in df.iterrows():
        qid = row["id"]
        if qid in review:
            df.at[i, "status"] = review[qid]["status"]
            df.at[i, "notes"]  = review[qid]["notes"]


def save_csv():
    flush_review_to_df()
    st.session_state.df.to_csv(CSV_PATH, index=False)
    st.toast("Saved ✓", icon="💾")


def go_to(idx):
    save_csv()
    st.session_state.batch_idx     = idx
    st.session_state.last_batch_idx = -1   # force widget re-sync on next render
    st.rerun()


# ── Sidebar ───────────────────────────────────────────────────────────────────

def render_sidebar(batches, current_idx):
    review = st.session_state.review

    with st.sidebar:
        st.title("ClimateQA Review")

        # ── Progress ──────────────────────────────────────────────────────────
        all_statuses = [v["status"] for v in review.values()]
        total      = len(all_statuses)
        n_accept   = all_statuses.count("accept")
        n_reject   = all_statuses.count("reject")
        n_reviewed = n_accept + n_reject

        st.progress(n_reviewed / total if total else 0,
                    text=f"{n_reviewed} / {total} reviewed")
        st.caption(
            f"✅ {n_accept} accepted · ❌ {n_reject} rejected · "
            f"⏳ {total - n_reviewed} pending"
        )

        st.divider()

        # ── Batch list ────────────────────────────────────────────────────────
        st.subheader("Batches")

        # Helper: batch completion status
        df = st.session_state.df
        for i, folder in enumerate(batches):
            ids       = df.loc[df["folder"] == folder, "id"].tolist()
            statuses  = [review.get(qid, {}).get("status", "pending") for qid in ids]
            done      = sum(1 for s in statuses if s != "pending")
            total_q   = len(statuses)
            if done == total_q and total_q > 0:
                icon = "✅"
            elif done > 0:
                icon = "🔵"
            else:
                icon = "⬜"

            label = f"{icon} {i + 1}. {folder}"
            btn_type = "primary" if i == current_idx else "secondary"
            if st.button(label, key=f"nav_{i}",
                         use_container_width=True, type=btn_type):
                go_to(i)

        st.divider()
        if st.button("💾 Save now", use_container_width=True):
            save_csv()


# ── Question card ─────────────────────────────────────────────────────────────

def question_card(row):
    qid    = row["id"]
    q_num  = qid.rsplit("_q", 1)[-1]
    diff   = row.get("difficulty", "")
    status = st.session_state.review.get(qid, {}).get("status", "pending")

    border = {"accept": "#2d9e5f", "reject": "#c0392b"}.get(status, "#555")

    st.markdown(
        f'<div style="border-left:4px solid {border}; padding:4px 10px; '
        f'margin-bottom:2px; border-radius:3px;">'
        f'<span style="font-size:0.72rem; color:#888;">'
        f'{DIFF_ICON.get(diff,"⚪")} {diff.upper()} · Q{q_num} · '
        f'{STATUS_ICON.get(status,"⏳")}</span></div>',
        unsafe_allow_html=True,
    )

    # Cat2 scenario
    scenario = row.get("scenario", "")
    if scenario:
        with st.expander("📊 Data scenario", expanded=True):
            st.text(scenario)

    st.markdown(f"**{row['question']}**")

    # Options — highlight correct
    correct = row.get("correct_answer", "")
    for letter in ["A", "B", "C", "D"]:
        text = row.get(f"option_{letter}", "")
        if not text:
            continue
        if letter == correct:
            st.markdown(
                f'<p style="color:#2d9e5f;font-weight:600;margin:2px 0;">'
                f'✅ <b>{letter}.</b> {text}</p>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<p style="margin:2px 0;">&nbsp;&nbsp;&nbsp;{letter}. {text}</p>',
                unsafe_allow_html=True,
            )

    with st.expander("Explanation"):
        st.write(row.get("explanation", ""))

    st.divider()

    # Status radio — on_change immediately updates the review store
    st.radio(
        "Status",
        STATUS_OPTS,
        key=f"status_{qid}",
        on_change=_on_status_change,
        args=(qid,),
        horizontal=True,
        label_visibility="collapsed",
    )

    # Notes — on_change immediately updates the review store
    st.text_area(
        "Notes",
        key=f"notes_{qid}",
        on_change=_on_notes_change,
        args=(qid,),
        placeholder="Notes (optional)…",
        height=68,
        label_visibility="collapsed",
    )


# ── Batch view ────────────────────────────────────────────────────────────────

def render_batch(batch_df, idx, n_batches):
    meta = batch_df.iloc[0]

    # ── Header + nav ──────────────────────────────────────────────────────────
    col_title, col_nav = st.columns([3, 1])
    with col_title:
        st.header(meta["folder"])
        st.caption(
            f"📁 {meta['batch_id']}  ·  {meta['category']}  ·  "
            f"{meta['source']}  ·  `{meta['prompt_type']}`"
        )
    with col_nav:
        st.write("")
        nav_l, nav_r = st.columns(2)
        with nav_l:
            if st.button("← Prev", disabled=(idx == 0), use_container_width=True):
                go_to(idx - 1)
        with nav_r:
            if st.button("Next →", disabled=(idx == n_batches - 1),
                         use_container_width=True):
                go_to(idx + 1)
        st.caption(f"Batch {idx + 1} of {n_batches}")

    # ── Passage ───────────────────────────────────────────────────────────────
    passage = meta.get("passage", "")
    if passage:
        with st.expander("📄 Source passage", expanded=False):
            st.text(passage)

    st.write("")

    # ── 4 model columns ───────────────────────────────────────────────────────
    cols = st.columns(4, gap="medium")
    for col, model in zip(cols, MODELS):
        model_rows = batch_df[batch_df["model"] == model]
        with col:
            st.subheader(MODEL_LABEL.get(model, model))
            if model_rows.empty:
                st.caption("*No responses generated.*")
                continue
            for _, row in model_rows.iterrows():
                question_card(row)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    st.set_page_config(
        page_title="ClimateQA Review",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown("""
    <style>
        .block-container { padding-top: 1.5rem; padding-bottom: 1rem; }
        .stRadio > div { gap: 0.4rem; }
        .stTextArea textarea { font-size: 0.82rem; }
        p { margin: 0.15rem 0; }
    </style>
    """, unsafe_allow_html=True)

    init()

    df      = st.session_state.df
    batches = df["folder"].unique().tolist()
    idx     = st.session_state.batch_idx

    render_sidebar(batches, idx)

    batch_df = df[df["folder"] == batches[idx]]

    # Re-sync widget keys from review store whenever the batch changes.
    # This ensures returning to a previously reviewed batch shows saved values.
    if st.session_state.last_batch_idx != idx:
        sync_widgets_for_batch(batch_df)
        st.session_state.last_batch_idx = idx

    render_batch(batch_df, idx, len(batches))


if __name__ == "__main__":
    main()
