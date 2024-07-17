from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from database import Base
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EmployeeSystemsBase(BaseModel):
    EmployeeId : Optional[int] = None
    SystemNo : str
    Vendor : str
    RamCapacity : int 
    Disk1Capacity : int
    Disk2Capacity : int

class EmployeeSystemsCreate(EmployeeSystemsBase):
    pass

class EmployeeSystemsRead(EmployeeSystemsBase):
    Id:int
    CreatedAt : datetime
    UpdatedAt : datetime

    class Config():
        from_attributes = True

class EmployeeSystems(Base):
    __tablename__ = "EmployeeSystems"

    Id = Column(Integer , primary_key=True , autoincrement=True)
    EmployeeId = Column(Integer , ForeignKey("Employees.Id" , ondelete = "NO ACTION"),nullable=True)
    SystemNo = Column(String)
    Vendor = Column(String) # master table to be created
    RamCapacity = Column(Integer) 
    Disk1Capacity = Column(Integer) 
    Disk2Capacity = Column(Integer)
    CreatedAt = Column(DateTime(timezone=True), server_default=func.now())
    UpdatedAt = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())