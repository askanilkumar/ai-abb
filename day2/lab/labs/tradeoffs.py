"""Lab 7 — Architecture trade-offs: 4 models side by side, then serverless vs hourly GPU vs on-prem."""
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import streamlit as st

from common import add_trace, call_model, plain, live, money, MODELS, available_models

LAB = "Lab 7 · Trade-offs"

CONTEXT = """SERVICE BULLETIN SB-2026-01 (Axion Controls, fictional)
Product: AX900 controller, firmware 4.0 to 4.1.3. Symptom: the ETH2 port stops responding after about 72 hours of
continuous operation when broadcast traffic on the plant network is above 2,000 packets per second. ETH1 keeps working.
Cause: a buffer in the ETH2 driver is not released when broadcast storms occur. Workaround: enable broadcast storm
control on the managed switch (limit 1,000 pps) or schedule a controlled restart of the ETH2 interface every 48 hours.
Fix: firmware 4.2 (driver buffer handling rewritten). Sites affected so far: 3 steel plants, 1 water treatment plant."""

QUESTION = ("A plant manager calls: 'Our AX900 lost its ETH2 connection again this morning.' Using only the bulletin, "
            "write 4 short bullet points: what is happening, what to check first, the workaround today, and the "
            "permanent fix. Plain English for a non-specialist.")


def ask(model):
    msg, info = call_model([{"role": "system", "content": "Answer only from the bulletin.\n\n" + CONTEXT},
                            {"role": "user", "content": QUESTION}], model=model)
    return model, msg.content, info


def show():
    st.title("⚖️ Lab 7 · Architecture trade-offs")
    tab1, tab2, tab3 = st.tabs(["A · Same question, four models", "B · Pay per token vs GPU by the hour vs on-prem",
                                "C · Team scenarios"])
    with tab1:
        st.markdown("Two models from OpenAI, two **open-weight** models (their weights are public, so ABB could run "
                    "them on its own servers). All four run on the same Azure Foundry today.")
        with st.expander("The bulletin and the question (same for all four)"):
            st.text(CONTEXT); st.markdown(f"**Question:** {QUESTION}")
        st.info("**Predict (pair):** which model will give the best answer? Which will be cheapest? Is the most "
                "expensive one 10× better?")
        models = available_models()
        if st.button("▶ Ask all four at once", type="primary", disabled=not live()):
            with st.spinner("Asking four models in parallel…"):
                with ThreadPoolExecutor(max_workers=4) as ex:
                    res = []
                    for f in [ex.submit(ask, m) for m in models]:
                        try:
                            res.append(f.result())
                        except Exception as e:
                            res.append((models[len(res)], f"⚠️ This model did not answer: {str(e)[:150]}", None))
            for m, _, info in res:
                if info:
                    add_trace(LAB, "compare models", m, [], "", info)
            st.session_state.to_res = res
        res = st.session_state.get("to_res")
        if res:
            cols = st.columns(len(res))
            rows = []
            for col, (m, text, info) in zip(cols, res):
                with col:
                    st.markdown(f"**{m}**")
                    if info:
                        st.caption(f"⏱️ {info['secs']:.1f}s · {info['tokens_in'] + info['tokens_out']:,} tokens · "
                                   f"💲 {money(info['cost'])}")
                    st.markdown(f"<div style='background:#fff;border:1px solid #C6CBC6;border-radius:6px;padding:8px;"
                                f"font-size:.88rem;min-height:300px'>{text}</div>", unsafe_allow_html=True)
                    q = st.slider("Your quality score", 1, 5, 3, key=f"q_{m}")
                    if info:
                        rows.append(dict(model=m, quality=q, seconds=round(info["secs"], 1),
                                         cost_per_answer=info["cost"], cost_per_100k_answers=info["cost"] * 100000))
            if rows:
                d = pd.DataFrame(rows)
                d["quality_per_$ (100k answers)"] = (d.quality / d.cost_per_100k_answers).round(3)
                st.dataframe(d.assign(cost_per_100k_answers=d.cost_per_100k_answers.map(lambda x: f"${x:,.0f}"),
                                      cost_per_answer=d.cost_per_answer.map(money)), hide_index=True, width="stretch")
                plain("start with the <b>smallest model that passes your eval</b>. Use the big model only where the "
                      "eval shows it is needed. At 100,000 answers a month, the difference is real money.")

    with tab2:
        st.markdown("Three ways to pay for the same model. Move the sliders and watch where the lines cross.")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("**☁️ Serverless (pay per token)**")
            model = st.selectbox("Model price", list(MODELS), index=0)
            pin, pout = MODELS[model][1]
            tin = st.number_input("Tokens in per request", 100, 20000, 1500, 100)
            tout = st.number_input("Tokens out per request", 50, 5000, 300, 50)
        with c2:
            st.markdown("**🖥️ Dedicated GPU in the cloud (by the hour)**")
            gpu_hr = st.number_input("GPU VM price per hour (USD) — check your Azure price", 0.5, 50.0, 4.0, 0.5)
            hours = st.slider("Hours per day it runs", 8, 24, 24)
            cap = st.number_input("Requests one GPU VM can serve per hour", 100, 50000, 3000, 100)
        with c3:
            st.markdown("**🏭 On-prem (your own servers)**")
            capex = st.number_input("Server + GPUs (USD, one-time)", 10000, 2000000, 120000, 10000)
            years = st.slider("Written off over (years)", 1, 5, 3)
            ops = st.number_input("People + power + support per month (USD)", 0, 100000, 6000, 500)
        per_req = (tin * pin + tout * pout) / 1e6
        rng = list(range(0, 400001, 5000))
        rows = []
        for r in rng:
            gpus = max(1, -(-r // max(1, int(cap * hours))))   # VMs needed for r requests/day
            rows.append({"requests per day": r, "Serverless": per_req * r * 30, "Cloud GPU": gpus * gpu_hr * hours * 30,
                         "On-prem": capex / (years * 12) + ops})
        d = pd.DataFrame(rows).set_index("requests per day")
        st.line_chart(d, height=320)
        cross = d[d["Serverless"] > d[["Cloud GPU", "On-prem"]].min(axis=1)]
        m1, m2, m3 = st.columns(3)
        m1.metric("Serverless cost per request", f"${per_req:.5f}")
        m2.metric("Serverless stops being cheapest at",
                  f"~{cross.index[0]:,} requests/day" if len(cross) else "not in this range")
        m3.metric("At 50,000 requests/day, monthly", money(per_req * 50000 * 30))
        plain("pay-per-token wins while usage is low or unpredictable — which is most pilots. Fixed capacity wins only "
              "at high, steady volume. On-prem is a decision about <b>data, network and control</b> (plants with no "
              "internet, IP, sovereignty) more than about cost — and it needs a team to run it.")

    with tab3:
        st.markdown("Each team takes one card, decides **model · hosting · framework**, and defends it in 2 minutes.")
        cards = [
            ("HR policy bot for 5,000 staff", "Low risk, public-ish data, spiky use (mornings, month end).",
             "Small model, serverless, buy (Copilot/Abby agent with the policy documents). Add an eval set of 50 real "
             "questions and a 'source + date' on every answer."),
            ("Code review assistant for 200 developers", "Source code is IP; steady daytime volume; quality matters.",
             "Mid/frontier model for reviews inside the company tenant (no training on your code), serverless to start; "
             "measure cost per pull request; revisit dedicated capacity if volume is steady and high."),
            ("Fault-code assistant inside a plant with no internet", "Air-gapped OT network, IEC 62443 zones, operators act on answers.",
             "Open-weight model on-prem on an edge server, RAG over local manuals, read-only (never writes to the "
             "control system), human confirms every action, offline eval before each model upgrade."),
        ]
        for title, ctx, ans in cards:
            with st.container(border=True):
                st.markdown(f"**{title}** — {ctx}")
                with st.expander("Reveal an architect's answer (after your team presents)"):
                    st.markdown(ans)
        st.markdown("**Framework choice in one line:** buy (Copilot, Abby) when the use case is common · managed "
                    "(Azure AI Foundry Agent Service) when you need your own data and tools with less plumbing · build "
                    "(LangGraph, CrewAI, Semantic Kernel) when you need full control — and own the upgrades.")
        plain("whatever you choose, put a <b>model gateway</b> and an <b>eval set</b> in front of it. Then swapping "
              "today's model for next quarter's better, cheaper one is a one-day test, not a project.")
