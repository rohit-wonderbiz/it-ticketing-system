from pydantic import BaseModel
from datetime import datetime

class EmployeeSystemsBase(BaseModel):
    EmployeeId : int
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