from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func , Enum
from sqlalchemy.orm import relationship
from database import Base
from pydantic import BaseModel
from datetime import datetime

class TicketsBase(BaseModel):
    EmployeeId : int
    TicketTitle : str
    Description : str
    TicketType :str
    Category : str
    Priority : str

class TicketsCreate(TicketsBase):
    pass

class TicketsRead(TicketsBase):
    Id : int
    CreatedAt : datetime
    UpdatedAt : datetime

class Tickets(Base):
    __tablename__ = "Tickets"

    Id = Column(Integer , primary_key=True , autoincrement=True)
    EmployeeId = Column(Integer , ForeignKey("Employees.Id", ondelete="NO ACTION") , nullable=True)
    TicketTitle = Column(String(50))
    Description = Column(String(300))
    TicketType = Column(String(10))
    Category = Column(String(30))
    Priority = Column(String(30))
    CreatedAt = Column(DateTime(timezone=True), server_default=func.now())
    UpdatedAt = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())