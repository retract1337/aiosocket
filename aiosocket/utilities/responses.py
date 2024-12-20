from aiosocket.models import ResponseModel


class ResponseBuilder:
    def __init__(
        self,
        status: bool,
        message: str,
        data: dict = None,
        type: str = "response",
    ) -> None:
        self.status = status
        self.message = message
        self.data = data
        self.type = type

    def build(self) -> ResponseModel:
        return ResponseModel(
            status=self.status,
            message=self.message,
            data=self.data,
            type=self.type,
        )
