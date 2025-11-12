from core.models import ChatCompletionRequest,ChatCompletionResponse,ModelsResponse

class Provider:
    def init(self,**args):
        pass
    def message(self,request:ChatCompletionRequest) -> ChatCompletionResponse:
        return ChatCompletionResponse(exception="Not implemented")
    def models_list(self) -> ModelsResponse: 
        return ModelsResponse(exception="Not implemented")
