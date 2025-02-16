from enum import Enum
from tortoise import Model
from tortoise.fields import *
from .ip_fields import IPNetworkField

class TargetType(Enum):
    ipam_netbox="netbox"
    server="server"
    nw="network"

class TargetRelay(Model):
    id = UUIDField(pk=True)
    target:ForeignKeyRelation["Target"] = ForeignKeyField("models.Target", related_name="targets")
    relay: ForeignKeyRelation["Relay"] = ForeignKeyField("models.Relay", related_name="relays")
    order = IntField()
    class Meta:
        table="target_relay"
        unique_together = ("target", "relay")
        ordering=("order",)

class Target(Model):
    id = UUIDField(pk=True)
    name = CharField(max_length=512)
    addr = IPNetworkField()
    conn_info = JSONField()
    type = CharEnumField(TargetType, max_length=512)
    relays:ManyToManyRelation["Relay"] = ManyToManyField("models.Relay", related_name="targets", through="target_relay")
    owners:ManyToManyRelation["User"] = ManyToManyField("models.User", related_name="targets")

from .user import User
from .relay import Relay