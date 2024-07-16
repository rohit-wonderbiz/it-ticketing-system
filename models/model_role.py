from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from database import Base
from pydantic import BaseModel
from datetime import datetime

class RolesBase(BaseModel):
    RoleName : str
    RoleCode : str = None

class RoleCreate(RolesBase):
    pass

class RoleRead(RolesBase):
    Id: int

    class Config():
        from_attributes = True
        
class Roles(Base):
    __tablename__ = "Roles"

    Id = Column(Integer , primary_key=True , autoincrement=True)
    RoleCode = Column(String, default="default")
    RoleName = Column(String)