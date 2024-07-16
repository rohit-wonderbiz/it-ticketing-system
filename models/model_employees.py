from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from database import Base
from pydantic import BaseModel

class EmployeesBase(BaseModel):
    FirstName : str
    LastName : str
    EmailId : str
    Password : str
    DesignationId : int
    RoleId : int
    Manager1Id : int
    Manager2Id  : int
    Phone : int
    SystemId : int
    CreatedAt : DateTime
    UpdatedAt : DateTime

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
    Phone = Column(Integer(10))
    SystemId = Column(Integer) #Foriegn key SystemId Table(Id)
    CreatedAt = Column(DateTime , server_default=func.current_timestamp)
    UpdatedAt = Column(DateTime , server_default=func.current_timestamp , onupdate=func.current_timestamp)