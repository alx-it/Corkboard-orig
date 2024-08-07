from datetime import datetime
from pydantic import BaseModel, Field


class Location(BaseModel):
    id: int = Field(gt=0, is_required=False)
    name: str = Field(max_length=64, unique=True, is_required=True)
    address: str = Field(max_length=128, is_required=True)
    slug: str = Field(max_length=64, unique=True, is_required=True)


class Regularity(BaseModel):
    id: int = Field(gt=0, is_required=False)
    name: str = Field(max_length=64, unique=True, is_required=True)


class Ticket(BaseModel):
    id: int = Field(gt=0, is_required=False)
    header: str = Field(max_length=128, is_required=True)
    text: str = Field(max_length=512, is_required=True)
    location: int = Field(gt=0, is_required=True)
    regularity: int = Field(gt=0, is_required=True)
    manager: int = Field(gt=0, is_required=True)
    updated: datetime = Field(is_required=False)
    complaint: bool = Field(default=False, is_required=False)


class TicketWrite(BaseModel):
    header: str = Field(max_length=128, is_required=True)
    text: str = Field(max_length=512, is_required=True)
    location: int = Field(gt=0, is_required=True)
    regularity: int = Field(gt=0, is_required=True)
    manager: int = Field(gt=0, is_required=True)
