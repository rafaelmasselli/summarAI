from typing import Any, Dict, Optional

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
        full_prompt = self._format_prompt_with_memory(prompt)
        return self.model.invoke(full_prompt, context or {})

    def get_model_info(self) -> Dict[str, Any]:
        return {
            "model_name": self.config.model_name,
            "provider": "Google",
            "type": "Chat",
            "config": self.config.to_dict(),
        }
