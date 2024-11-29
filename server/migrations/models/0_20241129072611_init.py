from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "action" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(512) NOT NULL,
    "action_module" VARCHAR(512) NOT NULL,
    "action_info" JSONB NOT NULL,
    "inerval" INT NOT NULL
);
COMMENT ON COLUMN "action"."action_module" IS 'dhcp_dnsmasq: dhcp_dnsmasq\ndns_dnsmasq: dns_dnsmasq\ncollect_ip: collect_ip';
CREATE TABLE IF NOT EXISTS "history" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "status" SMALLINT NOT NULL,
    "time" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "logs" TEXT NOT NULL,
    "action_id" UUID REFERENCES "action" ("id") ON DELETE SET NULL
);
COMMENT ON COLUMN "history"."status" IS 'planed: 0\nsuccess: 1\nfail: 2';
CREATE TABLE IF NOT EXISTS "relay" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(512) NOT NULL,
    "addr" INET NOT NULL,
    "conn_info" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "target" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(512) NOT NULL,
    "addr" INET NOT NULL,
    "conn_info" JSONB NOT NULL,
    "type" VARCHAR(512) NOT NULL
);
COMMENT ON COLUMN "target"."type" IS 'ipmi_netbox: netbox\nserver: server\nnw: network';
CREATE TABLE IF NOT EXISTS "target_relay" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "order" INT NOT NULL,
    "relay_id" UUID NOT NULL REFERENCES "relay" ("id") ON DELETE CASCADE,
    "target_id" UUID NOT NULL REFERENCES "target" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_target_rela_target__f1c4f5" UNIQUE ("target_id", "relay_id")
);
CREATE TABLE IF NOT EXISTS "user" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(1024) NOT NULL UNIQUE,
    "password" VARCHAR(1024) NOT NULL,
    "mail" VARCHAR(1024) NOT NULL UNIQUE,
    "created_in" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "token" (
    "token" VARCHAR(1024) NOT NULL  PRIMARY KEY,
    "created_in" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "expired_in" TIMESTAMPTZ NOT NULL,
    "user_id" UUID NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "action_target" (
    "action_id" UUID NOT NULL REFERENCES "action" ("id") ON DELETE CASCADE,
    "target_id" UUID NOT NULL REFERENCES "target" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_action_targ_action__ea0b02" ON "action_target" ("action_id", "target_id");
CREATE TABLE IF NOT EXISTS "action_user" (
    "action_id" UUID NOT NULL REFERENCES "action" ("id") ON DELETE CASCADE,
    "user_id" UUID NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_action_user_action__06737d" ON "action_user" ("action_id", "user_id");
CREATE TABLE IF NOT EXISTS "relay_user" (
    "relay_id" UUID NOT NULL REFERENCES "relay" ("id") ON DELETE CASCADE,
    "user_id" UUID NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_relay_user_relay_i_21b875" ON "relay_user" ("relay_id", "user_id");
CREATE TABLE IF NOT EXISTS "target_user" (
    "target_id" UUID NOT NULL REFERENCES "target" ("id") ON DELETE CASCADE,
    "user_id" UUID NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_target_user_target__376b6b" ON "target_user" ("target_id", "user_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
