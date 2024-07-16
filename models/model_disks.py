from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from database import Base
from pydantic import BaseModel


class DisksBase(BaseModel):
    Id = int

class DisksCreate(DisksBase):
    DiskType :str
    DiskCapacity : str

    class Config():
        orm_mode =True


class Disks(Base):
    __tablename__ = "Disks"
    Id = Column(Integer , primary_key=True , autoincrement= True)
    DiskType = Column(String(50))
    DiskCapacity = Column(Integer)