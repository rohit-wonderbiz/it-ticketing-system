from fastapi import FastAPI

from database import engine, Base

import database
from database import Base, engine
from apis.employees import employees
from apis.employee_systems import employee_systems
from apis.roles import roles
from apis.tickets import tickets
from apis.ticket_status import ticket_status
from apis.ticket_priority import ticket_priority
from apis.messages import message_route

# Create all tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(employees)
app.include_router(employee_systems)
app.include_router(roles)
app.include_router(tickets)
app.include_router(ticket_status)
app.include_router(ticket_priority)
app.include_router(message_route)