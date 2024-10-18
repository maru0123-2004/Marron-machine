from tortoise import Model
from tortoise.fields import *

from .array_fields import StrArrayField
from .ip_fields import IPNetworkField

class Policy(Model):
    id=UUIDField(pk=True)
    ipnetwork=IPNetworkField()
    actions=StrArrayField()
    permit=BooleanField()