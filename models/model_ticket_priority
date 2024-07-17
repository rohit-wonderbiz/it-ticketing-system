from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from database import Base
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
        orm_mode = True

#table
class TicketPriority(Base):
    __tablename__ = "TicketPriority"
    Id = Column(Integer , primary_key=True, autoincrement=True)
    PriorityName = Column(String(20))
