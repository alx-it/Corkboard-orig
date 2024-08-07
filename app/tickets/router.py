from datetime import datetime
from typing import List

from asyncpg import ForeignKeyViolationError
from fastapi import APIRouter, HTTPException, Path
from fastapi.exceptions import RequestValidationError, ValidationException
from sqlalchemy.sql import Executable
from starlette import status
from starlette.responses import JSONResponse

from app.db import database
from app.tickets.tables import ticket_table, location_table, regularity_table
from app.tickets import schemas


# Функция для получения id залогиненого пользователя
async def get_current_user():
    return 1


async def get_ticket_list(query: Executable, quantity: str):
    result = None
    if quantity == "one":
        result = await database.fetch_one(query)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found"
            )
    elif quantity == "many":
        result = await database.fetch_all(query)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Tickets not found"
            )
    return result


router = APIRouter()


@router.get("/list", response_model=List[schemas.Ticket])
async def list_tickets():
    query = ticket_table.select()
    return await get_ticket_list(query, "many")


@router.get("/my", response_model=List[schemas.Ticket])
async def my_tickets():
    user_id = await get_current_user()
    query = ticket_table.select().where(ticket_table.c.manager == user_id)
    return await get_ticket_list(query, "many")


@router.get("/by_location_id/{id}", response_model=List[schemas.Ticket])
async def list_tickets_by_id(id: int = Path(..., gt=0)):
    query = ticket_table.select().where(ticket_table.c.location == id)
    return await get_ticket_list(query, "many")


@router.get("/by_location_slug/{slug}", response_model=List[schemas.Ticket])
async def list_tickets_by_slug(slug: str):
    query_location = location_table.select().where(location_table.c.slug == slug)
    location = await database.fetch_one(query_location)
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect location"
        )
    location_id = location["id"]
    query = ticket_table.select().where(ticket_table.c.location == location_id)
    return await get_ticket_list(query, "many")


@router.get("/by_regularity_id/{id}", response_model=List[schemas.Ticket])
async def list_tickets_by_regularity(id: int = Path(..., gt=0)):
    query = ticket_table.select().where(ticket_table.c.regularity == id)
    return await get_ticket_list(query, "many")


@router.get("/{id}", response_model=schemas.Ticket)
async def get_ticket(id: int = Path(..., gt=0)):
    query = ticket_table.select().where(ticket_table.c.id == id)
    return await get_ticket_list(query, "one")


@router.post("/create", response_model=schemas.Ticket)
async def create_ticket(ticket: schemas.TicketWrite):
    updated = datetime.utcnow()
    query = ticket_table.insert().values(
        header=ticket.header,
        text=ticket.text,
        location=ticket.location,
        regularity=ticket.regularity,
        manager=await get_current_user(),
        updated=updated,
        complaint=False,
    )
    try:
        new_ticket_id = await database.execute(query)
    except ForeignKeyViolationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Validation error. Check if input values correct.",
        )
    except RequestValidationError:
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Could`nt execute request. Try again.",
        )
    return {**ticket.model_dump(), "id": new_ticket_id, "updated": updated}


@router.put("/{id}", response_model=schemas.Ticket)
async def update_ticket(ticket: schemas.TicketWrite, id: int = Path(..., gt=0)):
    query = ticket_table.select().where(ticket_table.c.id == id)
    check_ticket = await database.fetch_one(query)

    if not check_ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect ticket id"
        )

    updated = datetime.utcnow()
    update_query = (
        ticket_table.update()
        .where(ticket_table.c.id == id)
        .values(
            header=ticket.header,
            text=ticket.text,
            location=ticket.location,
            regularity=ticket.regularity,
            manager=await get_current_user(),
            updated=updated,
            complaint=False,
        )
        .returning(ticket_table.c.id)
    )
    try:
        new_ticket_id = await database.execute(update_query)
    except ForeignKeyViolationError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Validation error. Check if input values correct.",
        )
    except RequestValidationError:
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Could`nt execute request. Try again.",
        )
    return {**ticket.model_dump(), "id": new_ticket_id, "updated": updated}


@router.delete("/{id}", response_model=None)
async def delete_ticket(id: int = Path(..., gt=0)):
    query = (
        ticket_table.delete()
        .where(ticket_table.c.id == id)
        .returning(ticket_table.c.id)
    )
    try:
        result = await database.execute(query)
    except RequestValidationError:
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Could`nt execute request. Try again.",
        )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect ticket id"
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content="Successfully deleted")
