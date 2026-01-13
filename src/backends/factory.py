from typing import Dict, Type
from .provider_interface import LLMProvider
from .openai_provider import OpenAIProvider
from .ollama_provider import OllamaProvider
from .anthropic_provider import AnthropicProvider
from .gemini_provider import GeminiProvider
from .groq_provider import GroqProvider
from .llamacpp_provider import LlamaCppProvider

class ProviderFactory:
    _providers: Dict[str, Type[LLMProvider]] = {
        "openai": OpenAIProvider,
        "ollama": OllamaProvider,
        "anthropic": AnthropicProvider,
        "gemini": GeminiProvider,
        "groq": GroqProvider,
        "llamacpp": LlamaCppProvider
    }

    @staticmethod
    def create_provider(provider_type: str, **kwargs) -> LLMProvider:
        provider_class = ProviderFactory._providers.get(provider_type)
        if not provider_class:
            raise ValueError(f"Unknown provider type: {provider_type}")
        return provider_class(**kwargs)

    @staticmethod
    def get_available_providers():
        return list(ProviderFactory._providers.keys())
