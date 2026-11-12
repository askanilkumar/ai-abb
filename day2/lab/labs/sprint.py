"""Lab 6 — Sprint Board: AI over an Azure DevOps export. Six charts vs three sentences, with a fact check."""
import json
import re
from pathlib import Path

import pandas as pd
import streamlit as st

from common import chat, plain, live, info_line, MINI, FRONTIER

LAB = "Lab 6 · Sprint Board"
CSV = Path(__file__).resolve().parent.parent.parent / "data" / "axion_ado_export.csv"


@st.cache_data
def load():
    df = pd.read_csv(CSV).fillna("")
    df["Team"] = df["Area Path"].str.split("\\").str[-1]
    df["Sprint"] = df["Iteration Path"].str.extract(r"Sprint (\d+)")[0].astype(int)
    return df


def stats(df):
    st_ = df[df["Work Item Type"] == "User Story"].copy()
    st_["pts"] = pd.to_numeric(st_["Story Points"])
    planned = st_.pivot_table(index="Sprint", columns="Team", values="pts", aggfunc="sum")
    carried = st_[st_.Tags == "carried-over"].pivot_table(index="Sprint", columns="Team", values="pts", aggfunc="sum")
    carry_pct = (carried.reindex_like(planned).fillna(0) / planned * 100).round(0)
    done = (planned - carried.reindex_like(planned).fillna(0))
    bugs = df[df["Work Item Type"] == "Bug"]
    cust = bugs[bugs.Tags == "customer-found"].pivot_table(index="Sprint", columns="Team", values="ID", aggfunc="count")\
        .reindex(index=planned.index, columns=planned.columns).fillna(0).astype(int)
    sev = bugs.pivot_table(index="Sprint", columns="Severity", values="ID", aggfunc="count").fillna(0).astype(int)
    open_bugs = bugs[bugs.State == "Active"].groupby("Team").ID.count()
    return dict(completed_points=done, carry_over_pct=carry_pct, customer_found_bugs=cust, bugs_by_severity=sev,
                open_bugs_now=open_bugs)


def numbers_in(stats_):
    """Two sets: percentages (from the carry-over table) and plain counts (from every other table)."""
    pct, cnt = set(), set()
    for k, v in stats_.items():
        for x in pd.DataFrame(v).to_numpy().flatten():
            try:
                (pct if k == "carry_over_pct" else cnt).add(round(float(x), 0))
            except Exception:
                pass
    return pct, cnt


OUTSIDE = re.compile(r"\b(industry|benchmark|typical|best[- ]in[- ]class|on average across)\b", re.I)


def fact_check(text, nums):
    """Every number in the AI's text must exist in the data (sprint numbers 1-6 and v4.2 are allowed).
    Sentences that lean on 'industry' or 'typical' figures are flagged as not coming from your data."""
    pct, cnt = nums
    found, missing, out = [], [], []
    sentences = re.split(r"(?<=[.!?])\s+", text)
    for sent in sentences:
        if OUTSIDE.search(sent):
            out.append(sent)
        for m in re.finditer(r"(?<![\w.])(\d+(?:\.\d+)?)(\s?%)?", sent):
            n, is_pct = float(m.group(1)), bool(m.group(2))
            if not is_pct and (n in (4.2, 900) or (n <= 6 and n == int(n))):
                continue
            ok = round(n, 0) in (pct if is_pct else cnt | pct)
            (found if ok and sent not in out else missing).append(m.group(0).strip())
    marked = []
    for sent in sentences:
        t = sent
        for mm in set(missing):
            t = re.sub(rf"(?<![\w.]){re.escape(mm)}(?![\d])", f"<span style='background:#FBEDEA;color:#B3432B;"
                       f"font-weight:700'>{mm} ❗</span>", t)
        if sent in out:
            t = (f"<span style='background:#FFF8E8;border-bottom:2px solid #B37E00'>{t} ⚠️ <i>source: not your "
                 f"data</i></span>")
        marked.append(t)
    return " ".join(marked), found, missing


def show():
    st.title("📊 Lab 6 · Sprint Board — AI over Azure DevOps data")
    st.markdown("This is a real-format **Azure DevOps export** (306 work items, 4 teams, 6 sprints) of the AX900 "
                "programme. In production it comes from ADO Analytics / OData into Power BI.")
    df = load()
    s = stats(df)
    st.markdown("#### The dashboard everyone has — 6 charts")
    c = st.columns(3)
    with c[0]:
        st.caption("Completed story points"); st.line_chart(s["completed_points"], height=180)
    with c[1]:
        st.caption("Carry-over % of planned points"); st.line_chart(s["carry_over_pct"], height=180)
    with c[2]:
        st.caption("Customer-found bugs"); st.bar_chart(s["customer_found_bugs"], height=180)
    c = st.columns(3)
    with c[0]:
        st.caption("Bugs by severity"); st.bar_chart(s["bugs_by_severity"], height=180)
    with c[1]:
        st.caption("Open bugs now, by team"); st.bar_chart(s["open_bugs_now"], height=180)
    with c[2]:
        st.caption("Work items per sprint"); st.bar_chart(df.groupby(["Sprint", "Work Item Type"]).ID.count().unstack(), height=180)
    st.info("**Predict (pair):** in 10 seconds, what is the single biggest risk for the v4.2 release? Write it down.")

    data_txt = "\n\n".join(f"{k}:\n{pd.DataFrame(v).to_csv()}" for k, v in s.items())
    st.markdown("#### What a VP actually reads — 3 sentences")
    rule = st.toggle("Rule: every number must come from the data, and say which table", value=True)
    model = st.radio("Model", [MINI, FRONTIER], horizontal=True, key="sp_model")
    if st.button("✨ Write the executive summary", type="primary", disabled=not live()):
        sys = ("You write for a VP of Engineering. Exactly 3 sentences: the biggest delivery risk, the biggest quality "
               "risk, and one recommended action. Use specific numbers.")
        if rule:
            sys += " Use ONLY numbers that appear in the data tables, and name the table in brackets."
        else:
            sys += " Add context from typical industry benchmarks where useful."
        text, info = chat([{"role": "system", "content": sys}, {"role": "user", "content": data_txt}],
                          model=model, step="executive summary", lab=LAB)
        st.session_state.sp_sum = (text, info_line(info), rule)
    if "sp_sum" in st.session_state:
        text, inf, used_rule = st.session_state.sp_sum
        marked, found, missing = fact_check(text, numbers_in(s))
        st.markdown(f"<div style='background:#fff;border:2px solid #22262A;border-radius:8px;padding:14px;"
                    f"font-size:1.08rem'>{marked}</div>", unsafe_allow_html=True)
        st.caption(inf)
        if missing:
            st.error(f"Fact check: {len(found)} numbers found in the data, **{len(missing)} NOT found** "
                     f"({', '.join(missing)}). Where did they come from?")
        else:
            st.success(f"Fact check: all {len(found)} numbers are in the data.")
        st.caption("Try again with the rule switched OFF and compare the fact check.")

    st.markdown("#### Ask your data")
    q = st.text_input("Your question", "Which team carries over the most work, and is it getting better or worse?")
    if st.button("Ask", disabled=not live()):
        text, info = chat([{"role": "system", "content": "Answer in 2-3 sentences using only these tables. Quote the "
                            "numbers you use. If the data cannot answer, say so."},
                           {"role": "user", "content": f"{data_txt}\n\nQuestion: {q}"}], model=MINI, step="ask data", lab=LAB)
        st.session_state.sp_ans = text
    if "sp_ans" in st.session_state:
        st.markdown(st.session_state.sp_ans)
    st.caption("Try: *What is our customer satisfaction score?* (it is not in the data — does the AI admit it?)")
    plain("the AI never saw 306 rows — only 5 small summary tables. That is cheaper, faster and safer. And because "
          "every number is checked against the data in code, a made-up figure is caught before it reaches a VP.")
