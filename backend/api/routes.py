from fastapi import APIRouter
from backend.models.request_models import UserRequest
from backend.models.response_models import OrchestratorResponse
from backend.orchestrator import process_request

router = APIRouter()


@router.post("/process", response_model=OrchestratorResponse)
async def process_user_request(request: UserRequest):
    return process_request(request)