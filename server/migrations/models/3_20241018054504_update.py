from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "target" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "url" VARCHAR(1024) NOT NULL,
    "type" VARCHAR(50) NOT NULL UNIQUE,
    "interval" INT NOT NULL,
    "last_exec" TIMESTAMPTZ
);
COMMENT ON COLUMN "target"."type" IS 'netbox_hosts: netbox_hosts\nnetbox_ips: netbox_ips\nnetbox_invs: netbox_invs\ndhcp_isc: dhcp_isc\ndns_masq: dns_masq';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "target";"""
