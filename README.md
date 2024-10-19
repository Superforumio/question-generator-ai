# Question Generator AI

This project is a FastAPI application that generates questions and answers based on the content of a given URL. It uses Firecrawl to scrape web content and OpenAI's GPT model to generate Q&A pairs.

## Features

- Scrape content from a given URL using Firecrawl
- Generate question-answer pairs based on the scraped content using OpenAI's GPT model
- RESTful API endpoint for easy integration
- Configurable logging for better debugging and monitoring

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.8+
- Poetry (for dependency management)
- Firecrawl API key
- OpenAI API key

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Superforumio/question-generator-ai.git
   cd question-generator-ai
   ```

2. Install dependencies using Poetry:
   ```
   poetry install
   ```

3. Create a `.env` file in the project root and add your API keys:
   ```
   FIRECRAWL_API_KEY=your_firecrawl_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

There are two ways to run the application:

### 1. Using Uvicorn (recommended for development)

Start the FastAPI server with Uvicorn:

```
poetry run uvicorn main:app --reload --log-level info
```

This command starts the server with auto-reload enabled and sets the log level to INFO.

### 2. Running the Python script directly

Alternatively, you can run the Python script directly:

```
poetry run python main.py
```

This method is useful for seeing all logs directly in the console.

The API will be available at `http://localhost:8000`

## API Endpoints

### Generate Q&A Pairs

- **URL**: `/generate_qa/{url}`
- **Method**: GET
- **URL Params**: 
  - `url`: The URL to scrape and generate questions from (URL-encoded)
- **Success Response**:
  - **Code**: 200
  - **Content**: JSON array of question-answer pairs
    ```json
    [
      {
        "question": "What is FastAPI?",
        "answer": "FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.6+ based on standard Python type hints."
      },
      ...
    ]
    ```
- **Error Response**:
  - **Code**: 500
  - **Content**: `{ "detail": "Error message" }`

## Logging

The application uses Python's built-in logging module. Logs are output to the console and include information about the scraping process, API calls, and any errors that occur.

## Customization

- To adjust the number of Q&A pairs generated, modify the `generate_qa` function in `main.py`.
- To use a different OpenAI model, change the `model` parameter in the `client.chat.completions.create()` call.

## Troubleshooting

If you encounter any issues:

1. Check that your API keys are correctly set in the `.env` file.
2. Ensure all dependencies are installed by running `poetry install`.
3. Check the console logs for any error messages or unexpected behavior.

## Contributing

Contributions to the Question Generator AI project are welcome. Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
