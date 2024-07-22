from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from database import Base
# from models.model_role import RoleRead

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