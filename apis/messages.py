from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import SessionLocal
# from models import Messages, Tickets, Employees
from models.model_tickets import Tickets
from models.model_employees import Employees
from models.model_messages import Messages
from schemas.schema_messages import MessageRequest, MessageResponse
from staticFunctions.email_functions import send_email_notification

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

message_route = APIRouter()

@message_route.post('/ticket/{ticket_id}/message', response_model=MessageResponse)
def send_ticket_message(ticket_id: int, message_request: MessageRequest, db: Session = Depends(get_db)):
    # Verify that the ticket exists
    ticket = db.query(Tickets).filter(Tickets.Id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail=f"Ticket {ticket_id} not found")

    # Verify that the sender exists
    sender = db.query(Employees).filter(Employees.Id == message_request.SenderId).first()
    if not sender:
        raise HTTPException(status_code=404, detail=f"Sender {message_request.SenderId} not found")

    # Create a new message record
    new_message = Messages(
        TicketId=ticket_id,
        SenderId=message_request.SenderId,
        Message=message_request.Message
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    # Send email notification (this can be an optional feature)
    send_email_notification(new_message, db)

    return new_message
