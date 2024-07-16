from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from database import Base
from pydantic import BaseModel

class RamBase(BaseModel):
    Id : int
    
class RamCreate(RamBase):
    RamCapacity : int
    RamType : str

    class Config():
        orm_mode = True
    
class Ram(Base):
    Id = Column(Integer , primary_key=True , autoincrement=True)
    RamCapacity = Column(Integer)
    RamType = Column(String)