from sqlalchemy.orm import relationship 
from pydantic import BaseModel
from datetime import datetime

#Pydantic model
class TicketPriorityBase(BaseModel):
    PriorityName : str

class TicketPriorityCreate(TicketPriorityBase):
    pass

class TicketPriorityRead(TicketPriorityBase):
    Id : int 
    class Config():
        from_attributes = True