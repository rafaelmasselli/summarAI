from application.handlers.youtube_handler import YouTubeHandler


def resume_video():
    link = input("Enter the video link: ")
    youtube_handler = YouTubeHandler("gemini")
    return youtube_handler.handle_video_processing(link)


def main_handler():
    return resume_video()
