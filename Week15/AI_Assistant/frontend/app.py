"""
Simple Streamlit UI for the AI Assistant backend.
Talks to the FastAPI backend over the internal Docker network.
"""
import streamlit as st
import requests

BACKEND_URL = "http://backend:8000"  # internal Docker network hostname

st.set_page_config(page_title="AI Assistant", page_icon="🤖")
st.title("🤖 AI Assistant")

# ---- Sidebar: settings ----
with st.sidebar:
    st.header("Settings")
    provider = st.selectbox("Provider", ["local", "gemini", "openai"], index=0)
    use_tools = st.checkbox("Enable tool calling", value=False)
    temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
    max_tokens = st.slider("Max response length (tokens)", 128, 4096, 1024, 128)

    st.divider()
    st.header("RAG - Ingest a document")
    ingest_text = st.text_area("Paste text to add to knowledge base")
    source_name = st.text_input("Source label", value="pasted-text")
    if st.button("Ingest text"):
        if ingest_text.strip():
            resp = requests.post(
                f"{BACKEND_URL}/rag/ingest/text",
                json={"text": ingest_text, "source": source_name},
            )
            if resp.ok:
                st.success(f"Ingested {resp.json()['chunks_created']} chunk(s)")
            else:
                st.error(f"Failed: {resp.text}")

    uploaded_file = st.file_uploader("Or upload a .pdf / .txt file")
    if uploaded_file and st.button("Ingest file"):
        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
        resp = requests.post(f"{BACKEND_URL}/rag/ingest/file", files=files)
        if resp.ok:
            st.success(f"Ingested {resp.json()['chunks_created']} chunk(s) from {uploaded_file.name}")
        else:
            st.error(f"Failed: {resp.text}")

    st.divider()
    rag_mode = st.checkbox("Answer using ingested documents (RAG)", value=False)

# ---- Main chat area ----
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("chunks"):
            with st.expander("Retrieved context"):
                for c in msg["chunks"]:
                    st.caption(f"[{c['source']}] (distance: {c['distance']:.3f})")
                    st.text(c["text"])

user_input = st.chat_input("Ask something...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                if rag_mode:
                    resp = requests.post(
                        f"{BACKEND_URL}/rag/query",
                        json={"question": user_input, "provider": provider},
                        timeout=120,
                    )
                    resp.raise_for_status()
                    data = resp.json()
                    reply = data["answer"]
                    chunks = data["retrieved_chunks"]
                else:
                    resp = requests.post(
                        f"{BACKEND_URL}/chat",
                        json={
                            "message": user_input,
                            "provider": provider,
                            "temperature": temperature,
                            "max_tokens": max_tokens,
                            "use_tools": use_tools,
                        },
                        timeout=120,
                    )
                    resp.raise_for_status()
                    data = resp.json()
                    reply = data["reply"]
                    chunks = None

                st.markdown(reply)
                if chunks:
                    with st.expander("Retrieved context"):
                        for c in chunks:
                            st.caption(f"[{c['source']}] (distance: {c['distance']:.3f})")
                            st.text(c["text"])

                st.session_state.messages.append({"role": "assistant", "content": reply, "chunks": chunks})

            except requests.exceptions.RequestException as e:
                error_msg = f"Error contacting backend: {e}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
