from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import Annotated, Optional
from sqlalchemy.orm import Session

from models.model_ticket_priority import TicketPriority #Models
from schemas.schema_ticket_priority import TicketPriorityBase, TicketPriorityCreate, TicketPriorityRead #Pydantic model
from database import SessionLocal

ticket_priority = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# Ticket Priority Table GET Method ALL
@ticket_priority.get("/", status_code=status.HTTP_200_OK)
async def read():
    return "Hello"

# Ticket Priority Table GET Method ALL
@ticket_priority.get("/ticketPriority/", response_model=list[TicketPriorityRead], status_code=status.HTTP_200_OK)
async def read_all_ticketPriority(db: db_dependency):
    employee_ticketsPriority = db.query(TicketPriority).all()
    if not employee_ticketsPriority:
        raise HTTPException(status_code=404, detail='No Ticket Priority was found')
    return employee_ticketsPriority

# Ticket Priority Table GET Method
@ticket_priority.get("/ticketPriority/{ticketP_Id}", response_model=TicketPriorityRead, status_code=status.HTTP_200_OK)
async def read_ticketPriority(ticketP_Id: int, db: db_dependency):
    ticketsPriority = db.query(TicketPriority).filter(TicketPriority.Id == ticketP_Id).first()
    if ticketsPriority is None:
        raise HTTPException(status_code=404, detail='Ticket Priority was not found')
    return ticketsPriority

# Roles Table POST Method
@ticket_priority.post("/ticketPriority/", response_model=TicketPriorityRead, status_code=status.HTTP_201_CREATED)
async def create_ticketPriority(emp: TicketPriorityCreate, db: db_dependency):
    db_post = TicketPriority(**emp.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# Ticket Status Table DELETE Method
@ticket_priority.delete("/ticketPriority/{ticketSticketP_Id_Id}", status_code=status.HTTP_200_OK)
async def delete_ticketPriority(ticketP_Id: int, db: db_dependency):
    db_post = db.query(TicketPriority).filter(TicketPriority.Id == ticketP_Id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail='Ticket Priority was not found')
    db.delete(db_post)
    db.commit()
    return "Ticket Priority Deleted!"

# Ticket Priority Table EDIT Method
@ticket_priority.put("/ticketPriority/{ticketP_Id}", response_model=TicketPriorityRead, status_code=status.HTTP_200_OK)
async def update_ticketPriority(ticketP_Id: int, updated_post: TicketPriorityCreate, db: db_dependency):
    db_post = db.query(TicketPriority).filter(TicketPriority.Id == ticketP_Id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail='Ticket Priority was not found')

    for key, value in updated_post.model_dump().items():
        setattr(db_post, key, value)

    db.commit()
    db.refresh(db_post)
    return db_post