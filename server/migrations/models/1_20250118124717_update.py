from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "action" RENAME COLUMN "inerval" TO "interval";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "action" RENAME COLUMN "interval" TO "inerval";"""
