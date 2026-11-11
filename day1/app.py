"""Axion Service-Knowledge Assistant — the 'what your team ships' demo.

Thin Streamlit UI over the exact same pipeline built in Lab 3.
Run on the VM:  streamlit run app.py
(First run builds the index from corpus/ — takes ~20 seconds.)
"""
import os, json, time
from pathlib import Path

import numpy as np
import streamlit as st
from openai import OpenAI, AzureOpenAI

# ---------------- config (same as the labs) ----------------
ENDPOINT    = os.environ.get("FOUNDRY_ENDPOINT", "")
API_KEY     = os.environ.get("FOUNDRY_API_KEY", "")
MODEL_MINI  = os.environ.get("MODEL_MINI", "gpt-4o-mini")
MODEL_EMBED = os.environ.get("MODEL_EMBED", "text-embedding-3-small")
PRICE_IN, PRICE_OUT = 0.15, 0.60  # USD per 1M tokens — edit to your deployment

def get_client():
    if any(h in ENDPOINT for h in ("openai.azure.com", "cognitiveservices", "services.ai.azure.com")):
        return AzureOpenAI(azure_endpoint=ENDPOINT, api_key=API_KEY, api_version="2024-10-21")
    return OpenAI(base_url=ENDPOINT, api_key=API_KEY)

client = get_client()

def with_retry(fn, tries=3, wait=5):
    for a in range(tries):
        try:
            return fn()
        except Exception as e:
            if a == tries - 1: raise
            time.sleep(wait * (a + 1))

# ---------------- index (built once, cached) ----------------
def chunk_document(name, text, target_chars=1200, overlap=150):
    paras, chunks, buf = [p for p in text.split("\n\n") if p.strip()], [], ""
    for p in paras:
        if len(buf) + len(p) > target_chars and buf:
            chunks.append(buf.strip()); buf = buf[-overlap:] + "\n\n"
        buf += p + "\n\n"
    if buf.strip(): chunks.append(buf.strip())
    return [{"doc": name, "text": c} for c in chunks]

def embed(texts):
    r = with_retry(lambda: client.embeddings.create(model=MODEL_EMBED, input=texts))
    return np.array([d.embedding for d in r.data], dtype=np.float32)

@st.cache_resource(show_spinner="Indexing the corpus (one-time)…")
def build_index():
    docs = {p.name: p.read_text(encoding="utf-8") for p in sorted(Path("corpus").glob("*.md"))}
    chunks = [c for n, t in docs.items() for c in chunk_document(n, t)]
    vecs = [embed([c["text"] for c in chunks[i:i+64]]) for i in range(0, len(chunks), 64)]
    index = np.vstack(vecs)
    index /= np.linalg.norm(index, axis=1, keepdims=True)
    return chunks, index

SYSTEM = """You are the Axion Controls service-knowledge assistant.
Answer ONLY from the provided context. Cite sources as [doc-name].
If the context does not contain the answer, say exactly: "Not in the knowledge base — escalate to product support."
Structure: Answer / Why / Source."""

def answer(question, k):
    chunks, index = build_index()
    q = embed([question])[0]; q /= np.linalg.norm(q)
    top = np.argsort(-(index @ q))[:k]
    hits = [chunks[i] for i in top]
    context = "\n\n".join(f'[{h["doc"]}]\n{h["text"]}' for h in hits)
    t0 = time.perf_counter()
    r = with_retry(lambda: client.chat.completions.create(model=MODEL_MINI, temperature=0.2, messages=[
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}]))
    latency = time.perf_counter() - t0
    u = r.usage
    cost = (u.prompt_tokens * PRICE_IN + u.completion_tokens * PRICE_OUT) / 1e6
    return r.choices[0].message.content, hits, latency, u, cost

# ---------------- UI ----------------
st.set_page_config(page_title="Axion Service Assistant", page_icon="🔧", layout="centered")
st.title("🔧 Axion Service-Knowledge Assistant")
st.caption("The Lab 3 pipeline with a face on it — this is what your team ships. "
           "Synthetic corpus, no real data.")

with st.sidebar:
    st.header("Dials")
    k = st.slider("Chunks retrieved (k)", 1, 8, 4)
    st.markdown(f"**Model:** `{MODEL_MINI}`\n\n**Corpus:** 14 docs")
    st.markdown("---")
    st.markdown("Try:\n- *Drive trips F-07 hourly, filters clean, fw 2.3, 10 kHz — new fan kit?*\n"
                "- *What does E-22 mean?*\n- *How many OPC UA sessions does the AX-900 support?*")

question = st.text_input("Ask a service question", placeholder="e.g. Drive trips F-07 every hour…")

if question:
    if not (ENDPOINT and API_KEY):
        st.error("Model endpoint not configured — set FOUNDRY_ENDPOINT and FOUNDRY_API_KEY.")
    else:
        with st.spinner("Retrieving and answering…"):
            text, hits, latency, usage, cost = answer(question, k)
        st.markdown(text)
        c1, c2, c3 = st.columns(3)
        c1.metric("Latency", f"{latency:.1f}s")
        c2.metric("Tokens", f"{usage.prompt_tokens}↓ {usage.completion_tokens}↑")
        c3.metric("Cost", f"${cost:.5f}")
        with st.expander(f"Sources ({len(hits)} chunks)"):
            for h in hits:
                st.markdown(f"**{h['doc']}**")
                st.text(h["text"][:400])
