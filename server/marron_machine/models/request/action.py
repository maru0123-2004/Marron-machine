from typing import Optional
from pydantic import BaseModel

from ..db.action import ActionModule

class ActionCreate(BaseModel):
    name: str
    action_module: ActionModule
    action_info: dict
    interval: int

class ActionUpdate(BaseModel):
    name: Optional[str] = None
    action_module: Optional[ActionModule]=None
    action_info: Optional[dict]=None
    interval: Optional[int]=None