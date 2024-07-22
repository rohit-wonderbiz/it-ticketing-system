from typing import Optional
from pydantic import BaseModel , EmailStr
from datetime import datetime
from schemas.schema_role import RoleRead

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