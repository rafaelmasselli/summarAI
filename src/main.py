from dotenv import load_dotenv

from application.handlers.main_handler import main_handler


def main() -> None:
    load_dotenv()
    main_handler()


if __name__ == "__main__":
    main()
