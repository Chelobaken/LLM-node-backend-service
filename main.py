from fastapi import FastAPI
from core.api import router

app = FastAPI()
app.include_router(router.api_router)
