from core.retriever import retrieve_top_k


def test_top_k_retrieval_ranks_best_match_first():
    chunk_records = [
        {"chunk_id": "chunk-1", "source_name": "doc1.pdf", "page_number": 1, "text": "This is about Python.", "embedding": [1.0, 0.0]},
        {"chunk_id": "chunk-2", "source_name": "doc1.pdf", "page_number": 2, "text": "This is about Java.", "embedding": [0.2, 0.98]},
        {"chunk_id": "chunk-3", "source_name": "doc1.pdf", "page_number": 3, "text": "This is about C++.", "embedding": [0.0, 1.0]},
    ]

    query_embedding = [1.0, 0.0]
    results = retrieve_top_k(query_embedding, chunk_records, top_k=2, min_similarity=0.0)

    assert len(results) == 2
    assert results[0]["chunk_id"] == "chunk-1"
    assert results[0]["score"] >= results[1]["score"]
