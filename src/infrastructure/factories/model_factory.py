from typing import Optional

from domain.config.model_config import ModelConfig
from domain.interfaces.memory import Memory
from domain.interfaces.model import Model
from infrastructure.models.gemini import GeminiModel
from infrastructure.prompts.prompt_manager import PromptManager


class ModelFactory:
    _prompt_manager = PromptManager()

    @classmethod
    def create_model(
        cls,
        model_template: str,
        model_name: str,
        memory: Optional[Memory] = None,
        template_type: str = "default",
        **kwargs,
    ) -> Model:
        prompt_template = cls._prompt_manager.get_prompt_template(
            model_template, template_type
        )
        config = ModelConfig(
            prompt_template=prompt_template, model_name=model_name, **kwargs
        )
        return GeminiModel(config=config, memory=memory)
