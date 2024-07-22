from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TicketsBase(BaseModel):
    EmployeeId : int
    TicketTitle : str
    Description : str
    TicketStatusId : int = 1
    PriorityId : int

class TicketsCreate(TicketsBase):
    pass

class TicketsRead(TicketsBase):
    Id : int
    CreatedAt : datetime
    UpdatedAt : datetime

#
class TicketsUpdateStatus(BaseModel):
    Id : int
    EmployeeId : int
    TicketTitle : str
    Description : str
    TicketStatusId : int
    PriorityId : int

# class MessageRequest(BaseModel):
#     sender_id: int
#     message: str = Field(min_length=1)