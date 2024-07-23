from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import Annotated, Optional
from sqlalchemy.orm import Session

from models.model_tickets import Tickets #Models
from models.model_employees import Employees
from models.model_ticket_status import TicketStatus
from models.model_ticket_priority import TicketPriority
from schemas.schema_tickets import TicketsBase, TicketsCreate, TicketsRead, TicketsUpdateStatus #Pydantic model
from database import SessionLocal

from schemas.schema_employee_systems import TicketWithEmployeeSystems
from models.model_employee_systems import EmployeeSystems

from staticFunctions.email_functions import send_email, approve_ticket, deny_ticket

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


# get employees tickets(logs) for manager
@tickets.get("/getEmpolyeeTickets/{manager_id}", response_model=list[TicketsRead], status_code=status.HTTP_200_OK)
async def get_tickets_for_manager(manager_id: int, db: Session = Depends(get_db)):
    # Query to fetch tickets where the employee's Manager1Id matches the provided manager_id
    tickets = db.query(Tickets).join(Employees).filter(Employees.Manager1Id == manager_id).all()
    
    if not tickets:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No tickets found for this manager.")

    return tickets

# Tickets Table POST Method
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
        ticket_status = db.query(TicketStatus).filter(TicketStatus.Id == db_post.TicketStatusId).first()
        ticket_status_name = ticket_status.Status

        # Fetch the current ticket Priority
        ticket_priority = db.query(TicketPriority).filter(TicketPriority.Id == db_post.PriorityId).first()
        ticket_priority_name = ticket_priority.PriorityName

        # Fetch the employee system details
        employee_system = db.query(EmployeeSystems).filter(db_post.EmployeeId == EmployeeSystems.EmployeeId).first()
        
        # New Ticket HTML email body
        email_body = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    margin: 20px;
                    padding: 20px;
                }}
                h2 {{
                    color: #333;
                }}
                strong {{
                    font-weight: bold;
                }}
                .button-container {{
                    margin-top: 10px;
                    display: flex;
                    align-items: center;
                    justify-content: space-around;
                }}
                .button-container button {{
                    background-color: #4CAF50; /* Green */
                    border: none;
                    color: white;
                    padding: 10px 20px;
                    text-align: center;
                    text-decoration: none;
                    display: inline-block;
                    font-size: 16px;
                    cursor: pointer;
                    border-radius: 5px;
                    margin-right: 10px;
                }}
                .button-container button:hover {{
                    background-color: #45a049;
                }}
            </style>
        </head>
        <body>
            <h2>New IT Ticket Created by {employee_name}</h2>
            <p><strong>Ticket ID:</strong> {db_post.Id}</p>
            <p><strong>Title:</strong> {db_post.TicketTitle}</p>
            <p><strong>Description:</strong> {db_post.Description}</p>
            <p><strong>Status:</strong> {ticket_status_name}</p>
            <p><strong>Priority:</strong> {ticket_priority_name}</p>
            <h3>Employee System Details</h3>
            <p><strong>System No:</strong> {employee_system.SystemNo}</p>
            <p><strong>Vendor name:</strong> {employee_system.Vendor}</p>
            <p><strong>Ram Capacity:</strong> {employee_system.RamCapacity}</p>
            <p><strong>Disk 1 Capacity:</strong> {employee_system.Disk1Capacity}</p>
            <p><strong>Disk 2 Capacity:</strong> {employee_system.Disk2Capacity}</p>
            <div class="button-container">
                <form action="http://127.0.0.1:8000/ticket/approve/{db_post.Id}/{manager.Id}" method="post">
                    <button type="submit">Approve</button>
                </form>
                <form action="http://127.0.0.1:8000/ticket/deny/{db_post.Id}/{manager.Id}" method="post">
                    <button type="submit">Deny</button>
                </form>
            </div>
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

# Endpoint to approve a ticket
@tickets.post("/ticket/approve/{ticket_id}/{manager_id}", status_code=status.HTTP_204_NO_CONTENT)
async def approve_ticket_endpoint(ticket_id: int, manager_id: int, db: db_dependency):
    approve_ticket(ticket_id, db, manager_id)
    return {"message": "Ticket has been approved and IT officer, Employee has been notified."}

# Endpoint to deny a ticket
@tickets.post("/ticket/deny/{ticket_id}/{manager_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deny_ticket_endpoint(ticket_id: int, manager_id: int, db: db_dependency):
    deny_ticket(ticket_id, db, manager_id)
    return {"message": "Ticket has been denied and Employee has been notified."}



@tickets.get("/tickets-with-employee-systems", response_model=list[TicketWithEmployeeSystems], status_code=status.HTTP_200_OK)
async def read_all_tickets_with_employee_systems(db: Session = Depends(get_db)):
    tickets = db.query(Tickets).all()
    if not tickets:
        raise HTTPException(status_code=404, detail='No Ticket was found')

    tickets_with_employee_systems = []
    for ticket in tickets:
        employee_systems = db.query(EmployeeSystems).filter(EmployeeSystems.EmployeeId == ticket.EmployeeId).first()
        if not employee_systems:
            raise HTTPException(status_code=404, detail=f'Employee systems not found for ticket ID {ticket.Id}')
        
        tickets_with_employee_systems.append({
            "ticket": ticket,
            "employee_systems": employee_systems
        })

    return tickets_with_employee_systems

@tickets.get("/tickets/{ticket_id}/employee-systems", response_model=TicketWithEmployeeSystems)
def get_ticket_with_employee_systems(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(Tickets).filter(Tickets.Id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    employee_systems = db.query(EmployeeSystems).filter(EmployeeSystems.EmployeeId == ticket.EmployeeId).first()
    if not employee_systems:
        raise HTTPException(status_code=404, detail="Employee systems not found")

    return {
        "ticket": ticket,
        "employee_systems": employee_systems
    }

# Endpoint to close a ticket
@tickets.post("/ticket/close/{ticket_id}/{manager_id}", status_code=status.HTTP_204_NO_CONTENT)
async def close_ticket_endpoint(ticket_id: int, manager_id: int, db: db_dependency):
    # Fetch the ticket
    ticket = db.query(Tickets).filter(Tickets.Id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Fetch the manager
    manager = db.query(Employees).filter(Employees.Id == manager_id).first()
    if not manager:
        raise HTTPException(status_code=404, detail="Manager not found")

    manager_email = manager.UserEmail  # Assuming the email attribute in Employees model is named 'Email'
    
    # Fetch the employee from the Employees table
    employee = db.query(Employees).filter(Employees.Id == Tickets.EmployeeId).first()
    if employee is None:
        raise HTTPException(status_code=404, detail='Employee not found')
    
    # Fetch the employee name
    employee_name = str(employee.FirstName + " " + employee.LastName)

    # Fetch the employee system details
    employee_system = db.query(EmployeeSystems).filter(ticket.EmployeeId == EmployeeSystems.EmployeeId).first()

    # Fetch the current ticket status
    ticket_status = db.query(TicketStatus).filter(TicketStatus.Id == ticket.TicketStatusId).first()
    ticket_status_name = ticket_status.Status

    # Send email to manager to confirm if the issue is solved
    manager_email = manager.UserEmail
    email_body = f"""
            <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        line-height: 1.6;
                        margin: 20px;
                        padding: 20px;
                    }}
                    h2 {{
                        color: #333;
                    }}
                    strong {{
                        font-weight: bold;
                    }}
                    .button-container {{
                        margin-top: 10px;
                        display: flex;
                        align-items: center;
                        justify-content: space-around;
                    }}
                    .button-container button {{
                        background-color: #4CAF50; /* Green */
                        border: none;
                        color: white;
                        padding: 10px 20px;
                        text-align: center;
                        text-decoration: none;
                        display: inline-block;
                        font-size: 16px;
                        cursor: pointer;
                        border-radius: 5px;
                        margin-right: 10px;
                    }}
                    .button-container button:hover {{
                        background-color: #45a049;
                    }}
                </style>
            </head>
            <body>
                <h2>Is the issue for ticket ID {ticket.Id} solved?</h2>
                <p><strong>Ticket ID:</strong> {ticket.Id}</p>
                <p><strong>Title:</strong> {ticket.TicketTitle}</p>
                <p><strong>Description:</strong> {ticket.Description}</p>
                <p><strong>Status:</strong> {ticket_status_name}</p>
                <h3>Employee System Details</h3>
                <p><strong>System No:</strong> {employee_system.SystemNo}</p>
                <p><strong>Vendor name:</strong> {employee_system.Vendor}</p>
                <p><strong>Ram Capacity:</strong> {employee_system.RamCapacity}</p>
                <p><strong>Disk 1 Capacity:</strong> {employee_system.Disk1Capacity}</p>
                <p><strong>Disk 2 Capacity:</strong> {employee_system.Disk2Capacity}</p>
                <div class="button-container">
                    <form action="http://127.0.0.1:8000/ticket/confirm_close/{ticket.Id}/{manager_id}" method="post">
                        <button type="submit">Yes</button>
                    </form>
                    <form action="http://127.0.0.1:8000/ticket/reopen/{ticket.Id}/{manager_id}" method="post">
                        <button type="submit">No</button>
                    </form>
                </div>
            </body>
            </html>
            """

    send_email(manager_email, "Confirm Ticket Closure", email_body, body_type="html")
    return {"message": "Confirmation email sent to the manager."}


# Endpoint to confirm ticket closure
@tickets.post("/ticket/confirm_close/{ticket_id}/{manager_id}", status_code=status.HTTP_204_NO_CONTENT)
async def confirm_close(ticket_id: int, manager_id: int, db: db_dependency):
    # Fetch the ticket
    ticket = db.query(Tickets).filter(Tickets.Id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Update the ticket status to closed
    ticket.TicketStatusId = 4  # Assuming 4 is the status ID for 'Closed'
    db.commit()

    # Fetch the current ticket status
    ticket_status = db.query(TicketStatus).filter(TicketStatus.Id == ticket.TicketStatusId).first()
    ticket_status_name = ticket_status.Status

    # Fetch the employee
    employee = db.query(Employees).filter(Employees.Id == ticket.EmployeeId).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Fetch the employee system details
    employee_system = db.query(EmployeeSystems).filter(ticket.EmployeeId == EmployeeSystems.EmployeeId).first()

    # Notify the employee
    employee_email = employee.UserEmail

    # Confirm Close Ticket HTML email body for employee
    email_body = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 20px;
                padding: 20px;
            }}
            h2 {{
                color: #333;
            }}
            strong {{
                font-weight: bold;
            }}
            .button-container {{
                margin-top: 10px;
                display: flex;
                align-items: center;
                justify-content: space-around;
            }}
            .button-container button {{
                background-color: #4CAF50; /* Green */
                border: none;
                color: white;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                cursor: pointer;
                border-radius: 5px;
                margin-right: 10px;
            }}
            .button-container button:hover {{
                background-color: #45a049;
            }}
        </style>
    </head>
    <body>
        <h2>Your ticket ID {ticket.Id} has been closed.</h2>
        <p><strong>Ticket ID:</strong> {ticket.Id}</p>
        <p><strong>Title:</strong> {ticket.TicketTitle}</p>
        <p><strong>Description:</strong> {ticket.Description}</p>
        <p><strong>Status:</strong> {ticket_status_name}</p>
        <h3>Employee System Details</h3>
        <p><strong>System No:</strong> {employee_system.SystemNo}</p>
        <p><strong>Vendor name:</strong> {employee_system.Vendor}</p>
        <p><strong>Ram Capacity:</strong> {employee_system.RamCapacity}</p>
        <p><strong>Disk 1 Capacity:</strong> {employee_system.Disk1Capacity}</p>
        <p><strong>Disk 2 Capacity:</strong> {employee_system.Disk2Capacity}</p>
    </body>
    </html>
    """

    send_email(employee_email, "Ticket Closed", email_body, body_type="html")
    
    # Notify the employee and IT officer
    it_officer = db.query(Employees).filter(Employees.RoleId == 3).first()
    if it_officer is None:
        raise HTTPException(status_code=404, detail="IT Officer not found")

    it_officer_email = it_officer.UserEmail  # Replace with actual IT officer email

    # Confirm Ticket HTML email body for IT officer
    email_body = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 20px;
                padding: 20px;
            }}
            h2 {{
                color: #333;
            }}
            strong {{
                font-weight: bold;
            }}
            .button-container {{
                margin-top: 10px;
                display: flex;
                align-items: center;
                justify-content: space-around;
            }}
            .button-container button {{
                background-color: #4CAF50; /* Green */
                border: none;
                color: white;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                cursor: pointer;
                border-radius: 5px;
                margin-right: 10px;
            }}
            .button-container button:hover {{
                background-color: #45a049;
            }}
        </style>
    </head>
    <body>
        <h2>Ticket ID {ticket.Id} has been closed.</h2>
        <p><strong>Ticket ID:</strong> {ticket.Id}</p>
        <p><strong>Title:</strong> {ticket.TicketTitle}</p>
        <p><strong>Description:</strong> {ticket.Description}</p>
        <p><strong>Status:</strong> {ticket_status_name}</p>
        <h3>Employee System Details</h3>
        <p><strong>System No:</strong> {employee_system.SystemNo}</p>
        <p><strong>Vendor name:</strong> {employee_system.Vendor}</p>
        <p><strong>Ram Capacity:</strong> {employee_system.RamCapacity}</p>
        <p><strong>Disk 1 Capacity:</strong> {employee_system.Disk1Capacity}</p>
        <p><strong>Disk 2 Capacity:</strong> {employee_system.Disk2Capacity}</p>
    </body>
    </html>
    """
    send_email(it_officer_email, "Ticket Closed", email_body, body_type="html")

    return {"message": "Ticket has been closed and notifications sent."}

# Endpoint to reopen a ticket
@tickets.post("/ticket/reopen/{ticket_id}/{manager_id}", status_code=status.HTTP_204_NO_CONTENT)
async def reopen(ticket_id: int, manager_id: int, db: db_dependency):
    # Fetch the ticket
    ticket = db.query(Tickets).filter(Tickets.Id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Keep the ticket status approve (not closed) as needed
    ticket.TicketStatusId = 2  # Assuming 2 is the status ID for 'approve'
    db.commit()

    # Fetch the current ticket status
    ticket_status = db.query(TicketStatus).filter(TicketStatus.Id == ticket.TicketStatusId).first()
    ticket_status_name = ticket_status.Status

    # Fetch the employee system details
    employee_system = db.query(EmployeeSystems).filter(ticket.EmployeeId == EmployeeSystems.EmployeeId).first()

    # Notify the IT officer
    it_officer = db.query(Employees).filter(Employees.RoleId == 3).first()
    if it_officer is None:
        raise HTTPException(status_code=404, detail="IT Officer not found")

    it_officer_email = it_officer.UserEmail  # Replace with actual IT officer email

    # Reopen Ticket HTML email body for IT officer
    email_body = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 20px;
                padding: 20px;
            }}
            h2 {{
                color: #333;
            }}
            strong {{
                font-weight: bold;
            }}
            .button-container {{
                margin-top: 10px;
                display: flex;
                align-items: center;
                justify-content: space-around;
            }}
            .button-container button {{
                background-color: #4CAF50; /* Green */
                border: none;
                color: white;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                cursor: pointer;
                border-radius: 5px;
                margin-right: 10px;
            }}
            .button-container button:hover {{
                background-color: #45a049;
            }}
        </style>
    </head>
    <body>
        <h2>Your ticket ID {ticket.Id} has been reopened</h2>
        <p><strong>Ticket ID:</strong> {ticket.Id}</p>
        <p><strong>Title:</strong> {ticket.TicketTitle}</p>
        <p><strong>Description:</strong> {ticket.Description}</p>
        <p><strong>Status:</strong> {ticket_status_name}</p>
        <h3>Employee System Details</h3>
        <p><strong>System No:</strong> {employee_system.SystemNo}</p>
        <p><strong>Vendor name:</strong> {employee_system.Vendor}</p>
        <p><strong>Ram Capacity:</strong> {employee_system.RamCapacity}</p>
        <p><strong>Disk 1 Capacity:</strong> {employee_system.Disk1Capacity}</p>
        <p><strong>Disk 2 Capacity:</strong> {employee_system.Disk2Capacity}</p>
    </body>
    </html>
    """    

    send_email(it_officer_email, "Ticket Reopened", email_body, body_type="html")

    return {"message": "Ticket has been reopened and IT officer notified."}