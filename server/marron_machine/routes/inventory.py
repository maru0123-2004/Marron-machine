from typing import Dict, List
from uuid import UUID, uuid4
from fastapi import APIRouter, Depends

from ..models.response.user import User
from ..action.netbox import InventoryDict, get_inventories, create_inventory
from ..action.ipmi import get_inventory_from_ipmi, IPMIInventory
from ..exceptions import APIError, NotFound
from ..models.db.target import TargetType
from ..models.response.inventory import Inventory
from ..models.request.inventory import InventoryCreate, InventoryCreateForIPMI
from ..models.db import Inventory as InventoryDB, User as UserDB, Target as TargetDB
from .auth import get_user

router=APIRouter(tags=["Inventory"])

@router.get("/", response_model=List[Inventory])
async def gets(user:UserDB=Depends(get_user)):
    await user.fetch_related("inventories")
    return user.inventories

@router.post("/", response_model=Inventory)
async def create(inventory:InventoryCreate, user:UserDB=Depends(get_user)):
    target=await TargetDB.get_or_none(id=inventory.ipam_id)
    if target is None:
        raise NotFound(detail="Target is not found")
    if target.type != TargetType.ipam_netbox:
        raise APIError(detail="Target type must be IPAM")
    inventory_db=await InventoryDB.create(**inventory.model_dump())
    await inventory_db.owners.add(user)
    return inventory_db

@router.get("/suggest", response_model=Dict[UUID, List[InventoryDict]])
async def suggest(user:UserDB=Depends(get_user)):
    await user.fetch_related("targets")
    return {target.id:await get_inventories(target) for target in user.targets if target.type==TargetType.ipam_netbox}

@router.post("/create_from_ipmi", response_model=Inventory)
async def create_from_ipmi(inventory:InventoryCreateForIPMI, user:UserDB=Depends(get_user)):
    target=await TargetDB.get_or_none(id=inventory.ipam_id)
    if target is None:
        raise NotFound(detail="Target is not found")
    if target.type != TargetType.ipam_netbox:
        raise APIError(detail="Target type must be IPAM")
    inv=await get_inventory_from_ipmi(inventory.ipaddr, inventory.username, inventory.password, inventory.ipmi_interface_type)
    devid=await create_inventory(target=target, name=inventory.name, inventory=inv)
    return Inventory(id=uuid4, name=inventory.name, inventory_id=devid, ipam_id=target.id)

@router.get("/{invntory_id}", response_model=str)
async def get_url(inventory_id:UUID, user:UserDB=Depends(get_user)):
    inventory_db=await user.inventories.filter(id=inventory_id).first().prefetch_related("ipam")
    if inventory_db is None:
        raise NotFound()
    netbox_url=f"{inventory_db.ipam.conn_info.get('scheme', 'http')}://{inventory_db.ipam.addr.network_address}:{inventory_db.ipam.conn_info.get('port',80)}"
    return inventory_db.ipam.conn_info.get("qr_baseurl",netbox_url)+"/dcim/devices/"+inventory_db.inventory_id

@router.delete("/{inventory_id}", response_model=Inventory)
async def delete(inventory_id: UUID, user:UserDB=Depends(get_user)):
    inventory_db=await user.inventories.filter(id=inventory_id).first()
    if inventory_db is None:
        raise NotFound()
    await inventory_db.delete()
    return inventory_db

@router.get("/{inventory_id}/owner", response_model=List[User])
async def get_owner(inventory_id: UUID, user:UserDB=Depends(get_user)):
    inventory_db=await user.inventories.filter(id=inventory_id).first().prefetch_related("owners")
    if inventory_db is None:
        raise NotFound()
    return inventory_db.owners

@router.put("/{inventory_id}/owner", response_model=List[User])
async def add_owner(inventory_id: UUID, user_id:UUID, user:UserDB=Depends(get_user)):
    inventory_db=await user.inventories.filter(id=inventory_id).first()
    if inventory_db is None:
        raise NotFound()
    owner=await UserDB.get_or_none(id=user_id)
    if owner is None:
        raise NotFound(detail="Owner Not found")
    await inventory_db.owners.add(owner)
    await inventory_db.fetch_related("owners")
    return inventory_db.owners

@router.delete("/{inventory_id}/owner", response_model=List[User])
async def del_owner(inventory_id: UUID, user_id:UUID, user:UserDB=Depends(get_user)):
    inventory_db=await user.inventories.filter(id=inventory_id).first().prefetch_related("owners")
    if inventory_db is None:
        raise NotFound()
    if len(inventory_db.owners) <= 1:
        raise APIError(detail="Cant delete only you")
    owner=await UserDB.get_or_none(id=user_id)
    if owner is None:
        raise NotFound(detail="Owner Not found")
    await inventory_db.owners.remove(owner)
    await inventory_db.fetch_related("owners")
    return inventory_db.owners