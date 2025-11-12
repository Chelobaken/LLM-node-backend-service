from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from enum import Enum

from sqlalchemy import ( BigInteger, TIMESTAMP,UUID, Text, 
                        create_engine, Column, Integer, String, ForeignKey,
                        VARCHAR)
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.ext.automap import automap_base


class BaseResponse(BaseModel):
    message: Optional[str] = Field(default=None)

class BaseModelWithException(BaseModel):
    message: Optional[str] = Field(default=None)
    exception: Optional[Exception] = Field(default=None)

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
    role: ChatMessageRole
    content: str
    name: Optional[str] = Field(None, alias="name")

class ChatCompletionRequest(BaseModel):
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
    id: str = Field(..., alias="id")
    object: str = Field(..., alias="object")
    created: int = Field(..., alias="created")
    model: str = Field(..., alias="model")
    choices: List[ChatCompletionChoice]
    usage: Usage

class Model(BaseModel):
    id: int = Field(default=0)
    model: str = Field(default="")
    choices: Optional[List[ChatCompletionChoice]] = Field(default=None)

class ModelsResponse(BaseModelWithException):
    models:Optional[List[Model]] = Field(default=None)
    
# Модели для PostgreSQL

""" Base = declarative_base()

class Message(Base):
    __tablename__ = 'messages'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    role_id = Column(BigInteger, ForeignKey('participant_roles.id'), nullable=False)
    name_id = Column(BigInteger, ForeignKey('participant_names.id'), nullable=False)
    timestamp = Column(TIMESTAMP(False), nullable=False)
    content = Column(Text, nullable=False)
    dialog_id = Column(UUID, ForeignKey('dialogs.id'), nullable=False)
    model_id = Column(Integer, ForeignKey('models.id'), nullable=False)
    
    role = relationship("Role", back_populates="message")
    name = relationship("Name", back_populates="message")
    dialog = relationship("Dialog", back_populates="message")
    model = relationship("Model", back_populates="message")
    

class ParticipantRole(Base):
    __tablename__ = 'participant_roles'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    role = Column(VARCHAR(128), default='user', nullable=False)

class Model(Base):
    __tablename__ = 'models'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    model_id = Column(VARCHAR(32), nullable=False)
    
class ParticipantName(Base):
    __tablename__ = 'participant_names'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(128), nullable=False)
    
class User(Base):
    __tablename__ = 'users'
    
    id = Column(UUID, primary_key=True)
    username = Column(VARCHAR(24), nullable=False)
    hashed_password = Column(Text, nullable=False)
    
class Dialog(Base):
    __tablename__ = 'dialogs'
    
    id = Column(UUID, primary_key=True) 
    caption = Column(VARCHAR(128), nullable=False)
    hashed_password = Column(Text, nullable=False)

 
 
 
# Строка подключения к PostgreSQL
engine = create_engine('postgresql://username:password@localhost:5432/mydatabase')

# Создаем базовый класс с помощью automap_base
Base = automap_base()

# Отображаем таблицы
Base.prepare(engine, reflect=True)

# Теперь мы можем получить классы для таблиц
User = Base.classes.users  # Предположим, что есть таблица 'users'
AIModel = Base.classes.models  # и таблица 'addresses'
Message = Base.classes.messages
Roles = Base.classes.participant_roles
Names = Base.classes.participant_names
Dialogs = Base.classes.dialogs

# Пример использования:
from sqlalchemy.orm import Session
session = Session(engine)

# Пример запроса
users = session.query(User).all()
for user in users:
    print(user.name) """
    
    
