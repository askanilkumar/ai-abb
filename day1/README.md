# AI Engineering for Managers — ABB Bangalore · 12–13 Nov 2026

Course repository. Day 1: Choose and Build.

## Layout

| Path | What it is |
|---|---|
| `index.html` | Day 1 course page (serve via GitHub Pages) |
| `labs/lab1_stand_up_and_compare.ipynb` | Lab 1 · model comparison (09:55) |
| `labs/lab2_prompt_designs_measured.ipynb` | Lab 2 · four prompt designs (11:30) |
| `labs/lab3_build_the_rag_pipeline.ipynb` | Lab 3 · RAG build + break-and-fix (13:45) |
| `labs/lab4_make_it_trustworthy.ipynb` | Lab 4 · guardrails + evals (15:30) |
| `corpus/` | 14 synthetic Axion Controls documents + `service_tickets.csv` (200 rows) |
| `data/eval_seed.json` | 8 starter eval questions + the M5 multi-hop demo question |
| `frameworks/` | Editable takeaway templates: decision tree, prompt patterns, RAG reference, eval design sheet, zero-licence framework |
| `app.py` | Streamlit demo — the Lab 3 pipeline with a UI ("what your team ships"). `streamlit run app.py` |
| `generate_tickets.py` | Regenerates the ticket CSV (seeded, deterministic) |
| `build_notebooks.py` | Regenerates the four notebooks |

## VM prerequisites (golden image)

- Python 3.11+, `pip install openai numpy pandas jupyter streamlit`
- VS Code + Python + Jupyter extensions, repo cloned to `Documents\abb-ai-engineering`
- Environment variables set machine-wide:
  - `FOUNDRY_ENDPOINT` — Azure OpenAI / Foundry serverless endpoint
  - `FOUNDRY_API_KEY`
  - `MODEL_MINI` (default `gpt-4o-mini`), `MODEL_FRONTIER` (default `gpt-4o`), `MODEL_EMBED` (default `text-embedding-3-small`)
- The setup cell in every notebook auto-detects Azure vs OpenAI-compatible endpoints.
- Edit the `PRICE` table in the notebooks to match the actual deployment prices before Day 1.

## Planted patterns in the corpus (trainer notes)

- **SB-2025-04**: 28 F-07 tickets on VectorDrive fw < 2.4.1 at ≥ 8 kHz — used in Labs 1–3 and the M5 graph demo.
- **SB-2026-01**: 14 E-22 tickets on AX-900 fw ≤ 3.2 — used in Lab 2 classification.
- The M5 multi-hop question (tickets × bulletin × release notes join) is in `data/eval_seed.json`.

Everything is fictional. No ABB data anywhere.
