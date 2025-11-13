from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from core.providers.openruter import OpenrouterProvider
from core.models import ChatCompletionRequest
router = APIRouter(prefix="/ai", tags=["ai"])
provider = OpenrouterProvider() 
provider.init(model_name="gemma3:1b",stream=True,think=False)
@router.post("/")
async def list_containers(request: ChatCompletionRequest):
    return provider.message(request)
