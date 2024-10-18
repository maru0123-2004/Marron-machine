from ipaddress import IPv4Network, IPv6Network
from typing import List, Union
from uuid import UUID
from pydantic import BaseModel

class Policy(BaseModel):
    id: UUID
    ipnetwork: Union[IPv4Network, IPv6Network]
    actions: List[str]
    permit: bool