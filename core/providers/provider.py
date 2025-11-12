from models import ChatCompletionRequest,ChatCompletionResponse,ModelsResponse

class Provider:
    def init(Args:list):
        pass
    def message(request:ChatCompletionRequest) -> ChatCompletionResponse:
        pass
    def models_list() -> ModelsResponse:
        pass
