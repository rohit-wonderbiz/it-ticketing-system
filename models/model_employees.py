from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from typing import Optional
from database import Base
from pydantic import BaseModel , EmailStr
from datetime import datetime
from models.model_role import RoleRead

class EmployeesBase(BaseModel):
    FirstName : str
    LastName : str
    UserEmail : EmailStr
    UserPassword : str
    RoleId : int
    Manager1Id : Optional[int] = None
    Manager2Id  : Optional[int] = None
    Phone : int
    role: RoleRead

class EmployeesCreate(BaseModel):
    FirstName : str
    LastName : str
    UserEmail : EmailStr
    UserPassword : str
    RoleId : int
    Manager1Id : Optional[int] = None
    Manager2Id  : Optional[int] = None
    Phone : int

class EmployeesManagerRead(BaseModel):
    Id : int
    UserEmail : EmailStr
    FirstName : str

class EmployeesRead(EmployeesBase):
    Id : int
    CreatedAt : datetime
    UpdatedAt : datetime
    
class Employees(Base):
    __tablename__ = "Employees"

    Id = Column(Integer, primary_key=True, autoincrement=True)
    FirstName = Column(String(50))
    LastName = Column(String(50))
    UserEmail = Column(String(50) , unique=True)
    UserPassword = Column(String(50))
    RoleId = Column(Integer, ForeignKey("Roles.Id", ondelete="CASCADE"), nullable=True)
    Manager1Id = Column(Integer, ForeignKey('Employees.Id', ondelete="NO ACTION"), nullable=True)
    Manager2Id = Column(Integer, ForeignKey('Employees.Id', ondelete="NO ACTION"), nullable=True)
    CreatedAt = Column(DateTime(timezone=True), server_default=func.now())
    UpdatedAt = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    Phone = Column(Integer , unique=True)

    role = relationship("Roles",back_populates='emp')
    manager1 = relationship("Employees", remote_side=[Id], backref='subordinates1', foreign_keys=[Manager1Id])
    manager2 = relationship("Employees", remote_side=[Id], backref='subordinates2', foreign_keys=[Manager2Id])