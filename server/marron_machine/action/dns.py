import json
from typing import List
from aiofiles.tempfile import TemporaryDirectory

from ..models.db import Action, Target
from ..models.db.target import TargetType
from .netbox import get_hosts_with_name
from .runner import run_job

async def register_hostnames_dnsmasq(action:Action):
    targets:List[Target]=[]
    ipam=None
    for target in action.targets:
        if target.type == TargetType.server:
            targets.append(target)
        elif target.type == TargetType.ipam_netbox:
            ipam=target
    if ipam is None:
        raise ValueError("IPAM is not present")
    register_hosts=await get_hosts_with_name(ipam)
    
    history=None
    async with TemporaryDirectory() as tmpdir:
        for host in register_hosts:
            host_line={
                "dest":"/etc/hosts",
                "state":"present",
                "regexp":"^"+host["ipaddr"],
                "line":host["ipaddr"]+" "+host["hostname"], 
                "create":"yes"}
            with open(tmpdir+"/dns.yaml", "w") as conf:
                for target in targets:
                    if "ssh_privkey" in target.conn_info:
                        nowconf=open(tmpdir+"/temp_dns.yaml","w")
                    else:
                        nowconf=conf
                    for target_host in target.addr.hosts():
                        opts=[]
                        if "user" in target.conn_info:
                            opts.append(f"ansible_user='{target.conn_info['user']}'")
                        if "ssh_passwd" in target.conn_info:
                            opts.append(f"ansible_ssh_pass='{target.conn_info['ssh_passwd']}'")
                        if "sudo_passwd" in target.conn_info:
                            opts.append(f"ansible_sudo_pass='{target.conn_info['sudo_passwd']}'")
                        nowconf.write(str(target_host)+" "+" ".join(opts)+"\n")
                    if nowconf is not conf:
                        nowconf.close()
                        history, _=await run_job(inventory=tmpdir+"/temp_dns.yaml", module="lineinfile", 
                            module_args=json.dumps(host_line),
                            private_data_dir=tmpdir, host_pattern="all",
                            target=target, action=action, history=history, cmdline="--become"
                        )

            history,_=await run_job(inventory=tmpdir+"/dns.yaml", module="lineinfile",
                module_args=json.dumps(host_line),
                private_data_dir=tmpdir, host_pattern="all",
                target=target, action=action, history=history, cmdline="--become"
            )
            history,_=await run_job(inventory=tmpdir+"/dns.yaml", module="systemd_service",
                module_args=json.dumps({"state":"restarted", "name":"dnsmasq"}),
                private_data_dir=tmpdir, host_pattern="all",
                target=target, action=action, history=history, cmdline="--become"
            )