
import uuid
from meshagent.tools import Tool, Toolkit, ToolContext, RemoteToolkit
from meshagent.api.messaging import FileResponse, JsonResponse, TextResponse

class SaveJobDescriptionDetails(Tool):
    def __init__(self):
        super().__init__(
            name="save-job-description-details",
            title="save-job-description-details",
            description="Store information about open roles and their job description in the room database",
            input_schema={
                "type": "object",
                "additionalProperties": False,
                "required": ["hiring_manager", "job_title", "job_description_path", "required_skills"],
                "properties": {
                    "hiring_manager": {"type": "string"},
                    "job_title": {"type": "string"},
                    "job_description_path": {"type": "string"},
                    "required_skills": {"type": "string"}
                }
            }
        )
          
    async def execute(self, context:ToolContext, hiring_manager:str, job_title:str, job_description_path:str, required_skills:str|None):
        role_id = str(uuid.uuid4())
        record = {
                    "role_id": role_id,
                    "hiring_manager": hiring_manager,
                    "job_title": job_title,
                    "job_description_path": job_description_path,
                    "required_skills": required_skills
                }
        try:
            await context.room.database.insert(table="open_roles", records=[record])
        except Exception as e:
            return JsonResponse(json={"status":"error", "error":str(e), "job_description_path":job_description_path})
        return JsonResponse(json={"status":"ok", "saved":record})

# @service.path(identity="open-roles-toolkit", path="/open-roles-toolkit")
class OpenRolesToolkit(RemoteToolkit):
    def __init__(self):
        super().__init__(
            name="open-roles-toolkit",
            title="open-roles-toolkit",
            description="a toolkit for managing open roles",
            tools=[
                SaveJobDescriptionDetails()
            ],
        )