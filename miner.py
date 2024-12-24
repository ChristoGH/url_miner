"""News API integration module for fetching articles about human trafficking.

This module provides functionality to fetch articles from News API
with specific search criteria and date ranges.
"""

import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, TypedDict

from dotenv import load_dotenv
from newsapi import NewsApiClient
from newsapi.newsapi_exception import NewsAPIException


class Article(TypedDict):
    """Type definition for article data structure."""

    source: Dict[str, str]
    author: Optional[str]
    title: str
    description: Optional[str]
    url: str
    urlToImage: Optional[str]
    publishedAt: str
    content: Optional[str]


# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize NewsAPI client
NEWS_API_KEY: Optional[str] = os.environ.get("NEWS_API_KEY")
if not NEWS_API_KEY:
    logger.error("NEWS_API_KEY environment variable is not set")
    raise ValueError("NEWS_API_KEY environment variable is not set")

try:
    newsapi = NewsApiClient(api_key=NEWS_API_KEY)
except Exception as e:
    logger.error(f"Failed to initialize NewsAPI client: {e}")
    raise


def fetch_new_articles(
    days_back: int = 10,
    query: str = "incident of human trafficking",
    sort_by: str = "publishedAt",
) -> List[Article]:
    """Fetch recent articles from NewsAPI based on specified criteria.

    Args:
        days_back: Number of days to look back for articles. Defaults to 10.
        query: Search query string. Defaults to "human trafficking".
        sort_by: Sorting criteria for articles. Defaults to "publishedAt".

    Returns:
        List[Article]: List of article dictionaries containing
        information such as title, description, URL, etc.

    Raises:
        NewsAPIException: If there's an error with the NewsAPI request.
        ValueError: If date parameters are invalid.
    """
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)

        # Format dates as required by NewsAPI
        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")

        logger.info(
            f"Fetching articles from {start_date_str} to {end_date_str} "
            f"with query: {query}"
        )

        response = newsapi.get_everything(
            q=query,
            from_param=start_date_str,
            to=end_date_str,
            sort_by=sort_by,
        )

        articles: List[Article] = response.get("articles", [])

        logger.info(f"Successfully fetched {len(articles)} articles")
        return articles

    except NewsAPIException as e:
        logger.error(f"NewsAPI request failed: {e}")
        raise

    except Exception as e:
        logger.error(f"Unexpected error while fetching articles: {e}")
        raise


def main() -> None:
    """Run the main program to fetch and display articles."""
    articles = fetch_new_articles(query="human trafficking", days_back=1)
    print(articles)


if __name__ == "__main__":
    main()
