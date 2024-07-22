from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from database import Base

#table
class TicketPriority(Base):
    __tablename__ = "TicketPriority"
    Id = Column(Integer , primary_key=True, autoincrement=True)
    PriorityName = Column(String(20))
