from typing import Optional

from domain.config.model_config import ModelConfig
from domain.interfaces.memory import Memory
from domain.interfaces.model import Model
from infrastructure.models.gemini import GeminiModel
from infrastructure.prompts.prompt_manager import PromptManager
from util.logger import logger


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
        logger.debug(f"Creating model: {model_name} with template: {model_template}")

        try:
            prompt_template = cls._prompt_manager.get_prompt_template(
                model_template, template_type
            )
            logger.debug(f"Prompt template loaded for {model_template}/{template_type}")

            config = ModelConfig(
                prompt_template=prompt_template, model_name=model_name, **kwargs
            )

            logger.debug(f"Model configuration created: {config.to_dict()}")
            model = GeminiModel(config=config, memory=memory)
            logger.debug(f"Model instance created: {model.__class__.__name__}")

            return model
        except Exception as e:
            logger.error(f"Failed to create model: {str(e)}")
            raise
