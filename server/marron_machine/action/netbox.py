from typing import List, TypedDict
from netbox_python import NetBoxClient
from pydantic import IPvAnyAddress

from ..models.db import Target

def get_netbox_client(target:Target):
    if target.addr.prefixlen!=target.addr.max_prefixlen:
        raise ValueError("netbox target address must be /32(v4) or /128(v6)")
    netbox_url=f"{target.conn_info.get('scheme', 'http')}://{target.addr.network_address}:{target.conn_info.get('port',80)}"
    netbox=NetBoxClient(netbox_url, token=target.conn_info.get("api_key"))
    return netbox

async def register_hosts_with_name(target:Target, hosts:List["HostWithName"]):
    netbox=get_netbox_client(target)
    res=netbox.ipam.ip_addresses.list(address=[host["ipaddr"] for host in hosts])
    for host in hosts:
        if len(list(filter(lambda r:r["address"]==host['ipaddr'],res.data)))==0:
            netbox.ipam.ip_addresses.create(address=host["ipaddr"], dns_name=host['hostname'])

async def get_hosts_with_name(target:Target) -> List["HostWithName"]:
    netbox=get_netbox_client(target)
    res=netbox.ipam.ip_addresses.all()
    return [{"macaddr":"", "hostname":host["dns_name"], "ipaddr":host["address"].replace("/32","")} for host in res.data if host["dns_name"]!=""]

async def register_hosts(target:Target, hosts:List[IPvAnyAddress]):
    netbox=get_netbox_client(target)
    res=netbox.ipam.ip_addresses.list(address=[str(host)for host in hosts])
    for host in hosts:
        if len(list(filter(lambda r:r["address"]==host,res.data)))==0:
            netbox.ipam.ip_addresses.create(address=str(host))

class InventoryDict(TypedDict):
    id: str
    name: str

async def get_inventories(target:Target) -> List[InventoryDict]:
    netbox=get_netbox_client(target)
    devices=netbox.dcim.devices.all().data
    return [{"id":str(d["id"]), "name":d["name"]} for d in devices]
async def create_inventory(target:Target, name:str, inventory:"IPMIInventory", device_role="server", site="default"):
    netbox=get_netbox_client(target)
    manufacturer={"name":inventory.manufacturer, "slug":inventory.manufacturer.replace(" ","-")}
    role={"name":device_role, "slug":device_role.replace(" ","-")}
    inventory.name=inventory.name.rstrip()
    device=netbox.dcim.devices.create(device_type={"manufacturer":manufacturer, "model":inventory.name, "slug":inventory.name.replace(" ","-")}, role=role, site={"name":site,"slug":site}, serial=inventory.serial_number, name=name)
    return str(device.data["id"])
from .dhcp import HostWithName
from .ipmi import IPMIInventory