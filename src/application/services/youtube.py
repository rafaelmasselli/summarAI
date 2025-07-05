from typing import Any, Dict, List

from langchain_community.document_loaders import YoutubeLoader

from domain.interfaces.memory import Memory
from infrastructure.factories.model_factory import ModelFactory


class YoutubeService:
    def __init__(self, video_url: str):
        self.video_url = video_url

    def extract_text(self) -> List[Dict[str, Any]]:
        video_loader = YoutubeLoader.from_youtube_url(
            self.video_url, language=["pt", "pt-BR", "en"]
        )
        return video_loader.load()

    def process_with_model(
        self,
        model_type: str,
        model_name: str,
        template_type: str = "default",
        instructions: str = "",
        context: str = "",
        memory: Memory = None,
        **kwargs,
    ) -> str:
        docs = self.extract_text()
        texto_video = "\n".join(doc.page_content for doc in docs)

        model = ModelFactory.create_model(
            model_type=model_type,
            model_name=model_name,
            template_type=template_type,
            memory=memory,
            prompt_variables={
                "instructions": instructions,
                "context": context,
                "input": texto_video,
            },
            **kwargs,
        )

        return model.generate_text(texto_video)

    def summarize_video(
        self,
        model_type: str = "gemini",
        instructions: str = "Faça um resumo detalhado do vídeo",
        context: str = "",
        **kwargs,
    ) -> str:
        return self.process_with_model(
            model_type=model_type,
            template_type="summarize",
            instructions=instructions,
            context=context,
            **kwargs,
        )

    def analyze_technical_content(
        self,
        model_type: str = "gemini",
        model_name: str = "gemini-1.5-pro",
        instructions: str = "Analise os aspectos técnicos do vídeo",
        context: str = "",
        **kwargs,
    ) -> str:
        """Analisa o conteúdo técnico do vídeo usando o template 'technical_analysis'"""
        return self.process_with_model(
            model_type=model_type,
            model_name=model_name,
            template_type="technical_analysis",
            instructions=instructions,
            context=context,
            **kwargs,
        )
