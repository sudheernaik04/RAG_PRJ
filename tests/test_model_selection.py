from core.model_selector import select_ollama_model


def test_qwen_is_preferred():
    models = ["llama3.2:latest", "qwen2.5:latest"]
    assert select_ollama_model(models) == "qwen2.5:latest"


def test_llama_is_used_when_qwen_is_missing():
    models = ["llama3.1:latest", "mistral:latest"]
    assert select_ollama_model(models) == "llama3.1:latest"


def test_no_local_model_returns_none():
    assert select_ollama_model(["deepseek-r1:latest"]) is None
