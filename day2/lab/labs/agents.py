"""Lab 3 — Multi-agent Release Readiness Crew, with and without guardrails."""
import copy
import json

import streamlit as st

from common import add_trace, lf_crew, plain, live, money, MINI, available_models
from labs.crew import SCENARIOS, AGENTS, run_crew

LAB = "Lab 3 · Agents + Guardrails"


def bubble(agent, text, info=None):
    icon, colour = AGENTS[agent]
    st.markdown(f"<div style='display:flex;gap:10px;margin:6px 0'><div style='font-size:1.6rem'>{icon}</div>"
                f"<div style='flex:1;background:#fff;border:1.5px solid {colour};border-left:6px solid {colour};"
                f"border-radius:8px;padding:8px 12px'><b style='color:{colour}'>{agent}</b><br>"
                f"<span style='white-space:pre-wrap'>{text}</span></div></div>", unsafe_allow_html=True)


def tool_card(agent, name, args, result):
    icon, colour = AGENTS[agent]
    res = json.dumps(result, ensure_ascii=False)
    st.markdown(f"<div style='margin:2px 0 2px 46px;background:#F4F5F4;border:1px dashed #9AA19A;border-radius:6px;"
                f"padding:6px 10px;font-size:.85rem'>🔧 <b>{agent}</b> called tool <code>{name}</code>"
                f"({', '.join(f'{k}={v!r}' for k, v in args.items())[:120]})<br>"
                f"<span style='color:#4A5157'>↳ returned: {res[:400]}{'…' if len(res) > 400 else ''}</span></div>",
                unsafe_allow_html=True)


def guard_card(text):
    st.markdown(f"<div style='margin:4px 0 4px 46px;background:#E7F3EC;border:2px solid #2F7D4F;border-radius:6px;"
                f"padding:6px 10px;font-size:.9rem'>🛡️ <b>{text}</b></div>", unsafe_allow_html=True)


def action_card(text, detail):
    st.markdown(f"<div style='margin:4px 0 4px 46px;background:#FBEDEA;border:2px solid #B3432B;border-radius:6px;"
                f"padding:6px 10px;font-size:.9rem'>🚨 <b>{text}</b><br>“{detail.get('message', '')[:200]}”</div>",
                unsafe_allow_html=True)


def render(res, key):
    for i, e in enumerate(res["events"]):
        if e["kind"] == "say":
            bubble(e["agent"], e["text"])
        elif e["kind"] == "tool":
            tool_card(e["agent"], e["name"], e["args"], e["result"])
        elif e["kind"] == "guard":
            guard_card(e["text"])
        elif e["kind"] == "action":
            action_card(e["text"], e["detail"])
        elif e["kind"] == "pending":
            c1, c2, _ = st.columns([1, 1, 3])
            c1.button("✅ Approve email", key=f"ap{key}{i}", on_click=lambda: st.toast("Approved by a human — sent."))
            c2.button("❌ Reject", key=f"rj{key}{i}", on_click=lambda: st.toast("Rejected — not sent."))


def verdict_banner(res, expected):
    ok = res["verdict"] == expected
    colour = "#2F7D4F" if res["verdict"] == "GO" else "#B3432B"
    st.markdown(f"<div style='background:{colour};color:#fff;padding:14px;border-radius:8px;text-align:center;"
                f"font-size:1.6rem;font-weight:700'>FINAL VERDICT: {res['verdict']}</div>", unsafe_allow_html=True)
    c = st.columns(4)
    c[0].metric("Correct?", "✅ yes" if ok else f"❌ no (should be {expected})")
    c[1].metric("Customer data leaked?", "🚨 yes" if res["leaked"] else "no")
    c[2].metric("Email sent without approval?", "🚨 yes" if res["email_sent"] else "no")
    c[3].metric("Cost · time", f"{money(res['cost'])} · {res['secs']:.0f}s", f"{res['calls']} model calls",
                delta_color="off")


def show():
    st.title("🤝 Lab 3 · Agents + Guardrails")
    st.markdown("Five AI agents review the **AX900 v4.2** release together. Each one has its own job and its own "
                "tools. Watch them talk — then attack them.")
    with st.sidebar:
        st.selectbox("Model for the agents", [m for m in available_models()][:2] or [MINI], key="ag_model")

    names = list(SCENARIOS)
    scen = st.radio("Pick a scenario", names, horizontal=False, key="ag_scen")
    s = SCENARIOS[scen]
    c1, c2 = st.columns([2, 3])
    guards = c1.toggle("🛡️ Guardrails ON", value=False, key="ag_guards")
    c2.info("**Predict (pair):** what will the final verdict be? Will anything bad happen?")
    b1, b2, _ = st.columns([1, 1, 3])
    go = b1.button("▶ Run the crew", type="primary", disabled=not live())
    rp = b2.button("▶ Replay (no model)")
    if go or rp:
        with st.spinner("The agents are working… (20–40 seconds)"):
            try:
                res = run_crew(copy.deepcopy(s), guards, model=st.session_state.ag_model, sim=bool(rp))
            except Exception as e:
                st.error(f"Model call failed ({e}). Showing a replay instead.")
                res = run_crew(copy.deepcopy(s), guards, model=st.session_state.ag_model, sim=True)
        run_id = f"crew-{len(st.session_state.get('runs', [])) + 1}"
        for e in res["events"]:
            if e["kind"] == "llm":
                add_trace(LAB, f"{e['agent']}", e["info"]["model"], [], "", e["info"], run=run_id, send_lf=False)
        if not rp:
            lf_crew(f"Release Crew · {run_id}", scen, guards, res, s["expected"])
        st.session_state.setdefault("runs", []).append(dict(id=run_id, scenario=scen, guards=guards, **res))
        st.session_state.ag_last = dict(res=res, scen=scen, guards=guards, replay=bool(rp))

    last = st.session_state.get("ag_last")
    if last and last["scen"] == scen:
        st.markdown(f"#### Conversation · guardrails {'ON 🛡️' if last['guards'] else 'OFF'}"
                    f"{' · ▶ replay' if last['replay'] else ''}")
        render(last["res"], key=len(st.session_state.get("runs", [])))
        verdict_banner(last["res"], s["expected"])
        st.markdown("**Now flip the guardrail switch and run the same scenario again.**")

    with st.expander("What happened in the background"):
        st.markdown("""
- **An agent** = a model + a job description + tools. Each agent here is a separate model call with its own instructions.
- **Tool calling**: the model does not fetch data itself. It *asks* for a tool (grey cards); our code runs the tool and hands back the result.
- **The guardrails** are ordinary code around the AI, in four layers:
  1. **Input guard** — removes instructions hidden inside data (tickets, emails, documents)
  2. **Policy guard** — the rules from Lab 1, written as code; the AI cannot talk its way past them
  3. **Output guard** — masks names, phone numbers and emails before anything leaves
  4. **Action guard** — anything that touches a customer needs a human to approve
""")
        plain("the attack in scenario 1 is not a hacker trick — it is a sentence in a ticket. Anything the AI reads "
              "can try to give it orders. Guardrails are not inside the model; they are the code you put around it.")
