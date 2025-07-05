from typing import Dict, Optional, Type

from domain.config.model_config import ModelConfig
from domain.interfaces.memory import Memory
from domain.interfaces.model import Model
from infrastructure.prompts.prompt_manager import PromptManager


class ModelFactory:
    _models: Dict[str, Type[Model]] = {}
    _prompt_manager = PromptManager()

    @classmethod
    def register_model(
        cls, name: str, model_class: Type[Model], prompt_template: Optional[str] = None
    ) -> None:
        cls._models[name] = model_class
        if prompt_template:
            cls._prompt_manager.add_prompt_template(name, "custom", prompt_template)

    @classmethod
    def create_model(
        cls,
        model_type: str,
        model_name: str,
        template_type: str = "default",
        memory: Optional[Memory] = None,
        prompt_variables: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> Model:
        if model_type not in cls._models:
            raise ValueError(f"Tipo de modelo não suportado: {model_type}")

        prompt_template = cls._prompt_manager.get_prompt_template(
            model_type, template_type
        )

        config = ModelConfig(
            model_name=model_name, prompt_template=prompt_template, **kwargs
        )

        if prompt_variables:
            config.format_prompt(**prompt_variables)

        model_class = cls._models[model_type]
        return model_class(config=config, memory=memory)
