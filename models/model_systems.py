from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from database import Base
from pydantic import BaseModel

class SystemsBase(BaseModel):
    Id : int

    class Config():
        orm_mode = True

class Systems(Base):
    __tablename__ = "Systems"

    Id = Column(Integer , primary_key=True , autoincrement=True)
    SystemTypeId = Column(Integer) #foreign key System Table(Id)
    VendorId = Column(Integer) #foreign key Vendors Table(Id)
    RamId = Column(Integer) #foreign key Ram Table(Id)
    DiskId = Column(Integer) #foreign key Disks Table(Id)
