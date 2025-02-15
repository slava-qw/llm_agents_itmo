import httpx
from typing import List
# from ya_search_agent import ya_search
from .tav_agent import search_web as search_func


async def search_web(query: str):
    """
    Performs an external API search, returns no more than `max_results` of links.
    :param query: a search query.
    :param max_results: the maximum number of links to be returned.
    :return: a list of relevant links.
    """
    result, all_links = await search_func(query)

    return result, all_links

    # Dummy stub (we return some conditional links):
    # return [
    #     "https://itmo.ru/ru/",
    #     "https://abit.itmo.ru/",
    #     "https://news.itmo.ru/ru/"
    # ][:max_results]
