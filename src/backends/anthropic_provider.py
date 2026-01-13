from typing import Dict, Any, List
import anthropic
from .provider_interface import LLMProvider

class AnthropicProvider(LLMProvider):
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.name = "Anthropic"

    def generate(self, system_prompt: str, user_prompt: str, model: str, **kwargs) -> Dict[str, Any]:
        try:
            message = self.client.messages.create(
                model=model,
                max_tokens=kwargs.get("max_tokens", 4096),
                temperature=kwargs.get("temperature", 0.7),
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            return {
                "content": message.content[0].text,
                "raw": message.to_dict()
            }
        except Exception as e:
            raise e

    def list_models(self) -> List[str]:
        # Return common Claude models as API doesn't standardly list 'available' models for chat like this easily
        return ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"]

    def check_health(self) -> bool:
        return True # Client local check

    def get_name(self) -> str:
        return self.name
