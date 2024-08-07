from datetime import datetime
from typing import List

from asyncpg import ForeignKeyViolationError
from fastapi import APIRouter, Path, Depends, Request, status
from fastapi.exceptions import RequestValidationError, ValidationException
from sqlalchemy.sql import Executable
from starlette.responses import JSONResponse, HTMLResponse

from app.config import TG_BOT_TOKEN
from app.auth import schemas
from app.auth.functions import validate_telegram_data
from app.auth.exceptions import TelegramDataIsOutdated, TelegramDataError
from app.auth.schemas import TelegramAuth

router = APIRouter()


@router.get("/me", response_model=schemas.User)
async def get_me():
    return JSONResponse(status_code=status.HTTP_200_OK, content="Logged user")


@router.get("/tg_widget")
async def get_tg_widget():
    with open("app/auth/widget.html") as file:
        widget = file.read()
    return HTMLResponse(widget)


@router.post("/auth")
async def auth(request: Request, params: TelegramAuth = Depends(TelegramAuth)):
    try:
        result = validate_telegram_data(TG_BOT_TOKEN, params)

    except TelegramDataIsOutdated:
        return JSONResponse(
            content="The authentication data is expired.",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    except TelegramDataError:
        return JSONResponse(
            content="The request contains invalid data.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if result:
        # log_in logic here
        # await proceed_login()
        return JSONResponse(status_code=status.HTTP_200_OK, content="Logged in!")
