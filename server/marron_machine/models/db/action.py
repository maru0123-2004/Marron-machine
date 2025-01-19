from tortoise import Model
from tortoise.fields import *
from enum import Enum, IntEnum

class ActionModule(Enum):
    dhcp_dnsmasq="dhcp_dnsmasq"
    dns_dnsmasq="dns_dnsmasq"
    collect_ip="collect_ip"

class Action(Model):
    id = UUIDField(pk=True)
    name = CharField(max_length=512)
    targets:ManyToManyRelation["Target"] = ManyToManyField("models.Target", related_name="actions")
    action_module = CharEnumField(ActionModule, max_length=512)
    action_info = JSONField()
    interval = IntField()
    owners:ManyToManyRelation["User"] = ManyToManyField("models.User", related_name="actions")
    historys:ReverseRelation["History"]

class HistoryStatus(IntEnum):
    planed=0
    success=1
    fail=2

class History(Model):
    id = UUIDField(pk=True)
    status = IntEnumField(HistoryStatus)
    time = DatetimeField(auto_now_add=True)
    logs = TextField()
    action:ForeignKeyRelation[Action] = ForeignKeyField("models.Action", related_name="historys", on_delete=SET_NULL, null=True)

from .target import Target
from .user import User