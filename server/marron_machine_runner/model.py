from typing import List
from pydantic import BaseModel, IPvAnyAddress

class Relay(BaseModel):
    addr: IPvAnyAddress
    conn_info: dict

class Job(BaseModel):
    relays: List[Relay]