from typing import Any, Dict, List

from langchain_community.document_loaders import YoutubeLoader

from infrastructure.factories.model_factory import ModelFactory


class YoutubeService:
    def __init__(self, video_url: str):
        self.video_url = video_url

    def __extract_text(self) -> List[Dict[str, Any]]:
        video_loader = YoutubeLoader.from_youtube_url(
            self.video_url, language=["pt", "pt-BR", "en"]
        )
        return video_loader.load()

    def __process_with_model(self) -> str:
        docs = self.__extract_text()
        video_text = "\n".join(doc.page_content for doc in docs)
        return video_text

    def summarize_video(self) -> str:
        video_text = self.__process_with_model()
        model = ModelFactory.create_model(
            model_template="gemini",
            model_name="gemini-2.0-flash-001",
            template_type="default",
        )

        response = model.generate_text(video_text)
        return response.content
