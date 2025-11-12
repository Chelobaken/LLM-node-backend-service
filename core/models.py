from collections.abc import Iterable
from pydantic import BaseModel, Field
from typing import Any, Callable, Literal, Optional, List, Dict
from enum import Enum

class BaseResponse(BaseModel):
    message: Optional[str] = Field(default=None)

class BaseModelWithException(BaseModel):
    message: Optional[str] = Field(default=None)
    exception: Optional[str] = Field(default=None)
    
class BaseRequest(BaseModel):
    user_id:str
class Message(BaseModelWithException):
    content:str = Field(default="")
    thinking:str = Field(default="")
    complite:bool = Field(default=False)
# Стандартный набор моделей для типа api openai 
class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    
class ChatMessageRole(str, Enum):
    System = "system"
    User = "user"
    Assistant = "assistant"

class ChatCompletionMessage(BaseModel):
    role: Literal["system","user","assistant"]
    content: str
    name: Optional[str] = Field(None, alias="name")

    
class ChatCompletionRequest(BaseRequest):
    model: str
    messages: List[ChatCompletionMessage]
    max_tokens: Optional[int] = Field(None, alias="max_tokens")
    temperature: Optional[float] = Field(None, alias="temperature")
    top_p: Optional[float] = Field(None, alias="top_p")
    n: Optional[int] = Field(None, alias="n")
    stream: Optional[bool] = Field(None, alias="stream")
    stop: Optional[List[str]] = Field(None, alias="stop")
    think: Optional[bool] = Field(default=None)
    presence_penalty: Optional[float] = Field(None, alias="presence_penalty")
    frequency_penalty: Optional[float] = Field(None, alias="frequency_penalty")
    logit_bias: Optional[Dict[str, int]] = Field(None, alias="logit_bias")
    user: Optional[str] = Field(None, alias="user")

class ChatCompletionChoice(BaseModel):
    index: int
    message: ChatCompletionMessage
    finish_reason: str = Field(..., alias="finish_reason")

class ChatCompletionResponse(BaseModelWithException):
    id: Optional[str] = Field(default=None, alias="id")
    object: Optional[str] = Field(default=None, alias="object")
    created: Optional[int] = Field(default=None, alias="created")
    model: Optional[str] = Field(default=None, alias="model")
    choices: Optional[List[ChatCompletionChoice]] = Field(default=None)
    usage: Optional[Usage] = Field(default=None)

class Model(BaseModel):
    id: int = Field(default=0)
    model: str = Field(default="")
    choices: Optional[List[ChatCompletionChoice]] = Field(default=None)

class ModelsResponse(BaseModelWithException):
    models:Optional[List[Model]] = Field(default=None)