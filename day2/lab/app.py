"""ABB AI Lab — one app for all Day 2 labs. Start it from the desktop shortcut 'ABB AI Lab'."""
import importlib

import streamlit as st

st.set_page_config(page_title="ABB AI Lab", page_icon="🧪", layout="wide")
st.markdown("""<style>
.block-container{padding-top:3.2rem; max-width:1250px}
h1,h2,h3{font-family:'Saira Condensed',system-ui,sans-serif}
div[data-testid="stMetricValue"]{font-size:1.7rem}
</style>""", unsafe_allow_html=True)

from common import live  # noqa: E402

LABS = {
    "🏠 Start here": None,
    "1 · Prompt vs Spec": "labs.sdd",
    "2 · Build your RAG": "labs.build_rag",
    "3 · Agents + Guardrails": "labs.agents",
    "4 · Evals": "labs.evals",
    "5 · Observability": "labs.trace",
    "6 · Sprint Board (ADO)": "labs.sprint",
    "7 · Trade-offs": "labs.tradeoffs",
    "8 · Value Case": "labs.value",
    "9 · Break the Bot": "labs.breakbot",
}

STACK = ["Model", "Prompt / Spec", "Knowledge (RAG)", "Agents & tools", "Guardrails", "Evals", "Observability",
         "Architecture & cost", "Security", "Value"]
LAB_LAYER = {"1": 1, "2": 2, "3": 3, "4": 5, "5": 6, "6": 2, "7": 7, "8": 9, "9": 8}


def stack_bar(active=None):
    """The 10-layer AI stack from the course page; the layer this lab teaches is highlighted."""
    cells = "".join(
        f"<div style='flex:1;min-width:0;padding:5px 3px;text-align:center;font-size:.72rem;line-height:1.2;"
        f"font-weight:{700 if i == active else 500};border-radius:4px;"
        f"background:{'#E8A200' if i == active else '#EDEFED'};color:#22262A'>{i + 1}<br>{name}</div>"
        for i, name in enumerate(STACK))
    label = f"You are here: layer {active + 1} · {STACK[active]}" if active is not None else "The AI stack"
    st.markdown(f"<div style='font-size:.78rem;color:#4A5157;margin-bottom:3px'>🧭 AI stack — {label}</div>"
                f"<div style='display:flex;gap:4px;margin-bottom:12px'>{cells}</div>", unsafe_allow_html=True)


with st.sidebar:
    st.markdown("## 🧪 ABB AI Lab")
    choice = st.radio("Go to", list(LABS), label_visibility="collapsed")
    st.divider()
    st.caption("🟢 Model connection ready" if live() else "🟠 No model connection — Replay buttons still work")
    total = sum(t["cost"] for t in st.session_state.get("trace", []))
    st.caption(f"Model calls this session: {len(st.session_state.get('trace', []))} · cost ${total:.4f}")

num = choice.split(" ")[0]
stack_bar(LAB_LAYER.get(num))

if LABS[choice] is None:
    st.title("🧪 ABB AI Lab · Day 2")
    st.markdown("Every lab follows the same rhythm: **Predict → Click → See the result → Reveal → Decide.** "
                "Nothing to install, nothing to type except your ideas. Follow the course page for each lab.")
    st.markdown("""
| Lab | What you will see |
|---|---|
| 1 · Prompt vs Spec | The same AI scores very differently on 5 releases, depending only on what you tell it |
| 2 · Build your RAG | Your own "Chat with my PDF" app, written by AI, running on this VM |
| 3 · Agents + Guardrails | Five AI agents talking, using tools — and what happens when someone attacks them |
| 4 · Evals | One score card that tells you if your AI is good enough to ship |
| 5 · Observability | Every step, token and dollar your AI spent today |
| 6 · Sprint Board | Six charts vs three sentences: AI over Azure DevOps data |
| 7 · Trade-offs | Four models, one question — quality, speed and cost side by side |
| 8 · Value Case | How a wrong metric sells a false win — and your own value case |
| 9 · Break the Bot | Try to make a bot leak a secret |
""")
else:
    try:
        mod = importlib.import_module(LABS[choice])
        mod.show()
    except ModuleNotFoundError:
        st.title(choice)
        st.info("This lab opens later today. Follow the course page.")
