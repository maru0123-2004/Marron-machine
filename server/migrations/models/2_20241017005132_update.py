from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "policy" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "ipnetwork" INET NOT NULL,
    "actions" TEXT[] NOT NULL,
    "permit" BOOL NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "policy";"""
