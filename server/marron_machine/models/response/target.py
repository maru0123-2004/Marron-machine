from datetime import datetime
from typing import Union
from uuid import UUID
from pydantic import BaseModel

from ..db.target import TargetType

class Target(BaseModel):
    id:UUID
    url:str
    type:TargetType
    interval:int
    last_exec:Union[datetime, None]