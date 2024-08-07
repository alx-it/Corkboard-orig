from fastapi import FastAPI

from app.auth import router as auth_router
from app.tickets import router as tickets_router
from app.db import database

app = FastAPI(
    title="Corkboard",
    version="1.0.0",
    summary="FastAPI ticket system",
    description="Async FastAPI ticket system for communities with login and communications over Telegram bot",
    debug=True,
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(auth_router.router, prefix="/auth", tags=["Aутентификация"])
app.include_router(tickets_router.router, prefix="/tickets", tags=["Объявления"])
