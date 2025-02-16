import io
from typing import Union

from ..models.db.action import HistoryStatus
from ..models.db import Target, History
from ansible_runner.interface import run
import aiohttp
import marron_machine_runner
import aiofiles.tempfile

async def run_job(target:Target, action=None, event_handler=None, history:Union[History, None]=None, **opts):
    # Create job payload
    stdout=io.BytesIO()
    stdout.name="temp.dat"
    run(streamer="transmit", _output=stdout, **opts)
    stdout.seek(0)

    # run!
    result=io.BytesIO()
    if len(target.relays) == 0:
        result.write(await marron_machine_runner.run_job(stdout))
    else:
        relay=target.relays[0]
        data=aiohttp.FormData()
        data.add_field("file", stdout, filename="temp.dat")
        data.add_field("job", marron_machine_runner.model.Job(relays=target.relays).model_dump_json())
        async with aiohttp.ClientSession() as session:
            res=await session.post(f"{relay.conn_info.get('scheme', 'http')}://{relay.addr}:{relay.conn_info.get('port',80)}/job", data=data)
        if res.status == 200:
            result.write(await res.read())
    result.seek(0)

    # process data
    result_str=io.StringIO()
    def ev(event):
        if "stdout" in event:
            result_str.write(event["stdout"])
        if event_handler is not None:
            event_handler(event)
    async with aiofiles.tempfile.TemporaryDirectory() as tmpdir:
        run(streamer="process", _input=result, private_data_dir=tmpdir, event_handler=ev)
    
    # create history
    result_str.seek(0)
    result_str=result_str.read()
    if action is not None:
        if history is None:
            history=await History.create(status=HistoryStatus.success, action=action, logs=result_str)
        else:
            history.logs+="\n\n"+result_str
            await history.save()
    else:
        history=None
    return history, result_str