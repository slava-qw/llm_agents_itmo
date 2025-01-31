from yandex_cloud_ml_sdk import YCloudML

API_KEY = ""
FOLDER_ID = ""


async def give_answer(guide_prompt, prompt, links=None):
    str_links = "\n".join(links)
    messages = [
        {
            "role": "system",
            "text": guide_prompt,
        },
        {
            "role": "user",
            "text": f"{prompt}\n Relevant links:\n{str_links}",
        },
    ]
    sdk = YCloudML(
        folder_id=FOLDER_ID,
        auth=API_KEY,
    )

    result = (
        sdk.models.completions("yandexgpt").configure(temperature=0.5).run(messages)
    )

    return result.alternatives[0].text


