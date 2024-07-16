from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from database import Base
from pydantic import BaseModel

class VendorsBase(BaseModel):
    id : int

class VendorsCreate(VendorsBase):
    VendorName : str

    class Config():
        orm_mode = True

class Vendors(Base):
    __tablename__ = "Vendors"
    Id = Column(Integer , primary_key=True , autoincrement=True)
    VendorName = Column(String(50))