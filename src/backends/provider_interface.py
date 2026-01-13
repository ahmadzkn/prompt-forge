from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class LLMProvider(ABC):
    @abstractmethod
    def generate(self, system_prompt: str, user_prompt: str, model: str, **kwargs) -> Dict[str, Any]:
        """
        Generates a response from the LLM.
        Expected return format: {"content": str, "raw": dict}
        """
        pass

    @abstractmethod
    def list_models(self) -> List[str]:
        """
        Returns a list of available model names.
        """
        pass

    @abstractmethod
    def check_health(self) -> bool:
        """
        Checks if the backend is reachable/ready.
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """
        Returns the friendly name of the provider.
        """
        pass
