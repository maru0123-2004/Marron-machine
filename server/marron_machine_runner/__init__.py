from typing import BinaryIO, List
from fastapi import FastAPI, Form, UploadFile
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse
from .model import Job, Relay
import ansible_runner

runner=FastAPI(title="Marron-Machine-runner")

async def relay_job(relay_model:Relay, file:BinaryIO, another_relay:List[Relay]):
    yield

@runner.get("/ping")
async def ping():
    pass

@runner.post("/job", response_class=StreamingResponse)
async def job(file: UploadFile, job:str=Form()):
    job_model=Job.model_validate_json(job)
    if len(job_model.relays) != 0:
        relay=job_model.relays.pop()
        return EventSourceResponse(await relay_job(relay, file, job_model.relays), send_timeout=5)
    else:
        stdout=BinaryIO()
        ansible_runner.run_async(streamer="worker", _input=file.file, _output=stdout)
        return EventSourceResponse(stdout)