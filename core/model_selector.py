from __future__ import annotations

from typing import Any

import requests

OLLAMA_BASE_URL = "http://localhost:11434"


def detect_ollama_models(base_url: str = OLLAMA_BASE_URL) -> dict[str, Any]:
    """Query Ollama and return detected models plus connectivity status."""
    try:
        response = requests.get(f"{base_url}/api/tags", timeout=3)
        if response.status_code != 200:
            return {"connected": False, "available_models": [], "error": "Ollama endpoint returned a non-200 response."}
    except requests.RequestException as exc:
        return {"connected": False, "available_models": [], "error": str(exc)}

    try:
        payload = response.json()
    except ValueError:
        return {"connected": False, "available_models": [], "error": "Could not parse Ollama response."}

    models = []
    for model in payload.get("models", []) or []:
        name = model.get("name") or model.get("model")
        if name:
            models.append(name)

    return {"connected": True, "available_models": models, "error": None}


def select_ollama_model(available_models: list[str] | None = None) -> str | None:
    """Choose a Qwen model first, then a Llama model if needed."""
    models = available_models or []
    lowered = [name.lower() for name in models]

    for name, lower_name in zip(models, lowered):
        if "qwen" in lower_name:
            return name

    for name, lower_name in zip(models, lowered):
        if "llama" in lower_name:
            return name

    return None


def get_model_status() -> dict[str, Any]:
    detection = detect_ollama_models()
    selected_model = select_ollama_model(detection.get("available_models", []))
    return {
        "connected": detection["connected"],
        "available_models": detection.get("available_models", []),
        "selected_model": selected_model,
        "error": detection.get("error"),
    }
