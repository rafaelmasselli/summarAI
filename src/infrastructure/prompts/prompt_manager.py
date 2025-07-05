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
        """Carrega os prompts do arquivo YAML."""
        if not os.path.exists(self.prompts_file):
            raise FileNotFoundError(
                f"Arquivo de prompts não encontrado: {self.prompts_file}"
            )

        with open(self.prompts_file, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def get_prompt_template(
        self, model_type: str, template_type: str = "default"
    ) -> str:
        """
        Obtém um template de prompt específico.

        Args:
            model_type: Tipo do modelo (ex: "gemini")
            template_type: Tipo do template (ex: "summarize", "technical_analysis")

        Returns:
            str: Template do prompt

        Raises:
            KeyError: Se o modelo ou template não existir
        """
        if model_type not in self.prompts:
            raise KeyError(f"Modelo não encontrado: {model_type}")

        model_prompts = self.prompts[model_type]
        if template_type not in model_prompts:
            raise KeyError(f"Template não encontrado: {template_type}")

        return model_prompts[template_type]

    def add_prompt_template(
        self, model_type: str, template_type: str, template: str
    ) -> None:
        """
        Adiciona um novo template de prompt.

        Args:
            model_type: Tipo do modelo
            template_type: Tipo do template
            template: Template do prompt
        """
        if model_type not in self.prompts:
            self.prompts[model_type] = {}

        self.prompts[model_type][template_type] = template
        self._save_prompts()

    def _save_prompts(self) -> None:
        """Salva os prompts no arquivo YAML."""
        with open(self.prompts_file, "w", encoding="utf-8") as f:
            yaml.safe_dump(self.prompts, f, allow_unicode=True, sort_keys=False)
