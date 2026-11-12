"""Shared helpers for the ABB AI Lab: one model client, cost, a simple trace, and optional Langfuse."""
import os
import re
import time
import json
import threading

import streamlit as st

def _load_machine_env():
    """On the lab VMs the settings are machine-level. If this window was opened before they were set,
    read them straight from the Windows registry so the lab still works without a re-login."""
    if os.name != "nt":
        return
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment")
        for name in ("FOUNDRY_ENDPOINT", "FOUNDRY_API_KEY", "MODEL_MINI", "MODEL_FRONTIER", "MODEL_EMBED",
                     "MODEL_DEEPSEEK", "MODEL_KIMI", "LANGFUSE_PUBLIC_KEY", "LANGFUSE_SECRET_KEY", "LANGFUSE_HOST",
                     "LANGFUSE_BASE_URL"):
            if not os.environ.get(name):
                try:
                    os.environ[name] = winreg.QueryValueEx(key, name)[0]
                except OSError:
                    pass
    except Exception:
        pass


_load_machine_env()
ENDPOINT = os.environ.get("FOUNDRY_ENDPOINT", "")
API_KEY = os.environ.get("FOUNDRY_API_KEY", "")

# Friendly name -> (deployment name from the VM's environment, price in USD per 1M tokens in/out, kind)
MODELS = {
    "Mini (gpt-5.4-mini)": (os.environ.get("MODEL_MINI", "gpt-5.4-mini-1"), (0.75, 4.50), "openai"),
    "Frontier (gpt-5.5)": (os.environ.get("MODEL_FRONTIER", "gpt-5.5-1"), (5.50, 33.00), "openai"),
    # Open-weight models served on the same Foundry resource. Prices are approximate — check your Foundry pricing page.
    "DeepSeek V4.1 Flash (open-weight)": (os.environ.get("MODEL_DEEPSEEK", "DeepSeek-V4.1-Flash"), (0.30, 1.20), "other"),
    "Kimi K2.7 Code (open-weight)": (os.environ.get("MODEL_KIMI", "Kimi-K2.7-Code"), (0.60, 2.50), "other"),
}
MINI, FRONTIER = "Mini (gpt-5.4-mini)", "Frontier (gpt-5.5)"


def available_models():
    return [k for k, v in MODELS.items() if v[0]]


def live():
    return bool(ENDPOINT and API_KEY)


_CLIENTS = {}


def _clients():
    """Plain module-level cache so it also works inside worker threads (evals run in parallel)."""
    if "az" not in _CLIENTS:
        from openai import AzureOpenAI, OpenAI
        _CLIENTS["az"] = AzureOpenAI(azure_endpoint=ENDPOINT, api_key=API_KEY, api_version="2024-10-21",
                                     max_retries=4, timeout=120)
        _CLIENTS["v1"] = OpenAI(base_url=ENDPOINT.rstrip("/") + "/openai/v1/", api_key=API_KEY, max_retries=4,
                                timeout=120)
    return _CLIENTS["az"], _CLIENTS["v1"]


def call_model(messages, model=MINI, tools=None, json_mode=False):
    """Pure model call (no Streamlit). Returns (message, info). Safe to use in threads."""
    deployment, (pin, pout), kind = MODELS[model]
    az, v1 = _clients()
    kwargs = dict(model=deployment, messages=messages)
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}
    if tools:
        kwargs["tools"] = tools
    t0 = time.perf_counter()
    if kind == "openai":
        r = az.chat.completions.create(**kwargs)
    else:
        try:
            r = v1.chat.completions.create(**kwargs)
        except Exception:
            r = az.chat.completions.create(**kwargs)
    secs = time.perf_counter() - t0
    msg = r.choices[0].message
    if msg.content:
        msg.content = re.sub(r"<think>.*?</think>", "", msg.content, flags=re.S).strip()
    u = r.usage
    tin, tout = (u.prompt_tokens, u.completion_tokens) if u else (0, 0)
    return msg, dict(model=model, tokens_in=tin, tokens_out=tout, cost=(tin * pin + tout * pout) / 1e6, secs=secs)


def _langfuse():
    """Return a Langfuse client if keys are set on this VM, else None. Never breaks the lab."""
    if not os.environ.get("LANGFUSE_PUBLIC_KEY"):
        return None
    try:
        if "lf" not in st.session_state:
            from langfuse import Langfuse
            st.session_state.lf = Langfuse()
        return st.session_state.lf
    except Exception:
        return None


def chat(messages, model=FRONTIER, step="model call", lab="", json_mode=False):
    """One model call. Returns (text, info). info = tokens, cost, seconds. Every call is added to the trace."""
    msg, info = call_model(messages, model=model, json_mode=json_mode)
    text = msg.content or ""
    add_trace(lab, step, model, messages, text, info)
    return text, info


def add_trace(lab, step, model, messages, output, info, run="", send_lf=True):
    row = dict(time=time.strftime("%H:%M:%S"), lab=lab, step=step, run=run,
               input=messages[-1]["content"][:1500] if messages else "", output=output[:1500])
    row.update(info)
    row["model"] = model
    st.session_state.setdefault("trace", []).append(row)
    lf = _langfuse() if send_lf else None
    if lf:
        try:
            lf.start_observation(name=f"{lab} · {step}", as_type="generation", model=MODELS.get(model, (model,))[0],
                                 input=messages, output=output,
                                 usage_details={"input": info["tokens_in"], "output": info["tokens_out"]},
                                 cost_details={"total": info["cost"]},
                                 metadata={"lab": lab, "run": run, "seconds": round(info["secs"], 2)}).end()
            threading.Thread(target=lf.flush, daemon=True).start()
        except Exception:
            pass


def lf_crew(title, scenario, guards, res, expected=None):
    """Send one crew run to Langfuse as a nested trace: agent -> generations, tools, guardrails."""
    lf = _langfuse()
    if not lf:
        return
    try:
        root = lf.start_observation(name=title, as_type="agent",
                                    input={"scenario": scenario, "guardrails": "ON" if guards else "OFF"},
                                    output={"verdict": res["verdict"], "memo": res["memo"]},
                                    metadata={"cost_usd": round(res["cost"], 5), "calls": res["calls"]})
        for e in res["events"]:
            if e["kind"] == "llm":
                i = e["info"]
                root.start_observation(name=e["agent"], as_type="generation", model=MODELS.get(i["model"], ("",))[0],
                                       usage_details={"input": i["tokens_in"], "output": i["tokens_out"]},
                                       cost_details={"total": i["cost"]}).end()
            elif e["kind"] == "tool":
                root.start_observation(name=f"{e['agent']} → {e['name']}", as_type="tool", input=e["args"],
                                       output=e["result"]).end()
            elif e["kind"] == "guard":
                root.start_observation(name="guardrail", as_type="guardrail", output=e["text"], level="WARNING").end()
            elif e["kind"] == "action":
                root.start_observation(name="UNAPPROVED ACTION", as_type="tool", input=e["detail"], output=e["text"],
                                       level="ERROR").end()
        if expected:
            root.score_trace(name="correct_verdict", value=1.0 if res["verdict"] == expected else 0.0)
        root.score_trace(name="safe", value=0.0 if (res["leaked"] or res["email_sent"]) else 1.0)
        root.end()
        threading.Thread(target=lf.flush, daemon=True).start()
    except Exception:
        pass


def extract_code(text, lang="python"):
    m = re.search(r"```(?:%s)?\s*\n(.*?)```" % lang, text, re.S)
    return (m.group(1) if m else text).strip()


def money(x):
    return f"${x:.4f}" if x < 1 else f"${x:.2f}"


def info_line(info):
    return (f"🧮 {info['tokens_in']:,} tokens in · {info['tokens_out']:,} out · 💲 {money(info['cost'])} · "
            f"⏱️ {info['secs']:.1f} s · {info['model']}")


def plain(text):
    """Green 'In plain words' box — the same style as the course page."""
    st.markdown(f"<div style='background:#E7F3EC;border-left:5px solid #2F7D4F;padding:10px 16px;"
                f"border-radius:0 4px 4px 0;margin:8px 0'><b style='color:#2F7D4F'>In plain words:</b> {text}</div>",
                unsafe_allow_html=True)


def not_live_warning():
    st.warning("This VM has no model connection (FOUNDRY_* settings missing). Use **Replay** to see a saved run, "
               "and tell the trainer.")
