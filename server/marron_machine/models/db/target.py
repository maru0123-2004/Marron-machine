from enum import Enum
from tortoise import Model
from tortoise.fields import *

class TargetType(Enum):
    netbox_hosts="netbox_hosts"
    netbox_ips="netbox_ips"
    netbox_invs="netbox_invs"
    dhcp_isc="dhcp_isc"
    dns_masq="dns_masq"

class Target(Model):
    id=UUIDField(pk=True)
    url=CharField(max_length=1024)
    type=CharEnumField(TargetType, max_length=50, unique=True)
    interval=IntField()
    last_exec=DatetimeField(null=True)