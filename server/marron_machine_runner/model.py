from typing import List
from pydantic import BaseModel, IPvAnyAddress

class Relay(BaseModel):
    addr: IPvAnyAddress
    config: dict

class Job(BaseModel):
    relays: List[Relay]