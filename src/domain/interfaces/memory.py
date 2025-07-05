from abc import ABC, abstractmethod
from typing import Dict


class Memory(ABC):
    def __init__(self, memory_key: str = "chat_history"):
        self.memory_key = memory_key
        self._initialize_memory()

    @abstractmethod
    def _initialize_memory(self) -> None:
        pass

    @abstractmethod
    def save_context(self, input_text: str, output_text: str) -> None:
        pass

    @abstractmethod
    def get_memory_variables(self) -> Dict:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass
