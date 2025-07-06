from typing import Any, Dict, Optional

from langchain.schema.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from domain.interfaces.model import Model


class GeminiModel(Model):
    def _initialize_model(self) -> None:
        self.model = ChatGoogleGenerativeAI(
            model=self.config.model_name,
            temperature=self.config.temperature,
            **(self.config.additional_params or {}),
        )

    def generate_text(
        self, prompt: str, context: Optional[Dict[str, Any]] = None
    ) -> str:
        system_prompt = self.config.prompt_template

        messages = [SystemMessage(content=system_prompt), HumanMessage(content=prompt)]

        memory_context = self._get_memory_context()
        if memory_context:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(
                    content=f"{prompt}\n\nPrevious history:\n{memory_context}"
                ),
            ]

        return self.model.invoke(messages, context or {})

    def get_model_info(self) -> Dict[str, Any]:
        return {
            "model_name": self.config.model_name,
            "provider": "Google",
            "type": "Chat",
            "config": self.config.to_dict(),
        }
