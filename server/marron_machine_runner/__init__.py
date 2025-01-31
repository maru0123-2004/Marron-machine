from typing import BinaryIO, List
from fastapi import FastAPI, Form, UploadFile
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse
from .model import Job, Relay
import ansible_runner
import io, aiofiles, aiohttp
import ansible_runner.interface

runner=FastAPI(title="Marron-Machine-runner")

async def run_job(file:BinaryIO):
    file.name="temp.dat"
    output=io.BytesIO()
    output.name="temp.dat"
    async with aiofiles.tempfile.TemporaryDirectory() as tmpdir:
        ansible_runner.interface.run(streamer="worker", private_data_dir=tmpdir, _input=file, _output=output)
    output.seek(0)
    return output.read()

async def relay_job(relay_model:Relay, file:BinaryIO, another_relay:List[Relay]):
    data=aiohttp.FormData()
    data.add_field("file", file, filename="temp.dat")
    data.add_field("job", Job(relays=another_relay).model_dump_json())
    async with aiohttp.ClientSession() as session:
        res=await session.post(f"{relay_model.conn_info.get('scheme', 'http')}://{relay_model.addr}:{relay_model.conn_info.get('port',80)}/job", data=data)
    if res.status == 200:
        return await res.read()
    else:
        raise

@runner.get("/ping")
async def ping():
    pass

@runner.post("/job", response_class=StreamingResponse)
async def job(file: UploadFile, job:str=Form()):
    job_model=Job.model_validate_json(job)
    if len(job_model.relays) > 1:
        relay=job_model.relays.pop()
        return await relay_job(relay, file, job_model.relays)
    else:
        return await run_job(file.file)