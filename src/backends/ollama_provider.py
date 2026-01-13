from typing import Dict, Any, List
import ollama
from .provider_interface import LLMProvider

class OllamaProvider(LLMProvider):
    def __init__(self, host: str = "http://localhost:11434"):
        # Ollama library uses env var OLLAMA_HOST, or defaults to localhost:11434
        # We can set the client explicitly if needed, but the python lib is a bit static.
        # However, we can use the Client object in newer versions.
        self.client = ollama.Client(host=host)
        self.name = "Ollama"

    def generate(self, system_prompt: str, user_prompt: str, model: str, **kwargs) -> Dict[str, Any]:
        try:
            response = self.client.chat(model=model, messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt},
            ])
            return {
                "content": response['message']['content'],
                "raw": response
            }
        except Exception as e:
            raise e

    def list_models(self) -> List[str]:
        try:
            models = self.client.list()
            # Handle different return formats of ollama lib versions
            if 'models' in models:
                return [m['name'] for m in models['models']]
            return []
        except Exception:
            return []

    def check_health(self) -> bool:
        try:
            self.client.list()
            return True
        except Exception:
            return False

    def get_name(self) -> str:
        return self.name
