from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field , ValidationError
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from models.model_employees import Employees #Models
from models.model_employees import EmployeesBase, EmployeesCreate, EmployeesRead #Pydantic model
from database import SessionLocal

employees = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# Employees Table GET Method ALL
@employees.get("/", status_code=status.HTTP_200_OK)
async def read():
    return "Hello"

# Employees Table GET Method ALL
@employees.get("/employee/", response_model=list[EmployeesRead], status_code=status.HTTP_200_OK)
async def read_all_employee(db: db_dependency):
    employee_profiles = db.query(Employees).all()
    if not employee_profiles:
        raise HTTPException(status_code=404, detail='No employee profiles were found')
    return employee_profiles

# Employees Table GET Method
@employees.get("/employee/{emp_Id}", response_model=EmployeesRead, status_code=status.HTTP_200_OK)
async def read_employee(emp_Id: int, db: db_dependency):
    post = db.query(Employees).filter(Employees.Id == emp_Id).first()
    if post is None:
        raise HTTPException(status_code=404, detail='Employee was not found')
    return post

# original POST
# Employees Table POST Method
# @employees.post("/employee/", response_model=EmployeesRead, status_code=status.HTTP_201_CREATED)
# async def create_employee(emp: EmployeesCreate, db: db_dependency):
#     db_post = Employees(**emp.model_dump())
#     db.add(db_post)
#     db.commit()
#     db.refresh(db_post)
#     return db_post

# post method for employees with exceptional handling
@employees.post("/employee/", response_model=EmployeesRead, status_code=status.HTTP_201_CREATED)
async def create_employee(emp: EmployeesCreate, db: db_dependency):
    # Check if the email already exists
    existing_employee = db.query(Employees).filter(Employees.UserEmail == emp.UserEmail).first()
    if existing_employee:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists.")
    existing_phone = db.query(Employees).filter(Employees.Phone == emp.Phone).first()
    if existing_phone:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail="Phone number already exist")

    try:
        db_post = Employees(**emp.model_dump())
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post
    except ValidationError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid email format.")
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while creating the employee.")
    
# Original Employees Table DELETE Method
# @employees.delete("/employee/{emp_Id}", status_code=status.HTTP_200_OK)
# async def delete_employee(emp_Id: int, db: db_dependency):
#     db_post = db.query(Employees).filter(Employees.Id == emp_Id).first()
#     if db_post is None:
#         raise HTTPException(status_code=404, detail='Employee was not found')
#     db.delete(db_post)
#     db.commit()
#     return "Employee Deleted!"

# Employees Table delete Method with manager exception handling
@employees.delete("/employee/{emp_Id}", status_code=status.HTTP_200_OK)
async def delete_employee(emp_Id: int, db: db_dependency):
    db_post = db.query(Employees).filter(Employees.Id == emp_Id).first()
    
    if db_post is None:
        raise HTTPException(status_code=404, detail='Employee was not found')
    
    # Check for references in other employees
    referencing_employees = db.query(Employees).filter(
        (Employees.Manager1Id == emp_Id) | (Employees.Manager2Id == emp_Id)
    ).first()
    
    if referencing_employees:
        raise HTTPException(status_code=400, detail='Cannot delete this employee; they are referenced by other employee records.')

    db.delete(db_post)
    db.commit()
    return "Employee Deleted!"


# Employees Table EDIT Method
@employees.put("/employee/{emp_Id}", response_model=EmployeesRead, status_code=status.HTTP_200_OK)
async def update_employee(emp_Id: int, updated_post: EmployeesCreate, db: db_dependency):
    db_post = db.query(Employees).filter(Employees.Id == emp_Id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail='Employee was not found')

    for key, value in updated_post.model_dump().items():
        setattr(db_post, key, value)

    db.commit()
    db.refresh(db_post)
    return db_post