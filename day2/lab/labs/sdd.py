"""Lab 1 — Prompt vs Spec (spec-driven development). Same AI, same contract, same 5 hidden test releases."""
import streamlit as st

from common import chat, extract_code, info_line, plain, live, not_live_warning, FRONTIER, MINI, available_models
from labs import sdd_replay

LAB = "Lab 1 · Prompt vs Spec"

CONTRACT = """Write a Python function `evaluate_release(release: dict) -> dict`.
The input dict has these keys:
- version (str), module (str)
- safety_rated (bool): True if the module is safety-rated
- test_pass_rate (float): percentage of tests passed, 0 to 100
- open_sev1 (int), open_sev2 (int): number of open Severity-1 and Severity-2 defects
- max_cvss (float): highest CVSS score among open vulnerabilities, 0 to 10
- cve_network_facing (bool): True if that vulnerability is in a network-facing component
Return {"verdict": "GO" or "NO-GO", "reasons": [short strings]}.
Use only the Python standard library. Return only the code in one ```python block."""

VAGUE = "Build a release readiness checker for our firmware releases. It should tell us whether a release is GO or NO-GO."

SPEC = """PURPOSE: Decide GO / NO-GO for AX900 firmware releases at Axion Controls.
USERS: Release managers, before the steering committee.

BUSINESS RULES (all must pass for GO):
R1. Safety-rated modules need a test pass rate of at least 98.0%. Other modules need at least 94.0%.
R2. Any open Sev-1 defect -> NO-GO.
R3. More than 3 open Sev-2 defects -> NO-GO. Three or fewer is acceptable.
R4. Any vulnerability with CVSS 6.5 or higher in a network-facing component -> NO-GO, even if a fix is planned.
    Vulnerabilities in components that are not network-facing are allowed up to CVSS 8.9.

ACCEPTANCE TESTS:
- Safety-rated, 99% pass, nothing open -> GO
- Safety-rated, 96.5% pass -> NO-GO (R1)
- Not safety-rated, 94.5% pass, 2 open Sev-2 -> GO
- CVSS 6.8, network-facing -> NO-GO (R4)

OUT OF SCOPE: user interface, saving data.
Every NO-GO reason must name the rule number (R1 to R4)."""

# The 5 hidden test releases. The AI never sees these.
CASES = [
    dict(version="4.2.0", module="Safety Controller", safety_rated=True, test_pass_rate=99.1, open_sev1=0, open_sev2=1,
         max_cvss=3.1, cve_network_facing=False),
    dict(version="4.2.0", module="Safety I/O", safety_rated=True, test_pass_rate=97.0, open_sev1=0, open_sev2=0,
         max_cvss=2.0, cve_network_facing=False),
    dict(version="4.2.0", module="Ethernet Comms", safety_rated=False, test_pass_rate=95.8, open_sev1=0, open_sev2=2,
         max_cvss=6.6, cve_network_facing=True),
    dict(version="4.2.0", module="HMI Panel", safety_rated=False, test_pass_rate=94.3, open_sev1=0, open_sev2=3,
         max_cvss=5.0, cve_network_facing=False),
    dict(version="4.2.0", module="Drive Interface", safety_rated=False, test_pass_rate=98.8, open_sev1=0, open_sev2=4,
         max_cvss=0.0, cve_network_facing=False),
]
EXPECTED = [("GO", "All rules pass."),
            ("NO-GO", "R1: safety-rated module needs 98%; it has 97%."),
            ("NO-GO", "R4: CVSS 6.6 in a network-facing component (limit 6.5)."),
            ("GO", "94.3% is above the 94% limit for non-safety modules; 3 Sev-2 is allowed."),
            ("NO-GO", "R3: 4 open Sev-2 defects (limit 3).")]


def run_cases(code):
    ns = {}
    exec(compile(code, "ai_generated", "exec"), ns)
    fn = ns.get("evaluate_release")
    if not fn:
        raise ValueError("The AI did not write a function called evaluate_release.")
    out = []
    for c in CASES:
        try:
            r = fn(dict(c))
            v = str(r.get("verdict", "?")).upper().replace("_", "-").replace(" ", "-")
            v = "NO-GO" if "NO" in v else ("GO" if "GO" in v else v)
            out.append((v, "; ".join(map(str, r.get("reasons", []))) or "—"))
        except Exception as e:
            out.append(("ERROR", str(e)[:120]))
    return out


def board(results, reveal):
    score = sum(r[0] == e[0] for r, e in zip(results, EXPECTED))
    cols = st.columns(5)
    for i, (c, (v, why)) in enumerate(zip(CASES, results)):
        ok = v == EXPECTED[i][0]
        colour = "#2F7D4F" if v == "GO" else ("#B3432B" if v == "NO-GO" else "#777")
        border = ("4px solid #2F7D4F" if ok else "4px solid #B3432B") if reveal else "1px solid #C6CBC6"
        cols[i].markdown(
            f"<div style='border:{border};border-radius:8px;padding:10px;min-height:250px;background:#fff'>"
            f"<div style='font-size:.8rem;color:#4A5157'>Release {i+1}</div><b>{c['module']}</b><br>"
            f"<span style='font-size:.82rem'>{'🛡️ safety-rated' if c['safety_rated'] else 'standard'} · "
            f"pass {c['test_pass_rate']}%<br>Sev-1: {c['open_sev1']} · Sev-2: {c['open_sev2']}<br>"
            f"CVSS {c['max_cvss']} {'🌐 network' if c['cve_network_facing'] else ''}</span>"
            f"<div style='margin:8px 0;padding:6px;text-align:center;color:#fff;font-weight:700;border-radius:4px;"
            f"background:{colour}'>{v}</div><div style='font-size:.75rem;color:#4A5157'>{why[:140]}</div>"
            + (f"<div style='font-size:.75rem;margin-top:6px'><b>{'✅' if ok else '❌'} Correct: {EXPECTED[i][0]}</b>"
               f"<br>{EXPECTED[i][1]}</div>" if reveal else "") + "</div>", unsafe_allow_html=True)
    return score


def round_ui(key, title, default_prompt, help_text):
    st.markdown(f"### {title}")
    st.caption(help_text)
    prompt = st.text_area("Your instruction to the AI", default_prompt, height=110 if key == "vague" else 330,
                          key=f"prompt_{key}")
    with st.expander("Build contract — added automatically, the same in both rounds (it has no business rules)"):
        st.code(CONTRACT, language=None)
    c1, c2 = st.columns([1, 1])
    build = c1.button(f"🔨 Build", key=f"build_{key}", type="primary", disabled=not live())
    replay = c2.button("▶ Replay a saved run", key=f"replay_{key}")
    if build:
        with st.spinner("The AI is writing the code… (20–40 seconds)"):
            try:
                text, info = chat([{"role": "user", "content": prompt + "\n\n" + CONTRACT}],
                                  model=st.session_state.get("sdd_model", FRONTIER), step=f"build ({key})", lab=LAB)
                st.session_state[f"sdd_{key}"] = dict(code=extract_code(text), info=info_line(info))
            except Exception as e:
                st.error(f"The model call failed: {e}. Click Replay to continue with a saved run.")
    if replay:
        st.session_state[f"sdd_{key}"] = dict(code=sdd_replay.CODE[key], info="▶ Replay of a saved run (no model call)")
    res = st.session_state.get(f"sdd_{key}")
    if res:
        lines = len([l for l in res["code"].splitlines() if l.strip()])
        st.caption(f"{res['info']} · 📄 {lines} lines of code")
        with st.expander("See the code the AI wrote"):
            st.code(res["code"], language="python")
        try:
            res["results"] = run_cases(res["code"])
        except Exception as e:
            st.error(f"The AI's code did not run: {e}")
            return None
        st.markdown("**The 5 test releases (the AI never saw these):**")
        score = board(res["results"], st.session_state.get("sdd_reveal", False))
        res["score"] = score
        return res
    return None


def show():
    st.title("🧪 Lab 1 · Prompt vs Spec")
    st.markdown("Same AI. Same build contract. Same five test releases. **The only difference is what you tell it.**")
    if not live():
        not_live_warning()
    with st.sidebar:
        st.selectbox("Model that writes the code", [m for m in [FRONTIER, MINI] if m in available_models()] or [FRONTIER],
                     key="sdd_model")
    st.info("**Predict first (pair):** the vague prompt will score ___ / 5 and the spec will score ___ / 5. "
            "Write it on the course page.")
    t1, t2 = st.tabs(["Round 1 · Vague prompt", "Round 2 · Specification"])
    with t1:
        r1 = round_ui("vague", "Round 1 — the way most people ask", VAGUE,
                      "Click Build. Do not change the prompt. Then look at the verdicts.")
    with t2:
        r2 = round_ui("spec", "Round 2 — a one-page specification", SPEC,
                      "Read the rules. These are Axion's own rules — no AI can guess them. Click Build.")
    st.divider()
    st.toggle("🔍 Reveal the correct answers", key="sdd_reveal")
    if st.session_state.get("sdd_reveal"):
        s1 = st.session_state.get("sdd_vague", {}).get("score")
        s2 = st.session_state.get("sdd_spec", {}).get("score")
        c1, c2 = st.columns(2)
        c1.metric("Vague prompt", f"{s1} / 5" if s1 is not None else "not built")
        c2.metric("Specification", f"{s2} / 5" if s2 is not None else "not built")
        st.markdown("**Enter both scores in AhaSlides.**")
        plain("The AI was equally clever in both rounds. In round 1 it filled the gaps with sensible guesses "
              "(like 95% for every module) — and sensible guesses gave a **green GO to a safety module that fails "
              "Axion's 98% rule**. The spec did not make the AI smarter; it gave it the knowledge only your team has. "
              "And the acceptance tests inside the spec are how you check the AI's work.")
        with st.expander("Twist (2 minutes): the policy changes — safety modules now need 99%"):
            st.markdown("Spec team: change one number in R1 and click Build again. Vague-prompt team: what would you "
                        "even change? **A spec is a living asset; a prompt is a one-time wish.**")
