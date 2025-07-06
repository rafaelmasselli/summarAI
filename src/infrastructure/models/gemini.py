from typing import Any, Dict, Optional

from langchain.schema.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from domain.interfaces.model import Model
from util.logger import logger


class GeminiModel(Model):
    def _initialize_model(self) -> None:
        logger.debug(f"Initializing Gemini model: {self.config.model_name}")
        try:
            self.model = ChatGoogleGenerativeAI(
                model=self.config.model_name,
                temperature=self.config.temperature,
                **(self.config.additional_params or {}),
            )
            logger.debug("Gemini model initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini model: {str(e)}")
            raise

    def generate_text(
        self, prompt: str, context: Optional[Dict[str, Any]] = None
    ) -> str:
        logger.debug("Preparing to generate text with Gemini model")
        system_prompt = self.config.prompt_template

        messages = [SystemMessage(content=system_prompt), HumanMessage(content=prompt)]

        memory_context = self._get_memory_context()
        if memory_context:
            logger.debug("Using memory context in prompt")
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(
                    content=f"{prompt}\n\nPrevious history:\n{memory_context}"
                ),
            ]

        try:
            logger.debug("Sending request to Gemini API")
            response = self.model.invoke(messages, context or {})
            logger.debug("Response received from Gemini API")
            return response
        except Exception as e:
            logger.error(f"Error generating text with Gemini: {str(e)}")
            raise

    def get_model_info(self) -> Dict[str, Any]:
        info = {
            "model_name": self.config.model_name,
            "provider": "Google",
            "type": "Chat",
            "config": self.config.to_dict(),
        }
        logger.debug(f"Model info: {info}")
        return info
