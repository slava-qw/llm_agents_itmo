import time

from fastapi import Request, Response
from fastapi.responses import HTMLResponse
from schemas.request import PredictionRequest, PredictionResponse
from utils.logger import setup_logger

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import HttpUrl, parse_obj_as

from agents.search_agent import search_web
# from agents.ya_search_agent import ya_search

# from agents.news_agent import fetch_latest_news
from agents.llm_agent import generate_answer

from utils.text_refactoring import extract_multiple_choice_answers, detect_correct_choice_from_llm

# from utils.logger_sync import setup_logger
# logger = setup_logger()

app = FastAPI()
logger = None


@app.on_event("startup")
async def startup_event():
    global logger
    logger = await setup_logger()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    body = await request.body()
    await logger.info(
        f"Incoming request: {request.method} {request.url}\n"
        f"Request body: {body.decode()}"
    )

    response = await call_next(request)
    process_time = time.time() - start_time

    response_body = b""
    async for chunk in response.body_iterator:
        response_body += chunk

    await logger.info(
        f"Request completed: {request.method} {request.url}\n"
        f"Status: {response.status_code}\n"
        f"Response body: {response_body.decode()}\n"
        f"Duration: {process_time:.3f}s"
    )

    return Response(
        content=response_body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type,
    )


@app.post("/api/request", response_model=PredictionResponse)
async def predict(body: PredictionRequest):
    """
    The main endpoint. We receive the request and the id, and enter the JSON with the structure:
    {
        "id": <body.id >,
        "answer": <int or null>,
        "reasoning": <string>,
        "sources": <URL list>
      }
    """
    try:
        logger.info(f"Processing prediction request with id: {body.id}")

        choices = extract_multiple_choice_answers(body.query)
        num_choices = len(choices)

        # search_task = asyncio.create_task(search_web(body.query))
        # news_task = asyncio.create_task(fetch_latest_news(max_items=3))

        # found_links, news_links = await asyncio.gather(search_task, news_task)

        # all_links = found_links + news_links
        # context_for_llm = f"Ссылки: {', '.join(all_links)}"

        context_for_llm, all_links = await search_web(body.query)

        llm_text = await generate_answer(
            query=body.query,
            context=context_for_llm,
            links=all_links,
        )
        if num_choices > 0:
            answer_choice = detect_correct_choice_from_llm(llm_text, num_choices)
        else:
            answer_choice = None

        response = PredictionResponse(
            id=body.id,
            answer=answer_choice,
            reasoning=llm_text,  # in reasoning part put the full LLM response (for simplicity)
            sources=[parse_obj_as(HttpUrl, url) for url in all_links[:3]]  # take first 3
        )

        await logger.info(f"Successfully processed request {body.id}")
        return response

    except ValueError as e:
        error_msg = str(e)
        await logger.error(f"Validation error for request {body.id}: {error_msg}")
        raise HTTPException(status_code=400, detail=error_msg)
    except Exception as e:
        await logger.error(f"Internal error processing request {body.id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """
    Fancy главная страница для квиза об ИТМО.
    """
    html_content = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8" />
        <title>ITMO Quiz Landing Page</title>
        <style>
            body {
                margin: 0;
                padding: 0;
                background: linear-gradient(to bottom right, #2c3e50, #2980b9);
                font-family: 'Arial', sans-serif;
                color: #fff;
                text-align: center;
            }
            .container {
                max-width: 900px;
                margin: 0 auto;
                padding: 50px 20px 100px 20px;
            }
            h1 {
                margin: 30px 0;
                font-size: 3em;
                letter-spacing: 1px;
            }
            p {
                font-size: 1.2em;
                line-height: 1.6em;
                margin-bottom: 30px;
            }
            .button {
                display: inline-block;
                padding: 15px 30px;
                margin: 10px;
                font-size: 1.2em;
                color: #fff;
                background-color: #e67e22;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                text-decoration: none;
                transition: background-color 0.3s ease;
            }
            .button:hover {
                background-color: #f39c12;
            }
            .links a {
                color: #fff;
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Добро пожаловать в ITMO Quiz!</h1>
            <p>
                Этот сервис отвечает на ваши вопросы об Университете ИТМО, используя
                модели глубокого обучения и поиск актуальной информации из открытых источников.
            </p>
            <p>
                <strong>Как это работает?</strong> <br />
                Вы отправляете запрос, указывая вопрос (с вариантами ответов или без), а наш агент:
            </p>
            <ul style="text-align:left; display:inline-block; margin: 0 auto;">
                <li>Проверяет варианты ответов (если они есть).</li>
                <li>Использует языковую модель (LLM) для генерации текста.</li>
                <li>Подключается к поисковым и новостным источникам (RSS, Google/Bing).</li>
                <li>Формирует аккуратный JSON-ответ (id, answer, reasoning, sources).</li>
            </ul>
            <p>
                Ознакомьтесь с документацией и примерами:
                <div class="links">
                    <a href="https://github.com/roman02s/baseline-itmo" target="_blank">
                        GitHub Repositoy (Baseline-ITMO)
                    </a><br/>
                    <a href="https://itmo.ru/ru/" target="_blank">Официальный сайт Университета ИТМО</a>
                </div>
            </p>
            <p>Готовы протестировать?</p>
            <a class="button" href="https://yandex.ru/video/preview/10047068089015706478" target="_blank">Начать Quiz</a>
        </div>
    </body>
    </html>
    """
    return html_content


# if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=False)
