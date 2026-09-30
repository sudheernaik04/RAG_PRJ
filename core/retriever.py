from __future__ import annotations

from typing import Any

from core.embeddings import cosine_similarity


def retrieve_top_k(
    query_embedding: list[float] | Any,
    chunk_records: list[dict[str, Any]],
    top_k: int = 3,
    min_similarity: float = 0.15,
) -> list[dict[str, Any]]:
    """Find the most semantically relevant chunks using cosine similarity."""
    results = []
    for item in chunk_records:
        embedding = item.get("embedding")
        if embedding is None:
            continue
        score = cosine_similarity(query_embedding, embedding)
        if score >= min_similarity:
            results.append({
                "chunk_id": item.get("chunk_id"),
                "source_name": item.get("source_name"),
                "page_number": item.get("page_number"),
                "text": item.get("text"),
                "score": float(score),
            })

    results.sort(key=lambda entry: entry["score"], reverse=True)
    return results[:max(1, int(top_k))]


def build_context_block(retrieved_chunks: list[dict[str, Any]]) -> str:
    """Create a readable context block for the LLM from the top retrieved chunks."""
    if not retrieved_chunks:
        return "No relevant context was retrieved."

    blocks = []
    for chunk in retrieved_chunks:
        source = chunk.get("source_name", "unknown")
        page = chunk.get("page_number")
        chunk_id = chunk.get("chunk_id", "unknown")
        text = chunk.get("text", "")
        page_text = f" (Page {page})" if page else ""
        blocks.append(f"[Source: {source}{page_text}, Chunk: {chunk_id}]\n{text}")
    return "\n\n".join(blocks)
