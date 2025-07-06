# SummarAI

A tool for summarizing educational content using large language models (LLMs).

![SummarAI](https://img.shields.io/badge/SummarAI-v1.0-blue)
![Python](https://img.shields.io/badge/Python-3.9%2B-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Overview

SummarAI is an application that uses advanced language models to process and summarize educational content from YouTube videos. The application extracts the video transcript, processes the text using a language model (such as Google's Gemini), and generates a structured summary that is exported as a formatted PDF document.

## Features

- **Video Transcript Extraction**: Automatically extracts transcripts from YouTube videos
- **Advanced Text Processing**: Uses LLMs to generate concise and structured summaries
- **PDF Export**: Creates well-formatted PDF documents with the generated summaries
- **Logging System**: Provides detailed feedback on the execution process
- **Clean Architecture**: Code organization following Clean Architecture principles
- **Multiple Model Support**: Flexible infrastructure to use different LLMs

## Requirements

- Python 3.9 or higher
- Google API key to access the Gemini model
- Internet connection to access YouTube and Google APIs

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/rafaelmasselli/summarAI.git
   cd summarAI
   ```

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

3. (Optional) Configure additional parameters in the `.env` file:

   ```
   # Gemini model to be used
   MODEL_NAME=gemini-2.0-flash-001

   # Directory to save PDFs
   PDF_OUTPUT_DIR=./pdfs
   ```

## Usage

Run the main script:

```bash
python src/main.py
```

The program will:

1. Prompt for a YouTube video URL
2. Extract the video transcript
3. Process the text using the configured language model
4. Generate a structured summary
5. Save the summary as a PDF in the `pdfs` directory
6. Display detailed logs of the process

### Usage Example

```
$ python src/main.py
Enter the video link: https://www.youtube.com/watch?v=example
==================================================
2023-07-06 14:30:21 - INFO - Initializing application
==================================================
==================================================
2023-07-06 14:30:21 - INFO - Environment variables loaded
==================================================
==================================================
2023-07-06 14:30:21 - INFO - Starting video summarization process
==================================================
==================================================
2023-07-06 14:30:22 - INFO - Extracting video transcript...
==================================================
==================================================
2023-07-06 14:30:25 - INFO - Transcript extracted successfully (15234 characters)
==================================================
==================================================
2023-07-06 14:30:25 - INFO - Initializing language model...
==================================================
==================================================
2023-07-06 14:30:26 - INFO - Generating summary...
==================================================
==================================================
2023-07-06 14:30:40 - SUCCESS - ✓ Summary generated successfully.
==================================================
==================================================
2023-07-06 14:30:40 - INFO - Creating PDF document
==================================================
==================================================
2023-07-06 14:30:41 - INFO - Creating enhanced PDF document...
==================================================
==================================================
2023-07-06 14:30:42 - SUCCESS - ✓ PDF successfully created at: /path/to/pdfs/summary_20230706_143042.pdf
==================================================
==================================================
2023-07-06 14:30:42 - SUCCESS - ✓ PDF created successfully at: /path/to/pdfs/summary_20230706_143042.pdf
==================================================
```

## Project Structure

The project follows a clean architecture approach with three main layers:

```
src/
├── domain/             # Core business rules and interfaces
│   ├── config/         # Domain configurations
│   └── interfaces/     # Interfaces (contracts) for implementations
│
├── application/        # Use cases and business logic
│   ├── handlers/       # Application flow controllers
│   └── services/       # Application-specific services
│
├── infrastructure/     # Concrete implementations and integrations
│   ├── factories/      # Factories for object creation
│   ├── memory/         # Memory system implementations
│   ├── models/         # Language model implementations
│   └── prompts/        # Prompt template management
│
└── util/               # Shared utilities
    └── logger.py       # Logging system
```

### Main Components

#### Domain Layer

- **Interfaces**: Defines contracts that implementations must follow

  - `Model`: Interface for language models
  - `Memory`: Interface for memory systems

- **Configurations**: Configuration classes and data models
  - `ModelConfig`: Configuration for language models

#### Application Layer

- **Handlers**: Controllers that coordinate the application flow

  - `main_handler.py`: Manages the main application flow

- **Services**: Implement specific business logic
  - `youtube.py`: Service for extracting and processing YouTube videos
  - `pdf.py`: Service for creating PDF documents

#### Infrastructure Layer

- **Models**: Concrete implementations of language models

  - `gemini.py`: Implementation of Google's Gemini model

- **Factories**: Create object instances

  - `model_factory.py`: Factory for creating language models
  - `memory_factory.py`: Factory for creating memory systems

- **Prompts**: Management of prompt templates
  - `prompt_manager.py`: Manages prompt templates for different models
  - `base_prompts.yaml`: Prompt definitions in YAML format

#### Utilities

- **Logger**: Colored and formatted logging system
  - `logger.py`: Implementation of logs with different levels and file output

## Workflow

1. **URL Input**: The user provides a YouTube video URL
2. **Transcript Extraction**: The system extracts the video transcript
3. **LLM Processing**: The transcript is sent to the language model
4. **Summary Generation**: The model generates a structured summary of the content
5. **PDF Creation**: The summary is formatted and saved as a PDF document
6. **User Feedback**: Detailed logs are displayed throughout the process

## Customization

### Modifying Prompts

The prompts used to instruct the language model are defined in the `src/infrastructure/prompts/base_prompts.yaml` file. You can modify this file to change the instructions sent to the model.

```yaml
gemini:
  default: |
    You are an AI specialized in syntactic analysis and text summarization.
    Your goal is to read the provided text, identify the most relevant information, and present an objective and coherent summary.

    Specific instructions:
    1. Extract and highlight the most important information from the provided text.
    2. Remove irrelevant elements, redundancies, and informal language.
    3. Identify and highlight keywords such as country names (e.g., China), events, or central topics.
    4. The summary should clearly present what happened, who was involved, and the main impact or context.
    5. Analyze the following text and provide a summary according to the instructions above.
    6. Respond in Portuguese.
```

### Adding New Models

To add support for a new language model:

1. Create a new class that implements the `Model` interface in `src/infrastructure/models/`
2. Register the new model in the `ModelFactory`
3. Add prompt templates for the new model in `base_prompts.yaml`

## Troubleshooting

### Common Errors

- **Invalid API Key**: Check if your Google API key is correct in the `.env` file
- **Transcript Extraction Failure**: Make sure the video has available captions
- **PDF Error**: If there are issues with PDF generation, check the logs for specific details

### Logs

Logs are saved in the `logs/` directory and can be useful for diagnosing problems:

```bash
cat logs/summarai.log
```

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a branch for your feature (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT license - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [LangChain](https://github.com/langchain-ai/langchain) for providing tools to work with LLMs
- [Google Generative AI](https://ai.google.dev/) for making the Gemini model available
- [FPDF](https://github.com/py-pdf/fpdf2) for the PDF generation library
