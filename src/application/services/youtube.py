from typing import Any, Dict, List

from langchain_community.document_loaders import YoutubeLoader

from infrastructure.factories.model_factory import ModelFactory
from util.logger import logger


class YoutubeService:
    def __init__(self, video_url: str):
        self.video_url = video_url
        logger.debug(f"YoutubeService initialized with URL: {video_url}")

    def __extract_text(self) -> List[Dict[str, Any]]:
        logger.info("Extracting video transcript...")
        try:
            video_loader = YoutubeLoader.from_youtube_url(
                self.video_url, language=["pt", "pt-BR", "en"]
            )
            result = video_loader.load()
            logger.debug(f"Extracted {len(result)} document chunks")
            return result
        except Exception as e:
            logger.error(f"Failed to extract video transcript: {str(e)}")
            raise

    def __process_with_model(self) -> str:
        docs = self.__extract_text()
        video_text = "\n".join(doc.page_content for doc in docs)
        logger.info(f"Transcript extracted successfully ({len(video_text)} characters)")
        return video_text

    def summarize_video(self) -> str:
        logger.info("Processing video... This may take a moment.")
        video_text = self.__process_with_model()

        logger.info("Initializing language model...")
        model = ModelFactory.create_model(
            model_template="gemini",
            model_name="gemini-2.0-flash-001",
            template_type="default",
        )

        logger.info("Generating summary...")
        response = model.generate_text(video_text)
        logger.success("Summary generated successfully.")
        return response.content
