from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func , Enum
from sqlalchemy.orm import relationship
from database import Base
    
class TicketStatus(Base):
    __tablename__ = "TicketStatus"

    Id = Column(Integer , primary_key=True , autoincrement=True)
    Status = Column(String(15))