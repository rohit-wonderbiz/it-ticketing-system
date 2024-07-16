from fastapi import FastAPI

from database import engine, Base, SessionLocal

from apis.employees import employees
from models.model_vendors import Vendors
# from api.employer_profile import employer_profile
# from api.job_posting import job_posting

# Create all tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(employees)
# app.include_router(employer_profile)
# app.include_router(job_posting)