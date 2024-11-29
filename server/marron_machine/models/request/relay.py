from typing import Optional
from pydantic import BaseModel, IPvAnyAddress

class RelayCreate(BaseModel):
    name: str
    addr: IPvAnyAddress
    conn_info: dict

class RelayUpdate(BaseModel):
    name: Optional[str] = None
    addr: Optional[IPvAnyAddress] = None
    conn_info: Optional[dict] = None