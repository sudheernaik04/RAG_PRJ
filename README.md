# Local RAG Workshop App

A beginner-friendly local Retrieval-Augmented Generation (RAG) application for classroom use. It lets students upload PDF or DOCX files, extract text, split it into meaningful chunks, embed and retrieve relevant passages, and then ask a locally running LLM for a grounded answer through Ollama.

## What this project teaches

This workshop uses the exact conceptual flow:

Document
→ Extract
→ Clean
→ Chunk
→ Embed
→ Cosine Similarity
→ Retrieve
→ Context
→ LLM
→ Answer

The key idea is that the LLM does not automatically know the uploaded document. First, the system finds the most relevant document content, then it sends that content as context to the model.

## Why the stack was chosen

- Streamlit: beginner-friendly UI for teaching and demos
- PyMuPDF: reliable, local PDF extraction
- python-docx: local DOCX extraction
- sentence-transformers: local embeddings without API keys
- NumPy + scikit-learn: cosine similarity and vector math
- Ollama: local model runtime with Qwen or Llama

## Features

- PDF and DOCX upload support
- Clean text extraction and normalization
- Meaningful chunking with configurable size and overlap
- Local embedding generation with Sentence Transformers
- Cosine similarity retrieval with Top-K ranking
- Retrieval transparency panel showing scores and sources
- Model detection for Qwen and Llama through Ollama
- Grounded prompt construction for transparent, non-hallucinated answers
- Friendly error handling for missing Ollama services or absent models

## Workshop model policy

The app automatically detects Ollama models and uses:

1. Qwen when available
2. Llama as fallback when Qwen is not present
3. A clear setup message when neither is installed

This avoids hard-coding a single model tag and keeps the classroom workflow flexible.

## Local installation

From the project root:

```bash
python -m pip install -r requirements.txt
```

Then launch the app:

```bash
streamlit run app.py
```

## Ollama setup

Install Ollama from the official site and start the service:

```bash
ollama serve
```

Common verification:

```bash
curl http://localhost:11434/api/tags
```

## Install local models

Qwen:

```bash
ollama pull qwen2.5
```

Llama fallback:

```bash
ollama pull llama3.2
```

You can also install other nearby variants such as `qwen3`, `llama3.1`, or similar. The app searches for supported Qwen/Llama model names dynamically.

## App workflow

1. Upload a PDF or DOCX file.
2. Extract the text and clean it.
3. Split the document into chunks.
4. Generate embeddings locally.
5. Compute cosine similarity with the user’s question.
6. Retrieve the Top-K relevant chunks.
7. Show the retrieved context and similarity scores.
8. Send the question + relevant context to Ollama.
9. Return a grounded answer with source references when available.

## RAG in simple terms

RAG means the model is not expected to store the whole document in memory. Instead, it first searches for relevant passages, then reads just those passages as context before answering.

Embeddings capture meaning, and cosine similarity measures how close the query is to the stored chunk vectors. The best matches are then passed to the LLM so it can answer from evidence rather than guessing.

## Project structure

```text
.
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── core/
│   ├── __init__.py
│   ├── document_loader.py
│   ├── text_cleaner.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── retriever.py
│   ├── model_selector.py
│   ├── ollama_client.py
│   └── rag_pipeline.py
├── ui/
│   ├── __init__.py
│   ├── components.py
│   └── styles.py
├── data/
│   └── uploads/
├── tests/
│   ├── test_chunking.py
│   ├── test_model_selection.py
│   ├── test_retrieval.py
│   └── test_document_loading.py
└── test_text_cleaning.py
```

## Demo questions

Try questions such as:

- What are the eligibility requirements in this document?
- Which page mentions deadlines or assessment rules?
- Summarize the key course outcomes.
- What topics are covered in the first section?
- What is not mentioned in the uploaded document?

## Troubleshooting

### Ollama is not connected

- Start Ollama
- Verify `http://localhost:11434/api/tags` responds
- Confirm the service is running locally

### No model is available

- Install a Qwen model or Llama model
- Retry the app after the model finishes pulling

### PDF extraction is empty

- Confirm the file is valid and not image-only
- Some scanned PDFs may require OCR; this app intentionally keeps things lightweight and local

### No relevant answer is found

- Ask a question that matches the uploaded text
- Lower the similarity threshold in the settings as needed
- Inspect the retrieved context panel to see which chunks were returned

## Example workshop flow

1. Upload a syllabus or course policy PDF.
2. Explain how the document is split into chunks.
3. Show the similarity scores for retrieved passages.
4. Ask a question in natural language.
5. Inspect the retrieved context.
6. Compare the answer with the actual source text.
7. Discuss why grounding matters and how hallucinations can be reduced.

## Educational guidance

This project is designed for students to see the difference between:

- retrieval: finding evidence in the document
- generation: writing an answer using the retrieved context

The retrieved context should be treated as evidence, not as a hidden instruction source. That distinction is essential for safe and grounded AI systems.
