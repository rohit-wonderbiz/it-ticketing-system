from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func , Enum
from sqlalchemy.orm import relationship
from database import Base

class Tickets(Base):
    __tablename__ = "Tickets"

    Id = Column(Integer , primary_key=True , autoincrement=True)
    EmployeeId = Column(Integer , ForeignKey("Employees.Id", ondelete="NO ACTION") , nullable=True)
    TicketTitle = Column(String(50))
    Description = Column(String(300))
    TicketStatusId = Column(Integer , ForeignKey("TicketStatus.Id",ondelete="NO ACTION"), default=1)
    PriorityId = Column(Integer , ForeignKey("TicketPriority.Id" , ondelete="NO ACTION"), nullable=True)
    CreatedAt = Column(DateTime(timezone=True), server_default=func.now())
    UpdatedAt = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
