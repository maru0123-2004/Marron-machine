from tortoise import Model
from tortoise.fields import *

class Inventory(Model):
    id = UUIDField(pk=True)
    name = CharField(max_length=1024)
    inventory_id= CharField(max_length=1024)
    ipam:ForeignKeyRelation["Target"] = ForeignKeyField("models.Target", related_name="inventories")
    owners:ManyToManyRelation["User"] = ManyToManyField("models.User", related_name="inventories")

from .user import User
from .target import Target