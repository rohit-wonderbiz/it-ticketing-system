from fastapi import FastAPI

from database import engine, Base

import database
from database import Base, engine
from apis.employees import employees


# Create all tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(employees)
# app.include_router(employer_profile)
# app.include_router(job_posting)