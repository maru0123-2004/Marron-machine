from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends

from ..exceptions import NotFound
from .auth import get_user
from ..models.db import Policy as PolicyDB, User as UserDB
from ..models.response.policy import Policy
from ..models.request.policy import PolicyCreate

router=APIRouter(tags=["Policy"])

@router.get("/", response_model=List[Policy])
async def gets(user:UserDB=Depends(get_user)):
    return await PolicyDB.all()

@router.post("/", response_model=Policy)
async def create(policy:PolicyCreate, user:UserDB=Depends(get_user)):
    return await PolicyDB.create(**policy.model_dump())

@router.delete("/{policy_id}", response_model=Policy)
async def delete(policy_id:UUID, user:UserDB=Depends(get_user)):
    policy=await PolicyDB.get_or_none(id=policy_id)
    if policy is None:
        raise NotFound()
    await policy.delete()
    return policy