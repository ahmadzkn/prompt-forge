from typing import Dict, Any, List
import os
from groq import Groq
from .provider_interface import LLMProvider

class GroqProvider(LLMProvider):
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
        self.name = "Groq"

    def generate(self, system_prompt: str, user_prompt: str, model: str, **kwargs) -> Dict[str, Any]:
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                model=model,
                temperature=kwargs.get("temperature", 0.7),
            )
            return {
                "content": chat_completion.choices[0].message.content,
                "raw": chat_completion.to_dict()
            }
        except Exception as e:
            raise e

    def list_models(self) -> List[str]:
        try:
            models = self.client.models.list()
            return [m.id for m in models.data]
        except:
            return ["llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768"]

    def check_health(self) -> bool:
        return True

    def get_name(self) -> str:
        return self.name
