from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from app.routes.softium import router as softium_router
from app.routes.reports import router as reports_router
from app.logger_config import logger

app = FastAPI(title="Softium Reports Generator")


# --- middleware ---
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"➡️  {request.method} {request.url}")

    response = await call_next(request)

    logger.info(f"⬅️  {request.method} {request.url} — {response.status_code}")
    return response


# routes
app.include_router(softium_router)
app.include_router(reports_router)

app.mount("/", StaticFiles(directory="static", html=True), name="static")
