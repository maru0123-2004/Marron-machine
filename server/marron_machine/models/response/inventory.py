from uuid import UUID
from pydantic import BaseModel

class Inventory(BaseModel):
    id: UUID
    name: str
    inventory_id: str
    ipam_id: UUID