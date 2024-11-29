from tortoise import Model
from tortoise.fields import *

from .ip_fields import IPAddressField

class Relay(Model):
    id = UUIDField(pk=True)
    name = CharField(max_length=512)
    addr = IPAddressField()
    conn_info = JSONField()
    targets:ManyToManyRelation["Target"]
    owners:ManyToManyRelation["User"] = ManyToManyField("models.User", related_name="relays")

from .user import User
from .target import Target