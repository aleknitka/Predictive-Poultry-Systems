import os
from typing import Optional
from pydantic_ai.models import Model
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider


def get_model(model_id: Optional[str] = None) -> Model:
    """
    Returns a configured Model instance based on environment variables.
    Supported model_id prefixes: 'ollama:', 'openrouter:', 'openai:'.
    """
    model_id = model_id or os.getenv("LLM_MODEL_ID", "openai:gpt-4o")

    if model_id.startswith("ollama:"):
        model_name = model_id.split(":", 1)[1]
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
        provider = OpenAIProvider(
            base_url=base_url,
            api_key="ollama",  # Dummy key for Ollama
        )
        return OpenAIChatModel(model_name=model_name, provider=provider)

    if model_id.startswith("openrouter:"):
        model_name = model_id.split(":", 1)[1]
        api_key = os.getenv("OPENROUTER_API_KEY", "openrouter-dummy")
        provider = OpenAIProvider(
            base_url="https://openrouter.ai/api/v1", api_key=api_key
        )
        return OpenAIChatModel(model_name=model_name, provider=provider)

    if model_id.startswith("openai:"):
        model_name = model_id.split(":", 1)[1]
        api_key = os.getenv("OPENAI_API_KEY", "openai-dummy")
        provider = OpenAIProvider(api_key=api_key)
        return OpenAIChatModel(model_name=model_name, provider=provider)

    # Default to OpenAI if prefix is missing
    api_key = os.getenv("OPENAI_API_KEY", "openai-dummy")
    provider = OpenAIProvider(api_key=api_key)
    return OpenAIChatModel(model_name=model_id, provider=provider)
