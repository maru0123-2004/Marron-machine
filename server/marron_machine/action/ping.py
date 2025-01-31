from ipaddress import ip_address
import socket
from typing import List
from aiofiles.tempfile import TemporaryDirectory

from marron_machine.action.netbox import register_hosts
from marron_machine.action.runner import run_job

from ..models.db.target import TargetType
from ..models.db import Action, Target

async def search_host_ping(action: Action):
    # List Up targets
    targets:List[Target]=[]
    ipmi=None
    for target in action.targets:
        if target.type == TargetType.server:
            targets.append(target)
        elif target.type == TargetType.nw:
            targets.append(target)
        elif target.type == TargetType.ipmi_netbox:
            ipmi=target
    hosts=[]

    def ev(event):
        if event["event"] == "playbook_on_stats":
            for host in event["event_data"]["ok"].keys():
                try:
                    hosts.append(ip_address(host))
                except ValueError:
                    hosts.append(ip_address(socket.gethostbyname(host)))

    for target in targets:
        async with TemporaryDirectory() as tmpdir:
            config=f"""
            name: ping
            plugin: community.general.nmap
            address: {target.addr}
            """
            with open(tmpdir+"/ping.yaml", "w") as conf:
                conf.write(config)
            await run_job(inventory=tmpdir+"/ping.yaml", module="ping", 
                private_data_dir=tmpdir, host_pattern="all",
                cmdline="--connection local",
                target=target, action=action, event_handler=ev
            )
    
    if ipmi is not None:
        await register_hosts(ipmi, hosts)
    return hosts