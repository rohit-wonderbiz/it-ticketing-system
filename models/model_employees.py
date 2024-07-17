from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from typing import Optional
from database import Base
from pydantic import BaseModel
from datetime import datetime

class EmployeesBase(BaseModel):
    FirstName : str
    LastName : str
    Email : str
    Password : str
    RoleId : int
    Manager1Id : Optional[int] = None
    Manager2Id  : Optional[int] = None
    Phone : int

class EmployeesCreate(EmployeesBase):
    pass

class EmployeesRead(EmployeesBase):
    Id : int
    CreatedAt : datetime
    UpdatedAt : datetime
    
class Employees(Base):
    __tablename__ = "Employees"

    Id = Column(Integer, primary_key=True, autoincrement=True)
    FirstName = Column(String(50))
    LastName = Column(String(50))
    Email = Column(String(50))
    Password = Column(String(50))
    RoleId = Column(Integer, ForeignKey("Roles.Id", ondelete="CASCADE"), nullable=True)
    Manager1Id = Column(Integer, ForeignKey('Employees.Id', ondelete="NO ACTION"), nullable=True)
    Manager2Id = Column(Integer, ForeignKey('Employees.Id', ondelete="NO ACTION"), nullable=True)
    CreatedAt = Column(DateTime(timezone=True), server_default=func.now())
    UpdatedAt = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    Phone = Column(Integer)