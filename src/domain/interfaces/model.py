from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from domain.config.model_config import ModelConfig
from domain.interfaces.memory import Memory


class Model(ABC):
    def __init__(self, config: ModelConfig, memory: Optional[Memory] = None):
        self.config = config
        self.memory = memory
        self._initialize_model()

    @abstractmethod
    def _initialize_model(self) -> None:
        pass

    def _get_memory_context(self) -> str:
        if not self.memory:
            return ""

        memory_vars = self.memory.get_memory_variables()
        return memory_vars.get("chat_history", "")

    def _format_prompt_with_memory(self, prompt: str) -> str:
        memory_context = self._get_memory_context()
        if memory_context:
            return f"{prompt}\n\nHistórico anterior:\n{memory_context}".strip()
        return prompt

    @abstractmethod
    def generate_text(
        self, prompt: str, context: Optional[Dict[str, Any]] = None
    ) -> str:
        pass

    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        pass
