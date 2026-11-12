"""Lab 5 — Observability: every model call you made today, with tokens, cost and time. Plus Langfuse."""
import os

import pandas as pd
import streamlit as st

from common import plain, money
from labs.agents import render, AGENTS

LANGFUSE_URL = os.environ.get("LANGFUSE_BASE_URL") or os.environ.get("LANGFUSE_HOST") or "https://cloud.langfuse.com"


def show():
    st.title("🔭 Lab 5 · Observability — what did your AI actually do?")
    st.markdown("Evals tell you **if** the AI is good. Observability tells you **what it did, step by step, and what it "
                "cost** — in testing and, more importantly, in production.")
    trace = st.session_state.get("trace", [])
    if not trace:
        st.info("No model calls yet in this browser session. Run Lab 3 or Lab 4 first, then come back.")
        return
    df = pd.DataFrame(trace)
    m = st.columns(4)
    m[0].metric("Model calls", len(df))
    m[1].metric("Tokens", f"{int(df.tokens_in.sum() + df.tokens_out.sum()):,}")
    m[2].metric("Total cost", money(df.cost.sum()))
    m[3].metric("Slowest call", f"{df.secs.max():.1f} s")

    st.info("**Predict (pair):** which lab spent the most money today — and which agent was the most expensive?")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Cost by lab (USD)**")
        st.bar_chart(df.groupby("lab").cost.sum())
    with c2:
        st.markdown("**Cost by step / agent (USD)**")
        st.bar_chart(df.groupby("step").cost.sum().sort_values(ascending=False).head(10))

    runs = st.session_state.get("runs", [])
    if runs:
        st.markdown("### Replay one agent run, step by step")
        pick = st.selectbox("Pick a run", [f"{r['id']} · {r['scenario']} · guardrails {'ON' if r['guards'] else 'OFF'}"
                                           for r in runs][::-1])
        run = next(r for r in runs if pick.startswith(r["id"] + " "))
        st.caption(f"Verdict {run['verdict']} · {run['calls']} model calls · {run['tokens']:,} tokens · "
                   f"{money(run['cost'])} · {run['secs']:.1f}s")
        steps = [e for e in run["events"] if e["kind"] == "llm"]
        st.dataframe(pd.DataFrame([dict(step=i + 1, agent=AGENTS[e["agent"]][0] + " " + e["agent"],
                                        tokens=e["info"]["tokens_in"] + e["info"]["tokens_out"],
                                        cost_usd=round(e["info"]["cost"], 5), seconds=round(e["info"]["secs"], 2))
                                   for i, e in enumerate(steps)]), hide_index=True, width="stretch")
        with st.expander("Show the full conversation of this run"):
            render(run, key=f"tr{run['id']}")

    with st.expander("All model calls (raw trace table)"):
        st.dataframe(df[["time", "lab", "step", "model", "tokens_in", "tokens_out", "cost", "secs"]],
                     hide_index=True, width="stretch")

    st.markdown("### The same thing in a real tool: Langfuse")
    if os.environ.get("LANGFUSE_PUBLIC_KEY"):
        st.success("This VM sends every model call to Langfuse. The trainer will show the dashboard on the screen.")
    st.link_button("Open Langfuse", LANGFUSE_URL)
    st.markdown("""
| What a manager should watch in production | Why |
|---|---|
| Cost per answer, per day, per team | Budgets break quietly — one looping agent can burn a month's money in a night |
| Slowest 5% of response times | Users judge by the worst experience, not the average |
| Thumbs-down and escalation rate | The earliest sign that quality is dropping |
| Guardrail hits per day | A sudden jump means someone is attacking — or a new document has hidden text |
| Eval score after every change | Catches regressions before users do |
""")
    plain("if you cannot see what your AI did, you cannot fix it, cost it, or defend it in an audit. Ask your team on "
          "Monday: <b>for any answer our AI gave last week, can we show every step it took and what it cost?</b>")
