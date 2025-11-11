from fastapi import APIRouter, Depends, HTTPException, Response

router = APIRouter(prefix="/ai", tags=["ai"])
@router.get("/")
async def list_containers():
    return HTTPException(status_code=400, detail=f"Not implemented")
