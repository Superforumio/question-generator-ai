from typing import Union
from fastapi import FastAPI, HTTPException
from firecrawl import FirecrawlApp
import os
from dotenv import load_dotenv
from pydantic import BaseModel
import logging
from openai import OpenAI

load_dotenv()

firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

if not firecrawl_api_key:
    raise ValueError("FIRECRAWL_API_KEY is not set in the .env file")

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY is not set in the .env file")

firecrawl_app = FirecrawlApp(api_key=firecrawl_api_key)
openai.api_key = openai_api_key

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

        # Generate Q&A pairs using OpenAI's GPT model
        logger.info("Sending request to OpenAI API")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that generates questions and answers based on given content.",
                },
                {
                    "role": "user",
                    "content": f"Generate 5 question-answer pairs based on the following content:\n\n{content}",
                },
            ],
        )
        logger.info("Received response from OpenAI API")

        # Parse the generated Q&A pairs
        qa_pairs = []
        message_content = response.choices[0].message.content.strip().split("\n")
        for i in range(0, len(message_content), 2):
            if i + 1 < len(message_content):
                question = message_content[i].strip()
                answer = message_content[i + 1].strip()
                qa_pairs.append(QAPair(question=question, answer=answer))

        logger.info(f"Generated {len(qa_pairs)} Q&A pairs")
        return qa_pairs

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
