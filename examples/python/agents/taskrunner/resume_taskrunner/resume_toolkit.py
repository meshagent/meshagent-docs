import json
import uuid
from meshagent.tools import Tool, Toolkit, ToolContext, RemoteToolkit
from meshagent.api.messaging import FileResponse, JsonResponse, TextResponse


def _lower_or_none(val: str | None) -> str | None:
    if val is None:
        return None
    return val.lower()


class SaveCandidateDetails(Tool):
    def __init__(self):
        super().__init__(
            name="save-candidate-details",
            title="save-candidate-details",
            description="Store information about a candidate in the room database",
            input_schema={
                "type": "object",
                "additionalProperties": False,
                "required": ["resume_path","candidate_first_name", "candidate_last_name", "candidate_email", "candidate_phone_number", "resume_summary", "web_search_notes"],
                "properties": {
                    "resume_path": {"type": "string"},
                    "candidate_first_name": {"type": "string"},
                    "candidate_last_name" : {"type": "string"},
                    "candidate_email": {"type": "string"},
                    "candidate_phone_number": {"type":"string"},
                    "resume_summary": {"type": "string"},
                    "web_search_notes": {"type":"string"}
                }
            }
        )
    async def execute(self, context:ToolContext, resume_path:str, candidate_first_name:str, candidate_last_name:str, candidate_email:str, candidate_phone_number:str|None, resume_summary:str, web_search_notes:str|None):
        record = {
                    "resume_path": resume_path,
                    "candidate_first_name": _lower_or_none(candidate_first_name),
                    "candidate_last_name": _lower_or_none(candidate_last_name),
                    "candidate_email": _lower_or_none(candidate_email),
                    "candidate_phone_number": _lower_or_none(candidate_phone_number),
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
                "required": ["candidate_first_name", "candidate_last_name", "candidate_email"],
                "properties": {
                    "candidate_first_name": {"type": "string"},
                    "candidate_last_name": {"type": "string"},
                    "candidate_email":{"type": "string"}
                    },
            },
        )

    async def execute(self, context: ToolContext, candidate_first_name: str, candidate_last_name:str, candidate_email:str):
        candidate_first_name = _lower_or_none(candidate_first_name)
        candidate_last_name = _lower_or_none(candidate_last_name)
        candidate_email = _lower_or_none(candidate_email)
        results = await context.room.database.search(
            table="candidates", where={"candidate_first_name": candidate_first_name,"candidate_last_name":candidate_last_name, "candidate_email":candidate_email}, limit=10
        )

        if not results:
            return JsonResponse(
                json={
                    "status": "not_found",
                    "candidate_first_name": candidate_first_name,
                    "candidate_last_name":candidate_last_name,
                    "candidate_email":candidate_email
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
                "required":["candidate_first_name", "candidate_last_name", "resume_path"],
                "properties": {
                    "candidate_first_name": {"type": "string"},
                    "candidate_last_name": {"type": "string"},
                    "resume_path": {"type": "string"},
                },
            },
        )

    async def execute(
        self,
        context: ToolContext,
        candidate_first_name: str | None = None,
        candidate_last_name: str | None = None,
        resume_path: str | None = None,
        limit: int | None = None,
    ):
        where = {}
        if candidate_first_name:
            where["candidate_first_name"] = _lower_or_none(candidate_first_name)
        if candidate_last_name:
            where["candidate_last_name"] = _lower_or_none(candidate_last_name)
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
            description="Delete a candidate by name and email",
            input_schema={
                "type": "object",
                "additionalProperties": False,
                "required": ["candidate_first_name", "candidate_last_name", "candidate_email"],
                "properties": {
                    "candidate_first_name": {"type": "string"},
                    "candidate_last_name": {"type": "string"},
                    "candidate_email":{"type": "string"}
                    },
            },
        )

    async def execute(
        self,
        context: ToolContext,
        candidate_first_name: str,
        candidate_last_name: str,
        candidate_email: str,
    ):
        where = {
            "candidate_first_name": _lower_or_none(candidate_first_name),
            "candidate_last_name": _lower_or_none(candidate_last_name),
            "candidate_email": _lower_or_none(candidate_email),
        }
        await context.room.database.delete(table="candidates", where=where)
        return JsonResponse(json={"status": "ok", "deleted": where})
    
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
