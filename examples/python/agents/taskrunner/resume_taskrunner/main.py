import asyncio
import logging
import os

from meshagent.api.services import ServiceHost, ServicePath
from meshagent.otel import otel_config

from mailbot_toolkit import MailBotToolkit
from resume_toolkit import ResumeToolkit
from open_roles_toolkit import OpenRolesToolkit

otel_config(service_name="resume-runner")
log = logging.getLogger("resume-runner")
log.setLevel(logging.DEBUG) # switch to info later 

service = ServiceHost()

service.paths.append(ServicePath(path="/resume-toolkit", identity="resume-toolkit", cls=ResumeToolkit))
service.paths.append(ServicePath(identity="/mailbot-toolkit", path="/mailbot-toolkit", cls=MailBotToolkit))

asyncio.run(service.run())