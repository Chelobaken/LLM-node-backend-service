import fastapi
from .routes import ollama_api
api_router = fastapi.APIRouter()
api_router.include_router(ollama_api.router)
