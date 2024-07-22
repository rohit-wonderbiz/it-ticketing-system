from sqlalchemy.orm import relationship
from pydantic import BaseModel

class RolesBase(BaseModel):
    RoleName : str
    RoleCode : str = None

class RoleCreate(RolesBase):
    pass

class RoleRead(RolesBase):
    Id: int

    class Config():
        from_attributes = True
 