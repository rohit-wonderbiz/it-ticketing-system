from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import Annotated, Optional
from sqlalchemy.orm import Session

from models.model_tickets import Tickets #Models
from models.model_tickets import TicketsBase, TicketsCreate, TicketsRead #Pydantic model
from database import SessionLocal

tickets = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# Roles Table GET Method ALL
@tickets.get("/", status_code=status.HTTP_200_OK)
async def read():
    return "Hello"

# Roles Table GET Method ALL
@tickets.get("/ticket/", response_model=list[TicketsRead], status_code=status.HTTP_200_OK)
async def read_all_tickets(db: db_dependency):
    employee_tickets = db.query(Tickets).all()
    if not employee_tickets:
        raise HTTPException(status_code=404, detail='No Ticket was found')
    return employee_tickets

# Roles Table GET Method
@tickets.get("/ticket/{ticket_Id}", response_model=TicketsRead, status_code=status.HTTP_200_OK)
async def read_ticket(ticket_Id: int, db: db_dependency):
    tickets = db.query(Tickets).filter(Tickets.Id == ticket_Id).first()
    if tickets is None:
        raise HTTPException(status_code=404, detail='Ticket was not found')
    return tickets

# Roles Table POST Method
@tickets.post("/ticket/", response_model=TicketsRead, status_code=status.HTTP_201_CREATED)
async def create_ticket(emp: TicketsCreate, db: db_dependency):
    db_post = Tickets(**emp.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# Roles Table DELETE Method
@tickets.delete("/ticket/{ticket_Id}", status_code=status.HTTP_200_OK)
async def delete_ticket(ticket_Id: int, db: db_dependency):
    db_post = db.query(Tickets).filter(Tickets.Id == ticket_Id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail='Ticket was not found')
    db.delete(db_post)
    db.commit()
    return "Tickets Deleted!"

# Roles Table EDIT Method
@tickets.put("/ticket/{ticket_Id}", response_model=TicketsRead, status_code=status.HTTP_200_OK)
async def update_ticket(ticket_Id: int, updated_post: TicketsCreate, db: db_dependency):
    db_post = db.query(Tickets).filter(Tickets.Id == ticket_Id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail='Ticket was not found')

    for key, value in updated_post.model_dump().items():
        setattr(db_post, key, value)

    db.commit()
    db.refresh(db_post)
    return db_post