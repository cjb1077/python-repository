import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from db import init_db
from ingest import ingest_pdf
from retriever import search_similar


# Main streamlit application - this creates the UI and also contains the system messaging telling the chatbot how to
# interact with the user. Using ChatGPT 4o mini. ### IN PROGRESS ###
load_dotenv()

st.set_page_config(page_title="RAG Starter", page_icon="📚")

# Config inputs
with st.sidebar:
    st.header("Settings")
    if st.button("Initialize DB / Indexes"):
        init_db()
        st.success("Database ready.")


    st.subheader("OpenAI")
    api_key = st.text_input("OPENAI_KEY", os.getenv("OPENAI_KEY", ""), type="password")
    if api_key:
        os.environ["OPENAI_KEY"] = api_key
    embed_model = st.text_input("Embedding model", os.getenv("EMBED_MODEL", "text-embedding-3-small"))
    chat_model = st.text_input("Chat model", os.getenv("CHAT_MODEL", "gpt-4o-mini"))


    st.subheader("Ingest a PDF")
    uploaded = st.file_uploader("Upload .pdf", type=["pdf"])
    if uploaded is not None:
        tmp_path = f"/tmp/{uploaded.name}"
        with open(tmp_path, "wb") as f:
            f.write(uploaded.read())
        if st.button("Ingest PDF"):
            ingest_pdf(tmp_path)
            st.success(f"Ingested {uploaded.name}")


st.title("📚 Simple RAG Chatbot (Streamlit + Postgres)")
question = st.text_input("Ask a question about your PDFs:")

### IN PROGRESS ###

# call search_similar with question from user
if st.button("Search & Answer", disabled=not question):
    contexts = search_similar(question, k=100)


    st.subheader("Top Chunks")
    for i, (txt, dist) in enumerate(contexts, 1):
        with st.expander(f"Chunk {i} (distance={dist:.4f})", expanded=(i==1)):
            st.write(txt)


    if os.getenv("OPENAI_KEY"):
        client = OpenAI(api_key=os.getenv("OPENAI_KEY"))
        system = "You are a helpful assistant. Answer according to the documents given to you. Give any helpful information you can."
        context_text = "\n\n".join([c[0] for c in contexts])
        user = f"Question: {question}\n\nContext:\n{context_text}"
        resp = client.chat.completions.create(
            model=os.getenv("CHAT_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.9,
        )
        st.subheader("Answer")
        st.write(resp.choices[0].message.content)
    else:
        st.info("Provide an OPENAI_KEY in the sidebar to generate an answer. Retrieval still works.")



