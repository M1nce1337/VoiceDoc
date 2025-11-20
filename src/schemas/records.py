from pydantic import BaseModel
from datetime import datetime

class RecordSchema(BaseModel):
    id: int
    created_at: datetime
    text: str

    class Config:
        orm_node = True