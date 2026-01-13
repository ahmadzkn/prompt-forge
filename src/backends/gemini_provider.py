from typing import Dict, Any, List
import google.generativeai as genai
from .provider_interface import LLMProvider

class GeminiProvider(LLMProvider):
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.name = "Google Gemini"

    def generate(self, system_prompt: str, user_prompt: str, model: str, **kwargs) -> Dict[str, Any]:
        try:
            # Gemini doesn't have a strict 'system' role in the same way, usually passed in config or context
            # For 1.5, system instructions are supported.
            model_instance = genai.GenerativeModel(
                model_name=model,
                system_instruction=system_prompt
            )
            
            response = model_instance.generate_content(user_prompt)
            return {
                "content": response.text,
                "raw": response.to_dict() if hasattr(response, 'to_dict') else {}
            }
        except Exception as e:
            raise e

    def list_models(self) -> List[str]:
        try:
            # List models checking for generateContent support
            models = []
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                     models.append(m.name.replace("models/", ""))
            return models
        except:
            return ["gemini-1.5-pro-latest", "gemini-1.5-flash-latest"]

    def check_health(self) -> bool:
        return True

    def get_name(self) -> str:
        return self.name
