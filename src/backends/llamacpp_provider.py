from typing import Dict, Any, List
import os
try:
    from llama_cpp import Llama
except ImportError:
    Llama = None

from .provider_interface import LLMProvider

class LlamaCppProvider(LLMProvider):
    def __init__(self, model_path: str, **kwargs):
        if not Llama:
            raise ImportError("llama-cpp-python is not installed. Please install it to use this provider.")
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at: {model_path}")
            
        n_gpu_layers = kwargs.get("n_gpu_layers", 0)
        # Initialize Llama model
        self.llm = Llama(
            model_path=model_path,
            n_ctx=kwargs.get("n_ctx", 4096),
            n_gpu_layers=n_gpu_layers,
            verbose=False
        )
        self.name = "Llama.cpp"
        self.model_path = model_path

    def generate(self, system_prompt: str, user_prompt: str, model: str, **kwargs) -> Dict[str, Any]:
        try:
            # Llama.cpp python bindings use OpenAI-like create_chat_completion structure
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            response = self.llm.create_chat_completion(
                messages=messages,
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 4096),
                response_format={"type": "json_object"}
            )
            
            return {
                "content": response["choices"][0]["message"]["content"],
                "raw": response
            }
        except Exception as e:
            raise e

    def list_models(self) -> List[str]:
        # For Llama.cpp, the "model" is the loaded file.
        return [os.path.basename(self.model_path)]

    def check_health(self) -> bool:
        return self.llm is not None

    def get_name(self) -> str:
        return self.name
