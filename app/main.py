from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from app.api.lesson_data import router as lesson_data_router
from app.api.report_generation import router as reports_generation_router
from app.core.logger_config import logger

app = FastAPI(title="Script Reports Generator")


# --- middleware ---
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"➡️  {request.method} {request.url}")

    response = await call_next(request)

    logger.info(f"⬅️  {request.method} {request.url} — {response.status_code}")
    return response


# routes
app.include_router(lesson_data_router)
app.include_router(reports_generation_router)

app.mount("/", StaticFiles(directory="static", html=True), name="static")
