from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from database import Base

       
class Roles(Base):
    __tablename__ = "Roles"

    Id = Column(Integer , primary_key=True , autoincrement=True)
    RoleCode = Column(String, default="default")
    RoleName = Column(String)

    emp = relationship("Employees",back_populates='role')