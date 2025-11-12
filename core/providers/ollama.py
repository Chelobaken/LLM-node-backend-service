from core.models import ChatCompletionRequest,ChatCompletionResponse,ChatCompletionChoice,Message
from .provider import Provider
from ollama import Client

from collections import defaultdict
from typing import List, Union
class OllamaProvider(Provider):
    def init(self,**args):
        self._model_name=args["model_name"]
        self._stream=args["stream"]
        self._think=args["think"]
        self._ollama_client = Client(host="http://localhost:11434")
        self._stream_buff:dict[str,list[Message]] = defaultdict(list)
    async def message(self, request: ChatCompletionRequest) -> Union[Message, str]:
        if not self._model_name:
            return Message(exception="Model name doest set!")
        
        try:
            if request.stream:
                if_stream_mode=request.stream
            else:
                if_stream_mode=self._stream
            stream = self._ollama_client.chat(
                model=self._model_name,
                messages=[x.model_dump() for x in request.messages],
                stream=if_stream_mode
            )
            
            if if_stream_mode:
                await self._process_stream(stream, request.user_id)
                return request.user_id
            else:
                return await self._process_non_stream(stream)
                
        except Exception as e:
            raise Exception(f"Ollama error: {str(e)}")

    async def _process_stream(self, stream, user_id: str):
        self._stream_buff[user_id] = []  
        
        for chunk in stream:
            buff_message = Message()
            if hasattr(chunk.message, 'thinking') and chunk.message.thinking:
                buff_message.thinking += chunk.message.thinking
            if hasattr(chunk.message, 'content') and chunk.message.content:
                buff_message.content += chunk.message.content
            
            self._stream_buff[user_id].append(buff_message)

    async def _process_non_stream(self, stream) -> Message:
        message = Message()
        
        for chunk in stream:
            if hasattr(chunk.message, 'thinking') and chunk.message.thinking:
                message.thinking += chunk.message.thinking
            if hasattr(chunk.message, 'content') and chunk.message.content:
                message.content += chunk.message.content
        
        return message

    async def get_stream_messages(self, user_id: str) -> List[Message]:
        return self._stream_buff.get(user_id, [])
    
    async def clear_stream_buffer(self, user_id: str):
        if user_id in self._stream_buff:
            del self._stream_buff[user_id]
   