from core.models import ChatCompletionRequest,Message
from .provider import Provider
from core.config import settings
from core.utils.checkurl import checkurl
import requests
import json
class OpenrouterProvider(Provider):

    def init(self,**args):
        if not settings.OPENROUTERKEY:
            raise Exception(f"OLLAMA_URL doest not set!\nOllamaProvider is not initialized")
        self._model_name=args["model_name"]
        self._stream=args["stream"]
        self._think=args["think"]
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
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.OPENROUTERKEY}",
                },

                json=json.dumps({
                    "model": "kwaipilot/kat-coder-pro:free", # Optional
                    "messages":  [x.model_dump() for x in request.messages]
                })
            )
            return response.json   
        except Exception as e:
            raise Exception(f"Openrouter error: {str(e)}")

   