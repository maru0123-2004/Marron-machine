import datetime
from uuid import UUID
from pydantic import BaseModel

from ..db.action import HistoryStatus

class History(BaseModel):
    id: UUID
    status: HistoryStatus
    time: datetime.datetime
    logs: str