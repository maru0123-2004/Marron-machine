from pydantic import BaseModel

from ..db.target import TargetType

class TargetCreate(BaseModel):
    url:str
    type:TargetType
    interval:int