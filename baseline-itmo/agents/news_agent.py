import httpx
from typing import List

NEWS_RSS_URL = "https://news.itmo.ru/ru/rss"


async def fetch_latest_news(max_items: int = 3) -> List[str]:
    """
    We get a list of links to the latest news about ITMO (for example, from RSS).
    :param max_items: how many links to the latest news to return.
    """
    # Example: receiving RSS feed
    # # async with httpx.AsyncClient() as client:
    # resp = await client.get(NEWS_RSS_URL)

    # # Parse XML, pull out the necessary elements <item><link>...</link></item>
    #     # news_links = parse_rss(resp.text)
    #     # return news_links[:max_items]

    # To simplify, a stub
    return [
        "https://news.itmo.ru/ru/news/1",
        "https://news.itmo.ru/ru/news/2",
        "https://news.itmo.ru/ru/news/3",
    ][:max_items]
