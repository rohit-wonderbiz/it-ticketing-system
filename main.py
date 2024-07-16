from fastapi import FastAPI

from database import engine, Base

import database
from database import Base, engine
from apis.employees import employees
<<<<<<< HEAD
from models import model_role , model_systems

=======
from apis.systems import systems
>>>>>>> ba2edec20412622fa40adb2fc9a0ad99af975947

# Create all tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(employees)
app.include_router(systems)
# app.include_router(employer_profile)
# app.include_router(job_posting)