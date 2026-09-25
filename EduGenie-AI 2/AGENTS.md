# AGENTS.md

## Project overview
This repository is a FastAPI application for an AI-powered learning assistant named EduGenie. The app exposes educational endpoints for Q&A, explanations, quizzes, summaries, and learning-path recommendations.

## Working conventions
- Keep request/response validation in [schemas.py](schemas.py) aligned with the route signatures in [main.py](main.py).
- Use async endpoint handlers when calling model logic; do not block the event loop.
- Keep frontend assets under [static/](static/) and page templates under [templates/](templates/).
- Prefer reading existing modules before making changes; the project is small and the AI logic is split by feature.

## Key files
- [main.py](main.py): FastAPI app definition, routes, and startup config.
- [config.py](config.py): environment loading and app settings.
- [schemas.py](schemas.py): Pydantic models used by the API.
- [qna.py](qna.py): question-answering logic.
- [explanation_module.py](explanation_module.py): topic explanation logic.
- [quiz_module.py](quiz_module.py): quiz generation logic.
- [summary_module.py](summary_module.py): text summarization logic.
- [learning_path.py](learning_path.py): learning-path recommendations logic.

## Local run commands
From the repository root:

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

Then open:
- http://127.0.0.1:8000/
- http://127.0.0.1:8000/docs#/

## Environment and configuration
The app loads settings from [config.py](config.py) and the local `.env` file if present. Supported values include:
- `APP_NAME`
- `GEMINI_MODEL`
- `HOST`
- `PORT`

If an endpoint depends on Gemini, make sure the runtime environment contains the required API configuration before testing that route.

## Notes for AI coding agents
- When adding new routes, update the matching request/response models in [schemas.py](schemas.py) and keep the route naming consistent with the existing API style.
- For UI work, prefer editing the templates and static assets rather than hard-coding logic into the HTML.
- Treat `main.py` as the central integration point for the app.
