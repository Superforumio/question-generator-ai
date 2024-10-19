# Question Generator AI

This project is a FastAPI application that generates questions and answers based on the content of a given URL. It uses Firecrawl to scrape web content and OpenAI's GPT model to generate Q&A pairs.

## Features

- Scrape content from a given URL using Firecrawl
- Generate question-answer pairs based on the scraped content using OpenAI's GPT model
- RESTful API endpoint for easy integration

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

1. Start the FastAPI server:
   ```
   poetry run uvicorn main:app --reload
   ```

2. The API will be available at `http://localhost:8000`

3. To generate Q&A pairs for a URL, make a GET request to:
   ```
   http://localhost:8000/generate_qa/{url}
   ```
   Replace `{url}` with the URL you want to generate questions for.

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
