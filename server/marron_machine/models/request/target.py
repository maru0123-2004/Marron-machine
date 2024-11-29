from typing import Optional
from pydantic import BaseModel, IPvAnyNetwork

from ..db.target import TargetType

class TargetCreate(BaseModel):
    name: str
    addr: IPvAnyNetwork
    conn_info: dict
    type: TargetType

class TargetUpdate(BaseModel):
    name: Optional[str] = None
    addr: Optional[IPvAnyNetwork] = None
    conn_info: Optional[dict] = None
    type: Optional[TargetType] = None