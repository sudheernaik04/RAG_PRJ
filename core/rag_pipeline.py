from __future__ import annotations

from pathlib import Path
from typing import Any

from core.document_loader import extract_document_text
from core.embeddings import LocalEmbeddingModel
from core.model_selector import detect_ollama_models, select_ollama_model
from core.ollama_client import build_grounded_prompt, generate_answer
from core.retriever import build_context_block, retrieve_top_k
from core.text_cleaner import clean_text
from core.chunker import chunk_text


class LocalRAGPipeline:
    """Simple local RAG workflow for workshop demonstrations."""

    def __init__(
        self,
        embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        top_k: int = 3,
        min_similarity: float = 0.15,
        chunk_size: int = 400,
        overlap: int = 80,
    ):
        self.embedding_model = LocalEmbeddingModel(embedding_model_name)
        self.top_k = top_k
        self.min_similarity = min_similarity
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.indexed_document: dict[str, Any] | None = None

    def index_document(self, file_path: str | Path) -> dict[str, Any]:
        path = Path(file_path)
        text, page_count = extract_document_text(path)
        cleaned_text = clean_text(text)

        if not cleaned_text:
            raise ValueError("The uploaded document does not contain readable text.")

        chunks = chunk_text(cleaned_text, chunk_size=self.chunk_size, overlap=self.overlap, source_name=path.name)
        if not chunks:
            raise ValueError("The document text could not be split into useful chunks.")

        embeddings = self.embedding_model.encode([chunk["text"] for chunk in chunks])
        for chunk, embedding in zip(chunks, embeddings):
            chunk["embedding"] = embedding

        self.indexed_document = {
            "filename": path.name,
            "source_path": str(path),
            "page_count": page_count,
            "character_count": len(cleaned_text),
            "chunk_count": len(chunks),
            "chunks": chunks,
            "text": cleaned_text,
        }
        return self.indexed_document

    def query(
        self,
        question: str,
        model_name: str | None = None,
        top_k: int | None = None,
        min_similarity: float | None = None,
        temperature: float = 0.2,
    ) -> dict[str, Any]:
        if self.indexed_document is None:
            raise ValueError("No document has been indexed yet. Please upload and process a file first.")

        cleaned_question = clean_text(question)
        if not cleaned_question:
            raise ValueError("Please enter a valid question.")

        query_embedding = self.embedding_model.encode([cleaned_question])[0]
        selected_top_k = self.top_k if top_k is None else top_k
        selected_min_similarity = self.min_similarity if min_similarity is None else min_similarity

        retrieved = retrieve_top_k(
            query_embedding,
            self.indexed_document["chunks"],
            top_k=selected_top_k,
            min_similarity=selected_min_similarity,
        )

        if not retrieved:
            return {
                "answer": "I could not find relevant information in the uploaded document for that question. Please ask a question related to the document content.",
                "retrieved": [],
                "model": model_name,
                "context": "",
            }

        context_block = build_context_block(retrieved)

        if model_name is None:
            ollama_status = detect_ollama_models()
            model_name = select_ollama_model(ollama_status.get("available_models", []))

        if not model_name:
            return {
                "answer": "No suitable local Ollama model was detected. Please install Qwen or Llama and restart the app.",
                "retrieved": retrieved,
                "model": None,
                "context": context_block,
            }

        try:
            prompt = build_grounded_prompt(cleaned_question, context_block)
            answer = generate_answer(model_name, prompt, temperature=temperature)
        except Exception as exc:
            return {
                "answer": f"The local LLM could not answer from the retrieved context. Please check that Ollama is running and the selected model is available. Error: {exc}",
                "retrieved": retrieved,
                "model": model_name,
                "context": context_block,
            }

        return {
            "answer": answer,
            "retrieved": retrieved,
            "model": model_name,
            "context": context_block,
        }
