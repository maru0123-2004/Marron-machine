from aionetbox import AIONetbox
from pydantic import IPvAnyAddress
from ..models.db import Target

async def register_hosts(target:Target, hosts:IPvAnyAddress):
    AIONetbox(f"{target.conn_info.get('scheme', 'http')}://{target.addr}/", api_key=target.conn_info.get("api_key"))