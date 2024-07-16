from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from models.model_employees import Employees
from database import Sessionlocal

employees = APIRouter()

class EmployeesBase(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    phone: int
    address: str

class EmployeesCreate(EmployeesBase):
    pass

class EmployeesRead(EmployeesBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# Employees Table GET Method ALL
@employees.get("/get_all_employees/", response_model=list[EmployeesRead], status_code=status.HTTP_200_OK)
async def read_all_employee(db: db_dependency):
    employee_profiles = db.query(Employees).all()
    if not employee_profiles:
        raise HTTPException(status_code=404, detail='No employee profiles were found')
    return employee_profiles

# Employees Table GET Method
@employees.get("/get_employee_by_id/{emp_Id}", response_model=EmployeesRead, status_code=status.HTTP_200_OK)
async def read_employee(emp_Id: int, db: db_dependency):
    post = db.query(Employees).filter(Employees.id == emp_Id).first()
    if post is None:
        raise HTTPException(status_code=404, detail='Employee was not found')
    return post

# Employees Table POST Method
@employees.post("/add_employee/", response_model=EmployeesRead, status_code=status.HTTP_201_CREATED)
async def create_employee(emp: EmployeesCreate, db: db_dependency):
    db_post = Employees(**emp.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# Employees Table DELETE Method
@employees.delete("/delete_employee_by_id/{emp_Id}", status_code=status.HTTP_200_OK)
async def delete_employee(emp_Id: int, db: db_dependency):
    db_post = db.query(Employees).filter(Employees.id == emp_Id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail='Employee was not found')
    db.delete(db_post)
    db.commit()

# Employees Table EDIT Method
@employees.put("/edit_employee_by_id/{emp_Id}", response_model=EmployeesRead, status_code=status.HTTP_200_OK)
async def update_employee(emp_Id: int, updated_post: EmployeesCreate, db: db_dependency):
    db_post = db.query(Employees).filter(Employees.id == emp_Id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail='Employee was not found')

    for key, value in updated_post.model_dump().items():
        setattr(db_post, key, value)

    db.commit()
    db.refresh(db_post)
    return db_post