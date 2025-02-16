import base64
from typing import List, TypedDict

from ..models.db import Action, Target
from ..models.db.target import TargetType
from typing import List
from aiofiles.tempfile import TemporaryDirectory

class HostWithName(TypedDict):
    macaddr: str
    ipaddr: str
    hostname: str

from .netbox import register_hosts_with_name
from .runner import run_job

async def get_lease_dnsmasq(action:Action):
    # List Up targets
    targets:List[Target]=[]
    ipam=None
    for target in action.targets:
        if target.type == TargetType.server:
            targets.append(target)
        elif target.type == TargetType.ipam_netbox:
            ipam=target
    hosts=[]

    def ev(event):
        if event["event"] == "runner_on_ok":
            content=event["event_data"]["res"]["content"]
            if event["event_data"]["res"]["encoding"] == "base64":
                content_str=base64.b64decode(content).decode("utf-8")
                leases=content_str.splitlines()
            for lease in leases:
                lease_split=lease.split(" ")
                if len(lease_split)>=3:
                    _, macaddr, ipaddr, hostname, *_=lease_split
                    if hostname != "*":
                        hosts.append({"macaddr":macaddr, "ipaddr":ipaddr, "hostname":hostname})
    
    history=None
    async with TemporaryDirectory() as tmpdir:
        with open(tmpdir+"/dhcp.yaml", "w") as conf:
            for target in targets:
                if "ssh_privkey" in target.conn_info:
                    nowconf=open(tmpdir+"/temp_dhcp.yaml","w")
                else:
                    nowconf=conf
                for host in target.addr.hosts():
                    opts=[]
                    if "user" in target.conn_info:
                        opts.append(f"ansible_user='{target.conn_info['user']}'")
                    if "ssh_passwd" in target.conn_info:
                        opts.append(f"ansible_ssh_pass='{target.conn_info['ssh_passwd']}'")
                    nowconf.write(str(host)+" "+" ".join(opts)+"\n")
                if nowconf is not conf:
                    nowconf.close()
                    history, _=await run_job(inventory=tmpdir+"/temp_dhcp.yaml", module="slurp", 
                        module_args='{"path":"'+action.action_info.get("lease_file","/var/lib/misc/dnsmasq.leases")+'"}',
                        private_data_dir=tmpdir, host_pattern="all",
                        target=target, action=action, event_handler=ev, history=history
                    )

        await run_job(inventory=tmpdir+"/dhcp.yaml", module="slurp", 
            module_args='{"path":"'+action.action_info.get("lease_file","/var/lib/misc/dnsmasq.leases")+'"}',
            private_data_dir=tmpdir, host_pattern="all",
            target=target, action=action, event_handler=ev, history=history
        )

    if ipam is not None:
        await register_hosts_with_name(ipam, hosts)
    
    return hosts