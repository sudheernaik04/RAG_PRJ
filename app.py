from __future__ import annotations

from pathlib import Path

import streamlit as st

from core.model_selector import detect_ollama_models, select_ollama_model
from core.rag_pipeline import LocalRAGPipeline
from ui.components import render_retrieval_panel, render_status_badge
from ui.styles import get_styles

UPLOAD_DIR = Path(__file__).resolve().parent / "data" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def initialize_session_state() -> None:
    if "conversation" not in st.session_state:
        st.session_state.conversation = []
    if "pipeline" not in st.session_state:
        st.session_state.pipeline = LocalRAGPipeline()
    if "document_indexed" not in st.session_state:
        st.session_state.document_indexed = False
    if "document_metadata" not in st.session_state:
        st.session_state.document_metadata = {}


def process_uploaded_file(uploaded_file) -> None:
    pipeline = st.session_state.pipeline
    target_path = UPLOAD_DIR / uploaded_file.name
    target_path.write_bytes(uploaded_file.getvalue())

    with st.spinner("Extracting text, chunking content, and generating embeddings..."):
        try:
            metadata = pipeline.index_document(target_path)
            st.session_state.document_metadata = metadata
            st.session_state.document_indexed = True
            st.success(f"Document indexed successfully: {uploaded_file.name}")
        except Exception as exc:  # pragma: no cover - UI error path
            st.session_state.document_indexed = False
            st.session_state.document_metadata = {}
            st.error(f"Processing failed: {exc}")


def render_header() -> None:
    ollama_status = detect_ollama_models()
    selected_model = select_ollama_model(ollama_status.get("available_models", []))

    st.markdown(get_styles(), unsafe_allow_html=True)
    st.title("College RAG Workshop")
    st.caption("Upload a document, retrieve the most relevant passages, and ask grounded questions using a local LLM.")

    col1, col2, col3 = st.columns(3)
    with col1:
        render_status_badge("Ollama", "Connected" if ollama_status["connected"] else "Not connected", "ok" if ollama_status["connected"] else "bad")
    with col2:
        render_status_badge("Model", selected_model or "No suitable model", "ok" if selected_model else "warn")
    with col3:
        render_status_badge("Index", "Indexed" if st.session_state.document_indexed else "Not indexed", "ok" if st.session_state.document_indexed else "warn")

    if ollama_status["connected"]:
        detected = ", ".join(ollama_status.get("available_models", [])) or "No local models detected"
        st.caption(f"Detected Ollama models: {detected}")
    else:
        st.warning("Ollama is not running. Start Ollama locally before asking questions.")


def render_sidebar() -> None:
    st.sidebar.header("Workshop settings")
    st.sidebar.slider("Top-K", min_value=1, max_value=10, value=3, key="top_k")
    st.sidebar.slider("Similarity threshold", min_value=0.0, max_value=1.0, value=0.15, step=0.01, format="%.2f", key="min_similarity")
    st.sidebar.slider("Chunk size", min_value=100, max_value=800, value=400, step=50, key="chunk_size")
    st.sidebar.slider("Chunk overlap", min_value=0, max_value=200, value=80, step=10, key="chunk_overlap")
    st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.2, step=0.1, key="temperature")

    ollama_status = detect_ollama_models()
    selected_model = select_ollama_model(ollama_status.get("available_models", []))
    st.sidebar.subheader("Model status")
    if selected_model:
        st.sidebar.success(f"Selected model: {selected_model}")
    else:
        st.sidebar.warning("No Qwen or Llama model was detected. Install one from the setup instructions before continuing.")


def render_document_panel() -> None:
    uploaded_file = st.file_uploader("Upload a PDF or DOCX file", type=["pdf", "docx"], key="uploaded_file")
    if uploaded_file is not None:
        process_uploaded_file(uploaded_file)

    if st.session_state.document_indexed:
        metadata = st.session_state.document_metadata
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Document", metadata.get("filename", "n/a"))
        with col2:
            st.metric("Characters", len(metadata.get("text", "")))
        with col3:
            st.metric("Pages", metadata.get("page_count", 0))
        with col4:
            st.metric("Chunks", metadata.get("chunk_count", 0))


def render_chat_interface() -> None:
    if not st.session_state.document_indexed:
        st.info("Upload a document to enable grounded Q&A.")
        return

    if "conversation" not in st.session_state:
        st.session_state.conversation = []

    for entry in st.session_state.conversation:
        with st.chat_message(entry["role"]):
            st.markdown(entry["content"])

    user_question = st.chat_input("Ask a question about the uploaded document")
    if user_question:
        if not user_question.strip():
            st.warning("Please enter a question.")
            return

        pipeline = st.session_state.pipeline
        pipeline.top_k = st.session_state.top_k
        pipeline.min_similarity = st.session_state.min_similarity
        pipeline.chunk_size = st.session_state.chunk_size
        pipeline.overlap = st.session_state.chunk_overlap

        ollama_status = detect_ollama_models()
        selected_model = select_ollama_model(ollama_status.get("available_models", []))

        with st.spinner("Retrieving relevant chunks and generating a grounded answer..."):
            try:
                result = pipeline.query(
                    user_question,
                    model_name=selected_model,
                    top_k=st.session_state.top_k,
                    min_similarity=st.session_state.min_similarity,
                    temperature=st.session_state.temperature,
                )
            except Exception as exc:
                st.error(f"Something went wrong while querying the document: {exc}")
                return

        st.session_state.conversation.append({"role": "user", "content": user_question})
        st.session_state.conversation.append({"role": "assistant", "content": result["answer"]})

        with st.chat_message("user"):
            st.markdown(user_question)
        with st.chat_message("assistant"):
            st.markdown(result["answer"])

        if result.get("retrieved"):
            render_retrieval_panel(result["retrieved"])
        else:
            st.info("No relevant chunks passed the similarity threshold. The model was not asked to guess an answer.")


def main() -> None:
    initialize_session_state()
    render_header()
    render_sidebar()
    render_document_panel()
    render_chat_interface()


if __name__ == "__main__":
    main()
