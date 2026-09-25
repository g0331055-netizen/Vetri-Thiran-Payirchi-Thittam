from pathlib import Path
import importlib
from os import environ
from types import SimpleNamespace

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

try:
    settings = importlib.import_module("config").settings
except (ImportError, AttributeError):
    settings = SimpleNamespace(
        APP_NAME=environ.get("APP_NAME", "EduGenie"),
        GEMINI_MODEL=environ.get("GEMINI_MODEL", "gemini-pro"),
        HOST=environ.get("HOST", "127.0.0.1"),
        PORT=int(environ.get("PORT", "8000")),
    )
from explanation_module import explain_topic
from learning_path import get_learning_recommendations
from qna import answer_question
from quiz_module import generate_quiz
from schemas import (
    ApiResponse,
    ExplainRequest,
    LearningPathRequest,
    LearningPathResponse,
    QuizRequest,
    QuizResponse,
    TextRequest,
)
from summary_module import summarize_text


BASE_DIR = Path(__file__).resolve().parent


app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0",
)


# Static files
app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static"), check_dir=False),
    name="static",
)


# HTML templates
templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)


# ---------------------------------------------------------
# FRONTEND
# ---------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "app_name": settings.APP_NAME,
        },
    )


# ---------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "application": settings.APP_NAME,
        "model": settings.GEMINI_MODEL,
    }


# ---------------------------------------------------------
# QUESTION ANSWERING
# ---------------------------------------------------------

@app.post(
    "/qa",
    response_model=ApiResponse,
)
async def qa(payload: TextRequest):

    answer = await answer_question(
        payload.text
    )

    return ApiResponse(
        result=answer
    )


# ---------------------------------------------------------
# EXPLANATION
# ---------------------------------------------------------

@app.post(
    "/explain",
    response_model=ApiResponse,
)
async def explain(payload: ExplainRequest):

    answer = await explain_topic(
        payload.text,
        payload.level,
    )

    return ApiResponse(
        result=answer
    )


# ---------------------------------------------------------
# QUIZ
# ---------------------------------------------------------

@app.post(
    "/quiz",
    response_model=QuizResponse,
)
async def quiz(payload: QuizRequest):

    return await generate_quiz(
        payload.text,
        payload.num_questions,
    )


# ---------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------

@app.post(
    "/summarize",
    response_model=ApiResponse,
)
async def summarize(payload: TextRequest):

    summary = await summarize_text(
        payload.text
    )

    return ApiResponse(
        result=summary
    )


# ---------------------------------------------------------
# LEARNING PATH
# ---------------------------------------------------------

@app.post(
    "/learn/recommendations",
    response_model=LearningPathResponse,
)
async def learning_recommendations(
    payload: LearningPathRequest,
):

    return await get_learning_recommendations(
        payload.topic,
        payload.level,
    )


# ---------------------------------------------------------
# RUN DIRECTLY
# ---------------------------------------------------------

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
    )