from langchain.memory import ConversationBufferMemory

from domain.interfaces.memory import Memory


class BufferMemory(Memory):
    def _initialize_memory(self) -> None:
        self.memory = ConversationBufferMemory(
            memory_key=self.memory_key, return_messages=True
        )

    def save_context(self, input_text: str, output_text: str) -> None:
        self.memory.save_context({"input": input_text}, {"output": output_text})

    def get_memory_variables(self) -> dict:
        return self.memory.load_memory_variables({})

    def clear(self) -> None:
        self.memory.clear()
