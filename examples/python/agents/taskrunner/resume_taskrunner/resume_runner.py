import asyncio
import logging
from meshagent.api.services import ServiceHost
from meshagent.agents import TaskRunner
from meshagent.otel import otel_config

otel_config(service_name="resume-runner")
log = logging.getLogger("resume-runner")

service = ServiceHost() 

# Resume agent needs to take in a file, process the file, save the file and results to the room
# Agent should compare the resume to other job descriptions and indicate if the person is a match for them
@service.path(identity="resume-runner", path="/resumerunner")
class ResumeRunner(TaskRunner):
    def __init__(self):
        super().__init__(
            name="resume-runner",
            title="resume-runner",
            description="A TaskRunner that processes Resumes",
            input_schema={}
        )

asyncio.run(service.run())