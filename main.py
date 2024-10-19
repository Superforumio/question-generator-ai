from typing import Union
from fastapi import FastAPI, HTTPException
from firecrawl import FirecrawlApp
import os
import logging
from dotenv import load_dotenv
from pydantic import BaseModel
from openai import OpenAI
import re
import json

load_dotenv()

firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

if not firecrawl_api_key:
    raise ValueError("FIRECRAWL_API_KEY is not set in the .env file")

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY is not set in the .env file")

firecrawl_app = FirecrawlApp(api_key=firecrawl_api_key)

# Initialize the OpenAI client
client = OpenAI(api_key=openai_api_key)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


class QAPair(BaseModel):
    question: str
    answer: str


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/generate_qa/{url:path}", response_model=list[QAPair])
async def generate_qa(url: str):
    try:
        logger.info(f"Received request to generate Q&A for URL: {url}")

        # Scrape the single URL using Firecrawl
        logger.info("Starting Firecrawl scrape")
        scrape_result = firecrawl_app.scrape_url(url, params={"formats": ["markdown"]})
        logger.info("Firecrawl scrape completed")

        # Extract the markdown content from the scrape result
        content = scrape_result.get("markdown", "")
        logger.info(f"Extracted content length: {len(content)} characters")

        # Generate Q&A pairs using the specified model
        logger.info("Sending request to OpenAI API")
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Using the specified model name
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that generates questions and answers based on given content. Provide your response as a JSON array of objects, each with 'question' and 'answer' keys.",
                },
                {
                    "role": "user",
                    "content": f"Generate 5 question-answer pairs based on the following content. Ensure each pair has both a question and an answer:\n\n{content}",
                },
            ],
            response_format={"type": "json_object"},
        )
        logger.info("Received response from OpenAI API")

        # Parse the generated Q&A pairs
        response_content = json.loads(response.choices[0].message.content)
        logger.info(f"Parsed JSON content: {response_content}")

        # Handle different possible JSON structures
        if isinstance(response_content, list):
            qa_pairs = response_content
        elif isinstance(response_content, dict):
            qa_pairs = (
                response_content.get("qa_pairs")
                or response_content.get("pairs")
                or list(response_content.values())[0]
            )
        else:
            raise ValueError("Unexpected response format from OpenAI API")

        # Ensure each pair has 'question' and 'answer' keys
        qa_pairs = [
            {"question": pair.get("question", ""), "answer": pair.get("answer", "")}
            for pair in qa_pairs
            if isinstance(pair, dict)
        ]

        # Convert to QAPair objects
        qa_pairs = [
            QAPair(**pair) for pair in qa_pairs if pair["question"] and pair["answer"]
        ]

        logger.info(f"Generated {len(qa_pairs)} Q&A pairs")
        return qa_pairs

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
