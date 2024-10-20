from firecrawl import FirecrawlApp
from dotenv import load_dotenv
import os

load_dotenv()

app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

# Scrape a website:
scrape_status = app.scrape_url(
    "https://firecrawl.dev", params={"formats": ["markdown", "html"]}
)
print(scrape_status)

# Crawl a website:
crawl_status = app.crawl_url(
    "https://firecrawl.dev",
    params={"limit": 100, "scrapeOptions": {"formats": ["markdown", "html"]}},
)
print(crawl_status)
