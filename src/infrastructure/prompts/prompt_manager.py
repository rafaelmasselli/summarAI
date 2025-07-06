import os
from pathlib import Path
from typing import Dict, Optional

import yaml


class PromptManager:
    def __init__(self, prompts_file: Optional[str] = None):
        if prompts_file is None:
            current_dir = Path(__file__).parent
            prompts_file = current_dir / "base_prompts.yaml"

        self.prompts_file = prompts_file
        self.prompts = self._load_prompts()

    def _load_prompts(self) -> Dict:
        if not os.path.exists(self.prompts_file):
            raise FileNotFoundError(f"Prompts file not found: {self.prompts_file}")

        with open(self.prompts_file, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def get_prompt_template(
        self, model_type: str, template_type: str = "default"
    ) -> str:
        if model_type not in self.prompts:
            raise KeyError(f"Model not found: {model_type}")

        model_prompts = self.prompts[model_type]
        if template_type not in model_prompts:
            raise KeyError(f"Template not found: {template_type}")

        return model_prompts[template_type]

    def add_prompt_template(
        self, model_type: str, template_type: str, template: str
    ) -> None:
        if model_type not in self.prompts:
            self.prompts[model_type] = {}

        self.prompts[model_type][template_type] = template
        self._save_prompts()

    def _save_prompts(self) -> None:
        """Saves prompts to the YAML file."""
        with open(self.prompts_file, "w", encoding="utf-8") as f:
            yaml.safe_dump(self.prompts, f, allow_unicode=True, sort_keys=False)
