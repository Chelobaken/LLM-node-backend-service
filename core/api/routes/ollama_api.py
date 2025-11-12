from fastapi import APIRouter
from core.providers.ollama import OllamaProvider
from core.models import ChatCompletionRequest
router = APIRouter(prefix="/ai", tags=["ai"])
provider = OllamaProvider() 
provider.init(model_name="gemma3:1b",stream=True,think=False)
@router.get("/")
async def list_containers(request: ChatCompletionRequest):
    result = await provider.message(request)
    return result
