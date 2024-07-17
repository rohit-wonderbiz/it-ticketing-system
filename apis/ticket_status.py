from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import Annotated, Optional
from sqlalchemy.orm import Session

from models.model_ticket_status import TicketStatus #Models
from models.model_ticket_status import TicketStatusBase, TicketStatusCreate, TicketStatusRead #Pydantic model
from database import SessionLocal

ticket_status = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# Ticket Status Table GET Method ALL
@ticket_status.get("/", status_code=status.HTTP_200_OK)
async def read():
    return "Hello"

# Ticket Status Table GET Method ALL
@ticket_status.get("/ticketStatus/", response_model=list[TicketStatusRead], status_code=status.HTTP_200_OK)
async def read_all_ticketStatus(db: db_dependency):
    employee_ticketsStatus = db.query(TicketStatus).all()
    if not employee_ticketsStatus:
        raise HTTPException(status_code=404, detail='No Ticket Status was found')
    return employee_ticketsStatus

# Ticket Status Table GET Method
@ticket_status.get("/ticketStatus/{ticketS_Id}", response_model=TicketStatusRead, status_code=status.HTTP_200_OK)
async def read_ticketStatus(ticketS_Id: int, db: db_dependency):
    tickets = db.query(TicketStatus).filter(TicketStatus.Id == ticketS_Id).first()
    if tickets is None:
        raise HTTPException(status_code=404, detail='Ticket Status was not found')
    return tickets

# Roles Table POST Method
@ticket_status.post("/ticketStatus/", response_model=TicketStatusRead, status_code=status.HTTP_201_CREATED)
async def create_ticketStatus(emp: TicketStatusCreate, db: db_dependency):
    db_post = TicketStatus(**emp.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# Ticket Status Table DELETE Method
@ticket_status.delete("/ticketStatus/{ticketS_Id}", status_code=status.HTTP_200_OK)
async def delete_ticketStatus(ticketS_Id: int, db: db_dependency):
    db_post = db.query(TicketStatus).filter(TicketStatus.Id == ticketS_Id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail='Ticket Status was not found')
    db.delete(db_post)
    db.commit()
    return "Ticket Status Deleted!"

# Ticket Status Table EDIT Method
@ticket_status.put("/ticketStatus/{ticketS_Id}", response_model=TicketStatusRead, status_code=status.HTTP_200_OK)
async def update_ticketStatus(ticketS_Id: int, updated_post: TicketStatusCreate, db: db_dependency):
    db_post = db.query(TicketStatus).filter(TicketStatus.Id == ticketS_Id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail='Ticket Status was not found')

    for key, value in updated_post.model_dump().items():
        setattr(db_post, key, value)

    db.commit()
    db.refresh(db_post)
    return db_post