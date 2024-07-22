from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from database import Base

class Messages(Base):
    __tablename__ = 'Messages'

    Id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    TicketId = Column(Integer, ForeignKey('Tickets.Id'), nullable=False)
    SenderId = Column(Integer, ForeignKey('Employees.Id'), nullable=False)
    Message = Column(String, nullable=False)
    Timestamp = Column(DateTime(timezone=True), server_default=func.now())

    # sender = relationship("Employees", foreign_keys=[SenderId])
    # ticket = relationship("Tickets", foreign_keys=[TicketId])
