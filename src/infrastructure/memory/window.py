from langchain.memory import ConversationBufferWindowMemory

from domain.interfaces.memory import Memory


class WindowMemory(Memory):
    def __init__(self, memory_key: str = "chat_history", k: int = 5):
        self.k = k
        super().__init__(memory_key)

    def _initialize_memory(self) -> None:
        self.memory = ConversationBufferWindowMemory(
            memory_key=self.memory_key, k=self.k, return_messages=True
        )

    def save_context(self, input_text: str, output_text: str) -> None:
        self.memory.save_context({"input": input_text}, {"output": output_text})

    def get_memory_variables(self) -> dict:
        return self.memory.load_memory_variables({})

    def clear(self) -> None:
        self.memory.clear()
