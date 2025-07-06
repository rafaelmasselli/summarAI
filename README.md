# LLM Estudy

A tool for summarizing educational content using LLMs.

## Features

- YouTube video summarization
- PDF export of summaries
- Support for multiple language models

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
3. Activate the virtual environment:

   ```bash
   # On Linux/Mac
   source .venv/bin/activate

   # On Windows
   .\.venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Create a `.env` file in the root directory
2. Add your API keys:
   ```
   GOOGLE_API_KEY=your_google_api_key
   ```

## Usage

Run the main script:

```bash
python src/main.py
```

The program will:

1. Prompt you for a YouTube video URL
2. Extract the transcript
3. Generate a summary using the configured LLM
4. Save the summary as a PDF in the `pdfs` directory

## Project Structure

The project follows a clean architecture approach:

- `domain`: Core business rules and interfaces
- `application`: Use cases and business logic
- `infrastructure`: Concrete implementations and external integrations

## License

MIT
