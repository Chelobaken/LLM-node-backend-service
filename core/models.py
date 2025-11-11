from pydantic import BaseModel, Field
from typing import Optional

class BaseResponse(BaseModel):
    message: Optional[str] = Field(default=None)
    data: Optional[dict] = Field(default=None)

