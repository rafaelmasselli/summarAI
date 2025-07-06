import os
from pathlib import Path
from typing import Dict, Optional

import yaml

from util.logger import logger


class PromptManager:
    def __init__(self, prompts_file: Optional[str] = None):
        if prompts_file is None:
            current_dir = Path(__file__).parent
            prompts_file = current_dir / "base_prompts.yaml"

        self.prompts_file = prompts_file
        logger.debug(f"Initializing PromptManager with file: {self.prompts_file}")
        self.prompts = self._load_prompts()

    def _load_prompts(self) -> Dict:
        logger.debug(f"Loading prompts from: {self.prompts_file}")
        if not os.path.exists(self.prompts_file):
            logger.error(f"Prompts file not found: {self.prompts_file}")
            raise FileNotFoundError(f"Prompts file not found: {self.prompts_file}")

        try:
            with open(self.prompts_file, "r", encoding="utf-8") as f:
                prompts = yaml.safe_load(f)
                logger.debug(f"Loaded {len(prompts)} model templates")
                return prompts
        except Exception as e:
            logger.error(f"Error loading prompts: {str(e)}")
            raise

    def get_prompt_template(
        self, model_type: str, template_type: str = "default"
    ) -> str:
        logger.debug(f"Getting prompt template: {model_type}/{template_type}")

        if model_type not in self.prompts:
            logger.error(f"Model not found: {model_type}")
            raise KeyError(f"Model not found: {model_type}")

        model_prompts = self.prompts[model_type]
        if template_type not in model_prompts:
            logger.error(f"Template not found: {template_type}")
            raise KeyError(f"Template not found: {template_type}")

        logger.debug(f"Prompt template found for {model_type}/{template_type}")
        return model_prompts[template_type]

    def add_prompt_template(
        self, model_type: str, template_type: str, template: str
    ) -> None:
        logger.debug(f"Adding prompt template: {model_type}/{template_type}")

        if model_type not in self.prompts:
            logger.debug(f"Creating new model type: {model_type}")
            self.prompts[model_type] = {}

        self.prompts[model_type][template_type] = template
        self._save_prompts()
        logger.debug(f"Prompt template added: {model_type}/{template_type}")

    def _save_prompts(self) -> None:
        """Saves prompts to the YAML file."""
        logger.debug(f"Saving prompts to: {self.prompts_file}")
        try:
            with open(self.prompts_file, "w", encoding="utf-8") as f:
                yaml.safe_dump(self.prompts, f, allow_unicode=True, sort_keys=False)
            logger.debug("Prompts saved successfully")
        except Exception as e:
            logger.error(f"Error saving prompts: {str(e)}")
            raise
