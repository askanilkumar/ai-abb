"""Lab 2 — Build your own RAG app in 10 minutes. The AI writes it, the lab saves and starts it for you."""
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import streamlit as st

from common import chat, extract_code, info_line, plain, live, not_live_warning, FRONTIER
from labs import rag_replay

LAB = "Lab 2 · Build your RAG"
PORT = 8601
HERE = Path(__file__).resolve().parent
PDF = HERE.parent.parent / "build-your-rag" / "Axion_HR_Policy.pdf"
ARCH = HERE.parent.parent / "build-your-rag" / "rag_architecture.png"
MY = Path(os.path.expanduser("~")) / "Desktop" / "my-rag"

PROMPT = """Write a complete Python Streamlit app in ONE file called app.py. It is a "Chat with my PDF" app that uses RAG (retrieval-augmented generation).

THE MACHINE IS ALREADY SET UP. These environment variables exist. Do not ask me for keys and do not use a .env file:
- FOUNDRY_ENDPOINT and FOUNDRY_API_KEY: an Azure AI Foundry endpoint and its key
- MODEL_MINI: the chat model deployment name
- MODEL_EMBED: the embedding model deployment name

Use only these libraries: streamlit, openai, pypdf, numpy.
Create the client exactly like this:
    from openai import AzureOpenAI
    client = AzureOpenAI(azure_endpoint=os.environ["FOUNDRY_ENDPOINT"], api_key=os.environ["FOUNDRY_API_KEY"], api_version="2024-10-21")
Do NOT pass temperature or max_tokens to the model.

WHAT THE APP MUST DO:
1. Use st.set_page_config(layout="wide"). Page title: "📄 {NAME} – Chat with my PDF".
2. In the sidebar, a PDF file uploader.
3. When a PDF is uploaded: read the text of every page with pypdf. Split each page's text into chunks of about 800 characters with 100 characters of overlap. Keep the page number with every chunk.
4. Create embeddings for all chunks in one call: client.embeddings.create(model=os.environ["MODEL_EMBED"], input=list_of_chunk_texts). Store the chunks and vectors (a NumPy array) in st.session_state so this happens only once per file. Show "Indexed N chunks from M pages" in the sidebar.
5. Two tabs: "🏗️ How RAG works" and "💬 Chat".
6. Tab "How RAG works": show the picture rag_architecture.png that is in the same folder as app.py (build the path with os.path.dirname(os.path.abspath(__file__))) using st.image(path, caption="Reference architecture of a production RAG system"). If the file is missing, show st.info.
7. Tab "Chat": two columns with widths [3, 1].
   Left column: the chat. Show the messages inside st.container(height=480) using st.chat_message, keep the chat history in st.session_state, and put st.chat_input in the left column below that container.
   Right column: a panel titled "🔧 Under the hood" showing: the embedding model name (MODEL_EMBED); the embedding size (how many numbers are in one vector); the vector store: "In-memory NumPy array in st.session_state (no vector database)"; how many vectors are stored; similarity: cosine; chunks retrieved per question: 3; the chat model name (MODEL_MINI).
8. For every question: embed the question, find the 3 most similar chunks using cosine similarity with numpy, and call client.chat.completions.create(model=os.environ["MODEL_MINI"], messages=[...]) with this system message: "Answer only from the context. If the answer is not in the context, say: I could not find this in the document. Mention the page number."
9. Under every answer, an expander called "Sources" that shows the 3 chunks with their page number and similarity score.
10. Wrap the model calls in try/except and show any error with st.error.

Keep the code short and simple, with comments in plain English. Return only the complete code in one block."""

LEVEL_UPS = {
    "💲 Show the cost of every answer": "Add to my app: under every answer, show the input tokens, output tokens and the cost of that answer in US dollars (USD 0.75 per 1 million input tokens, USD 4.50 per 1 million output tokens). Show the total cost of the session in the sidebar. Give me the complete app.py.",
    "🔎 Show what was sent to the model": "Add to my app: an expander 'What was sent to the model' under every answer, showing the exact system and user messages. Add a sidebar slider 'Chunks to retrieve' from 1 to 8 (default 3). Give me the complete app.py.",
    "🛑 Refuse weak matches": "Add to my app: if the best similarity score is below 0.30, do not call the chat model. Reply 'I could not find this in the document.' and show the best score. Add a sidebar slider for this threshold (0.0 to 0.9). Give me the complete app.py.",
}


def _stop_old():
    pid_file = MY / ".pid"
    if pid_file.exists():
        try:
            pid = int(pid_file.read_text().strip())
            if os.name == "nt":
                subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], capture_output=True)
            else:
                os.kill(pid, 9)
        except Exception:
            pass


def save_and_start(code):
    MY.mkdir(parents=True, exist_ok=True)
    for f in (PDF, ARCH):
        if f.exists() and not (MY / f.name).exists():
            shutil.copy(f, MY / f.name)
    (MY / "app.py").write_text(code, encoding="utf-8")
    compile(code, "app.py", "exec")            # raises SyntaxError before we start anything
    _stop_old()
    flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    p = subprocess.Popen([sys.executable, "-m", "streamlit", "run", str(MY / "app.py"), "--server.port", str(PORT),
                          "--server.headless", "true", "--browser.gatherUsageStats", "false"],
                         cwd=str(MY), creationflags=flags, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    (MY / ".pid").write_text(str(p.pid))
    time.sleep(4)


def ask(messages, step):
    text, info = chat(messages, model=FRONTIER, step=step, lab=LAB)
    messages.append({"role": "assistant", "content": text})
    return extract_code(text), info


def deliver(code, info_text):
    st.session_state.rag_code, st.session_state.rag_info = code, info_text
    try:
        save_and_start(code)
        st.session_state.rag_err = ""
    except SyntaxError as e:
        st.session_state.rag_err = f"SyntaxError on line {e.lineno}: {e.msg}"


def show():
    st.title("🛠️ Lab 2 · Build your own RAG in 10 minutes")
    st.markdown("You describe it. The AI writes it. This lab saves it on your VM and starts it. "
                "**You will not type a single line of code.**")
    if not live():
        not_live_warning()
    st.session_state.setdefault("rag_msgs", [])

    st.markdown("#### Step 1 · Put your name on it, read the instruction, then click Build")
    name = st.text_input("Your name (it goes into your app's title)", key="rag_name", placeholder="e.g. Priya")
    who = name.strip() or "My"
    prompt = st.text_area("Your instruction (a short specification)", PROMPT.replace("{NAME}", who), height=320)
    c1, c2 = st.columns(2)
    if c1.button("🔨 Build my app", type="primary", disabled=not live()):
        st.session_state.rag_msgs = [{"role": "user", "content": prompt}]
        with st.spinner("The AI is writing your app… (30–60 seconds)"):
            try:
                code, info = ask(st.session_state.rag_msgs, "build app")
                deliver(code, info_line(info))
            except Exception as e:
                st.error(f"The model call failed: {e}. Click Replay to continue.")
    if c2.button("▶ Replay a saved build"):
        deliver(rag_replay.CODE.replace('"📄 My – Chat with my PDF"', repr(f"📄 {who} – Chat with my PDF")),
                "▶ Replay of a saved build (no model call)")

    code = st.session_state.get("rag_code")
    if not code:
        return
    lines = len([l for l in code.splitlines() if l.strip()])
    st.success(f"Your app is written: **{lines} lines of code**. Saved to `Desktop\\my-rag\\app.py`.")
    st.caption(st.session_state.rag_info)
    with st.expander("See the code the AI wrote — can you find the 6 RAG steps?"):
        st.code(code, language="python")
    if st.session_state.get("rag_err"):
        st.error(f"The code has a mistake: {st.session_state.rag_err}. Click **Fix it** below.")
    else:
        st.markdown("#### Step 2 · Open your app")
        st.link_button("🚀 Open my app (new tab)", f"http://localhost:{PORT}", type="primary")
        st.markdown(f"In your app: tab **🏗️ How RAG works** shows the architecture. Then go to **💬 Chat**, upload "
                    f"**{PDF.name}** from the **my-rag** folder on your Desktop, and ask the 5 questions on the course "
                    "page. Open **Sources** each time, and watch **🔧 Under the hood** on the right.")

    st.markdown("#### Step 3 · If you see a red error in your app")
    err = st.text_area("Paste the error text here", value=st.session_state.get("rag_err", ""), height=80)
    if st.button("🩹 Fix it", disabled=not (live() and err.strip() and st.session_state.rag_msgs)):
        st.session_state.rag_msgs.append({"role": "user", "content": "My app gave this error. Find the cause and give "
                                          "me the complete corrected app.py (whole file). Keep all my rules.\n\nERROR:\n" + err})
        with st.spinner("The AI is fixing your app…"):
            code, info = ask(st.session_state.rag_msgs, "fix error")
            deliver(code, info_line(info))
        st.rerun()

    st.markdown("#### Finished early? Level up")
    cols = st.columns(3)
    for col, (label, up) in zip(cols, LEVEL_UPS.items()):
        if col.button(label, disabled=not (live() and st.session_state.rag_msgs)):
            st.session_state.rag_msgs.append({"role": "user", "content": up})
            with st.spinner("The AI is adding the feature…"):
                code, info = ask(st.session_state.rag_msgs, "level up")
                deliver(code, info_line(info))
            st.rerun()
    st.caption("After a level-up, refresh your app tab to see the new version.")

    with st.expander("What happened in the background", expanded=False):
        st.markdown("1. **Read** the PDF  2. **Chunk** it into pieces  3. **Embed** each piece (AI)  "
                    "4. **Search** for the 3 closest pieces  5. **Prompt** = pieces + question + rules  "
                    "6. **Answer** (AI). Only steps 3 and 6 use AI.")
        plain("the model never reads your PDF. It only sees the three pieces the search found. "
              "If the search picks the wrong pieces, even the best model gives a wrong answer.")
