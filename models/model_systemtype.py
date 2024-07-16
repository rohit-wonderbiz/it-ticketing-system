from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from database import Base
from pydantic import BaseModel

class SystemTypeBase(BaseModel):
    Id : int

class SystemTypeCreate(SystemTypeBase):
    SystemTypeName : str

    class Config():
        orm_mode = True

class SytemType(Base):
    __tablename__ = "SystemType"

    Id = Column(Integer , primary_key=True , autoincrement=True)
    SystemTypeName = Column(String(50))