# The Zero-Licence Framework
*Day 1 close (16:45). Everything you built today, rebuilt on free and open-source components.
The architecture is the asset — not the licences.*

## Component mapping

| Today's lab used | Zero-licence equivalent | Notes |
|---|---|---|
| Azure AI Foundry serverless chat model | **Ollama** running an open model (e.g. Llama/Qwen/Mistral class) on a workstation or one GPU VM | Same OpenAI-compatible API — the lab code changes only `FOUNDRY_ENDPOINT` and model name |
| Foundry embedding model | **sentence-transformers** (e.g. `all-MiniLM-L6-v2`) locally | Embeddings become free; quality is good enough for most internal corpora — eval decides |
| NumPy in-memory index (labs) | Same NumPy — already free. At scale: **FAISS** or **Chroma** | Today's lab index IS already zero-licence |
| LLM-as-judge evals | Same pattern on the local model | Judge quality drops with smaller models — keep a frontier spot-check on a sample |
| Streamlit app (`app.py`) | Streamlit is already open source | No change |
| VS Code + Jupyter | Already free | No change |

## What actually changes

```python
# Day 1 lab code on Foundry:
client = OpenAI(base_url=os.environ["FOUNDRY_ENDPOINT"], api_key=os.environ["FOUNDRY_API_KEY"])

# Same code on Ollama (local):
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
```
One line. The chunking, retrieval, guardrails, evals — your actual IP — are untouched.

## What you trade

| You gain | You give up |
|---|---|
| Zero per-token cost | Hardware + ops become your problem |
| Data never leaves your network | Model quality ceiling (eval before trusting) |
| No vendor dependency | No provider-side caching, batching, quota management |
| Great for experimentation and sensitive pilots | Scaling beyond one box is real engineering |

## The honest decision rule

Zero-licence is **Tier 3** in the decision tree — choose it for data constraints or steady extreme
volume, not to avoid a bill that Lab 5 (tomorrow) will show you is smaller than you think.
Run the **same eval set** against the open model: if the score holds, the switch is defensible;
if it drops, you now know exactly what the licence was buying.

## Try it on the lab repo (after the course)

1. Install Ollama, pull a model: `ollama pull llama3.2`
2. `pip install sentence-transformers`
3. In the Lab 3 notebook: point `client` at Ollama, swap `embed()` for sentence-transformers.
4. Re-run Lab 4's eval. Compare the score to your Day 1 baseline. That comparison — not a blog
   post — is your answer.
