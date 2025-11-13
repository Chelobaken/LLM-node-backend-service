from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from core.providers.ollama import OllamaProvider
from core.models import ChatCompletionRequest
router = APIRouter(prefix="/ai", tags=["ai"])
provider = OllamaProvider() 
provider.init(model_name="gemma3:1b",stream=True,think=False)
@router.post("/")
async def list_containers(request: ChatCompletionRequest):
    return StreamingResponse(provider.message_stream(request),media_type="text/plain")
