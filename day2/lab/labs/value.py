"""Lab 8 — Value Case: proving AI value with no baseline. The trap, the honest range, and your own case."""
import io
import random
import statistics as stx

import pandas as pd
import streamlit as st

from common import plain

# A fictional 6-sprint Axion pilot: Team A used AI, Team B did not.
PILOT = pd.DataFrame({
    "Sprint": [1, 2, 3, 4, 5, 6] * 2,
    "Team": ["A · with AI"] * 6 + ["B · without AI"] * 6,
    "Cycle time (days)": [6.1, 5.2, 4.4, 4.0, 3.8, 3.7, 6.3, 6.4, 6.2, 6.1, 6.3, 6.2],
    "Review time (hours/PR)": [2.0, 2.5, 2.6, 2.3, 2.4, 2.3, 2.1, 2.0, 2.2, 2.1, 2.0, 2.1],
    "Rework %": [8, 11, 12, 9, 9, 8, 8, 8, 9, 8, 8, 8],
    "Escaped defects": [2, 3, 4, 2, 2, 2, 2, 2, 2, 3, 2, 2],
})


def tasks():
    random.seed(7)
    rows = []
    for i in range(30):
        est = random.choice([4, 6, 8, 8, 12, 16, 16, 24])
        saving = random.gauss(0.24, 0.12)
        rows.append(dict(task=f"T{i + 1}", estimate_without_ai=est, actual_with_ai=round(max(1, est * (1 - saving)), 1)))
    d = pd.DataFrame(rows)
    d["saving %"] = ((1 - d.actual_with_ai / d.estimate_without_ai) * 100).round(0)
    return d


def memo_docx(f):
    from docx import Document
    doc = Document()
    doc.add_heading(f"AI Value Case — {f['project']}", 1)
    for k, v in [("Hypothesis", f["hyp"]), ("How we compare (no baseline)", f["method"]),
                 ("Time", f["time"]), ("Cost", f["cost"]), ("Quality gate", f["quality"]),
                 ("Checkpoints", "Day 30: first numbers · Day 60: decide to scale or adjust · Day 90: go / stop"),
                 ("We stop if", f["stop"])]:
        doc.add_heading(k, 2)
        doc.add_paragraph(v)
    buf = io.BytesIO()
    doc.save(buf)
    return buf.getvalue()


def show():
    st.title("💼 Lab 8 · Value Case — proving AI value with no baseline")
    t1, t2, t3 = st.tabs(["A · The trap", "B · The honest range", "C · Your value case"])
    with t1:
        st.markdown("Axion ran a 6-sprint pilot: **Team A used AI, Team B did not.** The sponsor wants one number.")
        st.info("**Predict (pair):** how much better is Team A? Write a percentage.")
        metrics = st.multiselect("Which measures do we count?", list(PILOT.columns[2:]), default=["Cycle time (days)"])
        a = PILOT[PILOT.Team.str.startswith("A")].iloc[3:].mean(numeric_only=True)
        b = PILOT[PILOT.Team.str.startswith("B")].iloc[3:].mean(numeric_only=True)
        gains = {m: (b[m] - a[m]) / b[m] * 100 for m in metrics}       # positive = A better
        for m in metrics:
            st.line_chart(PILOT.pivot(index="Sprint", columns="Team", values=m), height=170)
        if gains:
            net = sum(gains.values()) / len(gains)
            colour = "#2F7D4F" if net > 20 else ("#B37E00" if net > 0 else "#B3432B")
            st.markdown(f"<div style='background:{colour};color:#fff;padding:14px;border-radius:8px;font-size:1.4rem;"
                        f"font-weight:700;text-align:center'>Headline: Team A is {net:+.0f}% better</div>",
                        unsafe_allow_html=True)
            st.caption(" · ".join(f"{m}: {g:+.0f}%" for m, g in gains.items()) + " (sprints 4–6, A vs B)")
        plain("count only speed and AI looks like a <b>40% win</b>. Add review time, rework and escaped defects and the "
              "story changes to <b>under 10%</b> — most of the speed gain is eaten by extra review time and rework. Choose the measures "
              "<b>before</b> the pilot starts, and always pair a speed measure with a quality gate.")
    with t2:
        st.markdown("**Estimate first, then measure** — no history needed. The team estimates each task *without AI* "
                    "in sprint planning (as usual), then records the actual time *with AI*.")
        d = tasks()
        st.scatter_chart(d, x="estimate_without_ai", y="actual_with_ai", height=300)
        s = sorted(d["saving %"])
        q1, med, q3 = s[len(s) // 4], stx.median(s), s[3 * len(s) // 4]
        c = st.columns(3)
        c[0].metric("Median saving", f"{med:.0f}%")
        c[1].metric("Middle half of tasks", f"{q1:.0f}% to {q3:.0f}%")
        c[2].metric("Tasks where AI made it slower", int((d["saving %"] < 0).sum()))
        plain(f"say <b>'AI saved {q1:.0f}–{q3:.0f}% on typical tasks, median {med:.0f}%, over 30 tasks'</b> — not "
              "'AI makes us 40% faster'. A range with its sample size is what convinces a CFO, and it is honest about "
              "the tasks where AI did not help.")
        with st.expander("Four ways to compare when there is no past data"):
            st.markdown("1. **Estimate first, then measure** (above) — for time.\n"
                        "2. **Split tasks inside the project** — similar tasks alternate with / without AI for 2 sprints.\n"
                        "3. **Cost per unit of work** — cost per test case, per requirement, per defect found (include "
                        "AI spend, review time, learning time).\n"
                        "4. **Quality as a gate** — speed counts only if escaped defects, rework % and change failure "
                        "rate do not get worse. The first 2 sprints become your baseline.")
    with t3:
        st.markdown("Fill this for **one real project** of yours. You get a one-page note for your manager.")
        f = {}
        f["project"] = st.text_input("Project", "AI-generated test cases for the AX900 Safety I/O module")
        f["hyp"] = st.text_area("Hypothesis (one sentence)", "Using AI to draft test cases from user stories cuts "
                                "test design effort by 20–30% without more escaped defects.", height=70)
        f["method"] = st.selectbox("How we compare without a baseline", [
            "Estimate first, then measure (planning estimate without AI vs actual with AI)",
            "Split tasks inside the project for 2 sprints (with / without AI)",
            "Cost per unit of work (per test case / requirement / defect)",
            "First 2 sprints as baseline, quality as a gate"])
        c = st.columns(4)
        hours = c[0].number_input("Hours saved per week (team)", 0.0, 500.0, 24.0)
        rate = c[1].number_input("Loaded cost per hour (INR)", 500, 20000, 2500, 100)
        ai = c[2].number_input("AI cost per month (INR)", 0, 1000000, 40000, 1000)
        overhead = c[3].number_input("Extra review hours per week", 0.0, 200.0, 6.0)
        net = ((hours - overhead) * 4.3 * rate) - ai
        st.metric("Net value per month (INR)", f"₹{net:,.0f}", "pays back" if net > 0 else "does not pay back yet",
                  delta_color="normal" if net > 0 else "inverse")
        f["time"] = f"Target 20–30% less effort; measured as a range over at least 20 tasks. Planned saving: {hours:.0f} h/week."
        f["cost"] = (f"Hours saved {hours:.0f}/week minus extra review {overhead:.0f}/week at ₹{rate:,}/hour, minus AI "
                     f"cost ₹{ai:,}/month = net ₹{net:,.0f} per month.")
        f["quality"] = st.text_input("Quality gate", "Escaped defects and rework % no worse than the first 2 sprints.")
        f["stop"] = st.text_input("We stop if…", "Net value is negative at day 60, or escaped defects rise for 2 sprints.")
        st.download_button("⬇️ Download my one-page Value Case (Word)", memo_docx(f),
                           file_name="AI_Value_Case.docx", type="primary")
