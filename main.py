from fastapi import FastAPI

from database import engine, Base

import database
from database import Base, engine
from apis.employees import employees
from apis.systems import systems
from apis.roles import roles
from apis.tickets import tickets
from apis.ticket_status import ticket_status

# Create all tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(employees)
app.include_router(systems)
app.include_router(roles)
app.include_router(tickets)
app.include_router(ticket_status)
