import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.model_tickets import Tickets
from models.model_employees import Employees
from models.model_employee_systems import EmployeeSystems
from models.model_ticket_status import TicketStatus
from models.model_ticket_priority import TicketPriority
from models.model_messages import Messages

def send_email(receiver_email, subject, body, body_type="plain"):
    sender_email = "test1.wonderbiz@gmail.com"  # Replace with your email address
    password = "lnmgtmzpuhsubskx"  # Replace with your email password

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    # Turn the body into a MIMEText object
    part = MIMEText(body, body_type)

    # Attach the part into message container
    message.attach(part)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
    except Exception as e:
        raise RuntimeError(f"Failed to send email. Error: {str(e)}")
    
# Function to approve a ticket
def approve_ticket(ticket_id: int, db: Session, manager_id):
    ticket = db.query(Tickets).filter(Tickets.Id == ticket_id).first()
    if ticket is None:
        raise HTTPException(status_code=404, detail=f"Ticket {ticket_id} not found")

    ticket.TicketStatusId = 2  # Assuming TicketStatusId=2 means approved

    db.commit()
    db.refresh(ticket)

    notify_ticket(ticket_id, db, manager_id)

# Function to send mail to IT Officer & Employee If APPROVE
def notify_ticket(ticket_id: int, db: Session, manager_id: int):
    ticket = db.query(Tickets).filter(Tickets.Id == ticket_id).first()
    if ticket is None:
        raise HTTPException(status_code=404, detail=f"Ticket {ticket_id} not found")

    it_officer = db.query(Employees).filter(Employees.RoleId == 3).first()
    if it_officer is None:
        raise HTTPException(status_code=404, detail="IT Officer not found")

    employee = db.query(Employees).filter(Employees.Id == ticket.EmployeeId).first()
    if employee is None:
        raise HTTPException(status_code=404, detail=f"Employee {ticket.EmployeeId} not found")

    manager = db.query(Employees).filter(Employees.Id == manager_id).first()
    if manager is None:
        raise HTTPException(status_code=404, detail=f"Manager {manager_id} not found")
    
    # Fetch the employee system details
    employee_system = db.query(EmployeeSystems).filter(ticket.EmployeeId == EmployeeSystems.EmployeeId).first()

    employee_name = f"{employee.FirstName} {employee.LastName}"
    manager_name = f"{manager.FirstName} {manager.LastName}"
    ticket_status = db.query(TicketStatus).filter(TicketStatus.Id == ticket.TicketStatusId).first()
    ticket_status_name = ticket_status.Status

    ticket_priority = db.query(TicketPriority).filter(TicketPriority.Id == ticket.PriorityId).first()
    ticket_priority_name = ticket_priority.PriorityName

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
        <h2>IT Ticket Approved</h2>
        <p><strong>Employee:</strong> {employee_name}</p>
        <p><strong>Approved by:</strong> {manager_name}</p>
        <p><strong>Ticket ID:</strong> {ticket.Id}</p>
        <p><strong>Title:</strong> {ticket.TicketTitle}</p>
        <p><strong>Description:</strong> {ticket.Description}</p>
        <p><strong>Status:</strong> {ticket_status_name}</p>
        <p><strong>Priority:</strong> {ticket_priority_name}</p>
        <h3>Your System Details</h3>
        <p><strong>System No:</strong> {employee_system.SystemNo}</p>
        <p><strong>Vendor name:</strong> {employee_system.Vendor}</p>
        <p><strong>Ram Capacity:</strong> {employee_system.RamCapacity}</p>
        <p><strong>Disk 1 Capacity:</strong> {employee_system.Disk1Capacity}</p>
        <p><strong>Disk 2 Capacity:</strong> {employee_system.Disk2Capacity}</p>
        <div class="button-container">
            <form action="http://127.0.0.1:8000/ticket/close/{ticket.Id}/{manager.Id}" method="post">
                <button type="submit">Close Ticket</button>
            </form>
        </div>
    </body>
    </html>
    """


    send_email(it_officer.UserEmail, f"New IT Ticket Approved by {manager_name}", email_body, body_type="html")
    
    email_body_emp = f"""
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
        </style>
    </head>
    <body>
        <h2>IT Ticket Approved</h2>
        <p><strong>Approved by:</strong> {manager_name}</p>
        <p><strong>Ticket ID:</strong> {ticket.Id}</p>
        <p><strong>Title:</strong> {ticket.TicketTitle}</p>
        <p><strong>Description:</strong> {ticket.Description}</p>
        <p><strong>Status:</strong> {ticket_status_name}</p>
        <p><strong>Priority:</strong> {ticket_priority_name}</p>
        <h3>Employee System Details</h3>
        <p><strong>System No:</strong> {employee_system.SystemNo}</p>
        <p><strong>Vendor name:</strong> {employee_system.Vendor}</p>
        <p><strong>Ram Capacity:</strong> {employee_system.RamCapacity}</p>
        <p><strong>Disk 1 Capacity:</strong> {employee_system.Disk1Capacity}</p>
        <p><strong>Disk 2 Capacity:</strong> {employee_system.Disk2Capacity}</p>
    </body>
    </html>
    """
    send_email(employee.UserEmail, f"Your IT Ticket is Approved by {manager_name}", email_body_emp, body_type="html")

# Function to deny a ticket
def deny_ticket(ticket_id: int, db: Session, manager_id: int):
    ticket = db.query(Tickets).filter(Tickets.Id == ticket_id).first()
    if ticket is None:
        raise HTTPException(status_code=404, detail=f"Ticket {ticket_id} not found")

    ticket.TicketStatusId = 3  # Assuming TicketStatusId=3 means denied

    db.commit()
    db.refresh(ticket)

    notify_employee(ticket_id, db, manager_id)

# Function to send mail to IT Officer If DENY
def notify_employee(ticket_id: int, db: Session, manager_id: int):
    ticket = db.query(Tickets).filter(Tickets.Id == ticket_id).first()
    if ticket is None:
        raise HTTPException(status_code=404, detail=f"Ticket {ticket_id} not found")

    employee = db.query(Employees).filter(Employees.Id == ticket.EmployeeId).first()
    if employee is None:
        raise HTTPException(status_code=404, detail=f"Employee {ticket.EmployeeId} not found")

    manager = db.query(Employees).filter(Employees.Id == manager_id).first()
    if manager is None:
        raise HTTPException(status_code=404, detail=f"Manager {manager_id} not found")

    employee_name = f"{employee.FirstName} {employee.LastName}"
    manager_name = f"{manager.FirstName} {manager.LastName}"
    ticket_status = db.query(TicketStatus).filter(TicketStatus.Id == ticket.TicketStatusId).first()
    ticket_status_name = ticket_status.Status

    ticket_priority = db.query(TicketPriority).filter(TicketPriority.Id == ticket.PriorityId).first()
    ticket_priority_name = ticket_priority.PriorityName

    # Fetch the employee system details
    employee_system = db.query(EmployeeSystems).filter(ticket.EmployeeId == EmployeeSystems.EmployeeId).first()

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
        </style>
    </head>
    <body>
        <h2>IT Ticket Rejected</h2>
        <p><strong>Employee:</strong> {employee_name}</p>
        <p><strong>Rejected by:</strong> {manager_name}</p>
        <p><strong>Ticket ID:</strong> {ticket.Id}</p>
        <p><strong>Title:</strong> {ticket.TicketTitle}</p>
        <p><strong>Description:</strong> {ticket.Description}</p>
        <p><strong>Status:</strong> {ticket_status_name}</p>
        <p><strong>Priority:</strong> {ticket_priority_name}</p>
        <h3>Employee System Details</h3>
        <p><strong>System No:</strong> {employee_system.SystemNo}</p>
        <p><strong>Vendor name:</strong> {employee_system.Vendor}</p>
        <p><strong>Ram Capacity:</strong> {employee_system.RamCapacity}</p>
        <p><strong>Disk 1 Capacity:</strong> {employee_system.Disk1Capacity}</p>
        <p><strong>Disk 2 Capacity:</strong> {employee_system.Disk2Capacity}</p>
    </body>
    </html>
    """

    send_email(employee.UserEmail, f"Your IT Ticket is rejected by {manager_name}", email_body, body_type="html")


# Function to send communication messages
def send_email_notification(message: Messages, db: Session):
    sender = db.query(Employees).filter(Employees.Id == message.SenderId).first()
    ticket = db.query(Tickets).filter(Tickets.Id == message.TicketId).first()

    if sender.RoleId == 3:  # Assuming RoleId=3 is IT officer
        receiver = db.query(Employees).filter(Employees.Id == ticket.EmployeeId).first()
    else:
        receiver = db.query(Employees).filter(Employees.RoleId == 3).first()

    if not receiver:
        raise HTTPException(status_code=404, detail="Receiver not found")

    # Fetch additional ticket details
    ticket_status = db.query(TicketStatus).filter(TicketStatus.Id == ticket.TicketStatusId).first()
    ticket_priority = db.query(TicketPriority).filter(TicketPriority.Id == ticket.PriorityId).first()

    # Fetch the employee system details
    employee_system = db.query(EmployeeSystems).filter(ticket.EmployeeId == EmployeeSystems.EmployeeId).first()

    # Construct email body with additional ticket details
    sender_name = f"{sender.FirstName} {sender.LastName}"
    receiver_email = receiver.UserEmail
    email_body = f"""
    <html>
    <body>
        <p><strong>From:</strong> {sender_name}</p>
        <p><strong>Message:</strong> {message.Message}</p>
        <p><strong>Ticket ID:</strong> {ticket.Id}</p>
        <p><strong>Title:</strong> {ticket.TicketTitle}</p>
        <p><strong>Description:</strong> {ticket.Description}</p>
        <p><strong>Status:</strong> {ticket_status.Status}</p>
        <p><strong>Priority:</strong> {ticket_priority.PriorityName}</p>
        <h3>Employee System Details</h3>
        <p><strong>System No:</strong> {employee_system.SystemNo}</p>
        <p><strong>Vendor name:</strong> {employee_system.Vendor}</p>
        <p><strong>Ram Capacity:</strong> {employee_system.RamCapacity}</p>
        <p><strong>Disk 1 Capacity:</strong> {employee_system.Disk1Capacity}</p>
        <p><strong>Disk 2 Capacity:</strong> {employee_system.Disk2Capacity}</p>
    </body>
    </html>
    """

    send_email(receiver_email, f"New Message on Ticket {message.TicketId}", email_body, body_type="html")

