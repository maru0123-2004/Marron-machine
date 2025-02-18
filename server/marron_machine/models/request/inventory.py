from typing import Optional
from uuid import UUID
from pydantic import BaseModel, IPvAnyAddress

class InventoryCreate(BaseModel):
    name: str
    inventory_id: str
    ipam_id: UUID

class InventoryCreateForIPMI(InventoryCreate):
    ipaddr: IPvAnyAddress
    username: str
    password: str
    inventory_id:Optional[str]=None
    ipmi_interface_type:Optional[str]="lanplus"
    ipmi_hostname: Optional[str]=None