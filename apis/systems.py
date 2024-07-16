from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from models.model_systems import Systems #Models
from models.model_systems import SystemsBase, SystemsCreate, SystemsRead #Pydantic model
from database import SessionLocal

systems = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# Systems Table GET Method ALL
@systems.get("/", status_code=status.HTTP_200_OK)
async def read():
    return "Hello"

# Systems Table GET Method ALL
@systems.get("/get_all_systems/", response_model=list[SystemsRead], status_code=status.HTTP_200_OK)
async def read_all_system(db: db_dependency):
    employee_system = db.query(Systems).all()
    if not employee_system:
        raise HTTPException(status_code=404, detail='No system were found')
    return employee_system

# Systems Table GET Method
@systems.get("/get_system_by_id/{sys_Id}", response_model=SystemsRead, status_code=status.HTTP_200_OK)
async def read_system(sys_Id: int, db: db_dependency):
    systems = db.query(Systems).filter(Systems.Id == sys_Id).first()
    if systems is None:
        raise HTTPException(status_code=404, detail='System was not found')
    return systems

# Systems Table POST Method
@systems.post("/add_system/", response_model=SystemsRead, status_code=status.HTTP_201_CREATED)
async def create_system(emp: SystemsCreate, db: db_dependency):
    db_post = Systems(**emp.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# Systems Table DELETE Method
@systems.delete("/delete_system_by_id/{sys_Id}", status_code=status.HTTP_200_OK)
async def delete_system(sys_Id: int, db: db_dependency):
    db_post = db.query(Systems).filter(Systems.Id == sys_Id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail='System was not found')
    db.delete(db_post)
    db.commit()
    return "Employee Deleted!"

# Systems Table EDIT Method
@systems.put("/edit_system_by_id/{sys_Id}", response_model=SystemsRead, status_code=status.HTTP_200_OK)
async def update_system(sys_Id: int, updated_post: SystemsCreate, db: db_dependency):
    db_post = db.query(Systems).filter(Systems.Id == sys_Id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail='System was not found')

    for key, value in updated_post.model_dump().items():
        setattr(db_post, key, value)

    db.commit()
    db.refresh(db_post)
    return db_post