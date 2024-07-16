from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from models.model_ticket_status import TicketStatus #Models
from models.model_ticket_status import TicketStatusCreate, TicketStatusBase, TicketStatusRead #Pydantic model
from database import SessionLocal

ticket_status = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

# get all tickets status 
@ticket_status.get("/get_all_ticket_status/", response_model=list[TicketStatusRead], status_code=status.HTTP_200_OK)
async def read_all_ticket_status(db: db_dependency):
    employee_system = db.query(TicketStatus).all()
    if not employee_system:
        raise HTTPException(status_code=404, detail='No Ticket Status were found')
    return employee_system

#get ticekts_status depending upon id
@ticket_status.get("/get_ticket_status_by_id/{ticket_status_id}", response_model=TicketStatusRead, status_code=status.HTTP_200_OK)
async def read_ticket_status(ticket_status_id: int, db: db_dependency):
    status = db.query(TicketStatus).filter(TicketStatus.Id == ticket_status_id).first()
    if status is None:
        raise HTTPException(status_code=404, detail='Role was not found')
    return status

# post new tickets_status
@ticket_status.post("/add_ticket_status/", response_model=TicketStatusCreate, status_code=status.HTTP_201_CREATED)
async def create_ticket_status(emp: TicketStatusCreate, db: db_dependency):
    db_post = TicketStatus(**emp.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# put/edit on ticket status depending upon id
@ticket_status.delete("/delete_ticket_status_by_id/{ticket_status_id}", status_code=status.HTTP_200_OK)
async def delete_ticket_status(ticket_status_id: int, db: db_dependency):
    db_post = db.query(TicketStatus).filter(TicketStatus.Id == ticket_status_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail='ticket status was not found')
    db.delete(db_post)
    db.commit()
    return "ticket status Deleted!"


# Roles Table EDIT Method
@ticket_status.put("/edit_role_by_id/{role_Id}", response_model=TicketStatusRead, status_code=status.HTTP_200_OK)
async def update_ticket_status(role_Id: int, updated_ticket_status: TicketStatusRead, db: db_dependency):
    db_post = db.query(TicketStatus).filter(TicketStatus.Id == role_Id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail='Ticket Status was not found')

    for key, value in updated_ticket_status.model_dump().items():
        setattr(db_post, key, value)

    db.commit()
    db.refresh(db_post)
    return db_post