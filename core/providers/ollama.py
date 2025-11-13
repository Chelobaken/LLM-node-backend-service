from core.models import ChatCompletionRequest,Message
from .provider import Provider
from ollama import Client
from core.config import settings
from core.utils.checkurl import checkurl
import requests
class OllamaProvider(Provider):

    def init(self,**args):
        if not settings.OLLAMA_URL:
            raise Exception(f"OLLAMA_URL doest not set!\nOllamaProvider is not initialized")
        if not checkurl(settings.OLLAMA_URL+"/api"):
            raise Exception(f"{settings.OLLAMA_URL+"/api"} invalid!\nOllamaProvider is not initialized")
        self._model_name=args["model_name"]
        self._stream=args["stream"]
        self._think=args["think"]
        self._ollama_client = Client(host=settings.OLLAMA_URL)
    def message_stream(self, request: ChatCompletionRequest):
        if not hasattr(self, '_model_name'):
            raise Exception(f"OllamaProvider is not initialized")
        try:
            response = requests.post(
                f"{settings.OLLAMA_URL}/api/generate",
                json={
                    "model": self._model_name,
                    "messages": [x.model_dump() for x in request.messages],
                    "stream": True
                },
                stream = True
            )
            for line in response.iter_lines():
                if line:
                    yield line.decode("utf-8")
        except Exception as e:
            raise Exception(f"Ollama error: {str(e)}")
    def message(self, request: ChatCompletionRequest):
        if not hasattr(self, '_model_name'):
            raise Exception(f"OllamaProvider is not initialized")
        
        try:
            stream = self._ollama_client.chat(
                model=self._model_name,
                messages=[x.model_dump() for x in request.messages],
                stream=False
            )
            if not stream.message:
                raise Exception(f"Ollama error: no message")
            message = Message()
            if stream.message.content:
                message.content=stream.message.content
            if stream.message.thinking:
                message.thinking=stream.message.thinking
            return message   
        except Exception as e:
            raise Exception(f"Ollama error: {str(e)}")

   