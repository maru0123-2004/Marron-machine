from pydantic import BaseModel, IPvAnyAddress
import pyipmi
import pyipmi.interfaces
from asyncer import asyncify

class IPMIInventory(BaseModel):
    manufacturer: str
    serial_number: str
    name: str

async def get_inventory_from_ipmi(ipaddress:IPvAnyAddress, username, password, int_type="lanplus"):
    interface = pyipmi.interfaces.create_interface(interface='ipmitool', interface_type=int_type)
    ipmi = pyipmi.create_connection(interface)
    ipmi.session.set_session_type_rmcp(host=str(ipaddress),port=623)
    ipmi.session.set_auth_type_user(username=username, password=password)
    ipmi.target = pyipmi.Target()
    ipmi.session.establish()
    product=await asyncify(ipmi.get_fru_product_area)()
    return IPMIInventory(
        manufacturer=product.manufacturer.string,
        serial_number=product.serial_number.string,
        name=product.name.string
    )
    