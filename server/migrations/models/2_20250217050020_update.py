from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "inventory" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(1024) NOT NULL,
    "inventory_id" VARCHAR(1024) NOT NULL,
    "ipam_id" UUID NOT NULL REFERENCES "target" ("id") ON DELETE CASCADE
);
        COMMENT ON COLUMN "target"."type" IS 'ipam_netbox: netbox
server: server
nw: network';
        CREATE TABLE "inventory_user" (
    "inventory_id" UUID NOT NULL REFERENCES "inventory" ("id") ON DELETE CASCADE,
    "user_id" UUID NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "inventory_user";
        COMMENT ON COLUMN "target"."type" IS 'ipmi_netbox: netbox
server: server
nw: network';
        DROP TABLE IF EXISTS "inventory";"""
