from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import Annotated, Optional
from sqlalchemy.orm import Session

from models.model_tickets import Tickets #Models
from models.model_employees import Employees
from models.model_ticket_status import TicketStatus
from models.model_ticket_priority import TicketPriority
from models.model_tickets import TicketsBase, TicketsCreate, TicketsRead #Pydantic model
from database import SessionLocal
from staticFunctions.email_functions import send_email

tickets = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# Tickets Table GET Method ALL
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

# Tickets Table GET Method
@tickets.get("/ticket/{ticket_Id}", response_model=TicketsRead, status_code=status.HTTP_200_OK)
async def read_ticket(ticket_Id: int, db: db_dependency):
    tickets = db.query(Tickets).filter(Tickets.Id == ticket_Id).first()
    if tickets is None:
        raise HTTPException(status_code=404, detail='Ticket was not found')
    return tickets

# # Tickets Table POST Method
# @tickets.post("/ticket/", response_model=TicketsRead, status_code=status.HTTP_201_CREATED)
# async def create_ticket(emp: TicketsCreate, db: db_dependency):
#     db_post = Tickets(**emp.model_dump())
#     db.add(db_post)
#     db.commit()
#     db.refresh(db_post)
#     return db_post

@tickets.post("/ticket/", response_model=TicketsRead, status_code=status.HTTP_201_CREATED)
async def create_ticket(emp: TicketsCreate, db: db_dependency):
    db_post = Tickets(**emp.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    # After successfully committing the ticket to the database, send an email
    try:
        # Fetch the employee from the Employees table
        employee = db.query(Employees).filter(Employees.Id == db_post.EmployeeId).first()
        if employee is None:
            raise HTTPException(status_code=404, detail='Employee not found')

        # Fetch the manager's email using Manager1Id
        manager = db.query(Employees).filter(Employees.Id == employee.Manager1Id).first()
        if manager is None:
            raise HTTPException(status_code=404, detail='Manager not found')

        manager_email = manager.UserEmail  # Assuming the email attribute in Employees model is named 'Email'
        
        # Fetch the employee name
        employee_name = str(employee.FirstName + " " + employee.LastName)

        # Fetch the current ticket status
        ticket_status = db.query(TicketStatus).filter(TicketStatus.Id == Tickets.TicketStatusId).first()
        ticket_status_name = ticket_status.Status

        # Fetch the current ticket Priority
        ticket_priority = db.query(TicketPriority).filter(TicketPriority.Id == Tickets.PriorityId).first()
        ticket_priority_name = ticket_priority.PriorityName

        # New Ticket HTML email body
        email_body = f"""
        <html>
        <body>
            <h2>New IT Ticket Created by {employee_name}</h2>
            <p><strong>Ticket ID:</strong> {db_post.Id}</p>
            <p><strong>Title:</strong> {db_post.TicketTitle}</p>
            <p><strong>Description:</strong> {db_post.Description}</p>
            <p><strong>Status:</strong> {ticket_status_name}</p>
            <p><strong>Priority:</strong> {ticket_priority_name}</p>
        </body>
        </html>
        """

        send_email(manager_email, f"New IT Ticket Created by {employee_name}", email_body, body_type="html")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")

    return db_post

# Tickets Table DELETE Method
@tickets.delete("/ticket/{ticket_Id}", status_code=status.HTTP_200_OK)
async def delete_ticket(ticket_Id: int, db: db_dependency):
    db_post = db.query(Tickets).filter(Tickets.Id == ticket_Id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail='Ticket was not found')
    db.delete(db_post)
    db.commit()
    return "Tickets Deleted!"

# Tickets Table EDIT Method
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