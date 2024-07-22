from pydantic import BaseModel


class TicketStatusBase(BaseModel):
    Status : str

class TicketStatusCreate(TicketStatusBase):
    pass

class TicketStatusRead(TicketStatusBase):
    Id : int

    