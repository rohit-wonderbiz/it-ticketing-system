from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from database import Base

class Messages(Base):
    __tablename__ = 'EMessages'

    Id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    TicketId = Column(Integer, ForeignKey('Tickets.Id', ondelete="NO ACTION"), nullable=False)
    SenderId = Column(Integer, ForeignKey('Employees.Id', ondelete="NO ACTION"), nullable=False)
    Message = Column(String, nullable=False)
    Timestamp = Column(DateTime(timezone=True), server_default=func.now())

