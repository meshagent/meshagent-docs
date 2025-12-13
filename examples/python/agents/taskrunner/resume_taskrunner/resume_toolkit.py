import json
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


class GetCandidateDetails(Tool):
    def __init__(self):
        super().__init__(
            name="get-candidate-details",
            title="get-candidate-details",
            description="Fetch a candidate by id",
            input_schema={
                "type": "object",
                "additionalProperties": False,
                "required": ["candidate_id"],
                "properties": {"candidate_id": {"type": "string"}},
            },
        )

    async def execute(self, context: ToolContext, candidate_id: str):
        results = await context.room.database.search(
            table="candidates", where={"candidate_id": candidate_id}, limit=1
        )

        if not results:
            return JsonResponse(
                json={
                    "status": "not_found",
                    "candidate_id": candidate_id,
                }
            )

        return JsonResponse(json={"status": "ok", "candidate": results[0]})


class ListCandidates(Tool):
    def __init__(self):
        super().__init__(
            name="list-candidates",
            title="list-candidates",
            description="List candidates by name or resume_path",
            input_schema={
                "type": "object",
                "additionalProperties": False,
                "required":["candidate_name", "resume_path"],
                "properties": {
                    "candidate_name": {"type": "string"},
                    "resume_path": {"type": "string"},
                },
            },
        )

    async def execute(
        self,
        context: ToolContext,
        candidate_name: str | None = None,
        resume_path: str | None = None,
        limit: int | None = None,
    ):
        where = {}
        if candidate_name:
            where["candidate_name"] = candidate_name
        if resume_path:
            where["resume_path"] = resume_path

        results = await context.room.database.search(
            table="candidates",
            where=where if where else None,
            limit=50,
        )
        return JsonResponse(json={"status": "ok", "candidates": results})


class DeleteCandidate(Tool):
    def __init__(self):
        super().__init__(
            name="delete-candidate",
            title="delete-candidate",
            description="Delete a candidate by id",
            input_schema={
                "type": "object",
                "required": ["candidate_id"],
                "additionalProperties": False,
                "properties": {"candidate_id": {"type": "string"}},
            },
        )

    async def execute(self, context: ToolContext, candidate_id: str):
        await context.room.database.delete(
            table="candidates",
            where=f"candidate_id = {json.dumps(candidate_id)}",
        )
        return JsonResponse(json={"status": "ok", "deleted": candidate_id})
    
# @service.path(identity="resume-toolkit", path="/resume-toolkit")
class ResumeToolkit(RemoteToolkit):
    def __init__(self):
        super().__init__(
            name="resume-toolkit",
            title="resume-toolkit",
            description="a toolkit for managing resumes",
            tools=[
                SaveCandidateDetails(), 
                GetCandidateDetails(),
                ListCandidates(),
                DeleteCandidate(),
            ],
        )