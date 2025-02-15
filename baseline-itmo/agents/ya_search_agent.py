import aiohttp
import asyncio
import os

API_KEY = ""
FOLDER_ID = ""
SEARCH_API_GENERATIVE = f"https://ya.ru/search/xml/generative?folderid={FOLDER_ID}"


async def ya_search(query: str):
    headers = {"Authorization": f"Api-Key {API_KEY}"}
    data = {
        "messages": [
            {
                "content": query,
                "role": "user"
            }
        ],
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(SEARCH_API_GENERATIVE, headers=headers, json=data) as response:
            content_type = response.headers.get("Content-Type", "")
            if "application/json" in content_type:
                response_data = await response.json()
                # print(response_data["message"]["content"])
                all_links = response_data["links"]
                # for i, link in enumerate(response_data["links"], start=1):
                #     print(f"[{i}]: {link}")
                return response_data, all_links

            elif "text/xml" in content_type:
                print("Error:", await response.text())
                return None, None
            else:
                print("Unexpected content type:", await response.text())
                return None, None


# if __name__ == "__main__":
    # asyncio.run(ya_search())
    # return_data, all_links = asyncio.run(ya_search("В каком году был основан ИТМО? Приведи также релевантные ссылки"))
    # print(return_data)
    # print(all_links)
