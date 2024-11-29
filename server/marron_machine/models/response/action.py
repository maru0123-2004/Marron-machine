from uuid import UUID
from pydantic import BaseModel

from ..db.action import ActionModule

class Action(BaseModel):
    name: str
    action_module: ActionModule
    action_info: dict
    interval: int