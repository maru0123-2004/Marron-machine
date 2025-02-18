import datetime
import io
from ipaddress import ip_address
import os
import pprint
import tempfile
from ansible_runner.interface import run
from pydantic import IPvAnyNetwork
from ansible_runner.interface import Processor,Worker
def scan(nw:IPvAnyNetwork=None):
    with tempfile.TemporaryDirectory() as tmpdir:
        config=f"""
        192.168.97.129 ansible_user='' ansible_ssh_pass=''
        """
        with open(tmpdir+"/ping.yaml", "w") as f:
            f.write(config)
        stdout=io.BytesIO()
        stdout.name="temp.dat"
        # with open(tmpdir+"/temp.dat", "wb") as stdout:
        a=run(streamer="transmit",inventory=tmpdir+"/ping.yaml", module="slurp", 
            module_args='{"path":"/var/lib/misc/dnsmasq.leases"}',
            private_data_dir=tmpdir, host_pattern="all",
            _output=stdout)
        # with open(tmpdir+"/temp.dat", "rb") as stdout:
        stdout.seek(0)
        stdout2=io.BytesIO()
        stdout2.name="temp.dat"
        with tempfile.TemporaryDirectory() as tmpdir2:
                # with open(tmpdir2+"/temp.dat","wb") as stdout2:
            run(streamer="worker",_input=stdout, _output=stdout2, private_data_dir=tmpdir2)
        stdout2.seek(0)
        with tempfile.TemporaryDirectory() as tmpdir3:
            a:Processor=run(streamer="process", _input=stdout2, private_data_dir=tmpdir3, event_handler=lambda e:print("event",e))
            print(a.rc)
        # for host in a:
        #     print(ip_address(host))

def ipmi():
    import pyipmi
    import pyipmi.interfaces
    interface = pyipmi.interfaces.create_interface(interface='ipmitool', interface_type="lanplus")
    ipmi = pyipmi.create_connection(interface)
    ipmi.session.set_session_type_rmcp(host='',port=623)
    ipmi.session.set_auth_type_user(username='',
                                password='')
    ipmi.target = pyipmi.Target()
    ipmi.session.establish()
    # device_id = ipmi.get_device_id()
    # pprint.pprint(device_id.__dict__)
    for k, v in ipmi.get_fru_board_area().__dict__.items():
        if isinstance(v, (str, int, bool, bytes, list, datetime.datetime)) or v is None:
            print(k, v)
        else:
            print(k, v.string)

if __name__ == "__main__":
    ipmi()