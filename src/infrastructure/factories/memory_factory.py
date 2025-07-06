from typing import Optional

from domain.interfaces.memory import Memory
from infrastructure.memory.buffer import BufferMemory
from infrastructure.memory.window import WindowMemory


class MemoryFactory:
    _memories = {"buffer": BufferMemory, "window": WindowMemory}

    @classmethod
    def register_memory(cls, name: str, memory_class: type) -> None:
        cls._memories[name] = memory_class

    @classmethod
    def create_memory(
        cls, memory_type: str, memory_key: str = "chat_history", k: Optional[int] = None
    ) -> Memory:
        if memory_type not in cls._memories:
            raise ValueError(f"Unsupported memory type: {memory_type}")

        memory_class = cls._memories[memory_type]

        if memory_type == "window" and k is not None:
            return memory_class(memory_key=memory_key, k=k)

        return memory_class(memory_key=memory_key)
