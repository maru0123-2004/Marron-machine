from uuid import UUID
from pydantic import BaseModel, IPvAnyNetwork

from ..db.target import TargetType

class Target(BaseModel):
    id: UUID
    name: str
    addr: IPvAnyNetwork
    conn_info: dict
    type: TargetType