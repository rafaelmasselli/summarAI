from dotenv import load_dotenv

from application.services.pdf import PdfService
from application.services.youtube import YoutubeService
from util.logger import logger


def summarize_video():
    link = input("Enter the video link: ")
    logger.info("Starting video summarization process")
    youtube_handler = YoutubeService(link)
    text = youtube_handler.summarize_video()
    logger.success("Video summarization completed")
    return text, link


def main() -> None:
    try:
        logger.info("Initializing application")
        load_dotenv()
        logger.info("Environment variables loaded")

        text, video_url = summarize_video()

        logger.info("Creating PDF document")
        pdf_service = PdfService()
        pdf_path = pdf_service.create_pdf(text, video_url)
        logger.success(f"PDF created successfully at: {pdf_path}")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
