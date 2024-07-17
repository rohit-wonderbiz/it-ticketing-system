from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from models.model_employee_systems import EmployeeSystems #Models
from models.model_employee_systems import EmployeeSystemsBase, EmployeeSystemsCreate, EmployeeSystemsRead #Pydantic model
from database import SessionLocal

employee_systems = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# Employee Systems Table GET Method ALL
@employee_systems.get("/", status_code=status.HTTP_200_OK)
async def read():
    return "Hello"

# Employee Systems Table GET Method ALL
@employee_systems.get("/employeeSystem/", response_model=list[EmployeeSystemsRead], status_code=status.HTTP_200_OK)
async def read_all_system(db: db_dependency):
    employee_system = db.query(EmployeeSystems).all()
    if not employee_system:
        raise HTTPException(status_code=404, detail='No system were found')
    return employee_system

# Employee Systems Table GET Method
@employee_systems.get("/employeeSystem/{sys_Id}", response_model=EmployeeSystemsRead, status_code=status.HTTP_200_OK)
async def read_system(sys_Id: int, db: db_dependency):
    systems = db.query(EmployeeSystems).filter(EmployeeSystems.Id == sys_Id).first()
    if systems is None:
        raise HTTPException(status_code=404, detail='System was not found')
    return systems

# Employee Systems Table POST Method
@employee_systems.post("/employeeSystem/", response_model=EmployeeSystemsRead, status_code=status.HTTP_201_CREATED)
async def create_system(emp: EmployeeSystemsCreate, db: db_dependency):
    db_post = EmployeeSystems(**emp.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# Employee Systems Table DELETE Method
@employee_systems.delete("/employeeSystem/{sys_Id}", status_code=status.HTTP_200_OK)
async def delete_system(sys_Id: int, db: db_dependency):
    db_post = db.query(EmployeeSystems).filter(EmployeeSystems.Id == sys_Id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail='System was not found')
    db.delete(db_post)
    db.commit()
    return "Employee Deleted!"

# Employee Systems Table EDIT Method
@employee_systems.put("/employeeSystem/{sys_Id}", response_model=EmployeeSystemsRead, status_code=status.HTTP_200_OK)
async def update_system(sys_Id: int, updated_post: EmployeeSystemsCreate, db: db_dependency):
    db_post = db.query(EmployeeSystems).filter(EmployeeSystems.Id == sys_Id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail='System was not found')

    for key, value in updated_post.model_dump().items():
        setattr(db_post, key, value)

    db.commit()
    db.refresh(db_post)
    return db_post