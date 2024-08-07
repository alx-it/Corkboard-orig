from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

from typing_extensions import Annotated


class Role(BaseModel):
    id: int = Field(gt=0, is_required=False)
    name: str = Field(max_length=64, is_required=True)


class User(BaseModel):
    id: int = Field(gt=0, is_required=False)
    first_name: str = Field(max_length=64, is_required=True)
    last_name: str = Field(max_length=64, is_required=True)
    user_name: str = Field(max_length=64, is_required=True)
    hashed_password: str = Field(max_length=1024, is_required=True)
    role: int = Field(gt=0, is_required=True)
    is_active: bool = Field(default=True, is_required=False)
    is_superuser: bool = Field(default=False, is_required=False)


class TelegramAuth(BaseModel):
    id: int = Field(gt=0, is_required=True)
    first_name: str = Field(is_required=True)
    last_name: str = Optional[Annotated[str, Field]]
    username: str = Field(is_required=True)
    photo_url: str = Optional[Annotated[str, Field]]
    auth_date: str = Field(is_required=True)
    hash: str = Field(is_required=True)
