from dataclasses import dataclass, field
from string import Template
from typing import Any, Dict, Optional


@dataclass
class ModelConfig:
    model_name: str
    temperature: float = 0
    max_tokens: Optional[int] = None
    top_p: float = 1.0
    prompt_template: str = ""
    additional_params: Dict[str, Any] = field(default_factory=dict)

    def format_prompt(self, **kwargs) -> str:
        template = Template(self.prompt_template)
        return template.safe_substitute(**kwargs)

    def to_dict(self) -> Dict[str, Any]:
        config = {
            "temperature": self.temperature,
            "top_p": self.top_p,
            "prompt_template": self.prompt_template,
        }

        if self.max_tokens:
            config["max_tokens"] = self.max_tokens

        if self.additional_params:
            config.update(self.additional_params)

        return config
