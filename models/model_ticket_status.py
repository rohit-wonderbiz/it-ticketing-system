from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func , Enum
from sqlalchemy.orm import relationship
from database import Base
from pydantic import BaseModel
from datetime import datetime

class TicketStatusBase(BaseModel):
    TicketId : int
    Status : str

class TicketStatusCreate(TicketStatusBase):
    pass

class TicketStatusRead(TicketStatusBase):
    Id : int

    
class TicketStatus(Base):
    __tablename__ = "TicketStatus"

    Id = Column(Integer , primary_key=True , autoincrement=True)
    TicketId = Column(Integer , ForeignKey("Tickets.Id",ondelete="NO ACTION"),nullable=True)
    Status = Column(String(15))