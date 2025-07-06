from application.services.pdf import PdfService
from application.services.youtube import YoutubeService


def summarize_video():
    link = input("Enter the video link: ")
    print("Processing video... This may take a moment.")

    youtube_handler = YoutubeService(link)
    text = youtube_handler.summarize_video()

    print("\nSummary generated successfully!")
    print("\nCreating PDF...")

    pdf_service = PdfService()
    pdf_path = pdf_service.create_pdf(text)

    print(f"\nSummary PDF saved at: {pdf_path}")
    print("\nProcess completed successfully!")


def main_handler():
    return summarize_video()
