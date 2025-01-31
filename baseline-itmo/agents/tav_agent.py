import asyncio

from tavily import TavilyClient

client = TavilyClient(api_key=None)


async def search_web(query: str):
    """
    Performs an external API search, returns no more than `max_results` of links.
    :param query: a search query.
    :param max_results: the maximum number of links to be returned.
    :return: a list of relevant links.
    """
    response = client.search(query)
    results = response['results']

    links = []
    context = ""

    for elem in results:
        links.append(elem['url'])
        context += elem['title'] + "\n" + elem['content'] + "\n\n"

    return context, links

# if __name__ == "__main__":
#     res, links = asyncio.run(search_web("What is Fermat's Last Theorem?"))
#     print(res)
#     print(links)



