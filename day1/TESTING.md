# Day 1 End-to-End Test Plan — all green before sleep
*ABB AI Engineering for Managers · test on the golden VM, 11 Nov 2026 evening.*
*Work top to bottom. Every box must be ✅ before cloning the VM image 18×.*

## Phase 0 — Golden VM prep

- [ ] Python 3.11+ present: `python --version`
- [ ] `pip install openai numpy pandas jupyter streamlit`
- [ ] Repo cloned at `Documents\abb-ai-engineering`
- [ ] Machine-wide env vars set (System → Environment Variables), then **open a NEW terminal/VS Code**:
  - `FOUNDRY_ENDPOINT` — the Foundry/Azure OpenAI endpoint URL
  - `FOUNDRY_API_KEY`
  - `MODEL_MINI` — the gpt-5.4-mini deployment name (2M TPM)
  - `MODEL_FRONTIER` — the frontier deployment name
  - `MODEL_EMBED` — embedding deployment name (default text-embedding-3-small)
- [ ] `PRICE` table edited in all 4 notebooks + `app.py` to the real per-1M-token rates of both deployments
- [ ] VS Code opens `labs/lab1_stand_up_and_compare.ipynb` and the Jupyter kernel starts

## Phase 1 — Notebooks (Run All, in order)

### Lab 1 (~3 min runtime)
- [ ] Setup cell prints "Client ready" with both model names
- [ ] 1.1 returns a one-sentence answer with latency/tokens/cost line
- [ ] 1.3 comparison table shows frontier cost **higher** than mini
- [ ] 1.5 prints `LAB1|mini_per_1k=...|frontier_per_1k=...`

### Lab 2 (~5 min)
- [ ] Bake-off table renders: 4 rows, quality_pct and cost columns filled
- [ ] V1 naive scores low (that's the lesson, not a bug); V3/V4 catch the SB-2025-04 ticket
- [ ] 2.6 prints `LAB2|best=V?|quality=..|cost_100k=..`

### Lab 3 (~6 min)
- [ ] 3.1 loads **14 documents**
- [ ] 3.3 builds index (~38 chunks)
- [ ] 3.4 F-07 question: answer cites SB-2025-04 / firmware 2.4.1, says don't buy the fan kit
- [ ] BREAK 1: 8,000-char chunks show **more** input tokens than 1,200-char
- [ ] BREAK 2: k=1 misses the session-limit answer, k=5 gets it (needs optipanel + release notes)
- [ ] BREAK 3: multi-hop question fails or waffles — expected, it's the M5 setup
- [ ] 3.6 saves `rag_index.npz` + `rag_chunks.json` (check files exist in `labs/`)
- [ ] 3.7 prints `LAB3|tokens_tuned=..|tokens_big=..` (tuned < big)

### Lab 4 (~8 min — three eval runs)
- [ ] 4.1 loads the saved index (if it errors, Lab 3 wasn't run in this folder)
- [ ] 4.2 guardrail: ALLOW on fault questions, BLOCK on injection + salary question
- [ ] 4.3 groundedness: PASS on real answer, FAIL on fabricated PSU answer
- [ ] 4.4 baseline prints a score (expect roughly 60–90%)
- [ ] 4.5 improved run prints delta (any direction is fine; the mechanism is the lesson)
- [ ] 4.7 prints `LAB4|baseline=..|improved=..`

## Phase 2 — Course page (index.html)

Open in the browser (double-click is fine; GitHub Pages once pushed):
- [ ] Saira fonts load (needs internet), hazard stripe + nav render
- [ ] Every nav item jumps to its section; score chip shows 0 / 16
- [ ] Click a quiz answer → instant right/wrong + explanation; score chip ticks up
- [ ] Paste each of the four LAB result lines into its Paste & check box → ✔ Checked
- [ ] Paste garbage into a box → ✘ with a helpful message
- [ ] **Refresh the page** → quiz answers and ✔ marks survive
- [ ] "Copy my result" fills clipboard; "Reset this page" clears everything
- [ ] Final score reads 16 / 16

## Phase 3 — Streamlit demo

- [ ] `streamlit run app.py` from the repo root (needs `corpus/` beside it)
- [ ] First question triggers one-time indexing (~20 s), then answers
- [ ] F-07 sidebar question → cites SB-2025-04, metrics row shows latency/tokens/cost
- [ ] Leave it indexed — the cache makes the in-room demo instant

## Phase 4 — Infrastructure (before cloning)

- [ ] Bastion shareable link opens a desktop on a NORMAL laptop/browser (the one test that settles everything)
- [ ] TPM quota on the mini deployment confirmed at 20 lakh (2M)
- [ ] VM auto-shutdown schedule + budget alert active
- [ ] After image-clone: spot-check 2 of the 18 VMs with Lab 1 only
- [ ] Seat cards printed: VM name, link, username, password

## If something goes red

| Symptom | Likely cause | Fix |
|---|---|---|
| Setup cell assertion error | Env vars not visible | Set machine-wide, reopen VS Code |
| `(retrying in 5s: ...)` lines then success | Brief rate limit | Fine — that's the retry working |
| 401/403 errors | Wrong key or endpoint | Re-check FOUNDRY_* values |
| 404 model not found | Deployment name ≠ MODEL_MINI value | Use the deployment name, not the model family name |
| Lab 4 file-not-found | Lab 3 not run from same folder | Run Lab 3 fully first |
| Fonts look wrong on page | No internet on test machine | Cosmetic only; fine in the room |
| Quiz/paste state not surviving refresh | Opened via file:// in a hardened browser | Works on GitHub Pages / normal Chrome |
