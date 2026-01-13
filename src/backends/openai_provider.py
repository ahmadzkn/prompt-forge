from typing import Dict, Any, List
from openai import OpenAI, APIError
from .provider_interface import LLMProvider

class OpenAIProvider(LLMProvider):
    def __init__(self, base_url: str, api_key: str = "lm-studio"):
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.name = "OpenAI / LM Studio"

    def generate(self, system_prompt: str, user_prompt: str, model: str, **kwargs) -> Dict[str, Any]:
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=kwargs.get("temperature", 0.7),
            )
            return {
                "content": response.choices[0].message.content,
                "raw": response.dict()
            }
        except Exception as e:
            raise e

    def list_models(self) -> List[str]:
        try:
            models = self.client.models.list()
            return [model.id for model in models.data]
        except Exception:
            return []

    def check_health(self) -> bool:
        try:
            # Simple check by listing models
            self.client.models.list()
            return True
        except Exception:
            return False

    def get_name(self) -> str:
        return self.name
