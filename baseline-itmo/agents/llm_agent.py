import asyncio
from typing import Optional
from .yagpt_llm import give_answer


async def generate_answer(
        query: str,
        context: str = "",
        links: Optional[str] = None,
) -> str:
    """
    Response generation using the selected free model (LLM).
        :param query: The user's original question.
        :param context: Additional context obtained from search or news.
        :param links:
        :return: the generated response.
    """

    guide_promt = ("Если в вопросе есть варианты ответов, то приведи правильный ответ на вопрос используя контекст и "
                   "ссылки в формате `Ответ: <правильный вариант ответа в виде цифры> \n Пояснение ответа`. Если "
                   "вариантов ответов нет, то просто приведи ответ на заданный вопрос.")

    prompt = f"{guide_promt}\nКонтекст:{context}\n\nВопрос: {query}\nОтвет:"

    response = await give_answer(guide_promt, prompt, links=links)
    return response
