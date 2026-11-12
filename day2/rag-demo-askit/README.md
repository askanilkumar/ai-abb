# AskIT — Advanced RAG demo (trainer-led, Day 2 Session 2)

Ported from the DXC Lab 3 build. Default provider is now **Azure AI Foundry (ABB)**, using the FOUNDRY_* and MODEL_* variables already on every lab VM. AWS Bedrock / OpenAI / Offline remain as fallbacks in the sidebar.

**Run:** double-click `run_demo.bat` (opens http://localhost:8502). Check first with `python check_setup.py`.

## 8-minute demo script
1. 🏗️ Architecture tab — the pipeline diagram.
2. 💬 Ask, **Compare with baseline** on: *What is the minimum password length?* → baseline quotes the old KB-001 v1.
3. Sidebar **Who is asking?** Employee vs Contractor: *Can I use a personal laptop for VPN access?*
4. *Which cafeteria serves vegan food on Fridays?* → FDE-grade says "I don't know".
5. 🧩 Ingestion → upload `sample_uploads\KB-099_printer_update_POISONED.md` → read the scan warning → ask *Where did the floor 3 printers move to?*
6. 📊 Evals → run Baseline and FDE-grade presets → compare scores. 💰 Usage & cost → cost per question.

Knowledge base: `data\kb\` (23 IT helpdesk articles, fictional).
