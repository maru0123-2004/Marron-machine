from ipaddress import IPv4Network, IPv6Network
from typing import List, Union
from uuid import UUID
from pydantic import BaseModel

class PolicyCreate(BaseModel):
    ipnetwork: Union[IPv4Network, IPv6Network]
    actions: List[str]
    permit: bool