from core.chunker import chunk_text


def test_chunking_creates_multiple_chunks():
    text = " ".join([f"sentence {index}" for index in range(1, 60)])
    chunks = chunk_text(text, chunk_size=10, overlap=3, source_name="demo")

    assert len(chunks) > 1
    assert all(chunk["text"] for chunk in chunks)
    assert chunks[0]["chunk_id"].startswith("demo")


def test_chunking_keeps_overlap():
    text = " ".join([f"word {index}" for index in range(1, 25)])
    chunks = chunk_text(text, chunk_size=8, overlap=2, source_name="demo")

    assert len(chunks) >= 2
    assert chunks[0]["text"] != chunks[1]["text"]
