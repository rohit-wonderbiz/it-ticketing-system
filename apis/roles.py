from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import Annotated, Optional
from sqlalchemy.orm import Session

from models.model_role import Roles #Models
from schemas.schema_role import RolesBase, RoleCreate, RoleRead #Pydantic model
from database import SessionLocal

roles = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# Roles Table GET Method ALL
@roles.get("/", status_code=status.HTTP_200_OK)
async def read():
    return "Hello"

# Roles Table GET Method ALL
@roles.get("/role/", response_model=list[RoleRead], status_code=status.HTTP_200_OK)
async def read_all_role(db: db_dependency):
    employee_roles = db.query(Roles).all()
    if not employee_roles:
        raise HTTPException(status_code=404, detail='No Role was found')
    return employee_roles

# Roles Table GET Method
@roles.get("/role/{role_Id}", response_model=RoleRead, status_code=status.HTTP_200_OK)
async def read_role(role_Id: int, db: db_dependency):
    roles = db.query(Roles).filter(Roles.Id == role_Id).first()
    if roles is None:
        raise HTTPException(status_code=404, detail='Role was not found')
    return roles

# Roles Table POST Method
@roles.post("/role/", response_model=RoleRead, status_code=status.HTTP_201_CREATED)
async def create_role(emp: RoleCreate, db: db_dependency):
    db_post = Roles(**emp.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# Roles Table DELETE Method
@roles.delete("/role/{role_Id}", status_code=status.HTTP_200_OK)
async def delete_role(role_Id: int, db: db_dependency):
    db_post = db.query(Roles).filter(Roles.Id == role_Id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail='Role was not found')
    db.delete(db_post)
    db.commit()
    return "Role Deleted!"

# Roles Table EDIT Method
@roles.put("/role/{role_Id}", response_model=RoleRead, status_code=status.HTTP_200_OK)
async def update_role(role_Id: int, updated_post: RoleCreate, db: db_dependency):
    db_post = db.query(Roles).filter(Roles.Id == role_Id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail='Role was not found')

    for key, value in updated_post.model_dump().items():
        setattr(db_post, key, value)

    db.commit()
    db.refresh(db_post)
    return db_post