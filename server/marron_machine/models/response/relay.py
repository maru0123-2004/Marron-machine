from uuid import UUID
from pydantic import BaseModel, IPvAnyAddress

class Relay(BaseModel):
    id: UUID
    name: str
    addr: IPvAnyAddress
    conn_info: dict