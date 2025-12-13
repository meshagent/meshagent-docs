import uuid
from meshagent.tools import Tool, Toolkit, ToolContext, RemoteToolkit
from meshagent.api.messaging import FileResponse, JsonResponse, TextResponse

class SaveCandidateDetails(Tool):
    def __init__(self):
        super().__init__(
            name="save-candidate-details",
            title="save-candidate-details",
            description="Store information about a candidate in the room database",
            input_schema={
                "type": "object",
                "additionalProperties": False,
                "required": ["resume_path", "candidate_name", "contact_info", "resume_summary", "web_search_notes"],
                "properties": {
                    "resume_path": {"type": "string"},
                    "candidate_name": {"type": "string"},
                    "contact_info": {"type": "string"},
                    "resume_summary": {"type": "string"},
                    "web_search_notes": {"type":"string"}
                }
            }
        )
    async def execute(self, context:ToolContext, resume_path:str, candidate_name:str, contact_info:str|None, resume_summary:str, web_search_notes:str|None):
        candidate_id = str(uuid.uuid4())
        record = {
                    "candidate_id": candidate_id,
                    "resume_path": resume_path,
                    "candidate_name": candidate_name,
                    "contact_info": contact_info,
                    "resume_summary": resume_summary, 
                    "web_search_notes": web_search_notes
                }
        try:
            await context.room.database.insert(table="candidates", records=[record])
        except Exception as e:
            return JsonResponse(json={"status":"error", "error":str(e), "resume_path":resume_path})
        return JsonResponse(json={"status":"ok", "saved":record})
    
# @service.path(identity="resume-toolkit", path="/resume-toolkit")
class ResumeToolkit(RemoteToolkit):
    def __init__(self):
        super().__init__(
            name="resume-toolkit",
            title="resume-toolkit",
            description="a toolkit for managing resumes",
            tools=[
                SaveCandidateDetails(), 
            ],
        )