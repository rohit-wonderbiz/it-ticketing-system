from pydantic import BaseModel
from datetime import datetime

class TicketsBase(BaseModel):
    EmployeeId : int
    TicketTitle : str
    Description : str
    TicketStatusId : int
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