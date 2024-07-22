from pydantic import BaseModel, Field
from datetime import datetime

class MessageRequest(BaseModel):
    SenderId: int
    Message: str = Field(min_length=1)

class MessageResponse(BaseModel):
    Id: int
    TicketId: int
    SenderId: int
    Message: str
    Timestamp: datetime

    class Config:
        from_attributes = True
