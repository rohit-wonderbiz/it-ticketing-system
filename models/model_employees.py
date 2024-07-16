from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from database import Base
from pydantic import BaseModel
from datetime import datetime

class EmployeesBase(BaseModel):
    FirstName : str
    LastName : str
    EmailId : int
    Password : str
    DesignationId : int
    RoleId : int
    Manager1Id : int
    Manager2Id  : int
    Phone : int
    SystemId : int

class EmployeesCreate(EmployeesBase):
    pass

class EmployeesRead(EmployeesBase):
    Id : int
    CreatedAt : datetime
    UpdatedAt : datetime
    
class Employees(Base):
    __tablename__ = "Employees"

    Id = Column(Integer , primary_key=True , autoincrement=True)
    FirstName = Column(String(50))
    LastName = Column(String(50))
    EmailId = Column(Integer)    #foriegn key Setting Table(Id)
    Password = Column(String(50))
    DesignationId = Column(Integer) #foriegn key Designation Table(Id)
    RoleId = Column(Integer)   #foriegn key Role Table(Id)
    Manager1Id = Column(Integer) #foriegn key Employees Table(Id)
    Manager2Id = Column(Integer) #foriegn key Employees Table(Id)
    Phone = Column(Integer)
    SystemId = Column(Integer) #Foriegn key SystemId Table(Id)
    CreatedAt = Column(DateTime(timezone=True), server_default=func.now())
    UpdatedAt = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())